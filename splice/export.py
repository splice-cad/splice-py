"""
Export harness to Splice-compatible JSON format.
"""

import uuid
from typing import Dict, Any, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .harness import Harness
    from .components import ComponentInstance, ConnectorInstance, CableInstance, WireInstance
    from .connections import Connection

from .components import ConnectorInstance, CableInstance, WireInstance, PinRef, CoreRef
from .connections import FlyingLead
from .types import ComponentType


def generate_wire_key(index: int) -> str:
    """Generate a wire key for a connection."""
    return f"W{index}"


def component_to_bom_item(component: "ComponentInstance") -> Dict[str, Any]:
    """
    Convert a component to a BOM item with part specification.

    Args:
        component: The component instance to convert

    Returns:
        BOM item dictionary
    """
    # Build the part object with spec
    part: Dict[str, Any] = {
        "id": str(uuid.uuid4()),  # Generate a UUID for the part
        "kind": component.kind.value,
        "mpn": component.mpn,
        "manufacturer": component.manufacturer,
    }

    # Add spec based on component type
    if isinstance(component, ConnectorInstance):
        spec: Dict[str, Any] = {
            "positions": component.positions,
            "part_id": part["id"],
        }

        # Add category-specific fields if present
        if component.category:
            spec["category"] = component.category

        # Add any custom fields to the spec
        for key, value in component.custom_fields.items():
            if key not in ["positions", "kind", "designator"]:
                spec[key] = value

        part["spec"] = spec

    elif isinstance(component, CableInstance):
        cores_spec = []
        for core in component.cores:
            cores_spec.append({
                "core_no": core.number,
                "awg": core.awg if hasattr(core, 'awg') else None,
                "core_color": core.color if hasattr(core, 'color') else None,
                "conductor_type": "stranded",  # Default
            })

        part["spec"] = {
            "core_count": len(component.cores),
            "cores": cores_spec,
            "part_id": part["id"],
            **component.custom_fields,
        }

    elif isinstance(component, WireInstance):
        part["spec"] = {
            "awg": component.awg,
            "color": component.color,
            "conductor_type": "stranded",  # Default
            "part_id": part["id"],
            **{k: v for k, v in component.custom_fields.items() if k not in ["awg", "color"]},
        }

    # Build the BOM item
    # Wires use "ft" (feet), connectors and cables use "each"
    unit = "ft" if component.kind == ComponentType.WIRE else "each"

    bom_item = {
        "instance_id": component.designator,
        "part": part,
        "unit": unit,
    }

    return bom_item


def wire_to_bom_item(wire_key: str, connection: "Connection") -> Dict[str, Any]:
    """
    Convert a wire specification to a BOM item.

    Args:
        wire_key: The wire key (e.g., "W1")
        connection: The connection containing the wire spec

    Returns:
        BOM item dictionary for the wire
    """
    wire = connection.wire

    part_id = str(uuid.uuid4())
    part = {
        "id": part_id,
        "kind": "wire",
        "mpn": wire.mpn,
        "manufacturer": wire.manufacturer,
        "spec": {
            "awg": wire.awg,
            "color": wire.color,
            "conductor_type": "stranded",  # Default
            "part_id": part_id,
            "stranding": None,
            "stripe": None,
        },
    }

    if wire.description:
        part["description"] = wire.description

    return {
        "instance_id": wire_key,
        "part": part,
        "unit": "ft",  # Wire length measured in feet
    }


