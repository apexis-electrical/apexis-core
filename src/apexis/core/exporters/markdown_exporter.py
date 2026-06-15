"""Archivo: src/apexis/core/exporters/markdown_exporter.py
Descripción: Exportador de infraestructura especializado en renderizar memorias
             técnicas en formato Markdown (.md). Optimizado con __slots__.
"""

import pathlib
from typing import Any

from apexis.core.interfaces.exporter import ReportExporterInterface


class MarkdownReportExporter(ReportExporterInterface):
    """Generador de reportes encargado de procesar mallas de strings para construir
    tablas en Markdown e inyectarlas de forma transparente en las plantillas normativas.
    """

    # Congelamos el slot para almacenar la ruta estática de la plantilla
    __slots__ = ("_template_path",)

    def __init__(self, template_path: str | None = None) -> None:
        """Inicializa el exportador fijando la ubicación de la plantilla detallada.
        """
        if template_path is None:
            # Apunta por defecto a la ruta exacta del subdirectorio de templates
            base_dir = pathlib.Path(__file__).parent.parent.parent
            self._template_path = (
                base_dir / "standards" / "aea90364" / "templates" / "detailed_report.md"
            )
        else:
            self._template_path = pathlib.Path(template_path)

    def export_report(self, results_table: list[dict[str, Any]], output_path: str) -> bool:
        """Lee la plantilla detallada, genera la tabla de alineación en Markdown,
        reemplaza el token {{RESULTS_TABLE}} y persiste el archivo final en disco.
        """
        template_file = pathlib.Path(self._template_path)
        dest_file = pathlib.Path(output_path)

        if not template_file.exists():
            raise FileNotFoundError(
                f"No se pudo inicializar el reporte técnico. La plantilla base "
                f"no se encuentra en la ruta física: {template_file}",
            )

        # 1. Construcción dinámica de la tabla RAW en formato Markdown s/ Memoria Técnica
        md_table = [
            "| Circuito | Ib (A) | Iz Corregida (A) | Sección Fase (mm²) | Sección PE (mm²) | Caída de Tensión (%) | Icc (kA) | Estado |",
            "| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
        ]

        for row in results_table:
            tag = row.get("tag", "UNK")
            ib = f"{row.get('ib_a', 0.0):.1f}"
            iz = f"{row.get('iz_a', 0.0):.1f}"
            sec = f"{row.get('section_mm2', 0.0):.1f}"
            pe = f"{row.get('pe_section_mm2', 0.0):.1f}"
            v_drop = f"{row.get('voltage_drop_pct', 0.0):.2f}%"
            icc = f"{row.get('icc_ka', 0.0):.2f}"
            status = row.get("status", "FAILED")

            # Formateamos visualmente la fila de alineación de la tabla
            md_table.append(f"| {tag} | {ib} | {iz} | {sec} | {pe} | {v_drop} | {icc} | {status} |")

        results_table_string = "\n".join(md_table)

        # 2. Operación atómica de lectura de plantilla y reemplazo de tokens
        with open(template_file, encoding="utf-8") as f:
            template_content = f.read()

        final_content = template_content.replace("{{RESULTS_TABLE}}", results_table_string)

        # 3. Escritura del documento técnico final en disco
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        with open(dest_file, "w", encoding="utf-8") as f:
            f.write(final_content)

        return dest_file.exists()
