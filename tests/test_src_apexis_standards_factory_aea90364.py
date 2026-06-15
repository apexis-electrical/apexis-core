"""Archivo: tests/test_src_apexis_standards_factory_aea90364.py
Descripción: Pruebas unitarias dinámicas de alta cobertura para validar la robustez,
             los métodos mágicos y las optimizaciones de la factoría StandardAdapterFactory.
"""

import pytest

from apexis.standards.aea90364.adapter import AEA90364Adapter
from apexis.standards.factory import ElectricalStandardEnum, StandardAdapterFactory


@pytest.fixture
def factory_instance() -> StandardAdapterFactory:
    """Fixture que provee una instancia fresca de la factoría optimizada para cada test.
    """
    return StandardAdapterFactory()


def test_factory_slots_optimization_check(factory_instance):
    # Validamos dinámicamente que la optimización __slots__ esté activa en la clase.
    # Una clase con __slots__ no posee un diccionario interno por defecto (__dict__).
    assert not hasattr(factory_instance, "__dict__")
    assert hasattr(StandardAdapterFactory, "__slots__")


def test_factory_magic_methods_output(factory_instance):
    # 1. Ejecutar las funciones mágicas de strings
    repr_output = repr(factory_instance)
    str_output = str(factory_instance)

    # 2. Asserts dinámicos comprobando la estructura de nombres de clase reales
    assert factory_instance.__class__.__name__ in repr_output
    assert "active_adapters" in repr_output
    assert "Standard Provider Engine" in str_output


def test_factory_resolve_active_adapter_dynamic(factory_instance):
    # 1. Variables de entrada
    input_str = "aea90364"

    # 2. Ejecución
    adapter = factory_instance.get_adapter(input_str)

    # 3. Assert de tipo de instancia
    assert isinstance(adapter, AEA90364Adapter)


def test_factory_mapped_but_pending_standard_exception(factory_instance):
    # Validamos que se lance NotImplementedError con el desglose exacto de la región
    input_unimplemented = "nec2023"
    catalog = factory_instance.get_catalog()

    # Buscamos el Enum asociado
    target_enum = ElectricalStandardEnum.NEC_2023
    assert target_enum in catalog["AMERICA"]

    with pytest.raises(NotImplementedError) as exc_info:
        factory_instance.get_adapter(input_unimplemented)

    assert input_unimplemented in str(exc_info.value)


def test_factory_completely_invalid_standard_exception(factory_instance):
    # Validamos que arroje ValueError si se ingresa texto basura o no homologado
    garbage_input = "norma_inexistente_de_prueba_bt"

    with pytest.raises(ValueError) as exc_info:
        factory_instance.get_adapter(garbage_input)

    assert garbage_input in str(exc_info.value)
