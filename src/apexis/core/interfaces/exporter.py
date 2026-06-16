"""
Archivo: src/apexis/core/interfaces/exporter.py
Descripción: Interfaz abstracta pura (Puerto de Salida) para los componentes de
             exportación y generación de reportes de memorias técnicas en APEXIS.
"""

from abc import ABC, abstractmethod
from typing import Any


class ReportExporterInterface(ABC):
    """
    Contrato formal que define las operaciones requeridas para transformar las tablas
    de resultados matemáticos del motor en documentos de ingeniería legibles.
    """

    __slots__ = ()

    @property
    @abstractmethod
    def resolved_extension(self) -> str:
        """
        Devuelve la extensión de archivo formal que genera este plugin (ej: '.md', '.docx')."""
        pass

    @abstractmethod
    def export_report(self, results_table: list[dict[str, Any]], output_path: str) -> bool:
        """
        Lee una plantilla base, inyecta la tabla de resultados y exporta el documento final.

        Args:
            results_table: Colección de circuitos calculados por el APEXISEngine.
            output_path: Ruta física de destino donde se guardará el archivo generado.

        Returns:
            bool: True si el reporte se generó y guardó con éxito, False de lo contrario.
        """
        pass
