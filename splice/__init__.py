"""
splice-py: Python library for programmatic Splice harness generation

Create cable harness designs in Python and export them as JSON files
for upload to Splice.
"""

__version__ = "0.1.0b1"

# Core classes
from .harness import Harness
from .types import ComponentType
from .parts import Wire, CableCore
from .connections import FlyingLead
from .components import PinRef, CoreRef
from .validation import ValidationResult

# Enums for type safety
from .enums import (
    WireColor,
    ConductorType,
    Stranding,
    FlyingLeadType,
    TerminationType,
    ConnectorGender,
    ConnectorShape,
    ConnectorCategory,
    ConnectionSide,
)

__all__ = [
    "__version__",
    # Core classes
    "Harness",
    "ComponentType",
    "Wire",
    "CableCore",
    "PinRef",
    "CoreRef",
    "FlyingLead",
    "ValidationResult",
    # Enums
    "WireColor",
    "ConductorType",
    "Stranding",
    "FlyingLeadType",
    "TerminationType",
    "ConnectorGender",
    "ConnectorShape",
    "ConnectorCategory",
    "ConnectionSide",
]
