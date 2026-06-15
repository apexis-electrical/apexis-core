"""Archivo: src/apexis/standards/aea90364/formulas/short_circuit.py
Descripción: Lógica matemática para determinar la corriente de cortocircuito (Icc)
             máxima presunta según diferentes metodologías analíticas e in-situ.
"""

import math
from typing import Any


def calculate_short_circuit_current(
    mode: str,
    circuit_data: dict[str, Any],
    grid_data: dict[str, Any] | None = None,
) -> float:
    """Orquesta la determinación de la corriente de cortocircuito eficaz presunta (I_k'')
    en kiloamperes (kA) basándose en la estrategia seleccionada por el usuario.

    Args:
        mode: Estrategia de cálculo ("manual", "impedance", "aea_tables", "skip").
        circuit_data: Diccionario del circuito del input ("short_circuit", "electrical").
        grid_data: Parámetros de la red aguas arriba (Requerido solo para "impedance").

    Returns:
        float: Corriente de cortocircuito máxima presunta en kA.

    """
    strategy = mode.lower()

    if strategy == "skip":
        return 0.0

    if strategy == "manual":
        # Método in-situ / Instrumento o Dato provisto por Distribuidora
        # Retorna directamente el valor hardcodeado por el usuario en el input
        return float(circuit_data.get("Icc_kA", 0.0))

    if strategy == "impedance":
        # Método por impedancias del lazo de falla (s/ AEA 90909 / IEC 60909)
        return _calculate_by_impedance_method(circuit_data, grid_data)

    if strategy == "aea_tables":
        # Tablas de orientación simplificadas (Anexo 770-B / 771-H)
        return _calculate_by_aea_tables_method(circuit_data)

    # Fallback de seguridad si introducen un modo no soportado
    return float(circuit_data.get("Icc_kA", 0.0))


def _calculate_by_impedance_method(
    circuit_data: dict[str, Any],
    grid_data: dict[str, Any] | None,
) -> float:
    """Cálculo analítico por impedancias acumuladas Z_k.
    Fórmula: I_k'' = (c * U_n) / (sqrt(3) * Z_k)
    """
    if not grid_data:
        return float(circuit_data.get("Icc_kA", 0.0))

    # Parámetros eléctricos del circuito
    electrical = circuit_data.get("electrical", {})
    voltage_v = float(electrical.get("voltage_v", 380.0))
    phase_type = str(electrical.get("phase_type", "3PH")).upper()

    # Factor de tensión c (s/ AEA 90909: 1.05 o 1.10 para máximas sobretensiones)
    c_factor = float(grid_data.get("c_factor", 1.05))

    # Impedancia aguas arriba acumulada (Red + Transfo + Cables previos)
    r_upstream = float(grid_data.get("r_upstream_ohm", 0.0))
    x_upstream = float(grid_data.get("x_upstream_ohm", 0.0))

    # Impedancia de este circuito en particular
    length_m = float(electrical.get("length_m", 0.0))
    parallels = int(electrical.get("parallels", 1))

    # Se asumen valores de catálogo o aproximados si no vienen del input de cable
    cable_info = circuit_data.get("cable", {})
    r_lineal = float(cable_info.get("resistance_ohm_per_m", 0.001))
    x_lineal = float(cable_info.get("reactance_ohm_per_m", 0.0001))

    # Cálculo de la resistencia y reactancia de este tramo
    r_cable = (r_lineal * length_m) / parallels
    x_cable = (x_lineal * length_m) / parallels

    # Resistencia y reactancia totales en el punto de falla
    r_total = r_upstream + r_cable
    x_total = x_upstream + x_cable

    # Impedancia del lazo Z_k
    z_k = math.sqrt((r_total**2) + (x_total**2))

    if z_k == 0.0:
        return 0.0

    # Aplicación de la fórmula según el tipo de fase (3PH o 1PH)
    if phase_type == "3PH":
        icc_amperes = (c_factor * voltage_v) / (math.sqrt(3.0) * z_k)
    else:
        # En 1PH el lazo de falla involucra Fase + Neutro (impedancia de ida y vuelta = 2 * Z)
        icc_amperes = (c_factor * voltage_v) / (2.0 * z_k)

    # Conversión a kiloamperes (kA)
    return round(icc_amperes / 1000.0, 2)


def _calculate_by_aea_tables_method(circuit_data: dict[str, Any]) -> float:
    """Simulación matemática del comportamiento decreciente de las tablas del Anexo 771-H.
    Estima la Icc remanente basándose en la distancia y sección.
    """
    electrical = circuit_data.get("electrical", {})
    length_m = float(electrical.get("length_m", 1.0))

    # Supongamos una Icc de cortocircuito en bornes de tablero de 4.5 kA
    icc_board = float(circuit_data.get("Icc_kA", 4.5))

    # Factor de atenuación exponencial empírico simulando la pérdida por longitud del conductor
    attenuation = math.exp(-0.015 * length_m)
    icc_estimated = icc_board * attenuation

    return round(max(icc_estimated, 1.0), 2)
