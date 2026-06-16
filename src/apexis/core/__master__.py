"""Archivo: src/apexis/core/__master__.py
Descripción: Punto de entrada unificado y fachada pública (Facade Pattern) de APEXIS Core.
             Expone los componentes principales para facilitar su consumo externo.
             Corregido removiendo la importación inexistente de ProtectionParameters.
"""

from apexis.core.domain.engine import APEXISEngine
from apexis.core.domain.entities import (
    CableParameters,
    CircuitPurpose,
    ElectricalCircuit,
    ElectricalParameters,
    InstallationParameters,
    ShortCircuitParameters,
)
from apexis.core.exporters.markdown_exporter import MarkdownReportExporter
from apexis.core.exporters.pandoc_exporter import PandocReportExporter
from apexis.core.utils.converters import PowerConverter
from apexis.standards.factory import ElectricalStandardEnum, StandardAdapterFactory

# Definimos de forma explícita qué componentes son exportados públicamente al hacer:
# from apexis.core import *
__all__ = (
    "APEXISEngine",
    "CableParameters",
    "CircuitPurpose",
    "ElectricalCircuit",
    "ElectricalParameters",
    "ElectricalStandardEnum",
    "InstallationParameters",
    "MarkdownReportExporter",
    "PandocReportExporter",
    "PowerConverter",
    "ShortCircuitParameters",
    "StandardAdapterFactory",
)
