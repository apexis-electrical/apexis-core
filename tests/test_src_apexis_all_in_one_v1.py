"""Archivo: tests/test_src_apexis_all_in_one_v1.py
Descripción: Suite de prueba integrada masiva (All-In-One v1) para el ecosistema APEXIS.
             Actúa como un Tribunal de Control independiente que audita el comportamiento
             del motor frente a la física estricta de la norma AEA 90364.
"""

from apexis.core.domain.engine import APEXISEngine
from apexis.core.utils.converters import PowerConverter


def test_apexis_core_engine_all_in_one_validation_v1() -> None:
    """Simulación integral End-to-End. Aplica mallas de auditoría matemática manual
    idénticas a la Memoria Técnica para verificar si el Core comete errores de límites o ecuaciones.
    """
    # -------------------------------------------------------------------------
    # 1. ENTRADAS CRUDAS (DATA-INPUTS REAL DE TU PROYECTO)
    # -------------------------------------------------------------------------
    standard_name = "aea90364"
    global_criteria = {"cos_phi": 0.90, "ampacity_margin": 1.00, "standard_section": "771"}

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
    load_value = 2.2
    load_unit = "kVA"
    voltage_v = 220.0

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
                "voltage_v": voltage_v,
                "parallels": 1,
                "length_m": lengths_sequence,
                "load": {
                    "value": load_value,
                    "unit": load_unit,
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

    # -------------------------------------------------------------------------
    # 2. ÁRBITRO DEL TEST (ALGORITMO DE CONTROL MATEMÁTICO MANUAL DE LA MEMORIA)
    # -------------------------------------------------------------------------
    # A. Corriente de proyecto teórica manual para 1PH: Ib = (S * 1000) / U
    manual_s_kva = PowerConverter.to_apparent_power_kva(
        load_value, load_unit, global_criteria["cos_phi"],
    )
    manual_ib = (manual_s_kva * 1000.0) / voltage_v  # 10.0 A

    # B. Longitud total manual sumando los tramos
    manual_total_length = sum(lengths_sequence)  # 55.43 m

    # C. Límite reglamentario de Caída de Tensión s/ Memoria Técnica (Iluminación = 3.0%)
    manual_v_drop_limit = 3.0 if circuits_batch[0]["purpose"]["type"] == "lighting" else 5.0
    gdc_unit_1ph = 0.040

    # D. Espectro comercial y ampacidades corregidas para Cu PVC B1-2x a 40°C
    manual_ampacity_table = {1.5: 15.0, 2.5: 21.0, 4.0: 28.0, 6.0: 36.0, 10.0: 50.0, 16.0: 66.0}

    manual_selected_section = None
    manual_calculated_v_drop_pct = None

    # El test ejecuta la simulación de bucle manual estricto tal como exige la ingeniería real
    for section, corrected_ampacity in manual_ampacity_table.items():
        # Verificación I: Térmica por sobrecarga
        if manual_ib > corrected_ampacity:
            continue

        # Verificación II: Caída de Tensión Monofásica Real RAW s/ AEA 90364-7-771
        # El coeficiente 0.040 de la norma ya contiene la ida y vuelta, NO se multiplica por 2.0
        # Fórmula oficial: Delta_V_% = ((Ib * L * GDC) / S) / U * 100
        manual_v_drop_abs = (manual_ib * manual_total_length * gdc_unit_1ph) / section
        v_drop_pct = (manual_v_drop_abs / voltage_v) * 100.0

        # Si supera el 3% reglamentario de iluminación, el árbitro manual rechaza la sección
        if v_drop_pct > manual_v_drop_limit:
            continue

        manual_selected_section = section
        manual_calculated_v_drop_pct = round(v_drop_pct, 2)
        break

    # Criterio III: Sección del Conductor de Protección (PE) s/ Tramos de la Memoria
    if manual_selected_section <= 16.0:
        manual_pe_section = manual_selected_section
    elif manual_selected_section <= 35.0:
        manual_pe_section = 16.0
    else:
        manual_pe_section = manual_selected_section / 2.0

    # -------------------------------------------------------------------------
    # 3. EJECUCIÓN DEL MOTOR CORE DE APEXIS
    # -------------------------------------------------------------------------
    engine = APEXISEngine(standard=standard_name, criteria=global_criteria)
    results_table = engine.calculate_circuits(circuits_batch)
    c01_res = results_table[0]

    # -------------------------------------------------------------------------
    # 4. CONTRA-AUDITORÍA FINAL (EL TEST COMPRUEBA SI EL CORE COMETIÓ UN BUG)
    # -------------------------------------------------------------------------
    assert c01_res["ib_a"] == round(manual_ib, 2)
    assert c01_res["total_length_m"] == round(manual_total_length, 3)

    # Comprobación de la sección comercial definitiva elegida y la caída arrojada
    assert c01_res["section_mm2"] == manual_selected_section
    assert c01_res["pe_section_mm2"] == manual_pe_section
    assert c01_res["voltage_drop_pct"] == manual_calculated_v_drop_pct
    assert c01_res["status"] == "APPROVED"
