"""
Tests for connection and termination classes.
"""

import pytest
from splice import (
    Harness,
    ComponentType,
    Wire,
    CableCore,
    FlyingLead,
    WireColor,
    FlyingLeadType,
)
from splice.connections import Connection, ConnectionEnd
from splice.components import PinRef, CoreRef


class TestFlyingLead:
    """Tests for FlyingLead class."""

    def test_create_bare_flying_lead(self):
        """Test creating a bare flying lead."""
        lead = FlyingLead(termination_type=FlyingLeadType.BARE)
        assert lead.termination_type == FlyingLeadType.BARE
        assert lead.strip_length_mm is None
        assert lead.tin_length_mm is None

    def test_create_tinned_flying_lead(self):
        """Test creating a tinned flying lead."""
        lead = FlyingLead(termination_type=FlyingLeadType.TINNED)
        assert lead.termination_type == FlyingLeadType.TINNED

    def test_create_heat_shrink_flying_lead(self):
        """Test creating a heat shrink flying lead."""
        lead = FlyingLead(termination_type=FlyingLeadType.HEAT_SHRINK)
        assert lead.termination_type == FlyingLeadType.HEAT_SHRINK

    def test_flying_lead_with_strip_length(self):
        """Test flying lead with strip length."""
        lead = FlyingLead(
            termination_type=FlyingLeadType.TINNED,
            strip_length_mm=5.0,
        )
        assert lead.strip_length_mm == 5.0

    def test_flying_lead_with_tin_length(self):
        """Test flying lead with tin length."""
        lead = FlyingLead(
            termination_type=FlyingLeadType.TINNED,
            tin_length_mm=3.0,
        )
        assert lead.tin_length_mm == 3.0

    def test_flying_lead_with_label(self):
        """Test flying lead with label."""
        lead = FlyingLead(
            termination_type=FlyingLeadType.BARE,
            label="GND",
        )
        assert lead.label == "GND"

    def test_flying_lead_default_type(self):
        """Test flying lead defaults to bare."""
        lead = FlyingLead()
        assert lead.termination_type == FlyingLeadType.BARE

    def test_flying_lead_string_type(self):
        """Test flying lead with string termination type."""
        lead = FlyingLead(termination_type="custom_type")
        assert lead.termination_type == "custom_type"

    def test_flying_lead_to_dict(self):
        """Test flying lead serialization."""
        lead = FlyingLead(
            termination_type=FlyingLeadType.TINNED,
            strip_length_mm=5.0,
            tin_length_mm=3.0,
            label="PWR",
        )
        data = lead.to_dict()

        assert data["type"] == "flying_lead"
        assert data["termination_type"] == "tinned"
        assert data["strip_length_mm"] == 5.0
        assert data["tin_length_mm"] == 3.0
        assert data["label"] == "PWR"

    def test_flying_lead_to_dict_minimal(self):
        """Test flying lead serialization with minimal data."""
        lead = FlyingLead(termination_type=FlyingLeadType.BARE)
        data = lead.to_dict()

        assert data["type"] == "flying_lead"
        assert data["termination_type"] == "bare"
        assert "strip_length_mm" not in data
        assert "tin_length_mm" not in data
        assert "label" not in data


