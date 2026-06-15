"""Archivo: src/apexis/standards/aea90364/adapter.py
Descripción: Adaptador de bajo nivel para la norma AEA 90364.
             Orquesta las consultas a lookup y ejecuta secuencialmente las fórmulas.
             Optimizado con __slots__ y métodos mágicos corporativos.
"""

from typing import Any

from apexis.standards.aea90364.data.lookup import AEA90364Lookup
from apexis.standards.aea90364.formulas.ampacity import (
    calculate_corrected_ampacity,
    calculate_design_current,
)
from apexis.standards.aea90364.formulas.derating import calculate_global_derating_factor
from apexis.standards.aea90364.formulas.short_circuit import calculate_short_circuit_current
from apexis.standards.aea90364.formulas.thermal_stress import verify_thermal_stress
from apexis.standards.aea90364.formulas.voltage_drop import (
    calculate_voltage_drop,
    verify_voltage_drop_limit,
)
from apexis.standards.aea90364.validators.circuit_validator import AEA90364CircuitValidator


class AEA90364Adapter:
    """Componente adaptador encargado de encapsular todas las reglas de negocio
    e inecuaciones de verificación técnica dictadas por la reglamentación argentina.
    """

    # Bloqueamos el __dict__ interno para optimizar el acceso a variables y la memoria RAM
    __slots__ = ("lookup",)

    def __init__(self, lookup_registry: AEA90364Lookup | None = None) -> None:
        """Inicializa el adaptador inyectando el registro de base de datos Lookup."""
        self.lookup: AEA90364Lookup = lookup_registry or AEA90364Lookup()

    def process_circuit_design(
        self,
        circuit_data: dict[str, Any],
        global_criteria: dict[str, Any],
    ) -> dict[str, Any]:
        """Ejecuta el bucle iterativo de dimensionamiento y validación completa para un circuito
        según las exigencias de la memoria técnica (Ampacidad -> Caída de Tensión -> Cortocircuito).

        Args:
            circuit_data: Diccionario completo de un circuito (ej: C-01 de tu data-inputs.py).
            global_criteria: Criterios globales definidos por el usuario (CRITERIA).

        Returns:
            Dict[str, Any]: Resultados del dimensionamiento listos para la {{RESULTS_TABLE}}.

        """
        electrical = circuit_data.get("electrical", {})
        installation = circuit_data.get("installation", {})
        purpose = circuit_data.get("purpose", {})
        short_circuit_config = circuit_data.get("short_circuit", {})
        cable_config = circuit_data.get("cable", {})

        # =========================================================================
        # ADUANA REGLAMENTARIA (BLOQUEA EL LAZO SI LOS INPUTS VIOLAN LA NORMA)
        # =========================================================================
        # 1. Validar la coherencia constructiva entre las fases y el método
        AEA90364CircuitValidator.validate_method_compatibility(
            installation_method=str(installation.get("installation_method", "B1-2x")),
            phase_type=str(electrical.get("phase_type", "1PH")),
        )
        # 2. Validar los rangos térmicos operativos de las tablas de factores
        AEA90364CircuitValidator.validate_ambient_temperature(
            ambient_temp_c=float(installation.get("installation_temp_c", 40.0)),
            insulation_material=str(installation.get("insulation", "PVC")),
        )
        # 3. Validar límites de calibres de las protecciones s/ Ámbito (Sección 770 o 771)
        if "protection" in circuit_data:
            AEA90364CircuitValidator.validate_protection_limits(
                nominal_current_a=float(circuit_data["protection"].get("nominal_current_a", 16.0)),
                standard_section=str(global_criteria.get("standard_section", "771")),
            )
        # =========================================================================

        # 1. Determinación de la corriente de proyecto (I_B)
        cos_phi = float(global_criteria.get("cos_phi", 0.90))
        design_current_ib = calculate_design_current(
            load_value=float(electrical.get("load", {}).get("value", 0.0)),
            load_unit=str(electrical.get("load", {}).get("unit", "kVA")),
            voltage_v=float(electrical.get("voltage_v", 220.0)),
            phase_type=str(electrical.get("phase_type", "1PH")),
            cos_phi=cos_phi,
        )

        # 2. Inicialización del piso de secciones mínimas por resistencia mecánica (s/ Memoria)
        purpose_type = str(purpose.get("type", "lighting")).lower()
        purpose_subtype = str(purpose.get("subtype", "iug")).lower()

        starting_section = 1.5
        if purpose_type == "outlet" or purpose_subtype == "tug":
            starting_section = 2.5
        elif purpose_type == "power" or purpose_subtype in ["tue", "hvac"]:
            starting_section = 4.0

        # 3. Obtener el espectro completo de secciones comerciales disponibles para el método
        material = str(installation.get("material", "Cu"))
        insulation = str(installation.get("insulation", "PVC"))
        method = str(installation.get("installation_method", "B1-2x"))

        available_sections = self.lookup.get_available_sections(material, insulation, method)
        # Filtramos para quedarnos solo con las secciones comerciales válidas s/ piso mínimo
        valid_sections = [s for s in available_sections if s >= starting_section]

        # 4. Cálculo del factor de derating global (F_derating estático ambiental del lazo)
        env_type = "SOIL" if method.upper().startswith("D") else "AIR"
        temp_factor = self.lookup.get_temperature_factor(
            ambient_temp_c=float(installation.get("installation_temp_c", 40.0)),
            insulation=insulation,
            environment=env_type,
        )

        # Obtenemos el factor de agrupación utilizando la tabla general simplificada
        grouped_circuits = int(installation.get("grouped_circuits", 1))
        phase_type = str(electrical.get("phase_type", "1PH")).upper()
        grouping_factor = float(
            self.lookup.factors.get("grouped_general", {})
            .get(str(grouped_circuits), {})
            .get(phase_type, 1.0),
        )

        global_derating = calculate_global_derating_factor(
            temperature_factor=temp_factor,
            grouping_factor=grouping_factor,
            installation_method=method,
            soil_type=str(installation.get("soil_type", "default")),
            wire_burial_depth_m=float(installation.get("wire_burial_depth_m", 0.0)),
            soil_tables=self.lookup.factors,
        )

        # 5. Algoritmo Iterativo de Selección y Comprobación definitiva
        selected_section = valid_sections[-1]  # Fallback si ninguna sección pasa las inecuaciones
        final_iz = 0.0
        final_v_drop_pct = 0.0
        final_icc_ka = 0.0
        thermal_stress_passed = False

        ampacity_margin = float(global_criteria.get("ampacity_margin", 1.00))
        parallels = int(electrical.get("parallels", 1))

        # Buscamos de menor a mayor la primera sección comercial normalizada que apruebe TODO
        for section in valid_sections:
            # A. Verificación de Ampacidad Corregida
            nominal_amp = self.lookup.get_base_ampacity(section, method, material, insulation)
            iz_corregida = calculate_corrected_ampacity(
                nominal_amp,
                global_derating,
                parallels,
                ampacity_margin,
            )

            if design_current_ib > iz_corregida:
                continue  # Falla térmica por régimen permanente -> evalúa sección superior

            # B. Verificación por Caída de Tensión Porcentual
            v_drop_method = str(cable_config.get("voltage_drop_method", "GDC"))
            v_drop_pct = calculate_voltage_drop(
                mode=v_drop_method,
                circuit_data=circuit_data,
                section_mm2=section,
                design_current_a=design_current_ib,
                tables_database=self.lookup.wires,
            )

            if not verify_voltage_drop_limit(v_drop_pct, purpose_type):
                continue  # Falla por caída de tensión -> evalúa sección superior

            # C. Verificación frente a Cortocircuito (Esfuerzo Térmico)
            sc_mode = str(short_circuit_config.get("mode", "skip"))
            icc_ka = calculate_short_circuit_current(sc_mode, circuit_data)
            time_s = float(short_circuit_config.get("time_s", 0.5))

            is_thermal_safe = verify_thermal_stress(
                icc_ka,
                time_s,
                section,
                material,
                insulation,
                parallels,
            )

            if sc_mode != "skip" and not is_thermal_safe:
                continue  # Falla por cortocircuito -> evalúa sección superior

            # Si el código llega aquí, encontramos la sección comercial definitiva que cumple TODO
            selected_section = section
            final_iz = iz_corregida
            final_v_drop_pct = v_drop_pct
            final_icc_ka = icc_ka
            thermal_stress_passed = is_thermal_safe
            break

        # 6. Dimensionamiento Directo del Conductor de Protección (PE) s/ tramos de la Memoria
        if selected_section <= 16.0:
            pe_section = selected_section
        elif selected_section <= 35.0:
            pe_section = 16.0
        else:
            pe_section = selected_section / 2.0

        # Retornamos el paquete consolidado de resultados estructurados para el Core
        return {
            "tag": circuit_data.get("tag", "UNKNOWN"),
            "ib_a": design_current_ib,
            "iz_a": final_iz,
            "section_mm2": selected_section,
            "pe_section_mm2": pe_section,
            "voltage_drop_pct": final_v_drop_pct,
            "icc_ka": final_icc_ka,
            "thermal_stress_ok": thermal_stress_passed,
            "status": "APPROVED" if final_iz >= design_current_ib else "FAILED",
        }

    def __repr__(self) -> str:
        """Representación técnica formal en consola (para desarrolladores y logs)."""
        return f"<{self.__class__.__name__}(lookup_registry={self.lookup!r})>"

    def __str__(self) -> str:
        """Representación legible de la identidad del adaptador."""
        return "APEXIS Regulation Adapter for Standard: AEA 90364 (Argentina)"
