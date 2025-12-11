"""
Tests for label classes and harness label methods.
"""

import pytest
from splice import (
    Harness,
    ComponentType,
    CableCore,
    WireColor,
    BundleLabel,
    LabelSettings,
)


class TestBundleLabel:
    """Tests for BundleLabel class."""

    def test_create_basic_label(self):
        """Test creating a basic bundle label."""
        label = BundleLabel(label_text="J1")
        assert label.label_text == "J1"
        assert label.is_auto_generated is False
        assert label.connector_instance_id is None
        assert label.cable_instance_id is None
        assert label.id is not None  # Should auto-generate UUID

    def test_label_default_values(self):
        """Test label default values."""
        label = BundleLabel(label_text="TEST")
        assert label.width_mm == 9.0
        assert label.font_size == 10.0
        assert label.text_color == "#000000"
        assert label.background_color == "#FFFFFF"
        assert label.wire_keys == []
        assert label.cable_end is None

    def test_label_with_custom_styling(self):
        """Test label with custom styling."""
        label = BundleLabel(
            label_text="WARNING",
            width_mm=15.0,
            font_size=12.0,
            text_color="#FFFFFF",
            background_color="#FF0000",
        )
        assert label.width_mm == 15.0
        assert label.font_size == 12.0
        assert label.text_color == "#FFFFFF"
        assert label.background_color == "#FF0000"

    def test_label_with_connector(self):
        """Test label attached to connector."""
        label = BundleLabel(
            label_text="PWR",
            connector_instance_id="X1",
        )
        assert label.connector_instance_id == "X1"
        assert label.cable_instance_id is None

    def test_label_with_cable(self):
        """Test label attached to cable."""
        label = BundleLabel(
            label_text="CTRL",
            cable_instance_id="C1",
            cable_end="both",
        )
        assert label.cable_instance_id == "C1"
        assert label.connector_instance_id is None
        assert label.cable_end == "both"

    def test_label_with_wire_keys(self):
        """Test label with specific wire keys."""
        label = BundleLabel(
            label_text="SIGNAL",
            connector_instance_id="X1",
            wire_keys=["W1", "W2", "W3"],
        )
        assert label.wire_keys == ["W1", "W2", "W3"]

    def test_label_unique_ids(self):
        """Test that labels get unique IDs."""
        label1 = BundleLabel(label_text="A")
        label2 = BundleLabel(label_text="B")
        assert label1.id != label2.id


class TestLabelSettings:
    """Tests for LabelSettings class."""

    def test_default_settings(self):
        """Test default label settings."""
        settings = LabelSettings()
        assert settings.show_labels_on_canvas is True
        assert settings.default_width_mm == 9.0

    def test_custom_settings(self):
        """Test custom label settings."""
        settings = LabelSettings(
            show_labels_on_canvas=False,
            default_width_mm=12.0,
        )
        assert settings.show_labels_on_canvas is False
        assert settings.default_width_mm == 12.0


class TestHarnessAddLabel:
    """Tests for Harness.add_label() method."""

    def test_add_label_to_connector(self, empty_harness):
        """Test adding a label to a connector."""
        x1 = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-1",
            manufacturer="Test",
            positions=2,
        )

        label = empty_harness.add_label(
            text="J1",
            connector=x1,
        )

        assert label in empty_harness.labels
        assert label.label_text == "J1"
        assert label.connector_instance_id == "X1"
        assert label.is_auto_generated is False

    def test_add_label_to_cable(self, empty_harness):
        """Test adding a label to a cable."""
        c1 = empty_harness.add_component(
            kind=ComponentType.CABLE,
            mpn="CABLE-1",
            manufacturer="Test",
            cores=[CableCore(1, awg=18, color=WireColor.RED)],
        )

        label = empty_harness.add_label(
            text="CTRL CABLE",
            cable=c1,
            cable_end="both",
        )

        assert label.cable_instance_id == "C1"
        assert label.cable_end == "both"

    def test_add_label_auto_designator(self, empty_harness):
        """Test adding a label with auto-generated designator."""
        x1 = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-1",
            manufacturer="Test",
            positions=2,
        )

        label = empty_harness.add_label(
            text="",
            connector=x1,
            auto_designator=True,
        )

        assert label.label_text == "X1"
        assert label.is_auto_generated is True

    def test_add_label_with_styling(self, empty_harness):
        """Test adding a label with custom styling."""
        x1 = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-1",
            manufacturer="Test",
            positions=2,
        )

        label = empty_harness.add_label(
            text="DANGER",
            connector=x1,
            width_mm=20.0,
            font_size=14.0,
            text_color="#FFFFFF",
            background_color="#FF0000",
        )

        assert label.width_mm == 20.0
        assert label.font_size == 14.0
        assert label.text_color == "#FFFFFF"
        assert label.background_color == "#FF0000"

    def test_add_label_uses_default_width(self, empty_harness):
        """Test that label uses default width from settings."""
        empty_harness.label_settings.default_width_mm = 15.0

        x1 = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-1",
            manufacturer="Test",
            positions=2,
        )

        label = empty_harness.add_label(text="TEST", connector=x1)

        assert label.width_mm == 15.0

    def test_add_label_with_wire_keys(self, empty_harness):
        """Test adding a label with specific wire keys."""
        x1 = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-1",
            manufacturer="Test",
            positions=3,
        )

        label = empty_harness.add_label(
            text="PWR",
            connector=x1,
            wire_keys=["W1", "W2"],
        )

        assert label.wire_keys == ["W1", "W2"]

    def test_add_label_requires_connector_or_cable(self, empty_harness):
        """Test that add_label raises error if neither connector nor cable specified."""
        with pytest.raises(ValueError, match="connector.*cable"):
            empty_harness.add_label(text="TEST")

    def test_add_label_rejects_both_connector_and_cable(self, empty_harness):
        """Test that add_label raises error if both connector and cable specified."""
        x1 = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-1",
            manufacturer="Test",
            positions=2,
        )
        c1 = empty_harness.add_component(
            kind=ComponentType.CABLE,
            mpn="CABLE-1",
            manufacturer="Test",
            cores=[CableCore(1, awg=18, color=WireColor.RED)],
        )

        with pytest.raises(ValueError, match="both"):
            empty_harness.add_label(text="TEST", connector=x1, cable=c1)

    def test_add_multiple_labels_to_same_connector(self, empty_harness):
        """Test adding multiple labels to the same connector."""
        x1 = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-1",
            manufacturer="Test",
            positions=2,
        )

        label1 = empty_harness.add_label(text="J1", connector=x1)
        label2 = empty_harness.add_label(text="POWER INPUT", connector=x1)

        assert len(empty_harness.labels) == 2
        assert label1.id != label2.id


