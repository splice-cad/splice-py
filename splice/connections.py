"""
Connection and termination classes for wiring.
"""

from typing import Union, Optional, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .components import PinRef, CoreRef
    from .parts import Wire

from .enums import FlyingLeadType


class FlyingLead:
    """
    Represents a flying lead termination (unterminated wire end).

    Attributes:
        termination_type: Type of termination (use FlyingLeadType enum or custom string)
        strip_length_mm: Optional strip length in millimeters
        tin_length_mm: Optional tin length in millimeters (for tinned terminations)
        label: Optional label for the flying lead
    """

    def __init__(
        self,
        termination_type: Union[FlyingLeadType, str] = FlyingLeadType.BARE,
        strip_length_mm: Optional[float] = None,
        tin_length_mm: Optional[float] = None,
        label: Optional[str] = None,
    ) -> None:
        self.termination_type = termination_type
        self.strip_length_mm = strip_length_mm
        self.tin_length_mm = tin_length_mm
        self.label = label

    def to_dict(self) -> Dict[str, Any]:
        """Convert flying lead to dictionary representation."""
        term_type = (
            self.termination_type.value
            if isinstance(self.termination_type, FlyingLeadType)
            else self.termination_type
        )

        data: Dict[str, Any] = {
            "type": "flying_lead",
            "termination_type": term_type,
        }
        if self.strip_length_mm is not None:
            data["strip_length_mm"] = self.strip_length_mm
        if self.tin_length_mm is not None:
            data["tin_length_mm"] = self.tin_length_mm
        if self.label:
            data["label"] = self.label
        return data


# Import here to avoid circular dependency
from .components import PinRef, CoreRef  # noqa: E402

ConnectionEnd = Union[PinRef, CoreRef, FlyingLead]


class Connection:
    """
    Represents a wire connection between two endpoints.

    Attributes:
        end1: First connection endpoint (PinRef, CoreRef, or FlyingLead)
        end2: Second connection endpoint (PinRef, CoreRef, or FlyingLead)
        wire: Wire specification for this connection
        length_mm: Optional wire length in millimeters
        label: Optional label for the connection
        label_end1: Optional label for end1
        label_end2: Optional label for end2
    """

    def __init__(
        self,
        end1: ConnectionEnd,
        end2: ConnectionEnd,
        wire: "Wire",  # Use string annotation to avoid circular import
        length_mm: Optional[float] = None,
        label: Optional[str] = None,
        label_end1: Optional[str] = None,
        label_end2: Optional[str] = None,
    ) -> None:
        self.end1 = end1
        self.end2 = end2
        self.wire = wire
        self.length_mm = length_mm
        self.label = label
        self.label_end1 = label_end1
        self.label_end2 = label_end2

    def _endpoint_to_dict(self, endpoint: ConnectionEnd) -> Dict[str, Any]:
        """Convert a connection endpoint to dictionary representation."""
        if isinstance(endpoint, FlyingLead):
            return endpoint.to_dict()
        elif isinstance(endpoint, PinRef):
            return {
                "type": "pin",
                "designator": endpoint.component.designator,
                "pin": endpoint.pin,
            }
        elif isinstance(endpoint, CoreRef):
            return {
                "type": "core",
                "designator": endpoint.component.designator,
                "core": endpoint.core,
            }
        else:
            raise ValueError(f"Unknown endpoint type: {type(endpoint)}")

    def to_dict(self) -> Dict[str, Any]:
        """Convert connection to dictionary representation."""
        data: Dict[str, Any] = {
            "end1": self._endpoint_to_dict(self.end1),
            "end2": self._endpoint_to_dict(self.end2),
            "wire": self.wire.to_dict(),
        }

        if self.length_mm is not None:
            data["length_mm"] = self.length_mm
        if self.label:
            data["label"] = self.label
        if self.label_end1:
            data["label_end1"] = self.label_end1
        if self.label_end2:
            data["label_end2"] = self.label_end2

        return data
