"""Archivo: tests/test_src_apexis_standards_aea90364_adapter.py
Descripción: Pruebas unitarias integradas dinámicas para validar el comportamiento del
             adaptador de la norma AEA 90364 bajo escenarios reales de circuitos.
"""

from apexis.standards.aea90364.adapter import AEA90364Adapter


def test_adapter_slots_and_magic_methods() -> None:
    """Valida de forma autónoma el blindaje de memoria por slots y las respuestas
    de los métodos mágicos de texto en el adaptador.
    """
    # Instanciamos el adaptador de manera directa
    adapter = AEA90364Adapter()

    # Validamos que la optimización __slots__ esté activa (no posee __dict__ interno)
    assert not hasattr(adapter, "__dict__")

    # Validamos las salidas de los métodos mágicos de strings
    assert "AEA90364Adapter" in repr(adapter)
    assert "AEA 90364" in str(adapter)


def test_process_circuit_design_c01_lighting_dynamic() -> None:
    """Valida el ciclo de diseño iterativo completo para el circuito C-01 utilizando
    asserts dinámicos acoplados a las tablas y fórmulas analíticas.
    """
    # 1. Clonamos exactamente el diccionario de tu circuito de entrada C-01
    mock_circuit_c01 = {
        "tag": "C-01",
        "origin": "TPBT",
        "destination": "IUG en Planta Baja",
        "purpose": {
            "type": "lighting",
            "subtype": "iug",
        },
        "electrical": {
            "phase_type": "1PH",
            "voltage_v": 220.0,
            "parallels": 1,
            "length_m": 15.0,  # Simplificado para control matemático directo
            "load": {
                "value": 2.2,
                "unit": "kVA",
            },
        },
        "installation": {
            "installation_method": "B1-2x",  # Forzamos B1-2x para empalmar con tus JSON expuestos
            "material": "Cu",
            "insulation": "PVC",
            "installation_temp_c": 40.0,  # 40°C provocará derating f_t = 1.00 s/ factors.json
            "grouped_circuits": 1,
            "soil_type": "default",
            "wire_burial_depth_m": 0.0,
        },
        "short_circuit": {
            "mode": "skip",
            "Icc_kA": 4.5,
            "time_s": 0.5,
        },
        "cable": {
            "voltage_drop_method": "GDC",
            "mode": "auto",
            "section_mm2": None,
        },
    }

    mock_criteria = {
        "cos_phi": 0.90,
        "ampacity_margin": 1.00,
    }

    # 2. Instanciamos el adaptador real
    adapter = AEA90364Adapter()

    # 3. Ejecutamos la lógica integrada
    results = adapter.process_circuit_design(mock_circuit_c01, mock_criteria)

    # 4. Asserts Dinámicos de Verificación
    # Ib esperado = (2.2 * 1000) / 220 = 10.0 A
    assert results["ib_a"] == 10.00

    # El piso de sección para 'lighting' es 1.5mm².
    # El cable Cu PVC B1-2x de 1.5mm² en bornes nominales s/ wires.json tiene una ampacidad de 15A.
    # El derating para 40°C en aire s/ factors.json es 1.00. Circuitos agrupados 1 = 1.00 -> Iz = 15.0A.
    # Ib (10A) <= Iz (15A) -> Aprueba ampacidad en 1.5mm².
    # Verificamos caída por GDC para 1.5mm²: (0.040 * 10 * 15) / 1.5 = 4.0V -> (4 / 220) * 100 = 1.82%
    # 1.82% <= 3.0% (Límite iluminación) -> Aprueba todo en 1.5mm².

    assert results["section_mm2"] == 1.5
    assert results["pe_section_mm2"] == 1.5  # S <= 16 -> PE = S
    assert results["voltage_drop_pct"] == 1.82
    assert results["status"] == "APPROVED"
