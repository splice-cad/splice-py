"""
Tests for JSON export functionality.
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
from splice.export import harness_to_splice_format


class TestHarnessToSpliceFormat:
    """Tests for harness_to_splice_format function."""

    def test_export_basic_harness(self, harness_with_components):
        """Test exporting a basic harness."""
        harness, _, _, _ = harness_with_components
        data = harness_to_splice_format(harness)

        assert "bom" in data
        assert "data" in data
        assert "mapping" in data["data"]
        assert "connector_positions" in data["data"]
        assert "cable_positions" in data["data"]
        assert "wire_anchors" in data["data"]
        assert "design_notes" in data["data"]
        assert "bundle_labels" in data["data"]
        assert "label_settings" in data["data"]
        assert "name" in data["data"]
        assert "description" in data["data"]

    def test_export_includes_harness_name(self, harness_with_components):
        """Test that harness name is included in export."""
        harness, _, _, _ = harness_with_components
        data = harness_to_splice_format(harness)

        assert data["data"]["name"] == harness.name

    def test_export_includes_description(self):
        """Test that harness description is included in export."""
        harness = Harness("Test", "Test Description")
        harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-1",
            manufacturer="Test",
            positions=2,
        )
        data = harness_to_splice_format(harness)

        assert data["data"]["description"] == "Test Description"


class TestBomExport:
    """Tests for BOM export format."""

    def test_connector_in_bom(self, empty_harness):
        """Test that connectors appear in BOM."""
        empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="43650-0300",
            manufacturer="Molex",
            positions=3,
            position=(100, 200),
        )
        data = harness_to_splice_format(empty_harness)

        assert "X1" in data["bom"]
        bom_item = data["bom"]["X1"]
        assert bom_item["instance_id"] == "X1"
        assert bom_item["unit"] == "each"
        assert bom_item["part"]["kind"] == "connector"
        assert bom_item["part"]["mpn"] == "43650-0300"
        assert bom_item["part"]["manufacturer"] == "Molex"

    def test_cable_in_bom(self, empty_harness):
        """Test that cables appear in BOM."""
        empty_harness.add_component(
            kind=ComponentType.CABLE,
            mpn="CABLE-4C",
            manufacturer="Alpha Wire",
            cores=[
                CableCore(1, awg=18, color=WireColor.RED),
                CableCore(2, awg=18, color=WireColor.BLACK),
            ],
        )
        data = harness_to_splice_format(empty_harness)

        assert "C1" in data["bom"]
        bom_item = data["bom"]["C1"]
        assert bom_item["part"]["kind"] == "cable"

    def test_wire_in_bom(self, empty_harness, wire_red_20awg):
        """Test that wires appear in BOM."""
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
        empty_harness.connect(x1.pin(1), x2.pin(1), wire=wire_red_20awg)

        data = harness_to_splice_format(empty_harness)

        # Wire should be in BOM as W1
        assert "W1" in data["bom"]
        wire_item = data["bom"]["W1"]
        assert wire_item["part"]["kind"] == "wire"
        assert wire_item["part"]["mpn"] == "20AWG-RED"
        assert wire_item["unit"] == "ft"

    def test_connector_spec_in_bom(self, empty_harness):
        """Test that connector spec is included in BOM."""
        empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-1",
            manufacturer="Test",
            positions=4,
        )
        data = harness_to_splice_format(empty_harness)

        spec = data["bom"]["X1"]["part"]["spec"]
        # Spec is flat, not nested under "connector"
        assert spec["positions"] == 4

    def test_category_connector_in_bom(self, empty_harness):
        """Test that category connectors have category in spec."""
        empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="PS-001",
            manufacturer="PULS",
            category=ConnectorCategory.POWER_SUPPLY,
            positions=4,
        )
        data = harness_to_splice_format(empty_harness)

        spec = data["bom"]["PS1"]["part"]["spec"]
        # Spec is flat, not nested under "connector"
        assert spec["category"] == "power_supply"


class TestMappingExport:
    """Tests for connection mapping export format."""

    def test_pin_to_pin_connection_mapping(self, empty_harness, wire_red_20awg):
        """Test pin-to-pin connection in mapping."""
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
        empty_harness.connect(x1.pin(1), x2.pin(1), wire=wire_red_20awg, length_mm=150)

        data = harness_to_splice_format(empty_harness)
        mapping = data["data"]["mapping"]

        assert "W1" in mapping
        conn = mapping["W1"]
        assert conn["end1"]["type"] == "connector_pin"
        assert conn["end1"]["connector_instance"] == "X1"
        assert conn["end1"]["pin"] == 1
        assert conn["end2"]["type"] == "connector_pin"
        assert conn["end2"]["connector_instance"] == "X2"
        assert conn["end2"]["pin"] == 1
        assert conn["length_mm"] == 150

    def test_flying_lead_connection_mapping(self, empty_harness, wire_red_20awg):
        """Test flying lead connection in mapping."""
        x1 = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-1",
            manufacturer="Test",
            positions=2,
        )
        flying_lead = FlyingLead(termination_type=FlyingLeadType.TINNED)
        empty_harness.connect(x1.pin(1), flying_lead, wire=wire_red_20awg)

        data = harness_to_splice_format(empty_harness)
        mapping = data["data"]["mapping"]

        conn = mapping["W1"]
        assert conn["end1"]["type"] == "connector_pin"
        assert conn["end2"]["type"] == "flying_lead"
        assert conn["end2"]["termination_type"] == "tinned"

    def test_connection_labels_in_mapping(self, empty_harness, wire_red_20awg):
        """Test connection labels in mapping."""
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
            label_end2="PWR",
        )

        data = harness_to_splice_format(empty_harness)
        conn = data["data"]["mapping"]["W1"]

        assert conn["label_end1"] == "V+"
        assert conn["label_end2"] == "PWR"


class TestPositionsExport:
    """Tests for position data export."""

    def test_connector_positions(self, empty_harness):
        """Test connector positions are exported."""
        empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-1",
            manufacturer="Test",
            positions=2,
            position=(100.5, 200.5),
        )
        data = harness_to_splice_format(empty_harness)

        positions = data["data"]["connector_positions"]
        assert "X1" in positions
        assert positions["X1"]["x"] == 100.5
        assert positions["X1"]["y"] == 200.5

    def test_cable_positions(self, empty_harness):
        """Test cable positions are exported."""
        empty_harness.add_component(
            kind=ComponentType.CABLE,
            mpn="CABLE-1",
            manufacturer="Test",
            cores=[CableCore(1, awg=18, color=WireColor.RED)],
            position=(300, 400),
        )
        data = harness_to_splice_format(empty_harness)

        positions = data["data"]["cable_positions"]
        assert "C1" in positions
        assert positions["C1"]["x"] == 300
        assert positions["C1"]["y"] == 400

    def test_components_without_position(self, empty_harness):
        """Test components without position don't appear in positions."""
        empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-1",
            manufacturer="Test",
            positions=2,
            # No position specified
        )
        data = harness_to_splice_format(empty_harness)

        assert "X1" not in data["data"]["connector_positions"]


