"""Archivo: src/apexis/core/interfaces/data_provider.py
Descripción: Interfaz abstracta pura (Puerto de Salida) para el suministro de datos
             técnicos y coeficientes físicos de las tablas normativas.
"""

from abc import ABC, abstractmethod


class DataProviderInterface(ABC):
    """Contrato formal que desacopla la persistencia de las tablas de datos estáticos
    (factores ambientales, capacidades de cables y constantes térmicas) del Core.
    """

    __slots__ = ()

    @abstractmethod
    def get_k_constant(self, material: str, insulation: str) -> float:
        """Contrato para obtener la constante térmica k ante esfuerzos de cortocircuito."""

    @abstractmethod
    def get_temperature_factor(
        self,
        ambient_temp_c: float,
        insulation: str,
        environment: str,
    ) -> float:
        """Contrato para obtener el coeficiente reductor f_t por temperatura de aire o suelo."""

    @abstractmethod
    def get_base_ampacity(
        self,
        section_mm2: float,
        installation_method: str,
        material: str,
        insulation: str,
    ) -> float:
        """Contrato para buscar la capacidad nominal base (I_tabla) de un conductor específico."""

    @abstractmethod
    def get_available_sections(
        self,
        material: str,
        insulation: str,
        installation_method: str,
    ) -> list[float]:
        """Contrato para obtener el catálogo completo de secciones comerciales normalizadas disponibles."""
