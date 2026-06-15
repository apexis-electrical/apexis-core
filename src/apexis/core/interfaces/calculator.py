"""Archivo: src/apexis/core/interfaces/calculator.py
Descripción: Interfaz abstracta pura (Puerto de Entrada) para los motores de cálculo
             de normativas eléctricas nacionales e internacionales en APEXIS.
"""

from abc import ABC, abstractmethod
from typing import Any


class ElectricalCalculatorInterface(ABC):
    """Contrato formal de Arquitectura Hexagonal que debe implementar de forma obligatoria
    cualquier adaptador de regulaciones (ej: AEA, NEC, IEC) para acoplarse al núcleo.
    """

    # Al ser una interfaz abstracta pura, congelamos los slots vacíos para optimización de RAM
    __slots__ = ()

    @abstractmethod
    def process_circuit_design(
        self,
        circuit_data: dict[str, Any],
        global_criteria: dict[str, Any],
    ) -> dict[str, Any]:
        """Obliga a calcular y resolver secuencialmente la ingeniería completa del circuito
        (Ampacidad corregida, Caída de tensión por estrategia y Solicitación térmica de cortocircuito).

        Args:
            circuit_data: Diccionario con los parámetros del circuito (Tag, Eléctrico, Instalación).
            global_criteria: Criterios generales de diseño definidos en el motor (CRITERIA).

        Returns:
            Dict[str, Any]: Resultados consolidados listos para indexarse en la {{RESULTS_TABLE}}.

        """
