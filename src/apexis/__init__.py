"""Archivo: src/apexis/__init__.py
Descripción: Punto de entrada raíz para el paquete distribuible de APEXIS.
             Expone la API pública simplificada directamente en el namespace principal.
"""

from apexis.core.__master__ import (
    APEXISEngine,
    CableParameters,
    CircuitPurpose,
    ElectricalCircuit,
    ElectricalParameters,
    ElectricalStandardEnum,
    InstallationParameters,
    MarkdownReportExporter,
    PandocReportExporter,
    PowerConverter,
    ShortCircuitParameters,
    StandardAdapterFactory,
)

# Definimos las exportaciones oficiales del módulo para el usuario final
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
