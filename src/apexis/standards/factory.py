"""Archivo: src/apexis/standards/factory.py
Descripción: Factoría central orquestadora de normas (Standard Provider) de nivel corporativo.
             Utiliza enums para el tipado estricto, __slots__ para optimización extrema de memoria,
             y métodos mágicos para un comportamiento inteligente y representable.
"""

from enum import Enum, unique
from typing import Any

from apexis.standards.aea90364.adapter import AEA90364Adapter


@unique
class ElectricalStandardEnum(Enum):
    """Enum inmutable que restringe de forma estricta los identificadores de normas
    reconocidos por la plataforma APEXIS, evitando errores de tipeo en las capas superiores.
    """

    AEA_90364 = "aea90364"
    NEC_2023 = "nec2023"
    NBR_5410 = "nbr5410"
    NOM_001 = "nom001"
    IEC_60364 = "iec60364"
    REBT_2002 = "rebt2002"
    VDE_0100 = "vde0100"
    JIS_C_3605 = "jis_c_3605"
    GB_50054 = "gb50054"
    IS_732 = "is732"
    SANS_10142 = "sans10142"
    ECP_301 = "ecp301"


class StandardAdapterFactory:
    """Factoría optimizada que gestiona el mapeo e instanciación de los adaptadores de normas.
    Utiliza __slots__ para congelar los atributos y disparar la velocidad en memoria.
    """

    # Optimizamos el espacio en memoria eliminando el __dict__ interno de la clase
    __slots__ = ("_active_adapters", "_global_registry")

    def __init__(self) -> None:
        """Inicializa la factoría registrando los adaptadores construidos y las hojas de ruta.
        """
        # Mapeo directo entre el Enum de la norma y su clase adaptadora en producción
        self._active_adapters: dict[ElectricalStandardEnum, Any] = {
            ElectricalStandardEnum.AEA_90364: AEA90364Adapter,
        }

        # Catálogo maestro estructurado por regiones continentales para auditorías del sistema
        self._global_registry: dict[str, dict[ElectricalStandardEnum, str]] = {
            "AMERICA": {
                ElectricalStandardEnum.AEA_90364: "Asociación Electrotécnica Argentina (Argentina)",
                ElectricalStandardEnum.NEC_2023: "National Electrical Code - NFPA 70 (Estados Unidos)",
                ElectricalStandardEnum.NBR_5410: "Norma Brasileira ABNT NBR 5410 (Brasil)",
                ElectricalStandardEnum.NOM_001: "Norma Oficial Mexicana - NOM-001-SEDE (México)",
            },
            "EUROPA": {
                ElectricalStandardEnum.IEC_60364: "International Electrotechnical Commission (Estándar Global)",
                ElectricalStandardEnum.REBT_2002: "Reglamento Electrotécnico para Baja Tensión (España)",
                ElectricalStandardEnum.VDE_0100: "Verband der Elektrotechnik - DIN VDE (Alemania)",
            },
            "ASIA": {
                ElectricalStandardEnum.JIS_C_3605: "Japanese Industrial Standards - Cables de Baja Tensión (Japón)",
                ElectricalStandardEnum.GB_50054: "Code for Design of Low-voltage Power Distribution (China)",
                ElectricalStandardEnum.IS_732: "Code of Practice for Electrical Wiring Installations (India)",
            },
            "AFRICA": {
                ElectricalStandardEnum.SANS_10142: "South African National Standard - Wiring of Premises (Sudáfrica)",
                ElectricalStandardEnum.ECP_301: "Egyptian Code of Practice for Electrical Installations (Egipto)",
            },
        }

    def get_adapter(self, standard_input: str) -> Any:
        """Resuelve de forma dinámica la instancia del adaptador a partir de un string de entrada.

        Args:
            standard_input: Cadena de texto provista por el JSON/Diccionario de entrada (ej: "aea90364").

        Returns:
            Any: Instancia pura del adaptador configurado y compatible con el motor Core.

        Raises:
            ValueError: Si la norma no existe en el catálogo global de APEXIS.
            NotImplementedError: Si la norma existe pero no tiene lógica matemática programada aún.

        """
        # Buscamos correspondencia en el Enum de manera segura e insensible a mayúsculas/espacios
        normalized_str = standard_input.strip().lower()
        matched_enum: ElectricalStandardEnum | None = None

        for e in ElectricalStandardEnum:
            if e.value == normalized_str:
                matched_enum = e
                break

        # Control de fallo 1: Si no coincide con ninguna norma del espectro internacional
        if matched_enum is None:
            raise ValueError(
                f"La norma '{standard_input}' no forma parte del catálogo reconocido por el ecosistema APEXIS. "
                f"Verifica los parámetros de configuración de tu proyecto.",
            )

        # Si encontramos el Enum y está listo en producción, lo despachamos instanciado
        if matched_enum in self._active_adapters:
            adapter_class = self._active_adapters[matched_enum]
            return adapter_class()

        # Control 2: Si está contemplado en el roadmap regional pero su código está pendiente
        for region, standards in self._global_registry.items():
            if matched_enum in standards:
                raise NotImplementedError(
                    f"La norma '{standard_input}' ({standards[matched_enum]}) está mapeada para la región "
                    f"{region}, pero su adaptador matemático se encuentra en fase de desarrollo o expansión.",
                )

        # Fallback de seguridad por consistencia de tipos
        raise ValueError(f"Estado de norma no controlado para: {standard_input}")

    def get_catalog(self) -> dict[str, dict[ElectricalStandardEnum, str]]:
        """Expone el registro global completo indexado por Enums para auditorías del motor de cálculo.
        """
        return self._global_registry

    def __repr__(self) -> str:
        """Representación técnica formal en consola (para desarrolladores y logs).
        """
        return f"<{self.__class__.__name__}(active_adapters={list(self._active_adapters.keys())})>"

    def __str__(self) -> str:
        """Representación legible e informativa del estado del objeto para el usuario final.
        """
        return f"APEXIS Standard Provider Engine [Normas Activas: {len(self._active_adapters)}]"
