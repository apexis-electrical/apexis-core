"""
Archivo: examples/basic_sizing_simulation.py
Descripción: Script de ejemplo formal que demuestra el uso end-to-end de APEXIS Core
             para el dimensionamiento de conductores bajo la norma AEA 90364.
             Actualizado para utilizar el pipeline simplificado de plugins de exportación.
"""

import pprint

from apexis import APEXISEngine, ElectricalStandardEnum, MarkdownReportExporter, PandocReportExporter


def main() -> None:
    """
    Simulación de cálculo de dimensionamiento e ingeniería para un lote de circuitos.
    """
    print("=" * 70)
    print("APEXIS Core Sizing Engine - Simulación Oficial")
    print("=" * 70)

    # 1. Configuración de criterios globales del motor (CRITERIA)
    global_criteria = {
        "cos_phi": 0.90,
        "ampacity_margin": 1.00,
        "standard_section": "771",  # Ámbito comercial/oficinas de la norma
    }

    # 2. Inicialización de los datos crudos del circuito de iluminación (C-01)
    circuits_input = [
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
                # Tramos secuenciales acumulados calculados automáticamente por la entidad
                "length_m": [
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
                ],
                "load": {
                    "value": 2.2,
                    "unit": "kVA",
                },
            },
            "installation": {
                "installation_method": "B1-2x",  # Conductores en cañería embutida
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

    # 3. Instanciamos el motor utilizando el Enum tipado de normas globales
    engine = APEXISEngine(standard=ElectricalStandardEnum.AEA_90364.value, criteria=global_criteria)

    print(f"\n[INFO] {engine}")
    print("[INFO] Procesando lazo iterativo de ingeniería eléctrica...")

    # 4. Ejecutamos el lote de dimensionamiento
    results_table = engine.calculate_circuits(circuits_input)

    # 5. Exposición de resultados en consola para la {{RESULTS_TABLE}}
    print("\n" + "=" * 70)
    print("MÉTRICAS FINALES DE DISEÑO APROBADAS POR LA NORMA AEA 90364")
    print("=" * 70)
    pprint.pprint(results_table, width=80, sort_dicts=False)
    print("=" * 70)

    # =========================================================================
    # PIPELINE DE CONFIGURACIÓN Y PROCESAMIENTO DE PLUGINS EN LOTE
    # =========================================================================
    print("\n[INFO] Ejecutando procesamiento de reportes en lote...")

    # Inicializamos el pipeline de complementos (puedes sumar más formatos en paralelo)
    exporters_pipeline = [
        MarkdownReportExporter(),
        PandocReportExporter(),  # Plugin que autogenera .md y .docx en simultáneo con estilos
        # DocxReportExporter(),   # Descomentar al implementar tu plugin de Word
        # PDFReportExporter(),    # Descomentar al implementar tu plugin de PDF
    ]

    # Ejecutamos la exportación masiva delegando al motor
    report_summary = engine.export_results(
        results_table=results_table,
        plugins=exporters_pipeline,
        output_path_base="outputs/simulation_report",
    )

    # Reporte final del pipeline en pantalla
    for format_ext, success_status in report_summary.items():
        status_msg = "ÉXITO" if success_status else "FALLA"
        print(f" -> Generación de Formato [{format_ext}]: {status_msg}")

    print("=" * 70)


if __name__ == "__main__":
    main()