class TestHarnessRemoveLabel:
    """Tests for Harness.remove_label() method."""

    def test_remove_label(self, empty_harness):
        """Test removing a label."""
        x1 = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-1",
            manufacturer="Test",
            positions=2,
        )
        label = empty_harness.add_label(text="TEST", connector=x1)

        assert len(empty_harness.labels) == 1
        empty_harness.remove_label(label)
        assert len(empty_harness.labels) == 0

    def test_remove_nonexistent_label_raises(self, empty_harness):
        """Test that removing a non-existent label raises error."""
        label = BundleLabel(label_text="FAKE")

        with pytest.raises(ValueError, match="not found"):
            empty_harness.remove_label(label)


class TestHarnessGetLabels:
    """Tests for Harness.get_labels() method."""

    def test_get_all_labels(self, empty_harness):
        """Test getting all labels."""
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

        empty_harness.add_label(text="L1", connector=x1)
        empty_harness.add_label(text="L2", connector=x2)

        labels = empty_harness.get_labels()
        assert len(labels) == 2

    def test_get_labels_by_connector(self, empty_harness):
        """Test filtering labels by connector."""
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

        empty_harness.add_label(text="L1-A", connector=x1)
        empty_harness.add_label(text="L1-B", connector=x1)
        empty_harness.add_label(text="L2", connector=x2)

        x1_labels = empty_harness.get_labels(connector=x1)
        assert len(x1_labels) == 2
        assert all(l.connector_instance_id == "X1" for l in x1_labels)

    def test_get_labels_by_cable(self, empty_harness):
        """Test filtering labels by cable."""
        x1 = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-1",
            manufacturer="Test",
            positions=2,
        )
        c1 = empty_harness.add_component(
            kind=ComponentType.CABLE,
            mpn="CABLE-1",
            manufacturer="Test",
            cores=[CableCore(1, awg=18, color=WireColor.RED)],
        )

        empty_harness.add_label(text="CONN", connector=x1)
        empty_harness.add_label(text="CABLE", cable=c1)

        cable_labels = empty_harness.get_labels(cable=c1)
        assert len(cable_labels) == 1
        assert cable_labels[0].label_text == "CABLE"

    def test_get_labels_empty_result(self, empty_harness):
        """Test get_labels returns empty list when no matches."""
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

        empty_harness.add_label(text="L1", connector=x1)

        x2_labels = empty_harness.get_labels(connector=x2)
        assert x2_labels == []


class TestLabelExport:
    """Tests for label serialization in harness export."""

    def test_labels_in_export(self, empty_harness):
        """Test that labels are included in harness export."""
        x1 = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-1",
            manufacturer="Test",
            positions=2,
        )

        empty_harness.add_label(
            text="J1",
            connector=x1,
            width_mm=12.0,
            background_color="#FFFF00",
        )

        data = empty_harness.to_dict()

        assert "bundle_labels" in data["data"]
        labels = data["data"]["bundle_labels"]
        assert len(labels) == 1

        # Get the label by its ID
        label_data = list(labels.values())[0]
        assert label_data["label_text"] == "J1"
        assert label_data["connector_instance_id"] == "X1"
        assert label_data["width_mm"] == 12.0
        assert label_data["background_color"] == "#FFFF00"

    def test_label_settings_in_export(self, empty_harness):
        """Test that label settings are included in harness export."""
        empty_harness.label_settings.show_labels_on_canvas = False
        empty_harness.label_settings.default_width_mm = 15.0

        # Need at least one component for valid harness
        empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-1",
            manufacturer="Test",
            positions=2,
        )

        data = empty_harness.to_dict()

        assert "label_settings" in data["data"]
        settings = data["data"]["label_settings"]
        assert settings["show_labels_on_canvas"] is False
        assert settings["default_width_mm"] == 15.0

    def test_cable_label_export(self, empty_harness):
        """Test that cable labels export correctly."""
        c1 = empty_harness.add_component(
            kind=ComponentType.CABLE,
            mpn="CABLE-1",
            manufacturer="Test",
            cores=[CableCore(1, awg=18, color=WireColor.RED)],
        )

        empty_harness.add_label(
            text="POWER CABLE",
            cable=c1,
            cable_end="both",
        )

        data = empty_harness.to_dict()
        label_data = list(data["data"]["bundle_labels"].values())[0]

        assert label_data["cable_instance_id"] == "C1"
        assert label_data["cable_end"] == "both"
        assert "connector_instance_id" not in label_data
