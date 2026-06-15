"""Archivo: src/apexis/core/domain/entities.py
Descripción: Entidades del dominio corporativas y fuertemente tipadas de APEXIS.
             Optimizadas con __slots__, inicializadores inteligentes y métodos mágicos
             para un procesamiento de cálculo de alto rendimiento.
"""

from collections.abc import Sequence
from typing import Any


class CircuitPurpose:
    """Representa el propósito y uso normativo específico del circuito."""

    __slots__ = ("subtype", "type")

    def __init__(self, type: str, subtype: str = "iug") -> None:
        self.type: str = type.strip().lower()
        self.subtype: str = subtype.strip().lower()

    def __repr__(self) -> str:
        return f"CircuitPurpose(type='{self.type}', subtype='{self.subtype}')"


class ElectricalParameters:
    """Parámetros eléctricos intrínsecos del circuito.
    Soporta la resolución automática de longitudes complejas acumuladas (Listas/Tuplas).
    """

    __slots__ = ("length_m", "load_unit", "load_value", "parallels", "phase_type", "voltage_v")

    def __init__(
        self,
        phase_type: str,
        voltage_v: float,
        parallels: int,
        length_m: float | Sequence[float],
        load: dict[str, Any],
    ) -> None:
        self.phase_type: str = phase_type.strip().upper()
        self.voltage_v: float = float(voltage_v)
        self.parallels: int = int(parallels)

        # Si el usuario pasa una secuencia de distancias (como tu suma en el input), la calculamos automáticamente
        if isinstance(length_m, (list, tuple)):
            self.length_m: float = round(sum(length_m), 3)
        else:
            self.length_m: float = float(length_m)

        self.load_value: float = float(load.get("value", 0.0))
        self.load_unit: str = str(load.get("unit", "kVA")).strip()

    def __repr__(self) -> str:
        return (
            f"ElectricalParameters(phase_type='{self.phase_type}', voltage_v={self.voltage_v}, "
            f"parallels={self.parallels}, length_m={self.length_m}, "
            f"load={self.load_value}{self.load_unit})"
        )


class InstallationParameters:
    """Variables ambientales y constructivas de la canalización eléctrica."""

    __slots__ = (
        "grouped_circuits",
        "installation_method",
        "installation_temp_c",
        "insulation",
        "material",
        "soil_type",
        "wire_burial_depth_m",
    )

    def __init__(
        self,
        installation_method: str,
        material: str,
        insulation: str,
        installation_temp_c: float,
        grouped_circuits: int = 1,
        soil_type: str = "default",
        wire_burial_depth_m: float = 0.0,
    ) -> None:
        self.installation_method: str = installation_method.strip()
        self.material: str = material.strip()
        self.insulation: str = insulation.strip().upper()
        self.installation_temp_c: float = float(installation_temp_c)
        self.grouped_circuits: int = int(grouped_circuits)
        self.soil_type: str = soil_type.strip().lower()
        self.wire_burial_depth_m: float = float(wire_burial_depth_m)

    def __repr__(self) -> str:
        return (
            f"InstallationParameters(method='{self.installation_method}', material='{self.material}', "
            f"insulation='{self.insulation}', temp={self.installation_temp_c}°C)"
        )


class ShortCircuitParameters:
    """Configuración para las verificaciones de esfuerzo térmico ante fallas."""

    __slots__ = ("icc_ka", "mode", "time_s")

    def __init__(self, mode: str, Icc_kA: float = 0.0, time_s: float = 0.5) -> None:
        self.mode: str = mode.strip().lower()
        self.icc_ka: float = float(Icc_kA)
        self.time_s: float = float(time_s)

    def __repr__(self) -> str:
        return f"ShortCircuitParameters(mode='{self.mode}', icc_ka={self.icc_ka}, time_s={self.time_s})"


class CableParameters:
    """Configuración y estado del conductor para el lazo de cálculo."""

    __slots__ = ("mode", "reactance_ohm_per_m", "section_mm2", "voltage_drop_method")

    def __init__(
        self,
        voltage_drop_method: str,
        reactance_ohm_per_m: float = 0.0,
        mode: str = "auto",
        section_mm2: float | None = None,
    ) -> None:
        self.voltage_drop_method: str = voltage_drop_method.strip().upper()
        self.reactance_ohm_per_m: float = float(reactance_ohm_per_m)
        self.mode: str = mode.strip().lower()
        self.section_mm2: float | None = float(section_mm2) if section_mm2 is not None else None

    def __repr__(self) -> str:
        return f"CableParameters(method='{self.voltage_drop_method}', mode='{self.mode}', section={self.section_mm2})"


class ElectricalCircuit:
    """Entidad raíz agregada del Dominio que unifica todas las sub-estructuras.
    Representa formalmente un circuito validado dentro del ecosistema APEXIS.
    """

    __slots__ = (
        "cable",
        "destination",
        "electrical",
        "installation",
        "origin",
        "purpose",
        "short_circuit",
        "tag",
    )

    def __init__(
        self,
        tag: str,
        origin: str,
        destination: str,
        purpose: dict[str, Any],
        electrical: dict[str, Any],
        installation: dict[str, Any],
        short_circuit: dict[str, Any],
        cable: dict[str, Any],
    ) -> None:
        self.tag: str = tag.strip().upper()
        self.origin: str = origin.strip().upper()
        self.destination: str = destination.strip()

        # Mapeo inteligente convirtiendo los diccionarios planos de entrada en Value Objects con __slots__
        self.purpose: CircuitPurpose = CircuitPurpose(**purpose)
        self.electrical: ElectricalParameters = ElectricalParameters(**electrical)
        self.installation: InstallationParameters = InstallationParameters(**installation)
        self.short_circuit: ShortCircuitParameters = ShortCircuitParameters(**short_circuit)
        self.cable: CableParameters = CableParameters(**cable)

    @property
    def equivalent_section_mm2(self) -> float:
        """Calcula dinámicamente la sección transversal equivalente por fase.
        Fórmula de la memoria técnica: S_eq = n_paralelos * S
        """
        if self.cable.section_mm2 is None:
            return 0.0
        return self.electrical.parallels * self.cable.section_mm2

    def __eq__(self, other: object) -> bool:
        """Método mágico de comparación. Considera idénticos a dos circuitos si
        comparten la misma etiqueta (tag) e idéntica carga eléctrica y longitud.
        """
        if not isinstance(other, ElectricalCircuit):
            return False
        return (
            self.tag == other.tag
            and self.electrical.load_value == other.electrical.load_value
            and self.electrical.length_m == other.electrical.length_m
        )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} Tag={self.tag} Destination='{self.destination}'>"

    def __str__(self) -> str:
        return f"Circuito Terminal APEXIS [{self.tag}] -> Destino: {self.destination} (L={self.electrical.length_m}m)"
