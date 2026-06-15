"""Archivo: tests/test_src_apexis_standards_aea90364_data_lookup.py
Descripción: Pruebas unitarias dinámicas para verificar la carga e integridad del
             registro de datos (Lookup) de la norma AEA 90364.
"""

import pytest

from apexis.standards.aea90364.data.lookup import AEA90364Lookup


@pytest.fixture
def lookup_registry():
    """Fixture de pytest que inicializa la clase Lookup levantando los archivos reales de disco.
    """
    return AEA90364Lookup()


def test_lookup_slots_and_magic_methods_integrity(lookup_registry):
    # 1. Validación de la optimización __slots__ (no debe existir __dict__)
    assert not hasattr(lookup_registry, "__dict__")

    # 2. Validación de las salidas de texto de los métodos mágicos
    repr_str = repr(lookup_registry)
    str_str = str(lookup_registry)

    assert "AEA90364Lookup" in repr_str
    assert "constants_loaded" in repr_str
    assert "AEA 90364 Data Registry" in str_str


def test_lookup_get_k_constant_dynamic(lookup_registry):
    # 1. Variables de entrada
    material = "Cu"
    insulation = "XLPE"

    # 2. Ejecución
    k_val = lookup_registry.get_k_constant(material, insulation)

    # 3. Assert dinámico contrastando contra la estructura leída directo del JSON cargado
    expected_k = lookup_registry.constants["k_values"][material][insulation]
    assert k_val == expected_k


def test_lookup_get_temperature_factor_dynamic(lookup_registry):
    # 1. Variables de entrada
    temp = 40.0
    insulation = "PVC"
    env = "AIR"

    # 2. Ejecución
    factor = lookup_registry.get_temperature_factor(temp, insulation, env)

    # 3. Assert dinámico cruzando las llaves del JSON de factores
    expected_factor = lookup_registry.factors["temperature_air"][insulation][str(int(temp))]
    assert factor == expected_factor


def test_lookup_get_base_ampacity_compound_method(lookup_registry):
    # 1. Variables de entrada (Probamos el cable de Cu de 2.5 mm² en cañería método B1 trifásico 3x)
    section = 2.5
    method = "B1-3x"
    material = "Cu"
    insulation = "PVC"

    # 2. Ejecución
    ampacity = lookup_registry.get_base_ampacity(section, method, material, insulation)

    # 3. Assert dinámico buscando manualmente en la lista leída del JSON de cables
    sections_list = lookup_registry.wires["materials"]["Cu"]["PVC"]["B1"]
    expected_ampacity = 0.0
    for entry in sections_list:
        if entry["section_mm2"] == section:
            expected_ampacity = entry["3x"]
            break

    assert ampacity == expected_ampacity


def test_lookup_get_available_sections(lookup_registry):
    # Validamos que devuelva las secciones comerciales en orden secuencial
    sections = lookup_registry.get_available_sections("Cu", "PVC", "B1-2x")

    assert len(sections) > 0
    assert sections[0] == 1.5
    assert sections[1] == 2.5
