"""Archivo: src/apexis/standards/aea90364/formulas/ampacity.py
Descripción: Lógica matemática para determinar la potencia normalizada, corriente de
             proyecto (Ib), ampacidad (Iz) y coordinación de sobrecargas de APEXIS.
             Delegación de conversiones físicas hacia el módulo global de utilitarios.
"""

from typing import Any

# CORREGIDO: Importación vital para evitar el NameError en el motor
from apexis.core.utils.converters import PowerConverter


def calculate_design_current(
    load_value: float, load_unit: str, voltage_v: float, phase_type: str, cos_phi: float = 0.90,
) -> float:
    """Normaliza la potencia de carga utilizando el convertidor global y calcula la
    corriente de proyecto (I_B) según las fórmulas de sistemas 1PH y 3PH de la memoria.
    """
    normalized_unit = load_unit.strip().upper()

    # Si la entrada ya es corriente directa Amperes, saltamos la conversión de potencia aparente
    if normalized_unit == "A":
        return round(load_value, 2)

    # Delegamos de forma limpia la normalización matemática de la física hacia el convertidor utilitario
    s_kva = PowerConverter.to_apparent_power_kva(load_value, load_unit, cos_phi)

    # Cálculo de corriente de proyecto (I_B) basado en el tipo de fase (3PH o 1PH)
    if phase_type.upper() == "3PH":
        ib = (s_kva * 1000.0) / (1.7320508 * voltage_v)
    else:
        ib = (s_kva * 1000.0) / voltage_v

    return round(ib, 2)


def lookup_nominal_ampacity(
    conductor_size: float,
    installation_method: str,
    material: str,
    insulation: str,
    ampacity_database: dict[str, Any],
) -> float:
    """Busca en la base de datos JSON de la norma la corriente nominal base (I_tabla)
    para un único conductor según su sección y método constructivo.
    """
    mat_key = material.upper()
    ins_key = insulation.upper()
    method_key = installation_method.upper()

    ampacity = (
        ampacity_database.get(mat_key, {})
        .get(ins_key, {})
        .get(method_key, {})
        .get(str(conductor_size))
    )

    if ampacity is None:
        return 0.0

    return float(ampacity)


def calculate_corrected_ampacity(
    nominal_ampacity: float,
    global_derating_factor: float,
    parallels: int = 1,
    ampacity_margin: float = 1.0,
) -> float:
    """Aplica la ecuación de corrección de la memoria técnica de APEXIS multiplicando
    la corriente base por los factores climáticos y el número de conductores en paralelo.
    """
    if nominal_ampacity <= 0.0 or global_derating_factor <= 0.0:
        return 0.0

    iz_corregida = nominal_ampacity * global_derating_factor * parallels * ampacity_margin
    return round(iz_corregida, 1)


def verify_protection_coordination(
    ib_design_current: float,
    in_nominal_protection: float,
    iz_corrected_ampacity: float,
    protection_standard: str = "IEC_60898",
) -> bool:
    """Valida las condiciones fundamentales de sobrecarga dictadas por la memoria.
    """
    condition_1 = ib_design_current <= in_nominal_protection <= iz_corrected_ampacity

    if not condition_1:
        return False

    if protection_standard.upper() == "IEC_60898":
        return True
    i2 = 1.45 * in_nominal_protection
    return i2 <= (iz_corrected_ampacity * 1.45)