class TestConnection:
    """Tests for Connection class."""

    def test_create_pin_to_pin_connection(self, empty_harness, wire_red_20awg):
        """Test creating a pin-to-pin connection."""
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

        conn = Connection(
            end1=x1.pin(1),
            end2=x2.pin(1),
            wire=wire_red_20awg,
            length_mm=100,
        )

        assert isinstance(conn.end1, PinRef)
        assert isinstance(conn.end2, PinRef)
        assert conn.wire == wire_red_20awg
        assert conn.length_mm == 100

    def test_create_pin_to_flying_lead_connection(
        self, empty_harness, wire_red_20awg, flying_lead_tinned
    ):
        """Test creating a pin-to-flying-lead connection."""
        x1 = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-1",
            manufacturer="Test",
            positions=2,
        )

        conn = Connection(
            end1=x1.pin(1),
            end2=flying_lead_tinned,
            wire=wire_red_20awg,
        )

        assert isinstance(conn.end1, PinRef)
        assert isinstance(conn.end2, FlyingLead)

    def test_create_core_to_pin_connection(self, empty_harness):
        """Test creating a cable-core-to-pin connection."""
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

        conn = Connection(
            end1=c1.core(1),
            end2=x1.pin(1),
            wire=None,  # Cable connections may not have wire
        )

        assert isinstance(conn.end1, CoreRef)
        assert isinstance(conn.end2, PinRef)

    def test_connection_with_labels(self, empty_harness, wire_red_20awg):
        """Test connection with endpoint labels."""
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

        conn = Connection(
            end1=x1.pin(1),
            end2=x2.pin(1),
            wire=wire_red_20awg,
            label_end1="V+",
            label_end2="PWR_IN",
        )

        assert conn.label_end1 == "V+"
        assert conn.label_end2 == "PWR_IN"

    def test_connection_with_deprecated_label(self, empty_harness, wire_red_20awg):
        """Test connection with deprecated single label."""
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

        conn = Connection(
            end1=x1.pin(1),
            end2=x2.pin(1),
            wire=wire_red_20awg,
            label="SIG",
        )

        assert conn.label == "SIG"

    def test_connection_to_dict(self, empty_harness, wire_red_20awg):
        """Test connection serialization."""
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

        conn = Connection(
            end1=x1.pin(1),
            end2=x2.pin(2),
            wire=wire_red_20awg,
            length_mm=150,
            label_end1="OUT",
            label_end2="IN",
        )
        data = conn.to_dict()

        assert "end1" in data
        assert "end2" in data
        assert "wire" in data
        assert data["length_mm"] == 150
        assert data["label_end1"] == "OUT"
        assert data["label_end2"] == "IN"

    def test_connection_to_dict_with_flying_lead(
        self, empty_harness, wire_red_20awg, flying_lead_tinned
    ):
        """Test connection serialization with flying lead."""
        x1 = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-1",
            manufacturer="Test",
            positions=2,
        )

        conn = Connection(
            end1=x1.pin(1),
            end2=flying_lead_tinned,
            wire=wire_red_20awg,
        )
        data = conn.to_dict()

        assert data["end1"]["type"] == "pin"
        assert data["end2"]["type"] == "flying_lead"
        assert data["end2"]["termination_type"] == "tinned"


class TestHarnessConnect:
    """Tests for Harness.connect() method."""

    def test_connect_creates_connection(self, empty_harness, wire_red_20awg):
        """Test that connect() creates and stores a connection."""
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

        conn = empty_harness.connect(x1.pin(1), x2.pin(1), wire=wire_red_20awg)

        assert conn in empty_harness.connections
        assert len(empty_harness.connections) == 1

    def test_connect_with_all_parameters(self, empty_harness, wire_red_20awg):
        """Test connect() with all parameters."""
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

        conn = empty_harness.connect(
            x1.pin(1),
            x2.pin(1),
            wire=wire_red_20awg,
            length_mm=200,
            label_end1="SRC",
            label_end2="DST",
        )

        assert conn.length_mm == 200
        assert conn.label_end1 == "SRC"
        assert conn.label_end2 == "DST"

    def test_connect_cable_core(self, harness_with_cable):
        """Test connecting cable cores."""
        harness, x1, x2, c1 = harness_with_cable

        # Connect x1 to cable core
        conn1 = harness.connect(x1.pin(1), c1.core(1))

        # Connect cable core to x2
        conn2 = harness.connect(c1.core(1), x2.pin(1))

        assert len(harness.connections) == 2
        assert conn1.wire is None  # Cable connections don't need wire
        assert conn2.wire is None

    def test_connect_multiple_wires(self, empty_harness, wire_red_20awg, wire_black_20awg):
        """Test creating multiple connections."""
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

        empty_harness.connect(x1.pin(1), x2.pin(1), wire=wire_red_20awg)
        empty_harness.connect(x1.pin(2), x2.pin(2), wire=wire_black_20awg)

        assert len(empty_harness.connections) == 2
