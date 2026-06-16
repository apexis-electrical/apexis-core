"""
Archivo: src/apexis/core/exporters/pandoc_exporter.py
Descripción: Adaptador de infraestructura especializado en compilar reportes técnicos
             en formato Word (.docx) usando Pandoc a partir de un archivo Markdown (.md)
             existente generado por el pipeline. Implementa ReportExporterInterface.
"""

import pathlib
from typing import Any

import pypandoc

from apexis.core.interfaces.exporter import ReportExporterInterface


class PandocReportExporter(ReportExporterInterface):
    """
    Componente de compilación que consume el archivo Markdown generado previamente
    en el pipeline y lo transforma en un documento de Word aplicando estilos institucionales.
    """

    __slots__ = ("_template_path",)

    def __init__(self) -> None:
        """
        Inicializa el exportador configurando la ruta por defecto de la plantilla de Word.
        """
        base_dir = pathlib.Path(__file__).parent.parent.parent.parent.parent
        self._template_path = base_dir / "templates" / "plantilla.docx"

    @property
    def resolved_extension(self) -> str:
        """
        Contrato de interfaz: Informa explícitamente al motor que este plugin compila a .docx.
        """
        return ".docx"

    def export_report(self, _results_table: list[dict[str, Any]], output_path: str) -> bool:
        """
        Toma el archivo .md generado previamente por el pipeline y lo compila a .docx.
        """
        try:
            dest_file = pathlib.Path(output_path)
            md_source_path = dest_file.with_suffix(".md")
            docx_target_path = dest_file.with_suffix(".docx")

            if not md_source_path.exists():
                print(f"[Error] Pandoc requiere el archivo origen generado: '{md_source_path}'")
                return False

            extra_args = []
            if pathlib.Path(self._template_path).exists():
                extra_args.append(f"--reference-doc={self._template_path}")

            pypandoc.convert_file(
                str(md_source_path),
                to="docx",
                outputfile=str(docx_target_path),
                extra_args=extra_args,
            )

            return docx_target_path.exists()

        except Exception as e:
            print(f"[Error] Fallo en la compilación de Pandoc a Word: {str(e)}")
            return False
