# splice-py

Python library for programmatic Splice harness generation. Create cable harness designs in Python and export them as JSON files for upload to Splice or save directly via the API.

## Installation

```bash
pip install splice-py
```

## Quick Start

```python
from splice import Harness, ComponentType, Wire, WireColor, Stranding

# Create harness
harness = Harness(
    name="My Cable Assembly",
    description="Power and signal distribution"
)

# Add connectors (auto-generates X1, X2 designators)
x1 = harness.add_component(
    kind=ComponentType.CONNECTOR,
    mpn="43650-0300",
    manufacturer="Molex",
    positions=3,
    position=(100, 100)
)

x2 = harness.add_component(
    kind=ComponentType.CONNECTOR,
    mpn="43650-0400",
    manufacturer="Molex",
    positions=4,
    position=(500, 100)
)

# Add wire and create connection using enums for type safety
wire_red = Wire(
    mpn="1234-RED-22",
    manufacturer="Alpha Wire",
    awg=22,
    color=WireColor.RED,  # Type-safe color enum
    stranding=Stranding.AWG_22_7_30  # Type-safe stranding enum
)

# Connect X1 pin 1 to X2 pin 1
harness.connect(
    x1.pin(1),
    x2.pin(1),
    wire=wire_red,
    length_mm=300,
    label="PWR_12V"
)

# Validate and export
harness.validate()
harness.save("my_harness.json")

# Option 1: Upload my_harness.json to Splice via the web interface
# Option 2: Upload directly via API (requires API key)
result = harness.upload(api_key="splice_abc123...")
print(f"Harness uploaded! View at: https://splice-cad.com/#/harness")
```

## Features

- 🐍 Pythonic API with full type hints
- 🎯 Type-safe enums for colors, stranding, categories, and more
- 🔧 Supports all Splice component types (connectors, cables, wires, terminals)
- 🏷️ Auto-generates standard designators (X1, W1, F1, CB1, etc.)
- ✅ Built-in validation
- 📋 Multi-core cable support
- 🔌 Flying lead terminations
- 📝 Design notes
- 🎨 Custom positioning
- 📦 Generates Splice-compatible JSON
- 🚀 Direct API upload to Splice account

## Type-Safe Enums

The library provides enums for common properties to prevent typos and enable IDE autocomplete:

```python
from splice import WireColor, Stranding, ConnectorCategory, FlyingLeadType

# Wire colors
WireColor.RED, WireColor.BLACK, WireColor.BLUE, etc.

# Wire stranding
Stranding.AWG_22_7_30  # 22 AWG: 7 strands of 30 AWG
Stranding.AWG_18_16_30  # 18 AWG: 16 strands of 30 AWG
Stranding.CLASS_5  # Flexible stranded

# Connector categories (for specialized components)
ConnectorCategory.FUSE  # Auto-generates F1, F2...
ConnectorCategory.CIRCUIT_BREAKER  # Auto-generates CB1, CB2...
ConnectorCategory.POWER_SUPPLY  # Auto-generates PS1, PS2...
ConnectorCategory.RELAY  # Auto-generates K1, K2...

# Flying lead terminations
FlyingLeadType.BARE
FlyingLeadType.TINNED
FlyingLeadType.HEAT_SHRINK
```

All enums also accept custom strings if you need values not in the enum.

## Component Types

```python
from splice import ComponentType

# Standard components
ComponentType.CONNECTOR    # X1, X2, X3...
ComponentType.CABLE        # W1, W2, W3...
ComponentType.WIRE         # W1, W2, W3...
ComponentType.TERMINAL     # Terminal crimps

# Category-specific (all use CONNECTOR kind with category field)
# Fuses → F1, F2...
# Circuit Breakers → CB1, CB2...
# Switches → S1, S2...
# Relays → K1, K2...
# Power Supplies → PS1, PS2...
# Motors → M1, M2...
```

## Examples

Complete working examples are available in the [`examples/`](./examples) directory. Reference JSON schemas are provided in the [`schemas/`](./schemas) directory.

### Multi-core Cable

```python
from splice import CableCore, WireColor

# Add cable with cores using enums for colors
w1 = harness.add_component(
    kind=ComponentType.CABLE,
    mpn="CABLE-4C-22",
    manufacturer="Alpha Wire",
    cores=[
        CableCore(1, awg=22, color=WireColor.RED),
        CableCore(2, awg=22, color=WireColor.BLACK),
        CableCore(3, awg=22, color=WireColor.WHITE),
        CableCore(4, awg=22, color=WireColor.GREEN)
    ]
)

# Connect cores
harness.connect(x1.pin(1), w1.core(1))
harness.connect(w1.core(1), x2.pin(1))
```

