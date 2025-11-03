# Splice JSON Schema Documentation

This document describes the JSON format exported by splice-py. The JSON files can be imported into the Splice web application for visualization and editing.

## Table of Contents

- [Top-Level Structure](#top-level-structure)
- [Enums Reference](#enums-reference)
- [BOM (Bill of Materials)](#bom-bill-of-materials)
- [Data Section](#data-section)
- [Part Types](#part-types)
- [Connection Types](#connection-types)
- [Examples](#examples)

## Top-Level Structure

The root object contains two required sections:

```json
{
  "bom": { /* Bill of Materials */ },
  "data": { /* Working harness data */ }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `bom` | object | Yes | Bill of materials with expanded part data |
| `data` | object | Yes | Harness working data (connections, positions) |

## Enums Reference

This section lists all enumerated types used throughout the schema. All enum values are lowercase strings unless otherwise noted.

### PartKind

The type of part in the BOM:

| Value | Description |
|-------|-------------|
| `connector` | Electrical connector |
| `terminal` | Crimp terminal or contact |
| `wire` | Single conductor wire |
| `cable` | Multi-core cable |
| `assembly` | Pre-assembled cable assembly |

### Gender

Contact gender for connectors:

| Value | Description |
|-------|-------------|
| `male` | Male/plug connector |
| `female` | Female/socket connector |
| `none` | Not applicable or gender-neutral |

### ConnectorShape

Physical shape of connector:

| Value | Description |
|-------|-------------|
| `circular` | Circular connector |
| `rectangular` | Rectangular connector |
| `dsub` | D-subminiature connector |
| `terminal_block` | Terminal block |
| `ferrule` | Ferrule/bootlace connector |
| `quickdisconnect` | Quick disconnect/spade terminal |
| `ring` | Ring terminal |
| `button` | Button connector |
| `other` | Other/custom shape |

### ConnectorCategory

Specialized component categories that affect designator prefixes:

| Value | Designator Prefix | Description |
|-------|------------------|-------------|
| `circuit_breaker` | CB | Circuit breaker |
| `fuse` | F | Fuse |
| `fan` | FAN | Cooling fan |
| `push_button` | BTN | Push button switch |
| `switch` | S | Toggle/rotary switch |
| `relay` | K | Electromechanical relay |
| `contactor` | K | Electrical contactor |
| `timer` | T | Timer relay |
| `pcb` | PCB | Printed circuit board |
| `power_supply` | PS | Power supply |
| `motor` | M | Electric motor |
| `other` | X | Other specialized component |

**Note**: Regular connectors without a category use the `X` prefix (X1, X2, X3...).

### ConductorType

Type of conductor construction:

| Value | Description |
|-------|-------------|
| `solid` | Solid core conductor |
| `stranded` | Stranded/multi-strand conductor |

### WireColor

Available wire colors:

| Value | Description |
|-------|-------------|
| `black` | Black |
| `brown` | Brown |
| `red` | Red |
| `orange` | Orange |
| `yellow` | Yellow |
| `green` | Green |
| `blue` | Blue |
| `violet` | Violet/Purple |
| `grey` | Grey/Gray (accepts both spellings) |
| `white` | White |
| `pink` | Pink |

**Note**: Custom colors can be specified as strings outside this enum.

### ConnectionSide

Side of a connector or cable where a wire attaches:

| Value | Description |
|-------|-------------|
| `left` | Left side |
| `right` | Right side |

### TerminationType

Flying lead termination type:

| Value | JSON Value | Description |
|-------|------------|-------------|
| Tinned | `tinned` | Wire end tinned with solder |
| Bare | `bare` | Bare stripped wire end |
| HeatShrink | `heat_shrink` | Heat shrink applied |

## BOM (Bill of Materials)

The BOM is a dictionary of component instances, keyed by designator (e.g., "X1", "W1", "CB1"):

```json
{
  "X1": {
    "instance_id": "X1",
    "part": { /* Part object */ },
    "unit": "each"
  }
}
```

### BOM Item Structure

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `instance_id` | string | Yes | Component designator (X1, W1, CB1, etc.) |
| `part` | object | Yes | Full part specification |
| `unit` | string | Yes | Unit of measure ("each", "ft", "m") |

### Part Object

All parts share common fields and a `spec` object specific to the part kind:

```json
{
  "id": "uuid-here",
  "kind": "connector",
  "mpn": "43650-0400",
  "manufacturer": "Molex",
  "description": "4 Position Connector",
  "spec": { /* Kind-specific specification */ }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string (UUID) | Yes | Unique part identifier |
| `kind` | string | Yes | Part type: "connector", "wire", "cable", "terminal" |
| `mpn` | string | Yes | Manufacturer part number |
| `manufacturer` | string | Yes | Manufacturer name |
| `description` | string | No | Human-readable description |
| `spec` | object | Yes | Kind-specific specification (see below) |

## Part Types

### Connector

Connectors use `kind: "connector"`. The spec is a flat object with all connector properties at the top level:

```json
{
  "kind": "connector",
  "spec": {
    "positions": 4,
    "part_id": "uuid-here",
    "contact_gender": "female",
    "shape": "rectangular",
    "category": "circuit_breaker",  // Optional: for specialized components
    "pin_mapping": {                // Optional: custom pin names (0-indexed keys)
      "0": "IN+",    // Pin 1
      "1": "IN-",    // Pin 2
      "2": "OUT+",   // Pin 3
      "3": "OUT-"    // Pin 4
    },
    "color": "black",
    "features": ["panel_mount"],
    // ... other connector fields
  }
}
```

#### Standard Connector Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `positions` | integer | Yes | Number of pins/positions |
| `part_id` | string (UUID) | Yes | Reference to part ID |
| `category` | string | No | Specialized category (see below) |
| `pin_mapping` | object | No | Custom pin names (0-indexed) |

#### Connector Categories

Categories control designator prefixes and specialized rendering. See [Enums Reference](#enums-reference) for complete list.

| Category | Prefix | Example Designators |
|----------|--------|-------------------|
| (none) | X | X1, X2, X3 |
| `power_supply` | PS | PS1, PS2 |
| `circuit_breaker` | CB | CB1, CB2 |
| `fuse` | F | F1, F2 |
| `fan` | FAN | FAN1, FAN2 |
| `push_button` | BTN | BTN1, BTN2 |
| `switch` | S | S1, S2 |
| `relay` | K | K1, K2 |
| `contactor` | K | K1, K2 |
| `timer` | T | T1, T2 |
| `pcb` | PCB | PCB1, PCB2 |
| `motor` | M | M1, M2 |
| `other` | X | X1, X2 |

#### Pin Mapping

Pin mappings provide custom names for connector pins. Keys are 0-indexed strings:

```json
{
  "pin_mapping": {
    "0": "LINE",    // Pin 1 (0-indexed)
    "1": "NEUTRAL", // Pin 2
    "2": "GROUND"   // Pin 3
  }
}
```

### Wire

Wires use `kind: "wire"`. The spec is a flat object containing wire properties:

```json
{
  "kind": "wire",
  "spec": {
    "awg": 22,
    "color": "red",
    "stripe": null,
    "stranding": "7/30",
    "conductor_type": "stranded",
    "part_id": "uuid-here"
  }
}
```

**Note**: Wire specs are exported flat at the spec level (not nested under `spec.wire`).

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `awg` | integer | Yes | Wire gauge (10-30 typical) |
| `color` | string | No | Primary wire color |
| `stripe` | string | No | Stripe color (if any) |
| `stranding` | string | No | Stranding pattern (e.g., "7/30") |
| `conductor_type` | string | Yes | "solid" or "stranded" |
| `part_id` | string (UUID) | Yes | Reference to part ID |

### Cable

Cables use `kind: "cable"`. The spec is a flat object with a `cores` array:

```json
{
  "kind": "cable",
  "spec": {
    "core_count": 2,
    "cores": [
      {
        "core_no": 1,
        "awg": 22,
        "core_color": "red",
        "conductor_type": "stranded"
      },
      {
        "core_no": 2,
        "awg": 22,
        "core_color": "black",
        "conductor_type": "stranded"
      }
    ],
    "part_id": "uuid-here"
  }
}
```

**Note**: Cable specs are exported flat at the spec level (not nested under `spec.cable`).

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `cores` | array | Yes | Array of cable core specifications |
| `core_count` | integer | Yes | Total number of cores |
| `part_id` | string (UUID) | Yes | Reference to part ID |

#### Cable Core Structure

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `core_no` | integer | Yes | Core number (1-indexed) |
| `awg` | integer | No | Wire gauge for this core |
| `core_color` | string | No | Color of this core |
| `conductor_type` | string | Yes | "solid" or "stranded" |

### Terminal

Terminals use `kind: "terminal"` for crimps and other wire terminations:

```json
{
  "kind": "terminal",
  "spec": {
    "wire_awg_min": 18,
    "wire_awg_max": 22,
    "plating": "tin",
    "part_id": "uuid-here"
  }
}
```

## Data Section

The `data` section contains harness working data including connections, positions, and metadata:

```json
{
  "data": {
    "name": "My Harness",
    "description": "Power distribution harness",
    "mapping": { /* Connections */ },
    "connector_positions": { /* Component positions */ },
    "cable_positions": { /* Cable positions */ },
    "wire_anchors": { /* Wire routing points */ },
    "design_notes": [ /* Annotations */ ]
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | No | Harness name |
| `description` | string | No | Harness description |
| `mapping` | object | Yes | Wire/cable connections (see below) |
| `connector_positions` | object | Yes | Connector X/Y positions on canvas |
| `cable_positions` | object | No | Cable X/Y positions on canvas |
| `wire_anchors` | object | No | Wire routing anchor points |
| `design_notes` | array | No | Design annotations |

### Positions

Position objects specify X/Y coordinates on the canvas, with optional dimensions:

```json
{
  "connector_positions": {
    "X1": { "x": 100, "y": 200 },
    "X2": { "x": 500, "y": 200, "width": 150, "height": 80 }
  }
}
```

**Position Fields**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `x` | number | Yes | X coordinate in pixels |
| `y` | number | Yes | Y coordinate in pixels |
| `width` | number | No | Width in pixels (for adjustable blocks) |
| `height` | number | No | Height in pixels (for adjustable blocks) |

### Termination Routing

Routing information for wire/cable terminations:

```json
{
  "routing": {
    "mode": "auto",
    "waypoints": [
      { "x": 740, "y": 52 }
    ],
    "bundleSide": "left"
  }
}
```

**TerminationRouting Fields**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `mode` | string | Yes | "auto" or "manual" routing |
| `waypoints` | array | No | Array of position objects for wire path |
| `bundleSide` | string | No | "left" or "right" (frontend-specific) |

## Connection Types

The `mapping` object contains all wire and cable connections, keyed by wire/cable designator:

### Wire Connection

A simple point-to-point wire connection:

```json
{
  "W1": {
    "end1": {
      "type": "connector_pin",
      "connector_instance": "X1",
      "pin": 1,  // 1-indexed (first pin)
      "side": "right"
    },
    "end2": {
      "type": "connector_pin",
      "connector_instance": "X2",
      "pin": 1,  // 1-indexed (first pin)
      "side": "left"
    },
    "length_mm": 300,
    "label": "POWER_12V",        // Deprecated: use label_end1/label_end2
    "label_end1": "12V_OUT",     // Signal name at end1
    "label_end2": "12V_IN",      // Signal name at end2
    "twisted_pair_id": "uuid"    // Optional: groups wires into twisted pairs
  }
}
```

**Connection Fields**:
- `label` - (deprecated) Single label for the connection, kept for backward compatibility
- `label_end1` - Signal name at end1 (preferred over `label`)
- `label_end2` - Signal name at end2
- `twisted_pair_id` - Optional UUID to group multiple wires into a twisted pair

### Cable Connection (Merged Format)

Cable cores use a merged connection format where each core appears once with both ends:

```json
{
  "C1.1": {  // Cable designator.core_number (core 1)
    "end1": {
      "type": "connector_pin",
      "connector_instance": "X1",
      "pin": 1,  // 1-indexed
      "side": "right"
    },
    "end2": {
      "type": "connector_pin",
      "connector_instance": "X2",
      "pin": 1,  // 1-indexed
      "side": "left"
    },
    "length_mm": 500,
    "label_end1": "V+"
  }
}
```

**Important:** Cable connections must follow this format:
- Mapping key: `{cable_designator}.{core_number}` (e.g., "C1.1", "C1.2")
- Core numbers in the key are 1-indexed (C1.1 = first core)
- Both `end1` and `end2` must be `connector_pin` type
- Pins are 1-indexed (pin 1 = first pin)
- Each core requires exactly one merged connection entry

### Flying Lead Connection

Flying leads are unterminated wire ends:

```json
{
  "W1": {
    "end1": {
      "type": "connector_pin",
      "connector_instance": "X1",
      "pin": 0,
      "side": "right"
    },
    "end2": {
      "type": "flying_lead",
      "termination_type": "tinned",
      "strip_length_mm": 6,
      "tin_length_mm": 3
    },
    "length_mm": 300,
    "label": "V+"
  }
}
```

### Connection End Types

#### connector_pin

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | "connector_pin" | Yes | End type identifier |
| `connector_instance` | string | Yes | Connector designator (e.g., "X1") |
| `pin` | integer | Yes | Pin number (1-indexed: pin 1 is first pin) |
| `side` | "left" \| "right" | Yes | Side of connector |
| `terminal_instance` | string | No | Terminal designator if using a crimp terminal |
| `routing` | object | No | Routing information (see TerminationRouting) |

#### cable_core

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | "cable_core" | Yes | End type identifier |
| `cable_instance` | string | Yes | Cable designator (e.g., "C1") |
| `core_no` | integer | Yes | Core number (1-indexed: core 1 is first core) |
| `side` | "left" \| "right" | Yes | Side of cable |
| `shield` | boolean | No | Whether this connection includes the shield |
| `routing` | object | No | Routing information (see TerminationRouting) |

#### flying_lead

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | "flying_lead" | Yes | End type identifier |
| `termination_type` | string | Yes | "bare", "tinned", or "heat_shrink" |
| `strip_length_mm` | number | No | Length of stripped insulation |
| `tin_length_mm` | number | No | Length of tinned section |
| `terminal_instance` | string | No | Terminal designator if using a terminal |
| `routing` | object | No | Routing information (see TerminationRouting) |

## Examples

### Complete Simple Harness

```json
{
  "bom": {
    "X1": {
      "instance_id": "X1",
      "part": {
        "id": "12345678-1234-1234-1234-123456789abc",
        "kind": "connector",
        "mpn": "43650-0300",
        "manufacturer": "Molex",
        "spec": {
          "positions": 3,
          "part_id": "12345678-1234-1234-1234-123456789abc"
        }
      },
      "unit": "each"
    },
    "X2": {
      "instance_id": "X2",
      "part": {
        "id": "87654321-4321-4321-4321-cba987654321",
        "kind": "connector",
        "mpn": "43650-0400",
        "manufacturer": "Molex",
        "spec": {
          "positions": 4,
          "part_id": "87654321-4321-4321-4321-cba987654321"
        }
      },
      "unit": "each"
    },
    "W1": {
      "instance_id": "W1",
      "part": {
        "id": "11111111-2222-3333-4444-555555555555",
        "kind": "wire",
        "mpn": "AWG22-RED",
        "manufacturer": "Alpha Wire",
        "spec": {
          "awg": 22,
          "color": "red",
          "conductor_type": "stranded",
          "stranding": "7/30",
          "stripe": null,
          "part_id": "11111111-2222-3333-4444-555555555555"
        },
        "description": "22 AWG Stranded Wire, Red"
      },
      "unit": "ft"
    }
  },
  "data": {
    "name": "Simple Harness",
    "description": "Basic point-to-point harness",
    "mapping": {
      "W1": {
        "end1": {
          "type": "connector_pin",
          "connector_instance": "X1",
          "pin": 1,
          "side": "right"
        },
        "end2": {
          "type": "connector_pin",
          "connector_instance": "X2",
          "pin": 1,
          "side": "left"
        },
        "length_mm": 300,
        "label_end1": "POWER"
      }
    },
    "connector_positions": {
      "X1": { "x": 100, "y": 100 },
      "X2": { "x": 500, "y": 100 }
    },
    "cable_positions": {},
    "wire_anchors": {}
  }
}
```

### Multi-Core Cable Example

```json
{
  "bom": {
    "C1": {
      "instance_id": "C1",
      "part": {
        "id": "cable-uuid",
        "kind": "cable",
        "mpn": "CABLE-4C-22",
        "manufacturer": "Alpha Wire",
        "spec": {
          "cores": [
            {
              "core_no": 1,
              "awg": 22,
              "core_color": "red",
              "conductor_type": "stranded"
            },
            {
              "core_no": 2,
              "awg": 22,
              "core_color": "black",
              "conductor_type": "stranded"
            }
          ],
          "core_count": 2,
          "part_id": "cable-uuid"
        }
      },
      "unit": "ft"
    }
  },
  "data": {
    "mapping": {
      "C1.1": {
        "end1": {
          "type": "connector_pin",
          "connector_instance": "X1",
          "pin": 1,
          "side": "right"
        },
        "end2": {
          "type": "connector_pin",
          "connector_instance": "X2",
          "pin": 1,
          "side": "left"
        },
        "length_mm": 500,
        "label_end1": "V+"
      },
      "C1.2": {
        "end1": {
          "type": "connector_pin",
          "connector_instance": "X1",
          "pin": 2,
          "side": "right"
        },
        "end2": {
          "type": "connector_pin",
          "connector_instance": "X2",
          "pin": 2,
          "side": "left"
        },
        "length_mm": 500,
        "label_end1": "GND"
      }
    }
  }
}
```

### Circuit Breaker with Pin Mapping

```json
{
  "bom": {
    "CB1": {
      "instance_id": "CB1",
      "part": {
        "id": "cb-uuid",
        "kind": "connector",
        "mpn": "2907565",
        "manufacturer": "Phoenix Contact",
        "spec": {
          "positions": 2,
          "category": "circuit_breaker",
          "pin_mapping": {
            "0": "IN+",
            "1": "OUT+"
          },
          "part_id": "cb-uuid"
        }
      },
      "unit": "each"
    }
  }
}
```

### Flying Lead Example

```json
{
  "data": {
    "mapping": {
      "W1": {
        "end1": {
          "type": "connector_pin",
          "connector_instance": "X1",
          "pin": 1,
          "side": "right"
        },
        "end2": {
          "type": "flying_lead",
          "termination_type": "tinned",
          "strip_length_mm": 6,
          "tin_length_mm": 3
        },
        "length_mm": 200,
        "label_end1": "V+"
      }
    }
  }
}
```

## Reference Schemas

Complete reference JSON schemas for working harnesses are available in the [`/schemas`](../schemas) directory:

- `Power Distribution_schema.json` - Industrial power distribution with circuit breakers
- `GNS430 NAV_schema.json` - Aviation harness with high-density connectors
- `Power In_schema.json` - Power cable with flying leads

## Designator Conventions

Component designators are automatically generated based on the component type and category:

| Prefix | Component Type | Category Enum | JSON Value |
|--------|---------------|---------------|------------|
| X | Standard Connector | (none) | (none) |
| W | Wire | (none) | (none) |
| C | Cable | (none) | (none) |
| T | Terminal | (none) | (none) |
| PS | Power Supply | `ConnectorCategory.POWER_SUPPLY` | `"power_supply"` |
| CB | Circuit Breaker | `ConnectorCategory.CIRCUIT_BREAKER` | `"circuit_breaker"` |
| F | Fuse | `ConnectorCategory.FUSE` | `"fuse"` |
| FAN | Fan | `ConnectorCategory.FAN` | `"fan"` |
| BTN | Push Button | `ConnectorCategory.PUSH_BUTTON` | `"push_button"` |
| S | Switch | `ConnectorCategory.SWITCH` | `"switch"` |
| K | Relay | `ConnectorCategory.RELAY` | `"relay"` |
| K | Contactor | `ConnectorCategory.CONTACTOR` | `"contactor"` |
| T | Timer | `ConnectorCategory.TIMER` | `"timer"` |
| PCB | PCB | `ConnectorCategory.PCB` | `"pcb"` |
| M | Motor | `ConnectorCategory.MOTOR` | `"motor"` |

**Note**: When using splice-py, pass the enum value (e.g., `ConnectorCategory.CIRCUIT_BREAKER`). In JSON, it appears as a lowercase string with underscores (e.g., `"circuit_breaker"`).

## Index Conventions

**IMPORTANT**: Different elements use different indexing conventions:

| Element | Index Type | Example | Notes |
|---------|-----------|---------|-------|
| **Connection pins** | 1-indexed integers | `"pin": 1`, `"pin": 2` | Pin 1 is the first pin |
| **Pin mapping keys** | 0-indexed strings | `"0": "IN+"`, `"1": "OUT+"` | Key "0" refers to pin 1 |
| **Cable core numbers** | 1-indexed integers | `"core_no": 1`, `"core_no": 2` | Core 1 is the first core |
| **Python API** | 1-indexed | `x1.pin(1)` | Matches JSON directly |

### Pin Mapping vs Connection Pins

This is the most confusing aspect of the schema:

- **Connections** use 1-indexed pins: `{"pin": 1}` refers to the first physical pin
- **Pin mappings** use 0-indexed string keys: `{"0": "VCC"}` assigns name "VCC" to the first physical pin (pin 1)

**Example**:
```json
{
  "spec": {
    "positions": 3,
    "pin_mapping": {
      "0": "VCC",    // Names pin 1
      "1": "GND",    // Names pin 2
      "2": "SIGNAL"  // Names pin 3
    }
  }
}

// Connection referencing pin 1 (which has name "VCC")
{
  "mapping": {
    "W1": {
      "end1": {
        "pin": 1  // This is the physical pin 1, named "VCC" above
      }
    }
  }
}

## Version History

- **v1.1** (2025-10) - Schema documentation corrections and enums
  - **CRITICAL FIX**: Corrected pin indexing - connections use 1-indexed pins (not 0-indexed)
  - Clarified pin_mapping uses 0-indexed string keys while connections use 1-indexed integers
  - Fixed spec structure - all specs are flat (not nested under connector/wire/cable keys)
  - Added comprehensive [Enums Reference](#enums-reference) section with all enum values
  - Fixed ConnectorCategory enum - added all actual categories (fan, push_button, contactor, timer, pcb, other)
  - Removed non-existent categories (sensor, valve) from documentation
  - Added missing Connection fields: `label_end1`, `label_end2`, `twisted_pair_id`
  - Added missing ConnectionTermination fields: `shield`, `routing`, `terminal_instance`
  - Added Position optional fields: `width`, `height`
  - Added TerminationRouting documentation with `bundleSide` field
  - Documented deprecated `label` field (use `label_end1`/`label_end2` instead)
  - Updated designator conventions table with JSON values

- **v1.0** (2025-01) - Initial schema documentation
  - Added pin_mapping support
  - Added cable core_color field
  - Documented merged cable connection format
  - Added connector category designators
