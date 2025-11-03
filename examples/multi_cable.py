"""
Multi-core cable example

Demonstrates using multi-core cables and connecting individual cores
to connector pins.
"""

from splice import Harness, ComponentType, CableCore, WireColor

# Create harness
harness = Harness(
    name="Multi-Core Cable Assembly",
    description="4-conductor cable with connectors on both ends"
)

# Add connectors
x1 = harness.add_component(
    kind=ComponentType.CONNECTOR,
    mpn="43650-0400",
    manufacturer="Molex",
    positions=4,
    position=(100, 100)
)

x2 = harness.add_component(
    kind=ComponentType.CONNECTOR,
    mpn="43650-0400",
    manufacturer="Molex",
    positions=4,
    position=(700, 100)
)

# Add multi-core cable (auto-generates W1) using enums for colors
w1 = harness.add_component(
    kind=ComponentType.CABLE,
    mpn="CABLE-4C-22",
    manufacturer="Alpha Wire",
    cores=[
        CableCore(1, awg=22, color=WireColor.RED),
        CableCore(2, awg=22, color=WireColor.BLACK),
        CableCore(3, awg=22, color=WireColor.WHITE),
        CableCore(4, awg=22, color=WireColor.GREEN)
    ],
    position=(400, 100)
)

# Connect each core
harness.connect(x1.pin(1), w1.core(1), label_end1="V+", label_end2="V+")
harness.connect(w1.core(1), x2.pin(1))

harness.connect(x1.pin(2), w1.core(2), label_end1="GND", label_end2="GND")
harness.connect(w1.core(2), x2.pin(2))

harness.connect(x1.pin(3), w1.core(3), label_end1="SIG_A", label_end2="SIG_A")
harness.connect(w1.core(3), x2.pin(3))

harness.connect(x1.pin(4), w1.core(4), label_end1="SIG_B", label_end2="SIG_B")
harness.connect(w1.core(4), x2.pin(4))

# Validate and save
result = harness.validate()
if result.valid:
    harness.save("multi_cable.json")
    print("✓ Multi-core cable harness saved!")
else:
    print("✗ Validation failed!")
    for error in result.errors:
        print(f"  ERROR: {error}")
    for warning in result.warnings:
        print(f"  WARNING: {warning}")
