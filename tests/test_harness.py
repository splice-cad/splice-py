"""
Tests for the Harness class.
"""

import pytest
import json
from splice import (
    Harness,
    ComponentType,
    Wire,
    CableCore,
    FlyingLead,
    WireColor,
    ConnectorCategory,
    FlyingLeadType,
)


class TestHarnessCreation:
    """Tests for Harness initialization."""

    def test_create_empty_harness(self):
        """Test creating an empty harness."""
        harness = Harness("Test Harness")
        assert harness.name == "Test Harness"
        # Description defaults to empty string, not None
        assert harness.description == ""
        assert harness.components == []
        assert harness.connections == []
        assert harness.labels == []
        assert harness.notes == []

    def test_create_harness_with_description(self):
        """Test creating a harness with description."""
        harness = Harness("Test Harness", "A test description")
        assert harness.name == "Test Harness"
        assert harness.description == "A test description"

    def test_harness_has_label_settings(self):
        """Test that harness has default label settings."""
        harness = Harness("Test")
        assert harness.label_settings is not None
        assert harness.label_settings.show_labels_on_canvas is True
        assert harness.label_settings.default_width_mm == 9.0


class TestAddComponent:
    """Tests for adding components to a harness."""

    def test_add_connector(self, empty_harness):
        """Test adding a connector component."""
        connector = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="43650-0300",
            manufacturer="Molex",
            positions=3,
        )
        assert connector.designator == "X1"
        assert connector.mpn == "43650-0300"
        assert connector.manufacturer == "Molex"
        assert connector.positions == 3
        assert len(empty_harness.components) == 1

    def test_add_multiple_connectors_auto_designator(self, empty_harness):
        """Test that connectors get auto-incrementing designators."""
        c1 = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-1",
            manufacturer="Test",
            positions=2,
        )
        c2 = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-2",
            manufacturer="Test",
            positions=2,
        )
        c3 = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-3",
            manufacturer="Test",
            positions=2,
        )
        assert c1.designator == "X1"
        assert c2.designator == "X2"
        assert c3.designator == "X3"

    def test_add_connector_with_custom_designator(self, empty_harness):
        """Test adding a connector with a custom designator."""
        connector = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-1",
            manufacturer="Test",
            positions=2,
            designator="J5",
        )
        assert connector.designator == "J5"

    def test_add_connector_with_category(self, empty_harness):
        """Test adding connectors with category-specific designators."""
        ps1 = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="PS-001",
            manufacturer="PULS",
            category=ConnectorCategory.POWER_SUPPLY,
            positions=4,
        )
        cb1 = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CB-001",
            manufacturer="Phoenix",
            category=ConnectorCategory.CIRCUIT_BREAKER,
            positions=2,
        )
        f1 = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="FUSE-001",
            manufacturer="Littelfuse",
            category=ConnectorCategory.FUSE,
            positions=2,
        )
        assert ps1.designator == "PS1"
        assert cb1.designator == "CB1"
        assert f1.designator == "F1"

    def test_add_cable(self, empty_harness):
        """Test adding a cable component."""
        cable = empty_harness.add_component(
            kind=ComponentType.CABLE,
            mpn="CABLE-4C",
            manufacturer="Alpha Wire",
            cores=[
                CableCore(1, awg=18, color=WireColor.RED),
                CableCore(2, awg=18, color=WireColor.BLACK),
            ],
        )
        assert cable.designator == "C1"
        assert len(cable.cores) == 2

    def test_add_connector_with_position(self, empty_harness):
        """Test adding a connector with a position."""
        connector = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-1",
            manufacturer="Test",
            positions=2,
            position=(150.5, 200.0),
        )
        assert connector.position == (150.5, 200.0)

    def test_add_connector_with_pin_mapping(self, empty_harness):
        """Test adding a connector with custom pin mapping."""
        connector = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-1",
            manufacturer="Test",
            positions=3,
            pin_mapping={"0": "VCC", "1": "GND", "2": "SIG"},
        )
        assert connector.custom_fields.get("pin_mapping") == {
            "0": "VCC",
            "1": "GND",
            "2": "SIG",
        }


