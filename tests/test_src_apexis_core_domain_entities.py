"""Archivo: tests/test_src_apexis_core_domain_entities.py
Descripción: Pruebas unitarias integradas dinámicas para validar las optimizaciones,
             métodos mágicos e inicialización de longitudes de las entidades del Core.
"""

import pytest

from apexis.core.domain.entities import ElectricalCircuit


def test_electrical_circuit_length_auto_resolution_and_slots():
    # 1. Copiamos los bloques exactos de tu entrada C-01, pasando la longitud como una lista/tupla de tramos
    lengths_sequence = (
        15.03,
        3.82,
        1.67,
        1.71,
        0.2,
        0.78,
        0.25,
        0.19,
        0.52,
        0.19,
        3.04,
        0.84,
        0.46,
        3.88,
        0.84,
        0.52,
        1.51,
        0.78,
        0.31,
        0.6,
        1.21,
        7.68,
        1.59,
        0.67,
        4.69,
        1.69,
        0.87,
    )

    mock_input_c01 = {
        "tag": "C-01",
        "origin": "TPBT",
        "destination": "IUG en Planta Baja",
        "purpose": {"type": "lighting", "subtype": "iug"},
        "electrical": {
            "phase_type": "1PH",
            "voltage_v": 220,
            "parallels": 1,
            "length_m": lengths_sequence,
            "load": {"value": 2.2, "unit": "kVA"},
        },
        "installation": {
            "installation_method": "B2-2x",
            "material": "Cu",
            "insulation": "PVC",
            "installation_temp_c": 40.0,
            "grouped_circuits": 1,
        },
        "short_circuit": {"mode": "skip", "Icc_kA": 4.5, "time_s": 0.5},
        "cable": {"voltage_drop_method": "GDC", "mode": "auto", "section_mm2": None},
    }

    # 2. Instanciamos la entidad
    circuit = ElectricalCircuit(**mock_input_c01)

    # 3. Asserts dinámicos de integridad
    # A. Verificamos que la longitud se haya sumado de forma automática y matemática exacta
    assert circuit.electrical.length_m == round(sum(lengths_sequence), 3)

    # B. Verificamos la propiedad de sección equivalente inicial (S=None -> S_eq=0.0)
    assert circuit.equivalent_section_mm2 == 0.0

    # C. Modificamos la sección simulando la respuesta del motor y reevaluamos la propiedad
    circuit.cable.section_mm2 = 2.5
    circuit.electrical.parallels = 2
    assert circuit.equivalent_section_mm2 == (2 * 2.5)

    # D. Verificamos el blindaje estructural de __slots__ (No debe permitir inyección de basura)
    assert not hasattr(circuit, "__dict__")
    with pytest.raises(AttributeError):
        circuit.property_inventada_error = (
            "test"  # Intentar meter un atributo fuera de slots debe reventar
        )

    # E. Verificamos las salidas de los métodos mágicos de representación
    assert "C-01" in repr(circuit)
    assert "IUG en Planta Baja" in str(circuit)
