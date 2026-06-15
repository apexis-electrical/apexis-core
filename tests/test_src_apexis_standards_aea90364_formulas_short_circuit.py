"""Archivo: tests/test_src_apexis_standards_aea90364_formulas_short_circuit.py
Descripción: Pruebas unitarias dinámicas para verificar los métodos de cálculo
             de cortocircuito (Icc) y la solicitación térmica (I^2t) de APEXIS.
"""

import math

from apexis.standards.aea90364.formulas.short_circuit import calculate_short_circuit_current
from apexis.standards.aea90364.formulas.thermal_stress import (
    get_material_constant_k,
    verify_thermal_stress,
)


def test_calculate_short_circuit_manual_mode():
    # 1. Definir variables de entrada
    mock_circuit = {"short_circuit": {"Icc_kA": 4.5, "time_s": 0.5}}

    # 2. Ejecutar la función
    icc = calculate_short_circuit_current(mode="manual", circuit_data=mock_circuit["short_circuit"])

    # 3. Assert dinámico directo
    assert icc == mock_circuit["short_circuit"]["Icc_kA"]


def test_calculate_short_circuit_impedance_3ph():
    # 1. Definir variables de entrada
    mock_circuit = {
        "electrical": {"phase_type": "3PH", "voltage_v": 380.0, "length_m": 50.0, "parallels": 1},
        "cable": {"resistance_ohm_per_m": 0.002, "reactance_ohm_per_m": 0.0001},
    }
    mock_grid = {"c_factor": 1.05, "r_upstream_ohm": 0.03, "x_upstream_ohm": 0.01}

    # 2. Ejecutar la función
    icc = calculate_short_circuit_current(
        mode="impedance", circuit_data=mock_circuit, grid_data=mock_grid,
    )

    # 3. Assert dinámico reproduciendo la topología completa de mallas
    r_cable = (
        mock_circuit["cable"]["resistance_ohm_per_m"] * mock_circuit["electrical"]["length_m"]
    ) / mock_circuit["electrical"]["parallels"]
    x_cable = (
        mock_circuit["cable"]["reactance_ohm_per_m"] * mock_circuit["electrical"]["length_m"]
    ) / mock_circuit["electrical"]["parallels"]
    r_total = mock_grid["r_upstream_ohm"] + r_cable
    x_total = mock_grid["x_upstream_ohm"] + x_cable
    z_k = math.sqrt((r_total**2) + (x_total**2))

    expected_icc_amperes = (mock_grid["c_factor"] * mock_circuit["electrical"]["voltage_v"]) / (
        math.sqrt(3.0) * z_k
    )
    assert icc == round(expected_icc_amperes / 1000.0, 2)


def test_verify_thermal_stress_cases():
    # 1. Definir variables de entrada
    icc = 1.5
    time = 0.1
    section_fail = 2.5
    section_pass = 6.0
    mat = "Cu"
    ins = "PVC"

    # 2. Ejecutar la función
    result_fail = verify_thermal_stress(icc, time, section_fail, mat, ins)
    result_pass = verify_thermal_stress(icc, time, section_pass, mat, ins)

    # 3. Asserts dinámicos comparando contra las ecuaciones de energía pasante
    k = get_material_constant_k(mat, ins)
    inserted_energy = (icc * 1000.0) ** 2 * time

    assert result_fail == (inserted_energy <= (k**2 * section_fail**2))
    assert result_pass == (inserted_energy <= (k**2 * section_pass**2))
