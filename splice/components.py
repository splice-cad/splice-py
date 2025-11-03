"""
Component instance classes for harness components.
"""

from typing import Optional, Tuple, List, Any, Dict, Union
from .types import ComponentType
from .parts import CableCore
from .enums import ConnectorCategory, ConnectorGender, ConnectorShape, WireColor


class PinRef:
    """Reference to a specific pin on a component."""

    def __init__(self, component: "ComponentInstance", pin: int) -> None:
        self.component = component
        self.pin = pin

    def __repr__(self) -> str:
        return f"PinRef({self.component.designator}.{self.pin})"


class CoreRef:
    """Reference to a specific core on a cable component."""

    def __init__(self, component: "CableInstance", core: int) -> None:
        self.component = component
        self.core = core

    def __repr__(self) -> str:
        return f"CoreRef({self.component.designator}:{self.core})"


class ComponentInstance:
    """
    Base class for all component instances in a harness.

    Attributes:
        kind: The component type
        designator: Unique identifier (e.g., X1, W1, F1)
        mpn: Manufacturer part number
        manufacturer: Manufacturer name
        position: Optional (x, y) position on canvas
        category: Optional category for specialized components
        custom_fields: Additional component-specific fields
    """

    def __init__(
        self,
        kind: ComponentType,
        designator: str,
        mpn: str,
        manufacturer: str,
        position: Optional[Tuple[float, float]] = None,
        category: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.kind = kind
        self.designator = designator
        self.mpn = mpn
        self.manufacturer = manufacturer
        self.position = position
        self.category = category
        self.custom_fields = kwargs

    def pin(self, pin_number: int) -> PinRef:
        """
        Create a reference to a specific pin on this component.

        Args:
            pin_number: The pin number (1-indexed)

        Returns:
            A PinRef object referencing this pin
        """
        return PinRef(self, pin_number)

    def to_dict(self) -> Dict[str, Any]:
        """Convert component to dictionary representation."""
        data: Dict[str, Any] = {
            "kind": self.kind.value,
            "designator": self.designator,
            "mpn": self.mpn,
            "manufacturer": self.manufacturer,
        }

        if self.position:
            data["position"] = {"x": self.position[0], "y": self.position[1]}

        if self.category:
            data["category"] = self.category

        # Add custom fields
        data.update(self.custom_fields)

        return data


class ConnectorInstance(ComponentInstance):
    """
    Represents a connector component instance.

    Connectors have a specific number of positions/pins and optional
    specifications like gender, shape, and category.

    Attributes:
        designator: Component designator (e.g., "X1")
        mpn: Manufacturer part number
        manufacturer: Manufacturer name
        positions: Number of pins/positions
        position: Optional (x, y) canvas position
        category: Optional category (use ConnectorCategory enum or custom string)
        gender: Optional connector gender (use ConnectorGender enum)
        shape: Optional connector shape (use ConnectorShape enum)
        **kwargs: Additional component-specific fields
    """

    def __init__(
        self,
        designator: str,
        mpn: str,
        manufacturer: str,
        positions: int,
        position: Optional[Tuple[float, float]] = None,
        category: Optional[Union[ConnectorCategory, str]] = None,
        gender: Optional[ConnectorGender] = None,
        shape: Optional[ConnectorShape] = None,
        **kwargs: Any,
    ) -> None:
        # Convert category enum to string if needed
        category_str = (
            category.value if isinstance(category, ConnectorCategory) else category
        )

        super().__init__(
            kind=ComponentType.CONNECTOR,
            designator=designator,
            mpn=mpn,
            manufacturer=manufacturer,
            position=position,
            category=category_str,
            positions=positions,
            **kwargs,
        )
        self.positions = positions
        self.gender = gender
        self.shape = shape

    def to_dict(self) -> Dict[str, Any]:
        """Convert connector to dictionary representation."""
        data = super().to_dict()
        data["positions"] = self.positions
        if self.gender:
            data["contact_gender"] = self.gender.value
        if self.shape:
            data["shape"] = self.shape.value
        return data


class CableInstance(ComponentInstance):
    """
    Represents a multi-core cable component instance.

    Cables have multiple cores that can be individually connected.
    """

    def __init__(
        self,
        designator: str,
        mpn: str,
        manufacturer: str,
        cores: List[CableCore],
        position: Optional[Tuple[float, float]] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            kind=ComponentType.CABLE,
            designator=designator,
            mpn=mpn,
            manufacturer=manufacturer,
            position=position,
            **kwargs,
        )
        self.cores = cores

    def core(self, core_number: int) -> CoreRef:
        """
        Create a reference to a specific core on this cable.

        Args:
            core_number: The core number (1-indexed)

        Returns:
            A CoreRef object referencing this core
        """
        return CoreRef(self, core_number)

    def to_dict(self) -> Dict[str, Any]:
        """Convert cable to dictionary representation."""
        data = super().to_dict()
        data["cores"] = [core.to_dict() for core in self.cores]
        return data


class WireInstance(ComponentInstance):
    """
    Represents a single wire component instance.

    This is typically used for individual wire specifications.

    Attributes:
        designator: Component designator (e.g., "W1")
        mpn: Manufacturer part number
        manufacturer: Manufacturer name
        awg: Wire gauge (AWG)
        color: Wire color (use WireColor enum or custom string)
        position: Optional (x, y) canvas position
        **kwargs: Additional component-specific fields
    """

    def __init__(
        self,
        designator: str,
        mpn: str,
        manufacturer: str,
        awg: int,
        color: Union[WireColor, str],
        position: Optional[Tuple[float, float]] = None,
        **kwargs: Any,
    ) -> None:
        # Convert color enum to string if needed
        color_str = color.value if isinstance(color, WireColor) else color

        super().__init__(
            kind=ComponentType.WIRE,
            designator=designator,
            mpn=mpn,
            manufacturer=manufacturer,
            position=position,
            awg=awg,
            color=color_str,
            **kwargs,
        )
        self.awg = awg
        self.color = color_str

    def to_dict(self) -> Dict[str, Any]:
        """Convert wire to dictionary representation."""
        data = super().to_dict()
        data["awg"] = self.awg
        data["color"] = self.color
        return data
