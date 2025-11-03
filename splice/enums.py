"""
Enums for common harness component properties.

Provides type-safe enums for wire colors, conductor types, stranding,
and other common specifications to help users avoid typos and ensure
valid values.
"""

from enum import Enum


class WireColor(str, Enum):
    """Common wire colors."""

    BLACK = "black"
    WHITE = "white"
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    YELLOW = "yellow"
    ORANGE = "orange"
    BROWN = "brown"
    PURPLE = "purple"
    GRAY = "gray"
    GREY = "gray"  # Alias
    PINK = "pink"
    VIOLET = "violet"
    TAN = "tan"
    NATURAL = "natural"
    CLEAR = "clear"


class ConductorType(str, Enum):
    """Wire conductor types."""

    SOLID = "solid"
    STRANDED = "stranded"


class Stranding(str, Enum):
    """Common wire stranding specifications."""

    # Solid
    SOLID = "solid"

    # Class 5 (flexible stranded) - most common
    CLASS_5 = "Class 5"

    # Common AWG stranding patterns
    AWG_24_7_32 = "7/32"      # 24 AWG: 7 strands of 32 AWG
    AWG_22_7_30 = "7/30"      # 22 AWG: 7 strands of 30 AWG
    AWG_20_7_28 = "7/28"      # 20 AWG: 7 strands of 28 AWG
    AWG_18_16_30 = "16/30"    # 18 AWG: 16 strands of 30 AWG
    AWG_16_26_30 = "26/30"    # 16 AWG: 26 strands of 30 AWG
    AWG_14_41_30 = "41/30"    # 14 AWG: 41 strands of 30 AWG
    AWG_12_65_30 = "65/30"    # 12 AWG: 65 strands of 30 AWG
    AWG_10_105_30 = "105/30"  # 10 AWG: 105 strands of 30 AWG


class TerminationType(str, Enum):
    """Types of wire terminations."""

    CONNECTOR_PIN = "connector_pin"
    CABLE_CORE = "cable_core"
    FLYING_LEAD = "flying_lead"


class FlyingLeadType(str, Enum):
    """Types of flying lead terminations."""

    BARE = "bare"
    TINNED = "tinned"
    HEAT_SHRINK = "heat_shrink"


class ConnectorGender(str, Enum):
    """Connector gender types."""

    MALE = "male"
    FEMALE = "female"
    NONE = "none"


class ConnectorShape(str, Enum):
    """Connector shape types."""

    CIRCULAR = "circular"
    RECTANGULAR = "rectangular"
    DSUB = "dsub"
    TERMINAL_BLOCK = "terminal_block"
    FERRULE = "ferrule"
    QUICK_DISCONNECT = "quickdisconnect"
    RING = "ring"
    BUTTON = "button"
    OTHER = "other"


class ConnectorCategory(str, Enum):
    """Specialized connector categories."""

    CIRCUIT_BREAKER = "circuit_breaker"
    FUSE = "fuse"
    FAN = "fan"
    PUSH_BUTTON = "push_button"
    SWITCH = "switch"
    RELAY = "relay"
    CONTACTOR = "contactor"
    TIMER = "timer"
    PCB = "pcb"
    POWER_SUPPLY = "power_supply"
    MOTOR = "motor"
    OTHER = "other"


class ConnectionSide(str, Enum):
    """Side of connector for wire routing."""

    LEFT = "left"
    RIGHT = "right"
