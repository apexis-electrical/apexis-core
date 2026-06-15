"""Archivo: src/apexis/standards/aea90364/formulas/voltage_drop.py
Descripción: Lógica matemática multimetodología para el cálculo y verificación de la
             caída de tensión por los métodos GDC, IMPEDANCE y TABLES según la norma AEA 90364.
             Corregido el error de factor duplicado en el método GDC.
"""

import math
from typing import Any


def calculate_voltage_drop(
    mode: str,
    circuit_data: dict[str, Any],
    section_mm2: float,
    design_current_a: float,
    gdc_unit_value: float = 0.040,
    tables_database: dict[str, Any] | None = None,
) -> float:
    """Función orquestadora principal que selecciona el método de cálculo de caída de
    tensión porcentual (%) según la estrategia definida por el usuario en el lazo de entrada.

    Args:
        mode: Estrategia seleccionada por el ingeniero ("GDC", "IMPEDANCE", "TABLES").
        circuit_data: Estructura completa del circuito con datos eléctricos y de instalación.
        section_mm2: Sección transversal nominal del conductor bajo prueba (mm²).
        design_current_a: Corriente de proyecto Ib calculada en amperes (A).
        gdc_unit_value: Gradiente extraído dinámicamente desde constants.json.
        tables_database: Opcional, base de datos de caída unitaria para el método TABLES.

    Returns:
        float: Caída de tensión final expresada en porcentaje (%).

    """
    strategy = mode.upper()
    electrical = circuit_data.get("electrical", {})

    voltage_v = float(electrical.get("voltage_v", 220.0))
    length_m = float(electrical.get("length_m", 0.0))
    phase_type = str(electrical.get("phase_type", "1PH")).upper()
    parallels = int(electrical.get("parallels", 1))

    # Control de fronteras físicas iniciales de seguridad matemática
    if section_mm2 <= 0.0 or length_m <= 0.0 or design_current_a <= 0.0:
        return 0.0

    # =========================================================================
    # MÉTODO 1: GRADIENTE DE CAÍDA DE TENSIÓN SIMPLIFICADO (GDC) s/ 771.19.7.c
    # =========================================================================
    if strategy == "GDC":
        # S_equivalent = n_paralelos * S (Sección equivalente acumulada por fase)
        equivalent_section = parallels * section_mm2

        # CORREGIDO: El gdc_unit_value de constants.json ya contempla el tipo de sistema
        # (0.040 para 1PH y 0.035 para 3PH). No se multiplica por ningún factor de fase.
        v_drop_abs = (gdc_unit_value * design_current_a * length_m) / equivalent_section

        # Transformación a magnitud porcentual relativa de la red
        percentage_drop = (v_drop_abs / voltage_v) * 100.0
        return round(percentage_drop, 2)

    # =========================================================================
    # MÉTODO 2: MÉTODO ANALÍTICO COMPLETO POR IMPEDANCIAS s/ 771.19.7.a
    # =========================================================================
    if strategy == "IMPEDANCE":
        cable_info = circuit_data.get("cable", {})
        r_lineal = float(cable_info.get("resistance_ohm_per_m", 0.001))
        x_lineal = float(cable_info.get("reactance_ohm_per_m", 0.0001))
        cos_phi = float(circuit_data.get("criteria", {}).get("cos_phi", 0.90))

        # Reducimos los parámetros lineales en base a la cantidad de conductores en paralelo
        equivalent_resistance = r_lineal / parallels
        equivalent_reactance = x_lineal / parallels

        # Resolución trigonométrica para obtener el componente de reactancia de la carga (sin_phi)
        sin_phi = math.sqrt(1.0 - (cos_phi**2))

        # Impedancia total activa proyectada sobre el vector de corriente de empleo
        impedance_term = (equivalent_resistance * cos_phi) + (equivalent_reactance * sin_phi)

        # Coeficiente de fases normativo explícito (k=2 para 1PH por lazo, sqrt(3) para 3PH)
        phase_multiplier = 1.7320508 if phase_type == "3PH" else 2.0

        # Caída absoluta y conversión directa a escala porcentual de diseño
        v_drop_abs = phase_multiplier * design_current_a * length_m * impedance_term
        percentage_drop = (v_drop_abs / voltage_v) * 100.0
        return round(percentage_drop, 2)

    # =========================================================================
    # MÉTODO 3: CÁLCULO MEDIANTE TABLAS DE CAÍDA UNITARIA s/ Tabla 771.19.IV
    # =========================================================================
    if strategy == "TABLES":
        if not tables_database:
            return 0.0

        installation = circuit_data.get("installation", {})
        mat_key = str(installation.get("material", "Cu")).upper()
        ins_key = str(installation.get("insulation", "PVC")).upper()

        # Estructura esperada en JSON: tables_database["CU"]["PVC"]["1PH"]["2.5"] -> valor en V/A.km
        v_drop_unit_km = (
            tables_database.get(mat_key, {})
            .get(ins_key, {})
            .get(phase_type, {})
            .get(str(section_mm2))
        )

        if v_drop_unit_km is None:
            return 0.0

        # Al tener conductores en paralelo por fase, la caída unitaria de corriente se divide
        effective_unit_drop = float(v_drop_unit_km) / parallels

        # Conversión métrica lineal de longitud a kilómetros (m / 1000)
        length_km = length_m / 1000.0
        v_drop_abs = effective_unit_drop * design_current_a * length_km

        percentage_drop = (v_drop_abs / voltage_v) * 100.0
        return round(percentage_drop, 2)

    return 0.0


def verify_voltage_drop_limit(percentage_drop: float, purpose_type: str) -> bool:
    """Valida si el porcentaje de caída de tensión cumple con los máximos permitidos.
    Límites de la Memoria de Cálculo: 1% tableros, 3% iluminación/tomas, 5% motores.
    """
    purpose = purpose_type.lower()

    if purpose in ["board", "tableros"]:
        limit = 1.0
    elif purpose in ["lighting", "outlet", "usos generales"]:
        limit = 3.0
    elif purpose in ["power", "motor", "fuerza motriz"]:
        limit = 5.0
    else:
        limit = 3.0

    return percentage_drop <= limit
