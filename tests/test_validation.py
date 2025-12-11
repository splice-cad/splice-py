"""
Tests for harness validation.
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
    ValidationResult,
)
from splice.validation import validate_harness


class TestValidationResult:
    """Tests for ValidationResult class."""

    def test_new_result_is_valid(self):
        """Test that new ValidationResult is valid by default."""
        result = ValidationResult()
        assert result.valid is True
        assert result.errors == []
        assert result.warnings == []

    def test_add_error_marks_invalid(self):
        """Test that adding an error marks result as invalid."""
        result = ValidationResult()
        result.add_error("Test error")

        assert result.valid is False
        assert "Test error" in result.errors

    def test_add_warning_keeps_valid(self):
        """Test that adding a warning keeps result valid."""
        result = ValidationResult()
        result.add_warning("Test warning")

        assert result.valid is True
        assert "Test warning" in result.warnings

    def test_multiple_errors(self):
        """Test multiple errors."""
        result = ValidationResult()
        result.add_error("Error 1")
        result.add_error("Error 2")

        assert len(result.errors) == 2
        assert result.valid is False


class TestEmptyHarnessValidation:
    """Tests for validating empty harnesses."""

    def test_empty_harness_is_invalid(self, empty_harness):
        """Test that an empty harness fails validation."""
        result = empty_harness.validate()

        assert result.valid is False
        assert any("no components" in e.lower() for e in result.errors)


class TestComponentValidation:
    """Tests for component validation."""

    def test_valid_connector(self, empty_harness):
        """Test that a valid connector passes validation."""
        empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-1",
            manufacturer="Test",
            positions=2,
        )
        result = empty_harness.validate()

        assert result.valid is True

    def test_connector_missing_mpn(self, empty_harness):
        """Test that connector with missing MPN fails validation."""
        empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="",  # Empty MPN
            manufacturer="Test",
            positions=2,
        )
        result = empty_harness.validate()

        assert result.valid is False
        assert any("mpn" in e.lower() for e in result.errors)

    def test_connector_missing_manufacturer(self, empty_harness):
        """Test that connector with missing manufacturer fails validation."""
        empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-1",
            manufacturer="",  # Empty manufacturer
            positions=2,
        )
        result = empty_harness.validate()

        assert result.valid is False
        assert any("manufacturer" in e.lower() for e in result.errors)

    def test_connector_invalid_positions(self, empty_harness):
        """Test that connector with invalid positions fails validation."""
        empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-1",
            manufacturer="Test",
            positions=0,  # Invalid
        )
        result = empty_harness.validate()

        assert result.valid is False
        assert any("positions" in e.lower() for e in result.errors)

    def test_cable_without_cores(self, empty_harness):
        """Test that cable without cores fails validation."""
        empty_harness.add_component(
            kind=ComponentType.CABLE,
            mpn="CABLE-1",
            manufacturer="Test",
            cores=[],  # No cores
        )
        result = empty_harness.validate()

        assert result.valid is False
        assert any("no cores" in e.lower() for e in result.errors)

    def test_cable_duplicate_core_numbers(self, empty_harness):
        """Test that cable with duplicate core numbers fails validation."""
        empty_harness.add_component(
            kind=ComponentType.CABLE,
            mpn="CABLE-1",
            manufacturer="Test",
            cores=[
                CableCore(1, awg=18, color=WireColor.RED),
                CableCore(1, awg=18, color=WireColor.BLACK),  # Duplicate
            ],
        )
        result = empty_harness.validate()

        assert result.valid is False
        assert any("duplicate core" in e.lower() for e in result.errors)


class TestDuplicateDesignatorValidation:
    """Tests for duplicate designator validation."""

    def test_duplicate_designator_fails(self, empty_harness):
        """Test that duplicate designators are rejected at add time."""
        empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-1",
            manufacturer="Test",
            positions=2,
            designator="J1",
        )
        # Duplicate designator is rejected when adding the component
        with pytest.raises(ValueError, match="already registered"):
            empty_harness.add_component(
                kind=ComponentType.CONNECTOR,
                mpn="CONN-2",
                manufacturer="Test",
                positions=2,
                designator="J1",  # Duplicate
            )

    def test_unique_designators_pass(self, empty_harness):
        """Test that unique designators pass validation."""
        empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-1",
            manufacturer="Test",
            positions=2,
            designator="J1",
        )
        empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-2",
            manufacturer="Test",
            positions=2,
            designator="J2",
        )
        result = empty_harness.validate()

        assert result.valid is True


class TestConnectionValidation:
    """Tests for connection validation."""

    def test_valid_connection(self, empty_harness, wire_red_20awg):
        """Test that a valid connection passes validation."""
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

        result = empty_harness.validate()
        assert result.valid is True

    def test_connection_invalid_pin_too_high(self, empty_harness, wire_red_20awg):
        """Test that connection to invalid pin fails validation."""
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
        # Connect to pin 5 on a 2-position connector
        empty_harness.connect(x1.pin(5), x2.pin(1), wire=wire_red_20awg)

        result = empty_harness.validate()
        assert result.valid is False
        assert any("invalid pin" in e.lower() for e in result.errors)

    def test_connection_invalid_pin_zero(self, empty_harness, wire_red_20awg):
        """Test that connection to pin 0 fails validation."""
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
        empty_harness.connect(x1.pin(0), x2.pin(1), wire=wire_red_20awg)

        result = empty_harness.validate()
        assert result.valid is False

    def test_connection_invalid_cable_core(self, empty_harness):
        """Test that connection to invalid cable core fails validation."""
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
        # Connect to core 5 on a 1-core cable
        empty_harness.connect(x1.pin(1), c1.core(5))

        result = empty_harness.validate()
        assert result.valid is False
        assert any("invalid core" in e.lower() for e in result.errors)


class TestCableConnectionValidation:
    """Tests for cable core connection validation."""

    def test_cable_core_max_two_connections(self, harness_with_cable):
        """Test that cable cores can have at most 2 connections."""
        harness, x1, x2, c1 = harness_with_cable

        # Valid: one connection on each side
        harness.connect(x1.pin(1), c1.core(1))
        harness.connect(c1.core(1), x2.pin(1))

        result = harness.validate()
        assert result.valid is True

    def test_cable_core_too_many_connections(self, empty_harness):
        """Test that cable core with > 2 connections fails validation."""
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
        x3 = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-3",
            manufacturer="Test",
            positions=3,
        )
        c1 = empty_harness.add_component(
            kind=ComponentType.CABLE,
            mpn="CABLE-1",
            manufacturer="Test",
            cores=[CableCore(1, awg=18, color=WireColor.RED)],
        )

        # Three connections to same core - invalid
        empty_harness.connect(x1.pin(1), c1.core(1))
        empty_harness.connect(c1.core(1), x2.pin(1))
        empty_harness.connect(c1.core(1), x3.pin(1))

        result = empty_harness.validate()
        assert result.valid is False
        assert any("maximum is 2" in e.lower() for e in result.errors)


class TestUnconnectedWarnings:
    """Tests for unconnected pin/core warnings."""

    def test_unconnected_pins_warning(self, empty_harness, wire_red_20awg):
        """Test that unconnected pins produce warnings."""
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
        # Only connect pin 1, leave pins 2 and 3 unconnected
        empty_harness.connect(x1.pin(1), x2.pin(1), wire=wire_red_20awg)

        result = empty_harness.validate()
        assert result.valid is True  # Still valid, just has warnings
        assert len(result.warnings) > 0
        assert any("unconnected pins" in w.lower() for w in result.warnings)

    def test_unconnected_cable_cores_warning(self, empty_harness):
        """Test that unconnected cable cores produce warnings."""
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
            cores=[
                CableCore(1, awg=18, color=WireColor.RED),
                CableCore(2, awg=18, color=WireColor.BLACK),
            ],
        )
        # Only connect core 1, leave core 2 unconnected
        empty_harness.connect(x1.pin(1), c1.core(1))

        result = empty_harness.validate()
        assert result.valid is True
        assert any("unconnected cores" in w.lower() for w in result.warnings)

    def test_fully_connected_no_warnings(self, empty_harness, wire_red_20awg, wire_black_20awg):
        """Test that fully connected harness has no unconnected warnings."""
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
        empty_harness.connect(x1.pin(2), x2.pin(2), wire=wire_black_20awg)

        result = empty_harness.validate()
        assert result.valid is True
        # Should have no "unconnected" warnings
        unconnected_warnings = [w for w in result.warnings if "unconnected" in w.lower()]
        assert len(unconnected_warnings) == 0


class TestMultiplePinUsageWarning:
    """Tests for multiple pin usage warnings."""

    def test_pin_used_twice_warning(self, empty_harness, wire_red_20awg, wire_black_20awg):
        """Test that using same pin twice produces a warning."""
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
        x3 = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-3",
            manufacturer="Test",
            positions=2,
        )

        # Connect x1.pin(1) to two different destinations
        empty_harness.connect(x1.pin(1), x2.pin(1), wire=wire_red_20awg)
        empty_harness.connect(x1.pin(1), x3.pin(1), wire=wire_black_20awg)

        result = empty_harness.validate()
        assert result.valid is True  # Valid but with warning
        assert any("multiple connections" in w.lower() for w in result.warnings)


class TestComplexHarnessValidation:
    """Tests for complex harness validation scenarios."""

    def test_complete_valid_harness(self, empty_harness):
        """Test a complete, valid harness passes validation."""
        # Add power supply
        ps1 = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="PS-001",
            manufacturer="PULS",
            positions=4,
        )

        # Add circuit breaker
        cb1 = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CB-001",
            manufacturer="Phoenix",
            positions=2,
        )

        # Add output terminal
        x1 = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="TERM-001",
            manufacturer="Phoenix",
            positions=4,
        )

        # Wires
        wire_red = Wire(mpn="18AWG-RED", manufacturer="Generic", awg=18, color=WireColor.RED)
        wire_black = Wire(mpn="18AWG-BLK", manufacturer="Generic", awg=18, color=WireColor.BLACK)

        # Connections
        empty_harness.connect(ps1.pin(1), cb1.pin(1), wire=wire_red, length_mm=200)
        empty_harness.connect(cb1.pin(2), x1.pin(1), wire=wire_red, length_mm=150)
        empty_harness.connect(ps1.pin(2), x1.pin(2), wire=wire_black, length_mm=250)

        result = empty_harness.validate()
        assert result.valid is True

    def test_harness_with_flying_leads(self, empty_harness, wire_red_20awg):
        """Test harness with flying leads passes validation."""
        x1 = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-1",
            manufacturer="Test",
            positions=2,
        )

        flying_lead = FlyingLead(termination_type=FlyingLeadType.TINNED)

        empty_harness.connect(x1.pin(1), flying_lead, wire=wire_red_20awg)

        result = empty_harness.validate()
        assert result.valid is True