class TestDesignNotesExport:
    """Tests for design notes export."""

    def test_design_notes_export(self, empty_harness):
        """Test design notes are exported."""
        empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-1",
            manufacturer="Test",
            positions=2,
        )
        empty_harness.add_note(
            position=(100, 200),
            title="Test Note",
            content=["Line 1", "Line 2"],
        )

        data = harness_to_splice_format(empty_harness)
        notes = data["data"]["design_notes"]

        assert len(notes) == 1
        assert notes[0]["title"] == "Test Note"
        assert notes[0]["content"] == ["Line 1", "Line 2"]
        # Position is flat x/y, not nested under "position"
        assert notes[0]["x"] == 100
        assert notes[0]["y"] == 200


class TestLabelExportFormat:
    """Tests for bundle labels export format."""

    def test_bundle_labels_export(self, empty_harness):
        """Test bundle labels are exported correctly."""
        x1 = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-1",
            manufacturer="Test",
            positions=2,
        )
        empty_harness.add_label(
            text="J1",
            connector=x1,
            width_mm=12,
            background_color="#FFFF00",
        )

        data = harness_to_splice_format(empty_harness)
        labels = data["data"]["bundle_labels"]

        assert len(labels) == 1
        label_data = list(labels.values())[0]
        assert label_data["label_text"] == "J1"
        assert label_data["connector_instance_id"] == "X1"
        assert label_data["width_mm"] == 12
        assert label_data["background_color"] == "#FFFF00"
        assert label_data["is_auto_generated"] is False

    def test_label_settings_export(self, empty_harness):
        """Test label settings are exported."""
        empty_harness.label_settings.show_labels_on_canvas = False
        empty_harness.label_settings.default_width_mm = 15.0

        empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-1",
            manufacturer="Test",
            positions=2,
        )

        data = harness_to_splice_format(empty_harness)
        settings = data["data"]["label_settings"]

        assert settings["show_labels_on_canvas"] is False
        assert settings["default_width_mm"] == 15.0