def connection_to_mapping_entry(connection: "Connection") -> Dict[str, Any]:
    """
    Convert a connection to a mapping entry.

    Args:
        connection: The connection to convert

    Returns:
        Mapping entry dictionary
    """
    mapping_entry: Dict[str, Any] = {}

    # Convert end1
    if isinstance(connection.end1, PinRef):
        mapping_entry["end1"] = {
            "type": "connector_pin",
            "connector_instance": connection.end1.component.designator,
            "pin": connection.end1.pin,
            "side": "left",  # Default side
            "terminal_instance": None,
        }
    elif isinstance(connection.end1, CoreRef):
        mapping_entry["end1"] = {
            "type": "cable_core",
            "cable_instance": connection.end1.component.designator,
            "core_no": connection.end1.core,
            "side": "left",  # Default side
        }
    elif isinstance(connection.end1, FlyingLead):
        mapping_entry["end1"] = {
            "type": "flying_lead",
            "termination_type": connection.end1.termination_type,
        }
        if connection.end1.strip_length_mm:
            mapping_entry["end1"]["strip_length_mm"] = connection.end1.strip_length_mm

    # Convert end2
    if isinstance(connection.end2, PinRef):
        mapping_entry["end2"] = {
            "type": "connector_pin",
            "connector_instance": connection.end2.component.designator,
            "pin": connection.end2.pin,
            "side": "left",  # Default side for end2
            "terminal_instance": None,
        }
    elif isinstance(connection.end2, CoreRef):
        mapping_entry["end2"] = {
            "type": "cable_core",
            "cable_instance": connection.end2.component.designator,
            "core_no": connection.end2.core,
            "side": "left",  # Default side for end2
        }
    elif isinstance(connection.end2, FlyingLead):
        mapping_entry["end2"] = {
            "type": "flying_lead",
            "termination_type": connection.end2.termination_type,
        }
        if connection.end2.strip_length_mm:
            mapping_entry["end2"]["strip_length_mm"] = connection.end2.strip_length_mm

    # Add length if specified
    if connection.length_mm is not None:
        mapping_entry["length_mm"] = connection.length_mm

    # Add labels
    if connection.label_end1:
        mapping_entry["label_end1"] = connection.label_end1
    if connection.label_end2:
        mapping_entry["label_end2"] = connection.label_end2
    elif connection.label:  # Fallback to single label
        mapping_entry["label"] = connection.label

    return mapping_entry


