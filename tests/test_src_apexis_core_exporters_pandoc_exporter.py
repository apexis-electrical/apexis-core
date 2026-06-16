"""
Archivo: tests/test_src_apexis_core_exporters_pandoc_exporter.py
Descripción: Pruebas unitarias para el adaptador PandocReportExporter enfocado en la
             compilación secuencial de archivos .md a .docx usando pathlib.
"""

import unittest
import pathlib

from unittest.mock import patch, MagicMock
from apexis.core.exporters.pandoc_exporter import PandocReportExporter


class TestPandocExporter(unittest.TestCase):
    """
    Suite de pruebas para validar la compilación por tuberías de PandocExporter.
    """

    def setUp(self) -> None:
        """
        Configura la instancia del adaptador para las pruebas.
        """
        self.exporter = PandocReportExporter()
        self.dummy_results = [{"circuit": "C1"}]
        self.base_output = "outputs/simulation_report"

    def test_resolved_extension_returns_docx(self) -> None:
        """
        Valida que el plugin declare explícitamente la extensión .docx al motor.
        """
        self.assertEqual(self.exporter.resolved_extension, ".docx")

    @patch("pypandoc.convert_file")
    @patch.object(pathlib.Path, "exists")
    def test_export_report_compiles_docx_from_existing_md(
        self, mock_exists: MagicMock, mock_convert: MagicMock
    ) -> None:
        """
        Valida que Pandoc lea el archivo .md existente y lo compile a .docx con la plantilla.
        """
        # Forzar a que todas las evaluaciones de Path.exists() retornen True en el flujo exitoso
        mock_exists.return_value = True

        result = self.exporter.export_report(self.dummy_results, self.base_output)

        self.assertTrue(result)

        # Se verifica la conversión forzando el tipado string como lo hace el exportador real
        mock_convert.assert_called_once_with(
            str(pathlib.Path("outputs/simulation_report.md")),
            to="docx",
            outputfile=str(pathlib.Path("outputs/simulation_report.docx")),
            extra_args=[f"--reference-doc={self.exporter._template_path}"],
        )

    @patch.object(pathlib.Path, "exists")
    def test_export_report_fails_if_source_md_does_not_exist(self, mock_exists: MagicMock) -> None:
        """
        Valida que se aborte la operación y retorne False si el paso previo de Markdown no existe.
        """
        # Simular que el archivo .md no ha sido creado por el exportador previo (.exists() -> False)
        mock_exists.return_value = False

        result = self.exporter.export_report(self.dummy_results, self.base_output)

        self.assertFalse(result)

    @patch("pypandoc.convert_file")
    @patch.object(pathlib.Path, "exists")
    def test_export_report_returns_false_on_binary_crash(
        self, mock_exists: MagicMock, mock_convert: MagicMock
    ) -> None:
        """
        Valida que fallos críticos en la conversión de Pandoc retornen False limpiamente.
        """
        mock_exists.return_value = True
        mock_convert.side_effect = Exception("Pandoc binary missing or corrupted")

        result = self.exporter.export_report(self.dummy_results, self.base_output)

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
