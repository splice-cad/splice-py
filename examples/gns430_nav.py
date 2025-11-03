"""
GNS430 NAV harness example

Aviation wiring harness for Garmin GNS430 NAV/COM radio,
connecting three high-density connectors with multiple signal wires.
"""

from splice import Harness, ComponentType, Wire, WireColor

# Create harness
harness = Harness(
    name="GNS430 NAV",
    description="Garmin GNS430 NAV/COM radio wiring harness"
)

# Add main 78-pin connector (DSUB-78)
x1 = harness.add_component(
    kind=ComponentType.CONNECTOR,
    mpn="204521-2",
    manufacturer="TE Connectivity Aerospace, Defense and Marine",
    positions=78,
    position=(-500, -480)
)

# Add 44-pin connector
x2 = harness.add_component(
    kind=ComponentType.CONNECTOR,
    mpn="204517-2",
    manufacturer="TE Connectivity Aerospace, Defense and Marine",
    positions=44,
    position=(800, -480)
)

# Add 25-pin connector (DSUB-25)
x3 = harness.add_component(
    kind=ComponentType.CONNECTOR,
    mpn="5-747912-2",
    manufacturer="TE Connectivity AMP Connectors",
    positions=25,
    position=(160, -480)
)

# Define wires - using different colors for different signal types
wire_white_24awg = Wire(
    mpn="24UL1007STRWHT",
    manufacturer="Remington Industries",
    awg=24,
    color=WireColor.WHITE,
    description="HOOK-UP STRND 24AWG WHITE"
)

wire_blue_24awg = Wire(
    mpn="24UL1007STRBLU",
    manufacturer="Remington Industries",
    awg=24,
    color=WireColor.BLUE,
    description="HOOK-UP STRND 24AWG BLU 500'"
)

wire_green_24awg = Wire(
    mpn="24UL1007STRGRE",
    manufacturer="Remington Industries",
    awg=24,
    color=WireColor.GREEN,
    description="HOOK-UP STRND 24AWG 300V GRN 25'"
)

wire_orange_24awg = Wire(
    mpn="24UL1007STRORG",
    manufacturer="Remington Industries",
    awg=24,
    color=WireColor.ORANGE,
    description="HOOK-UP STRND 24AWG ORANGE"
)

wire_yellow_24awg = Wire(
    mpn="24UL1007STRYLW",
    manufacturer="Remington Industries",
    awg=24,
    color=WireColor.YELLOW,
    description="HOOK-UP STRND 24AWG YELLOW"
)

# NAV/COM signal connections
harness.connect(
    x1.pin(46),
    x3.pin(23),
    wire=wire_white_24awg,
    length_mm=500,
    label="OUT A"
)

harness.connect(
    x1.pin(47),
    x3.pin(11),
    wire=wire_blue_24awg,
    length_mm=500,
    label="OUT B"
)

harness.connect(
    x1.pin(48),
    x3.pin(25),
    wire=wire_green_24awg,
    length_mm=500,
    label="IN A"
)

harness.connect(
    x1.pin(49),
    x3.pin(13),
    wire=wire_orange_24awg,
    length_mm=500,
    label="IN B"
)

harness.connect(
    x1.pin(54),
    x3.pin(3),
    wire=wire_yellow_24awg,
    length_mm=500,
    label="RS232 OUT"
)

# Additional connections (examples)
harness.connect(
    x1.pin(55),
    x3.pin(18),
    wire=wire_white_24awg,
    length_mm=500,
    label="RS232 IN"
)

harness.connect(
    x1.pin(12),
    x2.pin(8),
    wire=wire_blue_24awg,
    length_mm=400,
    label="AUDIO OUT"
)

harness.connect(
    x1.pin(13),
    x2.pin(20),
    wire=wire_green_24awg,
    length_mm=400,
    label="PTT"
)

harness.connect(
    x2.pin(21),
    x3.pin(8),
    wire=wire_orange_24awg,
    length_mm=600,
    label="GPS DATA"
)

# Validate and save
result = harness.validate()
if result.valid:
    harness.save("gns430_nav.json")
    print("✓ GNS430 NAV harness saved!")
    print(f"  Components: {len(harness.components)}")
    print(f"  Connections: {len(harness.connections)}")
else:
    print("✗ Validation failed!")
    for error in result.errors:
        print(f"  ERROR: {error}")
    for warning in result.warnings:
        print(f"  WARNING: {warning}")
