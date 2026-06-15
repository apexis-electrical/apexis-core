"""Archivo: tests/test_src_apexis_standards_aea90364_formulas_derating.py
Descripción: Pruebas unitarias dinámicas para validar las funciones de factores de
             corrección (derating) del módulo de la norma AEA 90364.
"""

from apexis.standards.aea90364.formulas.derating import (
    calculate_global_derating_factor,
    calculate_temperature_factor,
    lookup_grouping_factor,
)


def test_calculate_temperature_factor_air():
    # 1. Definir variables de entrada
    ambient_temp = 40.0
    mock_tables = {"PVC_AIR": {"30.0": 1.00, "40.0": 0.87, "50.0": 0.71}}

    # 2. Ejecutar la función
    factor = calculate_temperature_factor(
        ambient_temp=ambient_temp,
        installation_method="B2-2x",
        insulation_material="PVC",
        temperature_tables=mock_tables,
    )

    # 3. Assert dinámico basado en la estructura de datos
    expected_factor = mock_tables["PVC_AIR"][str(ambient_temp)]
    assert factor == expected_factor


def test_lookup_grouping_factor():
    # 1. Definir variables de entrada
    circuits = 3
    method = "B2-2x"
    method_family = method.split("-", maxsplit=1)[0].upper()
    mock_table = {"B2": [1.0, 0.80, 0.70]}

    # 2. Ejecutar la función
    factor = lookup_grouping_factor(
        grouped_circuits=circuits, installation_method=method, grouping_table=mock_table,
    )

    # 3. Assert dinámico mapeando el índice de la lista (n - 1)
    expected_index = circuits - 1
    expected_factor = mock_table[method_family][expected_index]
    assert factor == expected_factor


def test_calculate_global_derating_factor_air():
    # 1. Definir variables de entrada
    f_t = 0.87
    f_g = 0.70

    # 2. Ejecutar la función
    global_factor = calculate_global_derating_factor(
        temperature_factor=f_t, grouping_factor=f_g, installation_method="B2-2x",
    )

    # 3. Assert dinámico reproduciendo la ecuación de la memoria técnica
    assert global_factor == round(f_t * f_g, 2)
