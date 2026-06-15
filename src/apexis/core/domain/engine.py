"""Archivo: src/apexis/core/domain/engine.py
Descripción: Motor de cálculo principal (Core Orchestrator) del ecosistema APEXIS.
             Unifica la factoría de normas con las entidades y ejecuta los procesos.
             Optimizado con __slots__ y métodos mágicos de nivel corporativo.
"""

from collections.abc import Sequence
from typing import Any

from apexis.core.domain.entities import ElectricalCircuit
from apexis.core.interfaces.exporter import ReportExporterInterface
from apexis.standards.factory import StandardAdapterFactory


class APEXISEngine:
    """Orquestador central encargado de administrar los criterios de diseño globales,
    resolver el adaptador de normativa internacional y procesar lotes de circuitos.
    """

    __slots__ = ("_adapter", "criteria")

    def __init__(self, standard: str, criteria: dict[str, Any]) -> None:
        """Inicializa el motor resolviendo dinámicamente el adaptador de regulación solicitado.
        """
        self.criteria: dict[str, Any] = criteria

        factory = StandardAdapterFactory()
        self._adapter: Any = factory.get_adapter(standard)

    def calculate_circuits(self, raw_circuits: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Itera sobre un lote de circuitos planos de entrada, los procesa y dimensiona
        según las inecuaciones lógicas de la memoria de cálculo técnica.
        """
        results_table: list[dict[str, Any]] = []

        for circuit_dict in raw_circuits:
            domain_circuit = ElectricalCircuit(**circuit_dict)
            circuit_dict["electrical"]["length_m"] = domain_circuit.electrical.length_m

            circuit_result = self._adapter.process_circuit_design(circuit_dict, self.criteria)
            circuit_result["total_length_m"] = domain_circuit.electrical.length_m

            results_table.append(circuit_result)

        return results_table

    def export_results(
        self,
        results_table: list[dict[str, Any]],
        plugins: ReportExporterInterface | Sequence[ReportExporterInterface],
        output_path_base: str,
    ) -> dict[str, bool]:
        """NUEVO: Método de Procesamiento por Lotes de Plugins.
        Acepta un plugin individual o una lista de plugins, ejecutándolos en serie.
        Autodeduce la extensión del archivo s/ la naturaleza del plugin.

        Args:
            results_table: Tabla de métricas finales calculadas.
            plugins: Un plugin único o una secuencia de plugins [MD(), DOCX(), PDF()].
            output_path_base: Ruta base con el nombre del archivo sin extensión (ej: "outputs/memoria").

        Returns:
            Dict[str, bool]: Mapa de éxito indexado por el nombre de cada formato generado.

        """
        # Si el usuario pasa un único plugin suelto, lo transformamos en una lista para el bucle unificado
        plugins_list = [plugins] if not isinstance(plugins, (list, tuple)) else plugins

        execution_report: dict[str, bool] = {}

        for plugin in plugins_list:
            # Deducimos la extensión inspeccionando el nombre de la clase (ej: "MarkdownReportExporter" -> "md")
            class_name = plugin.__class__.__name__.lower()
            if "markdown" in class_name:
                ext = ".md"
            elif "docx" in class_name:
                ext = ".docx"
            elif "pdf" in class_name:
                ext = ".pdf"
            else:
                ext = ".txt"

            # Construimos la ruta de destino atómica (ej: "outputs/memoria" + ".md")
            final_output_path = f"{output_path_base}{ext}"

            # Ejecutamos el plugin y guardamos su estado en el reporte final
            success = plugin.export_report(results_table, final_output_path)
            execution_report[ext] = success

        return execution_report

    def __repr__(self) -> str:
        """Representación técnica para logs de depuración."""
        return f"<{self.__class__.__name__}(criteria_count={len(self.criteria)}, adapter={self._adapter!r})>"

    def __str__(self) -> str:
        """Representación textual amigable para reportes."""
        return f"APEXIS Main Core Engine [Módulo activo: {self._adapter!s}]"
