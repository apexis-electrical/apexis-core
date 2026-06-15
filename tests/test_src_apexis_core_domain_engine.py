"""Archivo: tests/test_src_apexis_core_domain_engine.py
Descripción: Pruebas unitarias e integradas dinámicas para validar la orquestación
             global del motor de cálculo principal APEXISEngine.
"""

import pathlib

from apexis.core.domain.engine import APEXISEngine


def test_engine_integration_latch_c01_dynamic() -> None:
    """Valida el flujo end-to-end simulando la ejecución real de APEXIS para el circuito C-01.
    """
    standard_name = "aea90364"
    global_criteria = {
        "cos_phi": 0.90,
        "ampacity_margin": 1.00,
    }

    # Declaramos la secuencia de tramos en una variable fija para la contraprueba
    lengths_sequence = [
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
    ]

    circuits_batch = [
        {
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
                "length_m": lengths_sequence,
                "load": {
                    "value": 2.2,
                    "unit": "kVA",
                },
            },
            "installation": {
                "installation_method": "B1-2x",
                "material": "Cu",
                "insulation": "PVC",
                "installation_temp_c": 40.0,
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
        },
    ]

    # CORREGIDO: Calculamos la sumatoria testigo ANTES de que el Core mute el diccionario
    expected_sum = round(sum(lengths_sequence), 3)

    engine = APEXISEngine(standard=standard_name, criteria=global_criteria)

    assert not hasattr(engine, "__dict__")
    assert "APEXISEngine" in repr(engine)
    assert "APEXIS Main Core Engine" in str(engine)

    results_table = engine.calculate_circuits(circuits_batch)

    assert len(results_table) == 1
    c01_res = results_table[0]

    assert c01_res["tag"] == "C-01"
    assert c01_res["ib_a"] == 10.00
    assert c01_res["section_mm2"] == 4.0
    assert c01_res["pe_section_mm2"] == 4.0
    assert c01_res["voltage_drop_pct"] == 2.52
    assert c01_res["status"] == "APPROVED"
    assert c01_res["total_length_m"] == expected_sum


def test_engine_batch_plugins_export_logic(tmp_path) -> None:
    """Verifica que el motor procese correctamente colecciones de plugins en paralelo.
    """
    from apexis.core.exporters.markdown_exporter import MarkdownReportExporter

    engine = APEXISEngine(standard="aea90364", criteria={"cos_phi": 0.90})
    mock_results = [{"tag": "C-01", "ib_a": 10.0, "section_mm2": 2.5}]

    dummy_report = tmp_path / "detailed_report.md"
    dummy_report.write_text("{{RESULTS_TABLE}}", encoding="utf-8")

    plugin_pipeline = [MarkdownReportExporter(template_path=str(dummy_report))]
    base_out = str(tmp_path / "project_report")

    summary = engine.export_results(mock_results, plugin_pipeline, base_out)

    assert ".md" in summary
    assert summary[".md"] is True
    assert pathlib.Path(f"{base_out}.md").exists()