### Flying Leads

```python
from splice import FlyingLead, FlyingLeadType

# Use enum for termination type
harness.connect(
    x1.pin(3),
    FlyingLead(
        termination_type=FlyingLeadType.TINNED,  # Type-safe enum
        strip_length_mm=10,
        tin_length_mm=5
    ),
    wire=wire_red,
    length_mm=200
)
```

### Category Components (Fuses, Relays, etc.)

```python
from splice import ConnectorCategory

# Add fuse (auto-generates F1) using enum for type safety
f1 = harness.add_component(
    kind=ComponentType.CONNECTOR,
    mpn="0251005.NRT1L",
    manufacturer="Littelfuse",
    category=ConnectorCategory.FUSE,  # Type-safe enum
    current_rating=5,
    positions=2
)

# Add circuit breaker (auto-generates CB1) using enum for type safety
cb1 = harness.add_component(
    kind=ComponentType.CONNECTOR,
    mpn="1492-CB1-G100",
    manufacturer="Allen-Bradley",
    category=ConnectorCategory.CIRCUIT_BREAKER,  # Type-safe enum
    current_rating=10,
    positions=2
)
```

### Custom Pin Naming

Components can have custom pin names using the `pin_mapping` parameter. Pin mappings are 0-indexed dictionaries:

```python
# Add power supply with custom pin names
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

# Add circuit breaker with custom pin names
cb1 = harness.add_component(
    kind=ComponentType.CONNECTOR,
    mpn="2907565",
    manufacturer="Phoenix Contact",
    category=ConnectorCategory.CIRCUIT_BREAKER,
    positions=2,
    pin_mapping={"0": "IN+", "1": "OUT+"}
)
```

### API Upload

Upload harnesses directly to your Splice account using an API key:

```python
from splice import Harness

harness = Harness("My Design")
# ... add components and connections ...

# Upload to Splice (requires API key from Account Settings)
result = harness.upload(
    api_key="splice_abc123...",
    is_public=False,  # Optional: make harness publicly visible
    api_url="https://splice-cad.com"  # Optional: custom API URL
)

print(f"Created harness: {result['id']}")
print(f"Owner: {result['owner_id']}")
print(f"Created at: {result['created_at']}")

# View in Splice web interface at:
# https://splice-cad.com/#/harness
```

**Getting an API Key:**
1. Log in to your Splice account at https://splice-cad.com
2. Go to Account Settings
3. Generate a new API key
4. Store it securely (treat like a password)

**Requirements:** The `requests` library is required for API upload:
```bash
pip install requests
```

### Batch Generation

```python
# Generate and upload 100 harness variants
for i in range(1, 101):
    harness = Harness(name=f"Assembly-{i:03d}")

    # Add components...
    # Make connections...

    # Option 1: Save to file
    harness.save(f"output/harness_{i:03d}.json")

    # Option 2: Upload directly to Splice
    # harness.upload(api_key="splice_abc123...")
```

## API Reference

### Harness

```python
class Harness:
    def __init__(self, name: str, description: str = "")

    def add_component(
        kind: ComponentType,
        mpn: str,
        manufacturer: str,
        designator: Optional[str] = None,  # Auto-generated
        position: Optional[Tuple[float, float]] = None,
        **kwargs
    ) -> ComponentInstance

    def connect(
        end1: Union[PinRef, CoreRef, FlyingLead],
        end2: Union[PinRef, CoreRef, FlyingLead],
        wire: Wire,
        length_mm: Optional[float] = None,
        label: Optional[str] = None
    ) -> Connection

    def validate() -> ValidationResult
    def save(filepath: str)
    def to_json() -> str
    def to_dict() -> dict

    def upload(
        api_key: str,
        is_public: bool = False,
        api_url: str = "https://splice-cad.com"
    ) -> Dict[str, Any]
```

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Type check
mypy splice

# Format code
black splice tests
isort splice tests

# Lint
flake8 splice tests
```

## License

MIT © Splice CAD

## Documentation

- [JSON Schema Reference](./docs/schema.md) - Complete documentation of the export format
- [API Reference](./docs/api.md) - Full API documentation (coming soon)

## Links

- [Examples](./examples) - Working example scripts
- [Reference Schemas](./schemas) - Complete JSON schemas from example harnesses
- [Splice Website](https://splice-cad.com)
- [GitHub Issues](https://github.com/splice-cad/splice-py/issues)
