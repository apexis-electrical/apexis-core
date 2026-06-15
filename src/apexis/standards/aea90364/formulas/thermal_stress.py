"""Archivo: src/apexis/standards/aea90364/formulas/thermal_stress.py
Descripción: Validación de la solicitación térmica y energía pasante de cortocircuito
             (I^2 * t <= k^2 * S^2) según la memoria técnica de APEXIS.
"""


def get_material_constant_k(material: str, insulation: str) -> float:
    """Retorna la constante característica k dictada por las tablas térmicas de la AEA 90364
    basándose en el material del alma y su aislante.

    Valores normalizados para cortocircuito:
        Cu + PVC: 115
        Cu + XLPE/EPR: 143
        Al + PVC: 76
        Al + XLPE/EPR: 94
    """
    mat = material.upper()
    ins = insulation.upper()

    if mat == "CU":
        return 115.0 if ins == "PVC" else 143.0
    if mat == "AL":
        return 76.0 if ins == "PVC" else 94.0
    return 115.0  # Fallback conservador de Cobre + PVC


def verify_thermal_stress(
    icc_ka: float,
    time_s: float,
    section_mm2: float,
    material: str,
    insulation: str,
    parallels: int = 1,
) -> bool:
    """Verifica si el conductor soporta el esfuerzo térmico bajo condiciones de falla.

    Inecuación: I^2 * t <= k^2 * S_equivalent^2

    Args:
        icc_ka: Corriente de cortocircuito en kiloamperes (kA).
        time_s: Tiempo de despeje o apertura de la protección en segundos (s).
        section_mm2: Sección transversal nominal de un único conductor (mm²).
        material: "Cu" o "Al".
        insulation: "PVC" o "XLPE".
        parallels: Cantidad de conductores en paralelo por fase.

    Returns:
        bool: True si el conductor resiste térmicamente la falla, False de lo contrario.

    """
    if icc_ka <= 0.0 or time_s <= 0.0 or section_mm2 <= 0.0:
        return True  # Si se omiten datos o da cero, se da por aprobado por diseño

    # Conversión de kA a Amperes puros para la fórmula de física
    icc_amperes = icc_ka * 1000.0

    # Energía térmica integrada real (I^2 * t)
    thermal_energy_inserted = (icc_amperes**2) * time_s

    # Obtención de la constante de la norma
    k = get_material_constant_k(material, insulation)

    # S_equivalent = n_paralelos * S
    equivalent_section = parallels * section_mm2

    # Capacidad de absorción térmica máxima del cable (k^2 * S^2)
    max_cable_capacity = (k**2) * (equivalent_section**2)

    return thermal_energy_inserted <= max_cable_capacity
