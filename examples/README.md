# Splice-py Examples

This directory contains example scripts demonstrating how to use the splice-py library to create cable harness designs.

## Examples

### 1. multi_cable.py
**Multi-Core Cable Assembly**

Demonstrates how to use multi-core cables in a harness. Shows proper cable core connection patterns where each core requires two connections (one on each end).

- Cable designator: C1 (not W1 - cables use "C" prefix)
- Mapping format: `C1.1`, `C1.2`, etc. (cable_designator.core_number)
- Creates merged connections with both ends as connector pins

**Key concepts:**
- Adding multi-core cables with `ComponentType.CABLE`
- Using `CableCore` to define individual conductors
- Connecting cable cores to connector pins
- Proper validation of cable connections

### 2. power_in.py
**Power Input Cable with Flying Leads**

Shows how to create a power input cable with a connector on one end and flying leads (stripped wire ends) on the other end.

**Key concepts:**
- Using `FlyingLead` termination type
- Flying lead connections for power inputs
- Simple 4-pin power connector

### 3. power_distribution.py
**Industrial Power Distribution Panel**

Demonstrates category-specific components with auto-generated designators. Shows a power distribution system with power supply, circuit breakers, and output terminals.

**Key concepts:**
- Using `ConnectorCategory` enums for specialized components
- Auto-generated designators: PS1 (power supply), CB1/CB2/CB3 (circuit breakers)
- Multiple wire connections in a distribution topology

### 4. gns430_nav.py
**Aviation Wiring Harness**

Example of a complex aviation harness connecting multiple high-density connectors for a Garmin GNS430 NAV/COM radio system.

**Key concepts:**
- High pin-count connectors (78, 44, and 25 positions)
- Multiple wire colors for different signal types
- Wire labeling for signal identification
- Realistic aviation connector part numbers

## Running the Examples

Each example can be run independently:

```bash
cd examples
python3 multi_cable.py
python3 power_in.py
python3 power_distribution.py
python3 gns430_nav.py
```

Each script will:
1. Create a harness with components and connections
2. Validate the design
3. Save to a JSON file that can be imported into Splice

## Output Files

The examples generate JSON files in the Splice import format:
- `multi_cable.json`
- `power_in.json`
- `power_distribution.json`
- `gns430_nav.json`

These files can be uploaded to the Splice web interface for visualization and further editing.

## Common Patterns

### Adding Components
```python
connector = harness.add_component(
    kind=ComponentType.CONNECTOR,
    mpn="43650-0400",
    manufacturer="Molex",
    positions=4,
    position=(100, 100)  # Optional canvas position
)
```

### Custom Pin Naming
Components can have custom pin names using the `pin_mapping` parameter. Pin mappings are 0-indexed dictionaries:

```python
# Example: Power supply with custom pin names
ps1 = harness.add_component(
    kind=ComponentType.CONNECTOR,
    mpn="CP10.241",
    manufacturer="PULS, LP",
    category=ConnectorCategory.POWER_SUPPLY,
    positions=8,
    position=(20, 40),
    pin_mapping={
        "0": "L",   # Line
        "1": "N",   # Neutral
        "2": "PE",  # Protective Earth
        "3": "+",   # Positive output
        "4": "-",   # Negative output
        "5": "-",   # Negative output
        "6": "NC",  # Not connected
        "7": "NC"   # Not connected
    }
)
```

See `power_distribution.py` for a complete example with pin mappings on multiple components.

### Creating Connections
```python
wire = Wire(
    mpn="20UL1015STRRED",
    manufacturer="Remington Industries",
    awg=20,
    color=WireColor.RED
)

harness.connect(
    connector1.pin(1),
    connector2.pin(1),
    wire=wire,
    length_mm=300,
    label="SIGNAL_NAME"
)
```

### Validation
```python
result = harness.validate()
if result.valid:
    harness.save("output.json")
else:
    for error in result.errors:
        print(f"ERROR: {error}")
```

## More Information

- [Main README](../README.md) - Installation and API documentation
- [JSON Schema Reference](../docs/schema.md) - Complete documentation of the JSON export format
- [Reference Schemas](../schemas) - Complete JSON schemas from these examples
