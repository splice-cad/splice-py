"""
Main Harness class for building cable harness designs.
"""

import json
from typing import List, Optional, Tuple, Any, Dict, Union
from .types import ComponentType
from .parts import Wire, CableCore
from .components import (
    ComponentInstance,
    ConnectorInstance,
    CableInstance,
    WireInstance,
)
from .connections import Connection, ConnectionEnd, FlyingLead
from .utils import DesignatorGenerator

try:
    import requests
except ImportError:
    requests = None  # type: ignore


class Harness:
    """
    Main class for creating and managing cable harness designs.

    A Harness contains components (connectors, cables, wires) and connections
    between them. It provides methods to add components, create connections,
    validate the design, and export to JSON.

    Attributes:
        name: Harness name
        description: Optional description
        components: List of all components in the harness
        connections: List of all connections between components
    """

    def __init__(self, name: str, description: str = "") -> None:
        """
        Initialize a new harness.

        Args:
            name: Name for the harness
            description: Optional description
        """
        self.name = name
        self.description = description
        self.components: List[ComponentInstance] = []
        self.connections: List[Connection] = []
        self.notes: List[Dict[str, Any]] = []
        self._designator_gen = DesignatorGenerator()

    def add_component(
        self,
        kind: ComponentType,
        mpn: str,
        manufacturer: str,
        designator: Optional[str] = None,
        position: Optional[Tuple[float, float]] = None,
        **kwargs: Any,
    ) -> ComponentInstance:
        """
        Add a component to the harness.

        Args:
            kind: The component type (from ComponentType enum)
            mpn: Manufacturer part number
            manufacturer: Manufacturer name
            designator: Optional custom designator (auto-generated if not provided)
            position: Optional (x, y) position on canvas
            **kwargs: Additional component-specific parameters:
                - positions: Number of positions/pins (for connectors)
                - cores: List of CableCore objects (for cables)
                - awg: Wire gauge (for wires)
                - color: Wire color (for wires)
                - category: Category for specialized components (fuse, relay, etc.)

        Returns:
            The created component instance

        Raises:
            ValueError: If required parameters are missing or invalid
        """
        # Get category if provided
        category = kwargs.get("category")

        # Generate designator if not provided
        if designator is None:
            designator = self._designator_gen.generate(kind, category)
        else:
            # Register custom designator
            self._designator_gen.register(designator)

        # Create appropriate component instance based on kind
        component: ComponentInstance

        if kind == ComponentType.CONNECTOR:
            positions = kwargs.get("positions")
            if positions is None:
                raise ValueError("Connector requires 'positions' parameter")

            component = ConnectorInstance(
                designator=designator,
                mpn=mpn,
                manufacturer=manufacturer,
                positions=positions,
                position=position,
                category=category,
                **{k: v for k, v in kwargs.items() if k not in ["positions", "category"]},
            )

        elif kind == ComponentType.CABLE:
            cores = kwargs.get("cores")
            if cores is None:
                raise ValueError("Cable requires 'cores' parameter")

            component = CableInstance(
                designator=designator,
                mpn=mpn,
                manufacturer=manufacturer,
                cores=cores,
                position=position,
                **{k: v for k, v in kwargs.items() if k != "cores"},
            )

        elif kind == ComponentType.WIRE:
            awg = kwargs.get("awg")
            color = kwargs.get("color")
            if awg is None or color is None:
                raise ValueError("Wire requires 'awg' and 'color' parameters")

            component = WireInstance(
                designator=designator,
                mpn=mpn,
                manufacturer=manufacturer,
                awg=awg,
                color=color,
                position=position,
                **{k: v for k, v in kwargs.items() if k not in ["awg", "color"]},
            )

        else:
            # Generic component
            component = ComponentInstance(
                kind=kind,
                designator=designator,
                mpn=mpn,
                manufacturer=manufacturer,
                position=position,
                category=category,
                **{k: v for k, v in kwargs.items() if k != "category"},
            )

        self.components.append(component)
        return component

    def connect(
        self,
        end1: ConnectionEnd,
        end2: ConnectionEnd,
        wire: Optional[Wire] = None,
        length_mm: Optional[float] = None,
        label: Optional[str] = None,
        label_end1: Optional[str] = None,
        label_end2: Optional[str] = None,
    ) -> Connection:
        """
        Create a connection between two endpoints.

        Args:
            end1: First endpoint (PinRef, CoreRef, or FlyingLead)
            end2: Second endpoint (PinRef, CoreRef, or FlyingLead)
            wire: Wire specification (required for most connections)
            length_mm: Optional wire length in millimeters
            label: Optional label for the connection
            label_end1: Optional label for end1
            label_end2: Optional label for end2

        Returns:
            The created Connection object

        Raises:
            ValueError: If wire is required but not provided
        """
        # Wire is required unless at least one end is a cable core
        if wire is None:
            from .components import CoreRef

            # Allow connections without wire spec if either end is a cable core
            if not (isinstance(end1, CoreRef) or isinstance(end2, CoreRef)):
                raise ValueError("Wire parameter is required for this connection type")

        connection = Connection(
            end1=end1,
            end2=end2,
            wire=wire,  # type: ignore
            length_mm=length_mm,
            label=label,
            label_end1=label_end1,
            label_end2=label_end2,
        )

        self.connections.append(connection)
        return connection

    def add_note(
        self, position: Tuple[float, float], title: str, content: List[str]
    ) -> None:
        """
        Add a design note to the harness.

        Args:
            position: (x, y) position on canvas
            title: Note title
            content: List of note content lines
        """
        self.notes.append(
            {"position": {"x": position[0], "y": position[1]}, "title": title, "content": content}
        )

    def validate(self) -> "ValidationResult":
        """
        Validate the harness design.

        Returns:
            ValidationResult object with validation status and any errors
        """
        from .validation import validate_harness

        return validate_harness(self)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert harness to dictionary representation in Splice import format.

        Returns:
            Dictionary representation suitable for JSON import to Splice
        """
        from .export import harness_to_splice_format

        return harness_to_splice_format(self)

    def to_json(self) -> str:
        """
        Convert harness to JSON string in Splice import format.

        Returns:
            JSON string representation compatible with Splice JSON import
        """
        return json.dumps(self.to_dict(), indent=2)

    def save(self, filepath: str) -> None:
        """
        Save harness to a JSON file in Splice import format.

        The generated JSON file can be uploaded to Splice via the web interface.

        Args:
            filepath: Path to output file
        """
        with open(filepath, "w") as f:
            f.write(self.to_json())

    def upload(
        self,
        api_key: str,
        is_public: bool = False,
        api_url: str = "https://splice-cad.com",
    ) -> Dict[str, Any]:
        """
        Upload harness to Splice via API.

        Requires an API key from your Splice account settings. The harness will be
        created in your account and can be accessed via the Splice web interface.

        Args:
            api_key: Your Splice API key (get from Account Settings)
            is_public: Whether to make the harness publicly visible (default: False)
            api_url: Splice API URL (default: https://splice-cad.com)

        Returns:
            Dictionary with the created harness details including:
                - id: Harness UUID
                - name: Harness name
                - owner_id: Your user UUID
                - created_at: Creation timestamp

        Raises:
            ImportError: If requests library is not installed
            ValueError: If harness validation fails
            requests.HTTPError: If the API request fails

        Example:
            >>> harness = Harness("My Design")
            >>> # ... add components and connections ...
            >>> result = harness.upload(api_key="splice_abc123...")
            >>> print(f"Created harness: {result['id']}")
        """
        if requests is None:
            raise ImportError(
                "The 'requests' library is required for upload functionality. "
                "Install it with: pip install requests"
            )

        # Validate harness first
        validation = self.validate()
        if not validation.valid:
            error_msg = "; ".join(validation.errors)
            raise ValueError(f"Harness validation failed: {error_msg}")

        # Get harness data in Splice format
        data = self.to_dict()

        # Prepare upload payload
        payload = {
            "name": self.name,
            "description": self.description or None,
            "bom": data["bom"],
            "data": data["data"],
            "is_public": is_public,
        }

        # Make API request
        url = f"{api_url}/api/v1/harnesses"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        return response.json()
