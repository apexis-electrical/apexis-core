"""Archivo: tests/test_src_apexis_core_master.py
Descripción: Pruebas unitarias para validar la integridad de la fachada pública (__master__.py)
             y el correcto ruteo de exportaciones del ecosistema APEXIS Core.
"""

import apexis.core.__master__ as master


def test_master_exports_integrity_dynamic() -> None:
    """Valida dinámicamente que todos los componentes clave declarados en la fachada pública
    existan, estén bien importados y sean accesibles desde el módulo raíz.
    """
    # 1. Comprobamos la existencia de la propiedad __all__
    assert hasattr(master, "__all__")

    # 2. Verificamos que cada string declarado en __all__ corresponda a un objeto real importado
    for export_name in master.__all__:
        assert hasattr(master, export_name)

    # 3. Asserts explícitos de control de tipos de los componentes core expuestos
    assert isinstance(master.__all__, tuple)
    assert "APEXISEngine" in master.__all__
    assert "ElectricalCircuit" in master.__all__
    assert "PowerConverter" in master.__all__
