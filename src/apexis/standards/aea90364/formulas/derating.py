"""Archivo: src/apexis/standards/aea90364/formulas/derating.py
Descripción: Lógica matemática para el cálculo de todos los factores de corrección
             (derating) aplicables a la ampacidad según la memoria técnica AEA 90364.
"""

from typing import Any


def calculate_temperature_factor(
    ambient_temp: float,
    installation_method: str,
    insulation_material: str,
    temperature_tables: dict[str, Any],
) -> float:
    """Busca el factor de corrección por temperatura ambiente o de terreno (f_t).
    Deduce el ambiente (aire o suelo) analizando el método de instalación.

    Args:
        ambient_temp: Temperatura ambiente real del proyecto (ej: 40.0).
        installation_method: Método de instalación del input (ej: "B2-2x").
        insulation_material: Material aislante ("PVC" o "XLPE").
        temperature_tables: Estructura de datos mapeada desde las tablas de la norma.

    Returns:
        float: Factor f_t de corrección térmica por temperatura.

    """
    # Los métodos D1 y D2 en AEA corresponden a instalaciones enterradas
    environment = "GROUND" if installation_method.upper().startswith("D") else "AIR"
    key = f"{insulation_material.upper()}_{environment}"

    factors_dict = temperature_tables.get(key, {})
    factor = factors_dict.get(str(ambient_temp))

    if factor is None:
        # Fallback de seguridad si el valor no está explícito en la tabla
        return 1.0

    return float(factor)


def lookup_grouping_factor(
    grouped_circuits: int,
    installation_method: str,
    grouping_table: dict[str, list[float]],
) -> float:
    """Busca el factor de corrección por agrupamiento de circuitos (f_g).

    Args:
        grouped_circuits: Cantidad de circuitos agrupados en la misma canalización (ej: 1).
        installation_method: Método de instalación del input (ej: "B2-2x").
        grouping_table: Lista de factores indexada por el prefijo del método.

    Returns:
        float: Factor f_g de agrupación (1.0 si no hay agrupamiento o no se encuentra).

    """
    if grouped_circuits <= 1:
        return 1.0

    # Extraemos el prefijo del método (ej: de "B2-2x" extraemos "B2")
    method_prefix = installation_method.split("-", maxsplit=1)[0].upper()
    factors_list = grouping_table.get(method_prefix)

    if not factors_list:
        return 1.0

    # El índice de la lista corresponde a (número de circuitos - 1)
    index = grouped_circuits - 1
    if index >= len(factors_list):
        return float(factors_list[-1])

    return float(factors_list[index])


def calculate_global_derating_factor(
    temperature_factor: float,
    grouping_factor: float,
    installation_method: str,
    soil_type: str = "default",
    wire_burial_depth_m: float = 0.0,
    soil_tables: dict[str, Any] | None = None,
) -> float:
    """Ejecuta la sumatoria multiplicativa de todos los coeficientes ambientales
    definidos en la ecuación maestra de la memoria técnica de APEXIS.

    Fórmula: F_derating = f_t * f_g * f_s * f_p * f_flex * f_sim

    Args:
        temperature_factor: Coeficiente por temperatura (f_t).
        grouping_factor: Coeficiente por agrupamiento (f_g).
        installation_method: Método de instalación para verificar si aplican f_s y f_p.
        soil_type: Tipo de suelo del input para resistividad térmica.
        wire_burial_depth_m: Profundidad de instalación en metros.
        soil_tables: Diccionario opcional con coeficientes f_s y f_p para enterrados.

    Returns:
        float: Factor de derating global acumulado (redondeado a 2 decimales).

    """
    f_t = temperature_factor
    f_g = grouping_factor
    f_s = 1.0
    f_p = 1.0
    f_flex = 1.0  # Reservado para conductores Clase 5 si fuera necesario
    f_sim = 1.0  # Reservado para asimetrías de conductores en paralelo

    is_buried = installation_method.upper().startswith("D")

    if is_buried and soil_tables:
        # Factor por resistividad térmica del suelo (f_s)
        f_s = soil_tables.get("resistivity", {}).get(soil_type.lower(), 1.0)
        # Factor por profundidad de instalación (f_p)
        depth_key = f"{wire_burial_depth_m:.2f}"
        f_p = soil_tables.get("depth", {}).get(depth_key, 1.0)

    global_factor = f_t * f_g * f_s * f_p * f_flex * f_sim
    return round(global_factor, 2)
