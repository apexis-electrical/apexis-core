"""Archivo: tests/test_src_apexis_standards_aea90364_formulas_voltage_drop.py
Descripción: Pruebas unitarias dinámicas para verificar los métodos de cálculo
             de caída de tensión (GDC, IMPEDANCE, TABLES) para 1PH y 3PH.
"""

from apexis.standards.aea90364.formulas.voltage_drop import (
    calculate_voltage_drop,
    verify_voltage_drop_limit,
)


def test_calculate_voltage_drop_gdc_mode_1ph() -> None:
    # 1. Definir variables de entrada
    section = 1.5
    current = 10.0
    gdc_test_val = 0.040
    mock_circuit = {
        "electrical": {"voltage_v": 220.0, "length_m": 15.0, "phase_type": "1PH", "parallels": 1},
    }

    # 2. Ejecutar la función
    p_drop = calculate_voltage_drop(
        mode="GDC",
        circuit_data=mock_circuit,
        section_mm2=section,
        design_current_a=current,
        gdc_unit_value=gdc_test_val,
    )

    # 3. Assert dinámico corregido: El GDC 0.040 ya incluye ida y vuelta, NO lleva phase_multiplier
    expected_v_drop_abs = (
        gdc_test_val * current * mock_circuit["electrical"]["length_m"]
    ) / section
    expected_p_drop = (expected_v_drop_abs / mock_circuit["electrical"]["voltage_v"]) * 100.0
    assert p_drop == round(expected_p_drop, 2)


def test_calculate_voltage_drop_gdc_mode_3ph() -> None:
    # 1. Definir variables de entrada
    section = 10.0
    current = 40.0
    gdc_test_val = 0.035
    mock_circuit = {
        "electrical": {"voltage_v": 380.0, "length_m": 50.0, "phase_type": "3PH", "parallels": 1},
    }

    # 2. Ejecutar la función
    p_drop = calculate_voltage_drop(
        mode="GDC",
        circuit_data=mock_circuit,
        section_mm2=section,
        design_current_a=current,
        gdc_unit_value=gdc_test_val,
    )

    # 3. Assert dinámico corregido para 3PH s/ factor duplicado
    expected_v_drop_abs = (
        gdc_test_val * current * mock_circuit["electrical"]["length_m"]
    ) / section
    expected_p_drop = (expected_v_drop_abs / mock_circuit["electrical"]["voltage_v"]) * 100.0
    assert p_drop == round(expected_p_drop, 2)


def test_calculate_voltage_drop_tables_mode() -> None:
    # 1. Definir variables de entrada
    section = 2.5
    current = 16.0
    mock_circuit = {
        "electrical": {"voltage_v": 220.0, "length_m": 100.0, "phase_type": "1PH", "parallels": 1},
        "installation": {"material": "Cu", "insulation": "PVC"},
    }
    mock_tables = {"CU": {"PVC": {"1PH": {"2.5": 15.2}}}}

    # 2. Ejecutar la función
    p_drop = calculate_voltage_drop(
        mode="TABLES",
        circuit_data=mock_circuit,
        section_mm2=section,
        design_current_a=current,
        tables_database=mock_tables,
    )

    # 3. Assert dinámico
    v_drop_unit = (
        mock_tables["CU"]["PVC"]["1PH"][str(section)] / mock_circuit["electrical"]["parallels"]
    )
    length_km = mock_circuit["electrical"]["length_m"] / 1000.0
    expected_v_drop_abs = v_drop_unit * current * length_km
    expected_p_drop = (expected_v_drop_abs / mock_circuit["electrical"]["voltage_v"]) * 100.0
    assert p_drop == round(expected_p_drop, 2)


def test_verify_voltage_drop_limit_cases() -> None:
    assert verify_voltage_drop_limit(percentage_drop=2.9, purpose_type="lighting") == (2.9 <= 3.0)
    assert verify_voltage_drop_limit(percentage_drop=3.1, purpose_type="lighting") == (3.1 <= 3.0)
