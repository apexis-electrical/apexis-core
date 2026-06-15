"""Archivo: tests/test_src_apexis_standards_aea90364_formulas_ampacity.py
Descripción: Pruebas unitarias dinámicas para validar los cálculos de corriente de proyecto,
             ampacidad nominal, ampacidad corregida y coordinación según AEA 90364.
"""

from apexis.standards.aea90364.formulas.ampacity import (
    calculate_corrected_ampacity,
    calculate_design_current,
    lookup_nominal_ampacity,
    verify_protection_coordination,
)


def test_calculate_design_current_1ph() -> None:
    """Valida el cálculo de la corriente de proyecto para un sistema 1PH.
    """
    # 1. Definir variables de entrada (Circuito C-01: 1PH, 220V, 2.2 kVA)
    load = 2.2
    voltage = 220.0
    phase = "1PH"

    # 2. Ejecutar la función
    ib = calculate_design_current(
        load_value=load, load_unit="kVA", voltage_v=voltage, phase_type=phase,
    )

    # 3. Assert dinámico reproduciendo la ecuación para 1PH
    assert ib == round((load * 1000.0) / voltage, 2)


def test_calculate_design_current_conversion_kw_3ph() -> None:
    """Valida la conversión de kW a kVA y el cálculo de corriente para un sistema 3PH.
    """
    # 1. Definir variables de entrada (Sistema 3PH, 380V, 4.5 kW)
    load_kw = 4.5
    voltage = 380.0
    phase = "3PH"
    cos_phi = 0.90

    # 2. Ejecutar la función
    ib = calculate_design_current(
        load_value=load_kw, load_unit="kW", voltage_v=voltage, phase_type=phase, cos_phi=cos_phi,
    )

    # 3. Assert dinámico reproduciendo la normalización S = P/cos_phi y ecuación 3PH
    s_kva = load_kw / cos_phi
    expected_ib = (s_kva * 1000.0) / (1.7320508 * voltage)
    assert ib == round(expected_ib, 2)


def test_lookup_nominal_ampacity() -> None:
    """Valida la búsqueda de ampacidad nominal base en la base de datos simulada.
    """
    # 1. Definir variables de entrada
    size = 2.5
    method = "B2-2x"
    mat = "Cu"
    ins = "PVC"
    mock_db = {"CU": {"PVC": {"B2-2X": {"2.5": 19.5}}}}

    # 2. Ejecutar la función
    ampacity = lookup_nominal_ampacity(
        conductor_size=size,
        installation_method=method,
        material=mat,
        insulation=ins,
        ampacity_database=mock_db,
    )

    # 3. Assert dinámico extrayendo las llaves normalizadas del mock
    assert ampacity == mock_db["CU"]["PVC"]["B2-2X"]["2.5"]


def test_calculate_corrected_ampacity() -> None:
    """Valida la aplicación de factores de corrección y márgenes de diseño sobre la ampacidad.
    """
    # 1. Definir variables de entrada
    nominal = 19.5
    derating = 0.61
    parallels = 2
    margin = 1.05

    # 2. Ejecutar la función
    iz = calculate_corrected_ampacity(
        nominal_ampacity=nominal,
        global_derating_factor=derating,
        parallels=parallels,
        ampacity_margin=margin,
    )

    # 3. Assert dinámico reproduciendo la ecuación multiplicativa de la memoria
    assert iz == round(nominal * derating * parallels * margin, 1)


def test_verify_protection_coordination() -> None:
    """Valida las inecuaciones lógicas de coordinación de protecciones por sobrecarga.
    """
    # 1. Definir variables de entrada
    ib = 10.0
    iz = 19.5
    in_valid = 16.0
    in_invalid = 25.0

    # 2. Ejecutar y evaluar con asserts lógicos directos
    assert verify_protection_coordination(ib, in_valid, iz) == (ib <= in_valid <= iz)
    assert verify_protection_coordination(ib, in_invalid, iz) == (ib <= in_invalid <= iz)
