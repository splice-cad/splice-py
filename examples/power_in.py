"""
Power In harness example

Creates a power input cable with a 4-pin connector and flying leads
for connecting to a power source.
"""

from splice import Harness, ComponentType, Wire, WireColor, FlyingLead

# Create harness
harness = Harness(
    name="Power In",
    description="Power input cable with flying leads"
)

# Add 4-pin power connector (Kycon KPJX-PM-4S)
x1 = harness.add_component(
    kind=ComponentType.CONNECTOR,
    mpn="KPJX-PM-4S",
    manufacturer="Kycon, Inc.",
    positions=4,
    position=(660, 30)
)

# Define wires
wire_red_20awg = Wire(
    mpn="20UL1015STRRED",
    manufacturer="Remington Industries",
    awg=20,
    color=WireColor.RED,
    description="HOOK-UP STRND 20AWG RED"
)

wire_black_20awg = Wire(
    mpn="20UL1007STRBLA",
    manufacturer="Remington Industries",
    awg=20,
    color=WireColor.BLACK,
    description="HOOK-UP STRND 20AWG BLACK"
)

# Create flying lead termination
flying_lead = FlyingLead(termination_type="stripped")

# Connect pins to flying leads
# Pin 1: Red wire (V+)
harness.connect(
    x1.pin(1),
    flying_lead,
    wire=wire_red_20awg,
    length_mm=300,
    label_end1="V+"
)

# Pin 2: Black wire (GND)
harness.connect(
    x1.pin(2),
    flying_lead,
    wire=wire_black_20awg,
    length_mm=300,
    label_end1="GND"
)

# Pin 3: Red wire (V+)
harness.connect(
    x1.pin(3),
    flying_lead,
    wire=wire_red_20awg,
    length_mm=300,
    label_end1="V+"
)

# Pin 4: Black wire (GND)
harness.connect(
    x1.pin(4),
    flying_lead,
    wire=wire_black_20awg,
    length_mm=300,
    label_end1="GND"
)

# Validate and save
result = harness.validate()
if result.valid:
    harness.save("power_in.json")
    print("✓ Power In harness saved!")
else:
    print("✗ Validation failed!")
    for error in result.errors:
        print(f"  ERROR: {error}")
    for warning in result.warnings:
        print(f"  WARNING: {warning}")
