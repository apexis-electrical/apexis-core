"""Archivo: tests/test_src_apexis_init.py
Descripción: Prueba de empaquetado para verificar que la raíz del namespace
             exponga correctamente los componentes sin necesidad de sub-rutas.
"""


def test_package_root_imports_success_dynamic() -> None:
    """Simula el comportamiento de un usuario que instaló la librería desde PyPI
    e intenta importar los componentes directo desde el nombre del paquete.
    """
    # CORREGIDO: Importación explícita desde la raíz para forzar la lectura del __init__.py
    from apexis import APEXISEngine, ElectricalCircuit, ElectricalStandardEnum, PowerConverter

    # Verificamos la existencia y consistencia de tipos de los objetos expuestos
    assert APEXISEngine is not None
    assert ElectricalCircuit is not None
    assert PowerConverter is not None
    assert ElectricalStandardEnum is not None
