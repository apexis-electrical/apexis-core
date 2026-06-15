"""Archivo: src/apexis/standards/aea90364/data/lookup.py
Descripción: Administrador y cargador de datos (Data Registry) para la norma AEA 90364.
             Levanta los archivos JSON y de las tablas de cables, constantes y factores,
             proveyendo métodos de búsqueda estricta para el adaptador de la norma.
             Optimizado con __slots__ y métodos mágicos corporativos de APEXIS.
"""

import json
import pathlib
from typing import Any


class AEA90364Lookup:
    """Clase encargada de encapsular el acceso a las tablas físicas de la norma AEA 90364.
    Mantiene los datos cargados en memoria tras la primera instanciación para evitar
    el overhead repetitivo de lectura de disco en sistemas de alta concurrencia.
    """

    # Bloqueamos el __dict__ interno para optimizar el acceso a variables y la memoria RAM
    __slots__ = ("constants", "factors", "wires")

    def __init__(self, data_dir: pathlib.Path | None = None) -> None:
        """Inicializa el registro cargando los tres archivos JSON fundamentales desde el disco.
        """
        if data_dir is None:
            # Obtiene la ruta de la carpeta actual donde reside este archivo lookup.py
            data_dir = pathlib.Path(__file__).parent

        self.constants: dict[str, Any] = self._load_json(data_dir / "constants.json")
        self.factors: dict[str, Any] = self._load_json(data_dir / "factors.json")
        self.wires: dict[str, Any] = self._load_json(data_dir / "wires.json")

    def _load_json(self, file_path: pathlib.Path) -> dict[str, Any]:
        """Lector utilitario interno para archivos JSON con codificación UTF-8 para garantizar
        la compatibilidad multiplataforma de caracteres especiales de ingeniería.
        """
        if not file_path.exists():
            return {}

        with open(file_path, encoding="utf-8") as f:
            return json.load(f)

    def get_k_constant(self, material: str, insulation: str) -> float:
        """Busca la constante térmica k de cortocircuito en constants.json según el material
        del conductor y el tipo de aislación.

        Args:
            material: Alma del conductor ("Cu" o "Al").
            insulation: Compuesto aislante ("PVC" o "XLPE").

        Returns:
            float: Constante adiabática k para la inecuación de energía pasante.

        """
        # Normalizamos a capitalización exacta del JSON (ej: "Cu", "Al", "PVC")
        mat_key = "Cu" if material.lower() == "cu" else "Al"
        ins_key = insulation.upper()

        return float(self.constants.get("k_values", {}).get(mat_key, {}).get(ins_key, 115.0))

    def get_gdc_constant(self, material: str, phase_type: str) -> float:
        """NUEVO: Busca el gradiente de caída unitario (GDC) dentro de constants.json
        para desacoplar los coeficientes fijos del código de Python.

        Args:
            material: Alma del conductor ("Cu" o "Al").
            phase_type: Configuración eléctrica de fases ("1PH" o "3PH").

        Returns:
            float: Coeficiente de gradiente de caída de tensión unitario.

        """
        mat_key = material.strip().upper()
        phase_key = phase_type.strip().upper()

        # Fallback de seguridad normativo histórico (Cu 1PH = 0.040) si falla la combinación
        return float(self.constants.get("gdc_defaults", {}).get(mat_key, {}).get(phase_key, 0.040))

    def get_temperature_factor(
        self, ambient_temp_c: float, insulation: str, environment: str,
    ) -> float:
        """Busca el factor de corrección por temperatura f_t en factors.json.

        Args:
            ambient_temp_c: Temperatura ambiente real del proyecto (ej: 40.0).
            insulation: Tipo de aislante ("PVC" o "XLPE").
            environment: Medio de tendido de la canalización ("AIR" o "SOIL").

        Returns:
            float: Coeficiente multiplicador de reducción térmica por clima.

        """
        env_key = f"temperature_{environment.lower()}"
        ins_key = insulation.upper()
        temp_key = str(int(ambient_temp_c))  # Las llaves en el JSON son enteros como strings ("40")

        factor = self.factors.get(env_key, {}).get(ins_key, {}).get(temp_key)
        return float(factor) if factor is not None else 1.0

    def get_base_ampacity(
        self, section_mm2: float, installation_method: str, material: str, insulation: str,
    ) -> float:
        """Busca la ampacidad base de tabla en wires.json cruzando el método
        de referencia (ej: B1) y la configuración de conductores cargados (ej: 2x, 3x).

        Soporta métodos compuestos pasados desde el input (ej: "B1-2x" o "D2-3xA").

        Args:
            section_mm2: Calibre nominal del conductor en mm².
            installation_method: Canalización compuesta (ej: "B1-2x").
            material: Metal conductor ("Cu" o "Al").
            insulation: Polímero protector ("PVC" o "XLPE").

        Returns:
            float: Capacidad de conducción en Amperes puros a bornes de laboratorio.

        """
        mat_key = "Cu" if material.lower() == "cu" else "Al"
        ins_key = insulation.upper()

        # Descomponemos el método de instalación del input (ej: "B1-2x" -> base="B1", config="2x")
        parts = installation_method.split("-")
        base_method = parts[0].upper()
        config_key = parts[1] if len(parts) > 1 else "2x"

        # Navegamos la estructura jerárquica de wires.json
        method_tables = self.wires.get("materials", {}).get(mat_key, {}).get(ins_key, {})
        sections_list: list[dict[str, Any]] = method_tables.get(base_method, [])

        # Buscamos el objeto correspondiente a la sección mm2 solicitada
        for entry in sections_list:
            if float(entry.get("section_mm2", 0.0)) == float(section_mm2):
                ampacity = entry.get(config_key)
                return float(ampacity) if ampacity is not None else 0.0

        return 0.0

    def get_available_sections(
        self, material: str, insulation: str, installation_method: str,
    ) -> list[float]:
        """Retorna la lista ordenada de todas las secciones mm2 comerciales disponibles
        para una combinación de conductor y método dada. Útil para el bucle iterativo del motor.

        Args:
            material: Metal conductor ("Cu" o "Al").
            insulation: Polímero protector ("PVC" o "XLPE").
            installation_method: Canalización de referencia (ej: "B1-2x").

        Returns:
            List[float]: Vector ordenado de calibres comerciales en mm² (ej: [1.5, 2.5, 4.0...]).

        """
        mat_key = "Cu" if material.lower() == "cu" else "Al"
        insulation_key = insulation.upper()
        base_method = installation_method.split("-", maxsplit=1)[0].upper()

        method_tables = self.wires.get("materials", {}).get(mat_key, {}).get(insulation_key, {})
        sections_list: list[dict[str, Any]] = method_tables.get(base_method, [])

        return [float(entry["section_mm2"]) for entry in sections_list if "section_mm2" in entry]

    def __repr__(self) -> str:
        """Representación técnica formal en consola (ideal para depuración y logs del sistema).
        """
        return (
            f"<{self.__class__.__name__}(constants_loaded={bool(self.constants)}, "
            f"factors_loaded={bool(self.factors)}, wires_loaded={bool(self.wires)})>"
        )

    def __str__(self) -> str:
        """Representación informativa simplificada y limpia del estado de las tablas de datos.
        """
        return (
            f"AEA 90364 Data Registry [Estado de carga de tablas: "
            f"Constantes={len(self.constants.get('k_values', {}))}, "
            f"Factores={len(self.factors)}, Materiales={len(self.wires.get('materials', {}))}]"
        )
