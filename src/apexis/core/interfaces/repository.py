"""Archivo: src/apexis/core/interfaces/repository.py
Descripción: Interfaz abstracta pura (Puerto de Salida) para el almacenamiento
             y recuperación de proyectos, tableros y memorias técnicas calculadas.
"""

from abc import ABC, abstractmethod
from typing import Any


class ProjectRepositoryInterface(ABC):
    """Contrato formal que rige las operaciones de persistencia e histórico de datos
    vivos generados por los usuarios dentro del ecosistema APEXIS.
    """

    __slots__ = ()

    @abstractmethod
    def save_project(self, project_id: str, results_table: list[dict[str, Any]]) -> bool:
        """Persiste la tabla consolidada de resultados finales ({{RESULTS_TABLE}}) de un proyecto.

        Args:
            project_id: Identificador único del proyecto o tablero del usuario.
            results_table: Colección de filas de circuitos calculadas y aprobadas por el motor.

        Returns:
            bool: True si la operación de almacenamiento fue exitosa, False de lo contrario.

        """

    @abstractmethod
    def load_project_inputs(self, project_id: str) -> list[dict[str, Any]] | None:
        """Recupera los datos de entrada originales (inputs crudos) para volver a correr el motor.

        Args:
            project_id: Identificador único del proyecto o tablero.

        Returns:
            Optional[List[Dict[str, Any]]]: Lote de circuitos crudos si existen, None de lo contrario.

        """
