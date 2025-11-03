"""
Component type definitions for Splice harness components.
"""

from enum import Enum
from typing import Optional


class ComponentType(Enum):
    """
    Enumeration of all supported component types in Splice.

    The type determines the auto-generated designator prefix:
    - CONNECTOR → X1, X2, X3...
    - CABLE → C1, C2, C3...
    - WIRE → W1, W2, W3...
    - TERMINAL → Terminal crimps (no auto-designator)

    Category-specific components use CONNECTOR with a category field:
    - Fuses → F1, F2... (category="fuse")
    - Circuit Breakers → CB1, CB2... (category="circuit_breaker")
    - Switches → S1, S2... (category="switch")
    - Relays → K1, K2... (category="relay")
    - Power Supplies → PS1, PS2... (category="power_supply")
    - Motors → M1, M2... (category="motor")
    """

    CONNECTOR = "connector"
    CABLE = "cable"
    WIRE = "wire"
    TERMINAL = "terminal"


# Category to designator prefix mapping
CATEGORY_DESIGNATORS = {
    "fuse": "F",
    "circuit_breaker": "CB",
    "switch": "S",
    "relay": "K",
    "power_supply": "PS",
    "motor": "M",
}


def get_designator_prefix(kind: ComponentType, category: Optional[str] = None) -> str:
    """
    Get the designator prefix for a component based on its kind and category.

    Args:
        kind: The component type
        category: Optional category for specialized connectors

    Returns:
        The designator prefix (e.g., "X", "W", "F", "CB")
    """
    if category and category in CATEGORY_DESIGNATORS:
        return CATEGORY_DESIGNATORS[category]

    if kind == ComponentType.CONNECTOR:
        return "X"
    elif kind == ComponentType.CABLE:
        return "C"
    elif kind == ComponentType.WIRE:
        return "W"
    elif kind == ComponentType.TERMINAL:
        return "T"

    return "X"  # Default fallback
