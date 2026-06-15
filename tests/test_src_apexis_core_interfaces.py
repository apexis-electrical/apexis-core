"""Archivo: tests/test_src_apexis_core_interfaces.py
Descripción: Pruebas unitarias para validar las restricciones, excepciones y el blindaje
             estructural por slots de las interfaces abstractas del Core.
"""

import pytest

from apexis.core.interfaces.calculator import ElectricalCalculatorInterface
from apexis.core.interfaces.data_provider import DataProviderInterface
from apexis.core.interfaces.repository import ProjectRepositoryInterface


def test_interfaces_are_strictly_abstract() -> None:
    """Verifica dinámicamente que ninguna interfaz pura pueda ser instanciada de forma directa,
    forzando el lanzamiento de un TypeError nativo.
    """
    # 1. Intentar instanciar el puerto de cálculo directo debe fallar
    with pytest.raises(TypeError) as exc_info_calc:
        ElectricalCalculatorInterface()
    assert "Can't instantiate abstract class" in str(exc_info_calc.value)

    # 2. Intentar instanciar el puerto de datos directo debe fallar
    with pytest.raises(TypeError) as exc_info_data:
        DataProviderInterface()
    assert "Can't instantiate abstract class" in str(exc_info_data.value)

    # 3. Intentar instanciar el puerto de repositorio directo debe fallar
    with pytest.raises(TypeError) as exc_info_repo:
        ProjectRepositoryInterface()
    assert "Can't instantiate abstract class" in str(exc_info_repo.value)


def test_interfaces_slots_optimization_integrity() -> None:
    """Valida que las tres interfaces puras tengan bloqueado el uso de memoria RAM
    mediante __slots__ vacíos, impidiendo que arrastren overhead oculto hacia las subclases.
    """
    assert hasattr(ElectricalCalculatorInterface, "__slots__")
    assert ElectricalCalculatorInterface.__slots__ == ()

    assert hasattr(DataProviderInterface, "__slots__")
    assert DataProviderInterface.__slots__ == ()

    assert hasattr(ProjectRepositoryInterface, "__slots__")
    assert ProjectRepositoryInterface.__slots__ == ()


def test_interface_implementation_enforcement() -> None:
    """Simula dinámicamente el error de un desarrollador externo que hereda de la interfaz
    pero olvida codificar una función obligatoria, verificando que Python bloquee la instanciación.
    """

    # Creamos una clase defectuosa de prueba que hereda pero no escribe el método 'process_circuit_design'
    class DefectiveCalculator(ElectricalCalculatorInterface):
        pass

    with pytest.raises(TypeError) as exc_info:
        DefectiveCalculator()

    assert "process_circuit_design" in str(exc_info.value)
