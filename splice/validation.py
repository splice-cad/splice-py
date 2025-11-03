"""
Validation logic for harness designs.
"""

from typing import List, Set, TYPE_CHECKING

if TYPE_CHECKING:
    from .harness import Harness
    from .components import ComponentInstance, ConnectorInstance

from .components import PinRef, CoreRef, ConnectorInstance, CableInstance
from .connections import FlyingLead


class ValidationResult:
    """
    Result of harness validation.

    Attributes:
        valid: Whether the harness is valid
        errors: List of validation error messages
        warnings: List of validation warning messages
    """

    def __init__(self) -> None:
        self.valid = True
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def add_error(self, message: str) -> None:
        """Add an error message and mark as invalid."""
        self.errors.append(message)
        self.valid = False

    def add_warning(self, message: str) -> None:
        """Add a warning message."""
        self.warnings.append(message)


def validate_harness(harness: "Harness") -> ValidationResult:
    """
    Validate a harness design.

    Checks for:
    - Duplicate designators
    - Invalid pin references
    - Invalid core references
    - Unconnected pins
    - Missing required fields

    Args:
        harness: The harness to validate

    Returns:
        ValidationResult with any errors or warnings
    """
    result = ValidationResult()

    # Check for empty harness
    if not harness.components:
        result.add_error("Harness has no components")
        return result

    # Check for duplicate designators
    designators: Set[str] = set()
    for component in harness.components:
        if component.designator in designators:
            result.add_error(f"Duplicate designator: {component.designator}")
        designators.add(component.designator)

    # Validate component fields
    for component in harness.components:
        if not component.mpn:
            result.add_error(f"Component {component.designator} missing MPN")
        if not component.manufacturer:
            result.add_error(f"Component {component.designator} missing manufacturer")

        # Validate connector positions
        if isinstance(component, ConnectorInstance):
            if component.positions < 1:
                result.add_error(
                    f"Connector {component.designator} has invalid positions: {component.positions}"
                )

        # Validate cable cores
        if isinstance(component, CableInstance):
            if not component.cores:
                result.add_error(f"Cable {component.designator} has no cores")
            core_numbers = set()
            for core in component.cores:
                if core.number < 1:
                    result.add_error(
                        f"Cable {component.designator} has invalid core number: {core.number}"
                    )
                if core.number in core_numbers:
                    result.add_error(
                        f"Cable {component.designator} has duplicate core number: {core.number}"
                    )
                core_numbers.add(core.number)

    # Build component lookup
    component_lookup = {c.designator: c for c in harness.components}

    # Track pin and core usage
    pin_usage: dict[str, Set[int]] = {}
    core_usage: dict[str, dict[int, int]] = {}  # Maps designator -> core_number -> connection_count

    # Validate connections
    for i, connection in enumerate(harness.connections):
        # Validate wire is present (unless at least one end is a cable core)
        if connection.wire is None:
            if not (isinstance(connection.end1, CoreRef) or isinstance(connection.end2, CoreRef)):
                result.add_error(f"Connection {i} missing wire specification")

        # Validate end1
        if isinstance(connection.end1, PinRef):
            designator = connection.end1.component.designator
            pin = connection.end1.pin

            if designator not in component_lookup:
                result.add_error(f"Connection {i} references unknown component: {designator}")
            else:
                component = component_lookup[designator]
                if isinstance(component, ConnectorInstance):
                    if pin < 1 or pin > component.positions:
                        result.add_error(
                            f"Connection {i} references invalid pin {pin} on {designator} "
                            f"(valid range: 1-{component.positions})"
                        )

            # Track pin usage
            if designator not in pin_usage:
                pin_usage[designator] = set()
            if pin in pin_usage[designator]:
                result.add_warning(f"Pin {designator}.{pin} used in multiple connections")
            pin_usage[designator].add(pin)

        elif isinstance(connection.end1, CoreRef):
            designator = connection.end1.component.designator
            core = connection.end1.core

            if designator not in component_lookup:
                result.add_error(f"Connection {i} references unknown component: {designator}")
            else:
                component = component_lookup[designator]
                if isinstance(component, CableInstance):
                    valid_cores = {c.number for c in component.cores}
                    if core not in valid_cores:
                        result.add_error(
                            f"Connection {i} references invalid core {core} on {designator}"
                        )

            # Track core usage
            if designator not in core_usage:
                core_usage[designator] = {}
            if core not in core_usage[designator]:
                core_usage[designator][core] = 0
            core_usage[designator][core] += 1

        # Validate end2 (same logic as end1)
        if isinstance(connection.end2, PinRef):
            designator = connection.end2.component.designator
            pin = connection.end2.pin

            if designator not in component_lookup:
                result.add_error(f"Connection {i} references unknown component: {designator}")
            else:
                component = component_lookup[designator]
                if isinstance(component, ConnectorInstance):
                    if pin < 1 or pin > component.positions:
                        result.add_error(
                            f"Connection {i} references invalid pin {pin} on {designator} "
                            f"(valid range: 1-{component.positions})"
                        )

            # Track pin usage
            if designator not in pin_usage:
                pin_usage[designator] = set()
            if pin in pin_usage[designator]:
                result.add_warning(f"Pin {designator}.{pin} used in multiple connections")
            pin_usage[designator].add(pin)

        elif isinstance(connection.end2, CoreRef):
            designator = connection.end2.component.designator
            core = connection.end2.core

            if designator not in component_lookup:
                result.add_error(f"Connection {i} references unknown component: {designator}")
            else:
                component = component_lookup[designator]
                if isinstance(component, CableInstance):
                    valid_cores = {c.number for c in component.cores}
                    if core not in valid_cores:
                        result.add_error(
                            f"Connection {i} references invalid core {core} on {designator}"
                        )

            # Track core usage
            if designator not in core_usage:
                core_usage[designator] = {}
            if core not in core_usage[designator]:
                core_usage[designator][core] = 0
            core_usage[designator][core] += 1

    # Check for cable cores with too many connections (max 2: one on each end)
    for designator, cores in core_usage.items():
        for core, count in cores.items():
            if count > 2:
                result.add_error(
                    f"Cable core {designator}.{core} has {count} connection(s), maximum is 2 "
                    f"(one on each side of the core)"
                )

    # Check for unconnected pins (warning only)
    for component in harness.components:
        if isinstance(component, ConnectorInstance):
            used_pins = pin_usage.get(component.designator, set())
            total_pins = set(range(1, component.positions + 1))
            unconnected = total_pins - used_pins
            if unconnected:
                result.add_warning(
                    f"Connector {component.designator} has unconnected pins: {sorted(unconnected)}"
                )

        elif isinstance(component, CableInstance):
            used_cores = set(core_usage.get(component.designator, {}).keys())
            total_cores = {c.number for c in component.cores}
            unconnected = total_cores - used_cores
            if unconnected:
                result.add_warning(
                    f"Cable {component.designator} has unconnected cores: {sorted(unconnected)}"
                )

    return result
