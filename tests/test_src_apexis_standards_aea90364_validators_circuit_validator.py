"""Archivo: tests/test_src_apexis_standards_aea90364_validators_circuit_validator.py
Descripción: Pruebas unitarias dinámicas con escenarios de fallas regulatorias para
             validar el comportamiento rígido de la aduana AEA90364CircuitValidator.
"""

import pytest

from apexis.standards.aea90364.validators.circuit_validator import AEA90364CircuitValidator


def test_validator_slots_integrity() -> None:
    """Valida la optimización de memoria RAM e inmutabilidad por slots de la aduana.
    """
    assert hasattr(AEA90364CircuitValidator, "__slots__")
    assert AEA90364CircuitValidator.__slots__ == ()


def test_validate_ambient_temperature_failures_dynamic() -> None:
    """Prueba que el validador detenga el motor si se superan las temperaturas límites de tabla.
    """
    # Escenario 1: Forzar error por PVC por encima de 60°C
    with pytest.raises(ValueError) as exc_pvc:
        AEA90364CircuitValidator.validate_ambient_temperature(
            ambient_temp_c=65.0, insulation_material="PVC",
        )
    assert "PVC por encima de 60°C" in str(exc_pvc.value)

    # Escenario 2: Forzar error por temperaturas inferiores a 10°C
    with pytest.raises(ValueError) as exc_low:
        AEA90364CircuitValidator.validate_ambient_temperature(
            ambient_temp_c=5.0, insulation_material="XLPE",
        )
    assert "tablas de factores de corrección" in str(exc_low.value)


def test_validate_protection_limits_failures_dynamic() -> None:
    """Prueba que se respeten los calibres máximos reglamentarios según las secciones 770 y 771.
    """
    # Escenario 1: Forzar error en Sección 770 por PIA mayor a 63A
    with pytest.raises(ValueError) as exc_770:
        AEA90364CircuitValidator.validate_protection_limits(
            nominal_current_a=80.0, standard_section="770",
        )
    assert "excede el límite máximo permitido de 63 A" in str(exc_770.value)


def test_validate_method_compatibility_failures_dynamic() -> None:
    """Prueba que el sistema bloquee cruzamientos incoherentes entre fases y conductores del método.
    """
    # Escenario 1: Lazo 1PH intentando usar un método compuesto trifásico 'B1-3x'
    with pytest.raises(ValueError) as exc_1ph_fail:
        AEA90364CircuitValidator.validate_method_compatibility(
            installation_method="B1-3x", phase_type="1PH",
        )
    assert "exige un tendido trifásico" in str(exc_1ph_fail.value)

    # Escenario 2: Lazo 3PH intentando usar un método compuesto monofásico 'B2-2x'
    with pytest.raises(ValueError) as exc_3ph_fail:
        AEA90364CircuitValidator.validate_method_compatibility(
            installation_method="B2-2x", phase_type="3PH",
        )
    assert "restringe el tendido a 2 conductores" in str(exc_3ph_fail.value)