def harness_to_splice_format(harness: "Harness") -> Dict[str, Any]:
    """
    Convert a Harness to Splice-compatible JSON format.

    The format is:
    {
      "bom": {
        "X1": { "instance_id": "X1", "part": {...}, "unit": "each" },
        "W1": { "instance_id": "W1", "part": {...}, "unit": "mm" }
      },
      "data": {
        "mapping": {
          "W1": { "end1": {...}, "end2": {...}, "length_mm": 300 }
        },
        "connector_positions": { "X1": { "x": 100, "y": 100 } },
        "cable_positions": {},
        "wire_anchors": {},
        "design_notes": [],
        "name": "Harness Name",
        "description": "..."
      }
    }

    Args:
        harness: The harness to convert

    Returns:
        Dictionary in Splice import format
    """
    bom: Dict[str, Any] = {}
    mapping: Dict[str, Any] = {}
    connector_positions: Dict[str, Dict[str, float]] = {}
    cable_positions: Dict[str, Dict[str, float]] = {}
    wire_anchors: Dict[str, Dict[str, float]] = {}
    design_notes: List[Dict[str, Any]] = []

    # Convert components to BOM items
    for component in harness.components:
        bom_item = component_to_bom_item(component)
        bom[component.designator] = bom_item

        # Add position data
        if component.position:
            position_data = {"x": component.position[0], "y": component.position[1]}

            if component.kind == ComponentType.CABLE:
                cable_positions[component.designator] = position_data
            else:
                connector_positions[component.designator] = position_data

    # Convert connections to mapping entries
    # For cable cores, we need to merge two connections into one mapping entry
    # with key format: {cable_designator}.{core_number}
    core_connections = {}  # Track partial cable core connections: key -> {connector_end, labels}
    wire_counter = 1

    for connection in harness.connections:
        # Check if this connection uses a cable core
        core_ref = None
        other_end = None

        if isinstance(connection.end1, CoreRef):
            core_ref = connection.end1
            other_end = connection.end2
        elif isinstance(connection.end2, CoreRef):
            core_ref = connection.end2
            other_end = connection.end1

        if core_ref:
            # Cable core connection - use format C1.1, C1.2, etc.
            wire_key = f"{core_ref.component.designator}.{core_ref.core}"

            # Check if we already have a partial connection for this core
            if wire_key in core_connections:
                # Merge the two connections - we now have both ends
                existing_data = core_connections[wire_key]

                # Build merged mapping entry with both connector ends
                mapping_entry = {}

                # Determine which end is end1 and which is end2
                # Use the existing end as end1, new end as end2
                mapping_entry["end1"] = existing_data["connector_end"]

                # Convert the other_end to mapping format
                if isinstance(other_end, PinRef):
                    mapping_entry["end2"] = {
                        "type": "connector_pin",
                        "connector_instance": other_end.component.designator,
                        "pin": other_end.pin,
                        "side": "left",
                        "terminal_instance": None,
                    }
                elif isinstance(other_end, FlyingLead):
                    mapping_entry["end2"] = {
                        "type": "flying_lead",
                        "termination_type": other_end.termination_type,
                    }
                    if other_end.strip_length_mm:
                        mapping_entry["end2"]["strip_length_mm"] = other_end.strip_length_mm

                # Merge labels
                if existing_data.get("label"):
                    mapping_entry["label_end1"] = existing_data["label"]
                if isinstance(connection.end1, CoreRef):
                    if connection.label_end2:
                        mapping_entry["label_end2"] = connection.label_end2
                else:
                    if connection.label_end1:
                        mapping_entry["label_end2"] = connection.label_end1

                # Add to final mapping
                mapping[wire_key] = mapping_entry
                del core_connections[wire_key]
            else:
                # First connection to this core - store the connector end
                connector_end_data = {}
                label = None

                if isinstance(other_end, PinRef):
                    connector_end_data = {
                        "type": "connector_pin",
                        "connector_instance": other_end.component.designator,
                        "pin": other_end.pin,
                        "side": "left",
                        "terminal_instance": None,
                    }
                    # Get label from the non-core end
                    if isinstance(connection.end1, CoreRef):
                        label = connection.label_end2
                    else:
                        label = connection.label_end1
                elif isinstance(other_end, FlyingLead):
                    connector_end_data = {
                        "type": "flying_lead",
                        "termination_type": other_end.termination_type,
                    }
                    if other_end.strip_length_mm:
                        connector_end_data["strip_length_mm"] = other_end.strip_length_mm

                core_connections[wire_key] = {
                    "connector_end": connector_end_data,
                    "label": label
                }
        else:
            # Regular wire connection - create wire BOM item
            wire_key = generate_wire_key(wire_counter)
            wire_counter += 1

            # Add wire to BOM
            if connection.wire is not None:
                wire_bom_item = wire_to_bom_item(wire_key, connection)
                bom[wire_key] = wire_bom_item

            # Add connection to mapping
            mapping_entry = connection_to_mapping_entry(connection)
            mapping[wire_key] = mapping_entry

    # Add any remaining partial cable core connections (only one end connected)
    for wire_key, data in core_connections.items():
        mapping[wire_key] = {
            "end1": data["connector_end"],
            "end2": None,
            "label_end1": data["label"],
            "label_end2": None,
        }

    # Convert design notes
    for note in harness.notes:
        design_note = {
            "id": str(uuid.uuid4()),
            "x": note["position"]["x"],
            "y": note["position"]["y"],
            "title": note.get("title", ""),
            "content": note.get("content", []),
        }
        design_notes.append(design_note)

    # Build the final structure
    return {
        "bom": bom,
        "data": {
            "mapping": mapping,
            "connector_positions": connector_positions,
            "cable_positions": cable_positions,
            "wire_anchors": wire_anchors,
            "design_notes": design_notes,
            "name": harness.name,
            "description": harness.description or "",
            "notes": None,
        },
    }