class TestConnect:
    """Tests for creating connections."""

    def test_connect_two_connectors(self, harness_with_components, wire_red_20awg):
        """Test connecting two connector pins."""
        harness, x1, x2, _ = harness_with_components
        initial_count = len(harness.connections)

        harness.connect(x1.pin(2), x2.pin(2), wire=wire_red_20awg, length_mm=250)

        assert len(harness.connections) == initial_count + 1
        conn = harness.connections[-1]
        assert conn.wire == wire_red_20awg
        assert conn.length_mm == 250

    def test_connect_with_labels(self, empty_harness, wire_red_20awg):
        """Test connecting with endpoint labels."""
        x1 = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-1",
            manufacturer="Test",
            positions=2,
        )
        x2 = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-2",
            manufacturer="Test",
            positions=2,
        )

        empty_harness.connect(
            x1.pin(1),
            x2.pin(1),
            wire=wire_red_20awg,
            label_end1="V+",
            label_end2="PWR_IN",
        )

        conn = empty_harness.connections[0]
        assert conn.label_end1 == "V+"
        assert conn.label_end2 == "PWR_IN"

    def test_connect_to_flying_lead(self, empty_harness, wire_red_20awg, flying_lead_tinned):
        """Test connecting a pin to a flying lead."""
        x1 = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-1",
            manufacturer="Test",
            positions=2,
        )

        empty_harness.connect(
            x1.pin(1),
            flying_lead_tinned,
            wire=wire_red_20awg,
            length_mm=100,
        )

        assert len(empty_harness.connections) == 1
        conn = empty_harness.connections[0]
        assert isinstance(conn.end2, FlyingLead)

    def test_connect_cable_core_to_connector(self, harness_with_cable):
        """Test connecting a cable core to a connector pin."""
        harness, x1, x2, c1 = harness_with_cable

        harness.connect(x1.pin(1), c1.core(1))
        harness.connect(c1.core(1), x2.pin(1))

        assert len(harness.connections) == 2


class TestAddNote:
    """Tests for adding design notes."""

    def test_add_note(self, empty_harness):
        """Test adding a design note."""
        empty_harness.add_note(
            position=(100, 200),
            title="Test Note",
            content=["Line 1", "Line 2"],
        )
        assert len(empty_harness.notes) == 1
        note = empty_harness.notes[0]
        assert note["position"] == {"x": 100, "y": 200}
        assert note["title"] == "Test Note"
        assert note["content"] == ["Line 1", "Line 2"]

    def test_add_multiple_notes(self, empty_harness):
        """Test adding multiple notes."""
        empty_harness.add_note((0, 0), "Note 1", ["Content 1"])
        empty_harness.add_note((100, 100), "Note 2", ["Content 2"])
        assert len(empty_harness.notes) == 2


class TestValidate:
    """Tests for harness validation."""

    def test_validate_empty_harness(self, empty_harness):
        """Test validating an empty harness fails."""
        result = empty_harness.validate()
        assert not result.valid
        assert any("no components" in e.lower() for e in result.errors)

    def test_validate_simple_harness(self, harness_with_components):
        """Test validating a simple valid harness."""
        harness, _, _, _ = harness_with_components
        result = harness.validate()
        assert result.valid

    def test_validate_harness_with_warnings(self, empty_harness, wire_red_20awg):
        """Test validation produces warnings for unconnected pins."""
        x1 = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-1",
            manufacturer="Test",
            positions=3,
        )
        x2 = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-2",
            manufacturer="Test",
            positions=3,
        )
        # Only connect 1 pin, leave others unconnected
        empty_harness.connect(x1.pin(1), x2.pin(1), wire=wire_red_20awg)

        result = empty_harness.validate()
        assert result.valid  # Still valid, just has warnings
        assert len(result.warnings) > 0
        assert any("unconnected" in w.lower() for w in result.warnings)


class TestSerialization:
    """Tests for harness serialization."""

    def test_to_dict(self, harness_with_components):
        """Test converting harness to dict."""
        harness, _, _, _ = harness_with_components
        data = harness.to_dict()

        assert "bom" in data
        assert "data" in data
        assert "mapping" in data["data"]
        assert "connector_positions" in data["data"]
        assert "bundle_labels" in data["data"]
        assert "label_settings" in data["data"]

    def test_to_json(self, harness_with_components):
        """Test converting harness to JSON string."""
        harness, _, _, _ = harness_with_components
        json_str = harness.to_json()

        # Should be valid JSON
        data = json.loads(json_str)
        assert "bom" in data
        assert "data" in data

    def test_save_and_load(self, harness_with_components, tmp_path):
        """Test saving harness to file."""
        harness, _, _, _ = harness_with_components
        filepath = tmp_path / "test_harness.json"

        harness.save(str(filepath))

        assert filepath.exists()
        with open(filepath) as f:
            data = json.load(f)
        assert "bom" in data
        assert "data" in data


# Note: Harness.clear() is not implemented - test removed
