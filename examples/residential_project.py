"""
Archivo: examples/residential_project.py
Descripción: Script formal de dimensionamiento eléctrico utilizando SELMA Engine
             bajo normativa AEA 90364 para proyecto residencial completo.
"""

import pprint

from apexis import APEXISEngine, ElectricalStandardEnum, MarkdownReportExporter


def main() -> None:
    """Simulación de cálculo de dimensionamiento e ingeniería para un lote de circuitos.
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

        # --------------------------------------------------------
        # C-01 – Iluminación Planta Baja
        # --------------------------------------------------------
        {
            "tag": "C-01",
            "origin": "TPBT",
            "destination": "IUG en Planta Baja",
            "purpose": {"type": "lighting", "subtype": "iug"},
            "electrical": {
                "phase_type": "1PH",
                "voltage_v": 220,
                "parallels": 1,
                "length_m": [
                    15.03, 3.82, 1.67, 1.71, 0.2, 0.78, 0.25, 0.19,
                    0.52, 0.19, 3.04, 0.84, 0.46, 3.88, 0.84, 0.52,
                    1.51, 0.78, 0.31, 0.6, 1.21, 7.68, 1.59, 0.67,
                    4.69, 1.69, 0.87
                ],
                "load": {"value": 2.2, "unit": "kVA"},
            },
            "installation": {
                "installation_method": "B2-2x",
                "material": "Cu",
                "insulation": "PVC",
                "installation_temp_c": 40.0,
                "grouped_circuits": 1,
                "soil_type": "default",
                "wire_burial_depth_m": 0.0,
            },
            "short_circuit": {"mode": "skip", "Icc_kA": 4.5, "time_s": 0.5},
            "cable": {
                "voltage_drop_method": "GDC",
                "reactance_ohm_per_m": 0.0,
                "mode": "auto",
                "section_mm2": None,
            },
        },

        # --------------------------------------------------------
        # C-02 – Iluminación Planta Alta
        # --------------------------------------------------------
        {
            "tag": "C-02",
            "origin": "TPBT",
            "destination": "IUG en Planta Alta",
            "purpose": {"type": "lighting", "subtype": "iug"},
            "electrical": {
                "phase_type": "1PH",
                "voltage_v": 220,
                "parallels": 1,
                "length_m": [
                    7.61, 7.57, 5.32, 2.69, 2.69, 6.58,
                    3.44, 3.44, 2.39, 1.76, 1.59, 1.26, 5.08
                ],
                "load": {"value": 2.2, "unit": "kVA"},
            },
            "installation": {
                "installation_method": "B2-2x",
                "material": "Cu",
                "insulation": "PVC",
                "installation_temp_c": 40.0,
                "grouped_circuits": 1,
                "soil_type": "default",
                "wire_burial_depth_m": 0.0,
            },
            "short_circuit": {"mode": "skip", "Icc_kA": 4.5, "time_s": 0.5},
            "cable": {
                "voltage_drop_method": "GDC",
                "reactance_ohm_per_m": 0.0,
                "mode": "auto",
                "section_mm2": None,
            },
        },

        # --------------------------------------------------------
        # C-03 a C-06 (TUG / TUE)
        # --------------------------------------------------------
        *[
            {
                "tag": f"C-{i:02d}",
                "origin": "TPBT",
                "destination": desc,
                "purpose": {"type": "outlet", "subtype": subtype},
                "electrical": {
                    "phase_type": "1PH",
                    "voltage_v": 220,
                    "parallels": 1,
                    "length_m": 50.0,
                    "load": {"value": load, "unit": "kVA"},
                },
                "installation": {
                    "installation_method": "B2-2x",
                    "material": "Cu",
                    "insulation": "PVC",
                    "installation_temp_c": 40.0,
                    "grouped_circuits": 1,
                    "soil_type": "default",
                    "wire_burial_depth_m": 0.0,
                },
                "short_circuit": {"mode": "skip", "Icc_kA": 4.5, "time_s": 0.5},
                "cable": {
                    "voltage_drop_method": "GDC",
                    "reactance_ohm_per_m": 0.0,
                    "mode": "auto",
                    "section_mm2": None,
                },
            }
            for i, desc, subtype, load in [
                (3, "TUG en Planta Baja", "tug", 2.2),
                (4, "TUG en Planta Alta", "tug", 2.2),
                (5, "TUE en Planta Baja", "tue", 3.3),
                (6, "TUE en Planta Alta", "tue", 3.3),
            ]
        ],

        # --------------------------------------------------------
        # C-07 a C-11 – Aires Acondicionados
        # --------------------------------------------------------
        *[
            {
                "tag": f"C-{i:02d}",
                "origin": "TPBT",
                "destination": "ACU para Aires Acondicionados",
                "purpose": {"type": "power", "subtype": "hvac"},
                "electrical": {
                    "phase_type": "1PH",
                    "voltage_v": 220,
                    "parallels": 1,
                    "length_m": [3.83, 7, 14.16, 1],
                    "load": {"value": 14, "unit": "A"},
                },
                "installation": {
                    "installation_method": "B2-2x",
                    "material": "Cu",
                    "insulation": "PVC",
                    "installation_temp_c": 40.0,
                    "grouped_circuits": 1,
                    "soil_type": "default",
                    "wire_burial_depth_m": 0.0,
                },
                "short_circuit": {"mode": "skip", "Icc_kA": 4.5, "time_s": 0.5},
                "cable": {
                    "voltage_drop_method": "GDC",
                    "reactance_ohm_per_m": 0.0,
                    "mode": "auto",
                    "section_mm2": None,
                },
            }
            for i in range(7, 12)
        ],
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
