"""Archivo: tests/test_src_apexis_core_exporters_markdown_exporter.py
Description: Pruebas unitarias dinámicas para auditar el funcionamiento, slots y
             reemplazo de tokens del generador de reportes MarkdownReportExporter.
"""

import pathlib

from apexis.core.exporters.markdown_exporter import MarkdownReportExporter


def test_exporter_slots_and_file_generation_dynamic(tmp_path: pathlib.Path) -> None:
    """Crea una plantilla efímera en la carpeta temporal de pytest, inyecta datos
    del lazo y valida dinámicamente que el token {{RESULTS_TABLE}} se pise con éxito.
    """
    # 1. Validamos la restricción física de slots de memoria
    assert hasattr(MarkdownReportExporter, "__slots__")
    assert "_template_path" in MarkdownReportExporter.__slots__

    # 2. Generamos una plantilla dummy temporal para simular detailed_report.md
    dummy_template = tmp_path / "dummy_report.md"
    dummy_template.write_text(
        "# Memoria de Cálculo\n\n{{RESULTS_TABLE}}\n\nFin del Reporte.", encoding="utf-8",
    )

    # Mapeamos una fila testigo de control
    mock_results = [
        {
            "tag": "C-01",
            "ib_a": 10.0,
            "iz_a": 26.0,
            "section_mm2": 4.0,
            "pe_section_mm2": 4.0,
            "voltage_drop_pct": 2.52,
            "icc_ka": 0.0,
            "status": "APPROVED",
        },
    ]

    output_report = tmp_path / "final_output_memory.md"

    # 3. Instanciamos e invocamos al exportador de infraestructura
    exporter = MarkdownReportExporter(template_path=str(dummy_template))
    success = exporter.export_report(mock_results, output_path=str(output_report))

    # 4. Asserts dinámicos cruzados
    assert success is True
    assert output_report.exists()

    # Leemos el archivo final generado para comprobar el parseo atómico
    generated_content = output_report.read_text(encoding="utf-8")

    assert (
        "{{RESULTS_TABLE}}" not in generated_content
    )  # El token tuvo que haber sido destruido y pisado
    assert "C-01" in generated_content
    assert "2.52%" in generated_content
    assert "|APPROVED|" in generated_content.replace(" ", "")
