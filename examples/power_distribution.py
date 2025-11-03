"""
Power Distribution harness example

Demonstrates using category-specific components (power supply and circuit breakers)
with auto-generated designators. This example shows a typical power distribution
panel with overcurrent protection.
"""

from splice import (
    Harness,
    ComponentType,
    Wire,
    WireColor,
    ConnectorCategory,
)

# Create power distribution harness
harness = Harness(
    name="Power Distribution",
    description="Industrial power distribution with circuit breakers"
)

# Add input connector (auto-generates X1) - AC power input
# Custom pin names can be added using pin_mapping parameter
x1 = harness.add_component(
    kind=ComponentType.CONNECTOR,
    mpn="PE0SSS000",
    manufacturer="TE Connectivity Corcom Filters",
    positions=3,
    position=(-560, 200),
    pin_mapping={"0": "L", "1": "N", "2": "E"}  # Custom pin names (0-indexed)
)

# Add power supply (auto-generates PS1) using enum for category
ps1 = harness.add_component(
    kind=ComponentType.CONNECTOR,
    mpn="CP10.241",
    manufacturer="PULS, LP",
    category=ConnectorCategory.POWER_SUPPLY,  # Use enum - auto-generates PS1
    positions=8,
    position=(20, 40),
    pin_mapping={
        "0": "L", "1": "N", "2": "PE", "3": "+",
        "4": "-", "5": "-", "6": "NC", "7": "NC"
    }
)

# Add main circuit breaker (auto-generates CB1) using enum for category
cb1 = harness.add_component(
    kind=ComponentType.CONNECTOR,
    mpn="2907565",
    manufacturer="Phoenix Contact",
    category=ConnectorCategory.CIRCUIT_BREAKER,  # Use enum - auto-generates CB1
    positions=2,
    position=(560, 40),
    pin_mapping={"0": "IN+", "1": "OUT+"}
)

# Add additional circuit breakers (auto-generates CB2, CB3)
cb2 = harness.add_component(
    kind=ComponentType.CONNECTOR,
    mpn="2908262",
    manufacturer="Phoenix Contact",
    category=ConnectorCategory.CIRCUIT_BREAKER,  # Use enum - auto-generates CB2
    positions=8,
    position=(1600, 40),
    pin_mapping={
        "0": "IN-", "1": "IN+", "2": "OUT-", "3": "OUT+",
        "4": "NC", "5": "NC", "6": "NC", "7": "NC"
    }
)

cb3 = harness.add_component(
    kind=ComponentType.CONNECTOR,
    mpn="2908262",
    manufacturer="Phoenix Contact",
    category=ConnectorCategory.CIRCUIT_BREAKER,  # Use enum - auto-generates CB3
    positions=8,
    position=(1600, 380),
    pin_mapping={
        "0": "IN+", "1": "IN-", "2": "OUT+", "3": "OUT-",
        "4": "NC", "5": "NC", "6": "NC", "7": "NC"
    }
)

# Add output terminal blocks (auto-generates X2, X3)
x2 = harness.add_component(
    kind=ComponentType.CONNECTOR,
    mpn="1047484",
    manufacturer="Phoenix Contact",
    positions=7,
    position=(560, 380)
)

x3 = harness.add_component(
    kind=ComponentType.CONNECTOR,
    mpn="1047479",
    manufacturer="Phoenix Contact",
    positions=7,
    position=(1080, 140)
)

# Define wires using enums for colors
wire_black = Wire(
    mpn="14AWG-BLK",
    manufacturer="Generic",
    awg=14,
    color=WireColor.BLACK,
    description="HOOK-UP STRND 14AWG BLACK"
)

wire_blue = Wire(
    mpn="14AWG-BLU",
    manufacturer="Generic",
    awg=14,
    color=WireColor.BLUE,
    description="HOOK-UP STRND 14AWG BLUE"
)

wire_white = Wire(
    mpn="14AWG-WHT",
    manufacturer="Generic",
    awg=14,
    color=WireColor.WHITE,
    description="HOOK-UP STRND 14AWG WHITE"
)

wire_green = Wire(
    mpn="14AWG-GRN",
    manufacturer="Generic",
    awg=14,
    color=WireColor.GREEN,
    description="HOOK-UP STRND 14AWG GREEN"
)

# AC input X1 to power supply PS1
harness.connect(x1.pin(1), ps1.pin(2), wire=wire_black, length_mm=400)  # W1: L -> N
harness.connect(x1.pin(2), ps1.pin(1), wire=wire_white, length_mm=400)  # W9: N -> L
harness.connect(x1.pin(3), ps1.pin(3), wire=wire_green, length_mm=400)  # W10: E -> PE

# Power supply PS1 to circuit breaker CB1
harness.connect(ps1.pin(4), cb1.pin(1), wire=wire_blue, length_mm=350)  # W5: V+ -> IN+

# Power supply PS1 to output terminal block X2
harness.connect(ps1.pin(6), x2.pin(1), wire=wire_black, length_mm=400)  # W2: V- -> (out)

# Circuit breaker CB1 to output terminal block X3
harness.connect(cb1.pin(2), x3.pin(1), wire=wire_blue, length_mm=350)  # W6: OUT+ -> (term)

# Output terminal blocks to circuit breakers
harness.connect(x2.pin(2), cb2.pin(3), wire=wire_black, length_mm=350)  # W3: (out) -> IN+
harness.connect(x2.pin(3), cb3.pin(2), wire=wire_black, length_mm=350)  # W4: (out) -> IN-

# X3 to circuit breakers
harness.connect(x3.pin(2), cb2.pin(1), wire=wire_blue, length_mm=400)  # W7: (term) -> IN-
harness.connect(x3.pin(3), cb3.pin(1), wire=wire_blue, length_mm=400)  # W8: (term) -> IN+

# Validate and save
result = harness.validate()
if result.valid:
    harness.save("power_distribution.json")
    print("✓ Power Distribution harness saved!")
    print(f"  Components: {len(harness.components)}")
    print(f"  Connections: {len(harness.connections)}")
    print("\nCategory components used:")
    print("  - PS1: Power Supply (auto-generated from category)")
    print("  - CB1, CB2, CB3: Circuit Breakers (auto-generated from category)")
    print("  - X1, X2, X3: Regular Connectors")
else:
    print("✗ Validation failed!")
    for error in result.errors:
        print(f"  ERROR: {error}")
    for warning in result.warnings:
        print(f"  WARNING: {warning}")
