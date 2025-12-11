"""
Label classes for bundle identification and heat-shrink printing.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Literal
import uuid


@dataclass
class BundleLabel:
    """
    Label for a connector or cable bundle.

    Labels can be attached to connectors or cables for identification purposes
    and heat-shrink label printing. Each label has customizable text, dimensions,
    and colors.

    Attributes:
        id: Unique identifier (auto-generated UUID)
        label_text: Text content of the label (e.g., "J1", "TO POWER SUPPLY")
        is_auto_generated: True if label uses the component designator automatically
        connector_instance_id: Instance ID of the connector this label belongs to
        cable_instance_id: Instance ID of the cable this label belongs to
        cable_end: Which end of the cable this label applies to ("start", "end", "both")
        wire_keys: Specific wire instance IDs this label covers (empty = all wires)
        width_mm: Label width in millimeters for heat-shrink printing
        font_size: Font size for label text
        text_color: Text color in hex format
        background_color: Background color in hex format
    """

    label_text: str
    is_auto_generated: bool = False
    connector_instance_id: Optional[str] = None
    cable_instance_id: Optional[str] = None
    cable_end: Optional[Literal["start", "end", "both"]] = None
    wire_keys: List[str] = field(default_factory=list)
    width_mm: float = 9.0
    font_size: float = 10.0
    text_color: str = "#000000"
    background_color: str = "#FFFFFF"
    id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class LabelSettings:
    """
    Global label display settings.

    Controls how labels are displayed on the harness canvas and provides
    default values for new labels.

    Attributes:
        show_labels_on_canvas: Whether to show labels on the harness canvas
        default_width_mm: Default label width in millimeters
    """

    show_labels_on_canvas: bool = True
    default_width_mm: float = 9.0