class TestJsonOutput:
    """Tests for JSON string output."""

    def test_to_json_is_valid_json(self, harness_with_components):
        """Test that to_json() produces valid JSON."""
        harness, _, _, _ = harness_with_components
        json_str = harness.to_json()

        # Should not raise
        data = json.loads(json_str)
        assert isinstance(data, dict)

    def test_to_json_is_pretty_printed(self, harness_with_components):
        """Test that to_json() produces formatted JSON."""
        harness, _, _, _ = harness_with_components
        json_str = harness.to_json()

        # Pretty-printed JSON should have newlines
        assert "\n" in json_str

    def test_to_dict_matches_to_json(self, harness_with_components):
        """Test that to_dict() and to_json() produce equivalent structure."""
        harness, _, _, _ = harness_with_components

        dict_data = harness.to_dict()
        json_data = json.loads(harness.to_json())

        # Compare structure - UUIDs will differ between calls
        # So we check that both have the same keys and structure
        assert set(dict_data.keys()) == set(json_data.keys())
        assert set(dict_data["data"].keys()) == set(json_data["data"].keys())
        assert set(dict_data["bom"].keys()) == set(json_data["bom"].keys())


class TestSaveToFile:
    """Tests for saving harness to file."""

    def test_save_creates_file(self, harness_with_components, tmp_path):
        """Test that save() creates a file."""
        harness, _, _, _ = harness_with_components
        filepath = tmp_path / "test.json"

        harness.save(str(filepath))

        assert filepath.exists()

    def test_save_file_is_valid_json(self, harness_with_components, tmp_path):
        """Test that saved file contains valid JSON."""
        harness, _, _, _ = harness_with_components
        filepath = tmp_path / "test.json"

        harness.save(str(filepath))

        with open(filepath) as f:
            data = json.load(f)

        assert "bom" in data
        assert "data" in data

    def test_save_file_matches_to_dict(self, harness_with_components, tmp_path):
        """Test that saved file has same structure as to_dict() output."""
        harness, _, _, _ = harness_with_components
        filepath = tmp_path / "test.json"

        harness.save(str(filepath))

        with open(filepath) as f:
            file_data = json.load(f)

        dict_data = harness.to_dict()
        # Compare structure - UUIDs will differ between calls
        assert set(file_data.keys()) == set(dict_data.keys())
        assert set(file_data["data"].keys()) == set(dict_data["data"].keys())
        assert set(file_data["bom"].keys()) == set(dict_data["bom"].keys())
