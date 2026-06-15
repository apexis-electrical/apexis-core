"""Archivo: src/apexis/standards/aea90364/validators/circuit_validator.py
Descripción: Validadores de reglas normativas (Rules) de la reglamentación AEA 90364.
             Valida límites legales y de fronteras de tablas antes del cálculo.
             Optimizado con __slots__ y métodos estáticos.
"""


class AEA90364CircuitValidator:
    """Componente encargado de ejecutar las reglas de frontera de la AEA 90364
    para asegurar la integridad de los datos de entrada frente a la ley eléctrica argentina.
    """

    # Bloqueamos la memoria RAM eliminando el __dict__ interno de la clase
    __slots__ = ()

    @staticmethod
    def validate_ambient_temperature(ambient_temp_c: float, insulation_material: str) -> None:
        """Regla de Rango Térmico: Valida que la temperatura de instalación se encuentre
        dentro de los límites de las tablas de derating de la AEA 90364.

        Límites:
            - Temperatura mínima física: 10°C (inicio de las tablas de factores).
            - PVC máximo admitido en régimen permanente: 60°C s/ tablas de reducción.
            - XLPE máximo admitido en régimen permanente: 80°C s/ tablas de reducción.
        """
        temp = float(ambient_temp_c)
        insulation = insulation_material.strip().upper()

        if temp < 10.0:
            raise ValueError(
                f"Temperatura de instalación inválida ({temp}°C). El límite inferior de las "
                f"tablas de factores de corrección por temperatura de la AEA 90364 es de 10°C.",
            )

        if insulation == "PVC" and temp > 60.0:
            raise ValueError(
                f"Temperatura crítica detectada ({temp}°C) para aislación de PVC. La norma "
                f"AEA 90364 no posee factores de reducción para PVC por encima de 60°C.",
            )

        if insulation == "XLPE" and temp > 80.0:
            raise ValueError(
                f"Temperatura crítica detectada ({temp}°C) para aislación de XLPE. La norma "
                f"AEA 90364 no posee factores de reducción para XLPE por encima de 80°C.",
            )

    @staticmethod
    def validate_protection_limits(nominal_current_a: float, standard_section: str) -> None:
        """Regla de Calibres Máximos s/ Ámbito: Aplica las cláusulas de limitación de corriente
        asignada para tableros residenciales o comerciales según la sección de la norma.

        Límites:
            - Sección 770 (Viviendas unifamiliares): Máximo absoluto de calibres = 63 A.
            - Sección 771 (Uso general/oficinas): Máximo admitido para MCB/PIA = 125 A.
        """
        current = float(nominal_current_a)
        section = standard_section.strip().upper()

        if "770" in section and current > 63.0:
            raise ValueError(
                f"Violación de Cláusula s/ Sección 770: El calibre de la protección ({current}A) "
                f"excede el límite máximo permitido de 63 A para viviendas de hasta 63 A de demanda.",
            )

        if "771" in section and current > 125.0:
            raise ValueError(
                "Violación de Cláusula s/ Sección 771: El calibre máximo asignado para interruptores "
                "automáticos en miniatura (MCB) operados por personal BA1 es de 125 A.",
            )

    @staticmethod
    def validate_method_compatibility(installation_method: str, phase_type: str) -> None:
        """Regla de Coherencia Constructiva: Valida que la sub-configuración de conductores cargados
        del método (ej: 2x, 3x) sea perfectamente compatible con el tipo de fase eléctrica del lazo.

        Límites:
            - Si el circuito es 1PH, no puede utilizar métodos de 3 conductores cargados (3x, 3xT, 3xP).
            - Si el circuito es 3PH, no puede utilizar métodos de 2 conductores cargados (2x, 2xA, 2xB).
        """
        method = installation_method.strip().upper()
        phase = phase_type.strip().upper()

        # CORREGIDO: Normalizamos la lista resultante del split a mayúsculas de forma segura
        if "-" in method:
            config_parts = [part.upper() for part in method.split("-")]
            config_key = config_parts if len(config_parts) > 1 else ["2X"]
        else:
            config_key = ["2X"]

        if phase == "1PH" and any(x in config_key for x in ["3X", "3XT", "3XP"]):
            raise ValueError(
                f"Incoherencia constructiva: El circuito está configurado como 1PH, pero el método de "
                f"instalación elegido ({installation_method}) exige un tendido trifásico de 3 conductores cargados.",
            )

        if phase == "3PH" and any(x in config_key for x in ["2X", "2XA", "2XB"]):
            raise ValueError(
                f"Incoherencia constructiva: El circuito está configurado como 3PH, pero el método de "
                f"instalación elegido ({installation_method}) restringe el tendido a 2 conductores cargados.",
            )
