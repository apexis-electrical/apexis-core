"""Archivo: src/apexis/core/utils/converters.py
Descripción: Convertidores utilitarios globales para el ecosistema APEXIS.
             Centraliza las transformaciones de unidades de potencia y magnitudes físicas.
             Optimizado con __slots__ y métodos estáticos.
"""


class PowerConverter:
    """Clase utilitaria encargada de normalizar cualquier unidad de potencia
    prevista en la memoria técnica hacia la unidad base de cálculo: kVA (S).
    """

    # Bloqueamos los slots para evitar el overhead del diccionario dinámico interno
    __slots__ = ()

    @staticmethod
    def to_apparent_power_kva(value: float, unit: str, cos_phi: float = 0.90) -> float:
        """Normaliza de forma estricta cualquier unidad de potencia a kilovolt-amperes (kVA)
        según las ecuaciones descritas en la sección de Normalización de Carga de la memoria.

        Fórmulas:
            S (kVA) = P (kW) / cos_phi
            S (kVA) = P (W) / (1000 * cos_phi)
            S (kVA) = S (VA) / 1000
            S (kVA) = (HP * 0.746) / (cos_phi * 0.85) -> Asume rendimiento típico de motor del 85%

        Args:
            value: Magnitud numérica de la carga.
            unit: String de la unidad de medida (ej: "kW", "HP", "VA", "W", "kVA").
            cos_phi: Factor de potencia de diseño adoptado globalmente (CRITERIA).

        Returns:
            float: Potencia aparente normalizada en kVA (redondeada a 3 decimales).

        """
        normalized_unit = unit.strip().upper()

        if value <= 0.0:
            return 0.0

        if normalized_unit == "KVA":
            return round(value, 3)

        if normalized_unit == "VA":
            return round(value / 1000.0, 3)

        if normalized_unit == "KW":
            return round(value / cos_phi, 3)

        if normalized_unit == "W":
            return round((value / 1000.0) / cos_phi, 3)

        if normalized_unit == "HP":
            # Conversión de potencia mecánica a eléctrica aparente considerando rendimiento térmico (0.85)
            mechanical_kw = value * 0.746
            electrical_kva = mechanical_kw / (cos_phi * 0.85)
            return round(electrical_kva, 3)

        if normalized_unit == "MVA":
            return round(value * 1000.0, 3)

        if normalized_unit == "MW":
            return round((value * 1000.0) / cos_phi, 3)

        # Fallback de seguridad si la unidad no es explícitamente soportada
        return round(value, 3)
