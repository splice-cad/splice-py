"""
Wire and cable part definitions.
"""

from typing import Optional, Dict, Any, Union
from dataclasses import dataclass

from .enums import WireColor, Stranding, ConductorType


@dataclass
class Wire:
    """
    Represents a single wire specification.

    Attributes:
        mpn: Manufacturer part number
        manufacturer: Manufacturer name
        awg: Wire gauge (AWG)
        color: Wire color (use WireColor enum or custom string)
        description: Optional description
        stranding: Optional stranding specification (use Stranding enum or custom string)
        conductor_type: Conductor type (default: STRANDED)
    """

    mpn: str
    manufacturer: str
    awg: int
    color: Union[WireColor, str]
    description: Optional[str] = None
    stranding: Optional[Union[Stranding, str]] = None
    conductor_type: ConductorType = ConductorType.STRANDED

    def to_dict(self) -> Dict[str, Any]:
        """Convert wire to dictionary representation."""
        data: Dict[str, Any] = {
            "mpn": self.mpn,
            "manufacturer": self.manufacturer,
            "awg": self.awg,
            "color": self.color.value if isinstance(self.color, WireColor) else self.color,
        }
        if self.description:
            data["description"] = self.description
        if self.stranding:
            data["stranding"] = (
                self.stranding.value if isinstance(self.stranding, Stranding) else self.stranding
            )
        if self.conductor_type:
            data["conductor_type"] = (
                self.conductor_type.value
                if isinstance(self.conductor_type, ConductorType)
                else self.conductor_type
            )
        return data


@dataclass
class CableCore:
    """
    Represents a single core within a multi-core cable.

    Attributes:
        number: Core number (1-indexed)
        awg: Wire gauge for this core
        color: Core color (use WireColor enum or custom string)
        label: Optional label for the core
        stranding: Optional stranding specification
        conductor_type: Conductor type (default: STRANDED)
    """

    number: int
    awg: int
    color: Union[WireColor, str]
    label: Optional[str] = None
    stranding: Optional[Union[Stranding, str]] = None
    conductor_type: ConductorType = ConductorType.STRANDED

    def __post_init__(self) -> None:
        """Validate core number is positive."""
        if self.number < 1:
            raise ValueError(f"Core number must be positive, got {self.number}")

    def to_dict(self) -> Dict[str, Any]:
        """Convert core to dictionary representation."""
        data: Dict[str, Any] = {
            "number": self.number,
            "awg": self.awg,
            "color": self.color.value if isinstance(self.color, WireColor) else self.color,
        }
        if self.label:
            data["label"] = self.label
        if self.stranding:
            data["stranding"] = (
                self.stranding.value if isinstance(self.stranding, Stranding) else self.stranding
            )
        if self.conductor_type:
            data["conductor_type"] = (
                self.conductor_type.value
                if isinstance(self.conductor_type, ConductorType)
                else self.conductor_type
            )
        return data
