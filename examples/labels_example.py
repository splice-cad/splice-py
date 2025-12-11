"""
Bundle Labels example

Demonstrates adding labels to connectors and cables for identification
and heat-shrink label printing.
"""

from splice import (
    Harness,
    ComponentType,
    Wire,
    WireColor,
    CableCore,
    ConnectorCategory,
)

# Create harness
harness = Harness(
    name="Labeled Power Distribution",
    description="Power distribution harness with bundle labels for heat-shrink printing"
)

# Configure global label settings
harness.label_settings.default_width_mm = 12
harness.label_settings.show_labels_on_canvas = True

# Add AC input connector
x1 = harness.add_component(
    kind=ComponentType.CONNECTOR,
    mpn="PE0SSS000",
    manufacturer="TE Connectivity",
    positions=3,
    position=(100, 200),
    pin_mapping={"0": "L", "1": "N", "2": "PE"}
)

# Add power supply
ps1 = harness.add_component(
    kind=ComponentType.CONNECTOR,
    mpn="CP10.241",
    manufacturer="PULS, LP",
    category=ConnectorCategory.POWER_SUPPLY,
    positions=5,
    position=(500, 200),
    pin_mapping={"0": "L", "1": "N", "2": "PE", "3": "+24V", "4": "0V"}
)

# Add circuit breaker
cb1 = harness.add_component(
    kind=ComponentType.CONNECTOR,
    mpn="2907565",
    manufacturer="Phoenix Contact",
    category=ConnectorCategory.CIRCUIT_BREAKER,
    positions=2,
    position=(900, 200),
    pin_mapping={"0": "IN", "1": "OUT"}
)

# Add output terminal
x2 = harness.add_component(
    kind=ComponentType.CONNECTOR,
    mpn="1047484",
    manufacturer="Phoenix Contact",
    positions=4,
    position=(1300, 200)
)

# Add a multi-core cable
c1 = harness.add_component(
    kind=ComponentType.CABLE,
    mpn="CABLE-4C-18",
    manufacturer="Alpha Wire",
    cores=[
        CableCore(1, awg=18, color=WireColor.RED),
        CableCore(2, awg=18, color=WireColor.BLACK),
        CableCore(3, awg=18, color=WireColor.GREEN),
        CableCore(4, awg=18, color=WireColor.WHITE),
    ],
    position=(700, 400)
)

# ============================================================================
# ADD LABELS
# ============================================================================

# Label the AC input connector with custom text
harness.add_label(
    text="AC INPUT",
    connector=x1,
    width_mm=15,
    font_size=10,
    text_color="#FFFFFF",
    background_color="#FF0000"  # Red background for AC warning
)

# Label power supply with auto-generated designator
harness.add_label(
    text="",
    connector=ps1,
    auto_designator=True  # Will use "PS1"
)

# Add a descriptive label to power supply
harness.add_label(
    text="24V DC OUTPUT",
    connector=ps1,
    width_mm=18,
    background_color="#FFFF00"  # Yellow
)

# Label circuit breaker
harness.add_label(
    text="MAIN BREAKER",
    connector=cb1,
    width_mm=15,
    background_color="#FFA500"  # Orange
)

# Label output terminal
harness.add_label(
    text="TO LOADS",
    connector=x2,
    width_mm=12,
    background_color="#00FF00"  # Green
)

# Label cable at both ends
harness.add_label(
    text="CONTROL CABLE",
    cable=c1,
    cable_end="both",
    width_mm=14,
    font_size=8,
    background_color="#0000FF",  # Blue
    text_color="#FFFFFF"
)

# ============================================================================
# CREATE CONNECTIONS
# ============================================================================

wire_black = Wire(mpn="18AWG-BLK", manufacturer="Generic", awg=18, color=WireColor.BLACK)
wire_blue = Wire(mpn="18AWG-BLU", manufacturer="Generic", awg=18, color=WireColor.BLUE)
wire_green = Wire(mpn="18AWG-GRN", manufacturer="Generic", awg=18, color=WireColor.GREEN)

# AC input to power supply
harness.connect(x1.pin(1), ps1.pin(1), wire=wire_black, length_mm=300, label_end1="L")
harness.connect(x1.pin(2), ps1.pin(2), wire=wire_blue, length_mm=300, label_end1="N")
harness.connect(x1.pin(3), ps1.pin(3), wire=wire_green, length_mm=300, label_end1="PE")

# Power supply to circuit breaker
harness.connect(ps1.pin(4), cb1.pin(1), wire=wire_blue, length_mm=250, label_end1="+24V")

# Circuit breaker to output
harness.connect(cb1.pin(2), x2.pin(1), wire=wire_blue, length_mm=250, label_end2="+24V OUT")

# Power supply ground to output
harness.connect(ps1.pin(5), x2.pin(2), wire=wire_black, length_mm=400, label_end1="0V", label_end2="0V OUT")

# Cable connections (core 1 and 2)
harness.connect(x2.pin(3), c1.core(1))
harness.connect(c1.core(1), x1.pin(1))  # Would connect elsewhere in real design

# ============================================================================
# VALIDATE AND SAVE
# ============================================================================

result = harness.validate()
if result.valid:
    harness.save("labels_example.json")
    print("Labels Example harness saved!")
    print(f"  Components: {len(harness.components)}")
    print(f"  Connections: {len(harness.connections)}")
    print(f"  Labels: {len(harness.labels)}")
    print("\nLabels created:")
    for label in harness.labels:
        target = label.connector_instance_id or label.cable_instance_id
        print(f"  - {target}: \"{label.label_text}\" ({label.width_mm}mm, bg={label.background_color})")
else:
    print("Validation failed!")
    for error in result.errors:
        print(f"  ERROR: {error}")
