"""Archivo: tests/test_src_apexis_core_utils_converters.py
Descripción: Pruebas unitarias dinámicas con fórmulas testigo para validar la precisión
             y optimización del módulo utilitario PowerConverter.
"""

from apexis.core.utils.converters import PowerConverter


def test_converter_slots_and_integrity() -> None:
    """Valida la optimización física de slots en la clase estática utilitaria.
    """
    assert hasattr(PowerConverter, "__slots__")
    assert PowerConverter.__slots__ == ()


def test_converter_to_apparent_power_kva_dynamic() -> None:
    """Audita dinámicamente las conversiones aplicando fórmulas testigo manuales del test.
    """
    cos_phi_test = 0.85

    # 1. Prueba de kW a kVA
    kw_value = 5.5
    calculated_from_kw = PowerConverter.to_apparent_power_kva(kw_value, "kW", cos_phi=cos_phi_test)
    expected_from_kw = kw_value / cos_phi_test
    assert calculated_from_kw == round(expected_from_kw, 3)

    # 2. Prueba de W a kVA
    w_value = 1500.0
    calculated_from_w = PowerConverter.to_apparent_power_kva(w_value, "W", cos_phi=cos_phi_test)
    expected_from_w = (w_value / 1000.0) / cos_phi_test
    assert calculated_from_w == round(expected_from_w, 3)

    # 3. Prueba de VA a kVA
    va_value = 2500.0
    calculated_from_va = PowerConverter.to_apparent_power_kva(va_value, "VA")
    expected_from_va = va_value / 1000.0
    assert calculated_from_va == round(expected_from_va, 3)

    # 4. Prueba de HP a kVA (Fórmula de la memoria con rendimiento motor = 0.85)
    hp_value = 2.0
    calculated_from_hp = PowerConverter.to_apparent_power_kva(hp_value, "HP", cos_phi=cos_phi_test)
    expected_from_hp = (hp_value * 0.746) / (cos_phi_test * 0.85)
    assert calculated_from_hp == round(expected_from_hp, 3)

    # 5. Prueba de kVA directo (Debe retornar el mismo valor)
    kva_value = 12.34
    assert PowerConverter.to_apparent_power_kva(kva_value, "kVA") == kva_value
