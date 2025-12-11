"""
Tests for component classes.
"""

import pytest
from splice import (
    Harness,
    ComponentType,
    Wire,
    CableCore,
    WireColor,
    ConnectorCategory,
    ConnectorGender,
    ConnectorShape,
    ConductorType,
)
from splice.components import (
    ComponentInstance,
    ConnectorInstance,
    CableInstance,
    WireInstance,
    PinRef,
    CoreRef,
)


class TestPinRef:
    """Tests for PinRef class."""

    def test_create_pin_ref(self, empty_harness):
        """Test creating a pin reference."""
        connector = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-1",
            manufacturer="Test",
            positions=3,
        )
        pin_ref = connector.pin(1)

        assert isinstance(pin_ref, PinRef)
        assert pin_ref.component == connector
        assert pin_ref.pin == 1

    def test_pin_ref_repr(self, empty_harness):
        """Test PinRef string representation."""
        connector = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-1",
            manufacturer="Test",
            positions=3,
        )
        pin_ref = connector.pin(2)
        assert "X1" in repr(pin_ref)
        assert "2" in repr(pin_ref)


class TestCoreRef:
    """Tests for CoreRef class."""

    def test_create_core_ref(self, empty_harness):
        """Test creating a core reference."""
        cable = empty_harness.add_component(
            kind=ComponentType.CABLE,
            mpn="CABLE-1",
            manufacturer="Test",
            cores=[
                CableCore(1, awg=18, color=WireColor.RED),
                CableCore(2, awg=18, color=WireColor.BLACK),
            ],
        )
        core_ref = cable.core(1)

        assert isinstance(core_ref, CoreRef)
        assert core_ref.component == cable
        assert core_ref.core == 1

    def test_core_ref_repr(self, empty_harness):
        """Test CoreRef string representation."""
        cable = empty_harness.add_component(
            kind=ComponentType.CABLE,
            mpn="CABLE-1",
            manufacturer="Test",
            cores=[CableCore(1, awg=18, color=WireColor.RED)],
        )
        core_ref = cable.core(1)
        assert "C1" in repr(core_ref)
        assert "1" in repr(core_ref)


class TestConnectorInstance:
    """Tests for ConnectorInstance class."""

    def test_create_basic_connector(self, empty_harness):
        """Test creating a basic connector."""
        connector = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="43650-0300",
            manufacturer="Molex",
            positions=3,
        )
        assert isinstance(connector, ConnectorInstance)
        assert connector.kind == ComponentType.CONNECTOR
        assert connector.positions == 3
        assert connector.designator == "X1"

    def test_connector_with_gender(self, empty_harness):
        """Test connector with gender specification."""
        connector = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-M",
            manufacturer="Test",
            positions=2,
            gender=ConnectorGender.MALE,
        )
        assert connector.gender == ConnectorGender.MALE

    def test_connector_with_shape(self, empty_harness):
        """Test connector with shape specification."""
        connector = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-CIRC",
            manufacturer="Test",
            positions=4,
            shape=ConnectorShape.CIRCULAR,
        )
        assert connector.shape == ConnectorShape.CIRCULAR

    def test_connector_with_category_enum(self, empty_harness):
        """Test connector with category enum."""
        connector = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CB-001",
            manufacturer="Phoenix",
            positions=2,
            category=ConnectorCategory.CIRCUIT_BREAKER,
        )
        assert connector.category == ConnectorCategory.CIRCUIT_BREAKER.value
        assert connector.designator == "CB1"

    def test_connector_with_category_string(self, empty_harness):
        """Test connector with category as string."""
        connector = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CUSTOM-001",
            manufacturer="Test",
            positions=2,
            category="custom_category",
        )
        assert connector.category == "custom_category"

    def test_connector_to_dict(self, empty_harness):
        """Test connector serialization."""
        connector = empty_harness.add_component(
            kind=ComponentType.CONNECTOR,
            mpn="CONN-1",
            manufacturer="Test",
            positions=3,
            position=(100, 200),
            gender=ConnectorGender.FEMALE,
            shape=ConnectorShape.RECTANGULAR,
        )
        data = connector.to_dict()

        assert data["kind"] == "connector"
        assert data["mpn"] == "CONN-1"
        assert data["manufacturer"] == "Test"
        assert data["positions"] == 3
        assert data["position"] == {"x": 100, "y": 200}
        assert data["contact_gender"] == "female"
        assert data["shape"] == "rectangular"


class TestCableInstance:
    """Tests for CableInstance class."""

    def test_create_basic_cable(self, empty_harness):
        """Test creating a basic cable."""
        cable = empty_harness.add_component(
            kind=ComponentType.CABLE,
            mpn="CABLE-4C",
            manufacturer="Alpha Wire",
            cores=[
                CableCore(1, awg=18, color=WireColor.RED),
                CableCore(2, awg=18, color=WireColor.BLACK),
            ],
        )
        assert isinstance(cable, CableInstance)
        assert cable.kind == ComponentType.CABLE
        assert cable.designator == "C1"
        assert len(cable.cores) == 2

    def test_cable_multiple_auto_designators(self, empty_harness):
        """Test multiple cables get unique designators."""
        c1 = empty_harness.add_component(
            kind=ComponentType.CABLE,
            mpn="CABLE-1",
            manufacturer="Test",
            cores=[CableCore(1, awg=18, color=WireColor.RED)],
        )
        c2 = empty_harness.add_component(
            kind=ComponentType.CABLE,
            mpn="CABLE-2",
            manufacturer="Test",
            cores=[CableCore(1, awg=18, color=WireColor.BLACK)],
        )
        assert c1.designator == "C1"
        assert c2.designator == "C2"

    def test_cable_core_method(self, empty_harness):
        """Test cable.core() method creates CoreRef."""
        cable = empty_harness.add_component(
            kind=ComponentType.CABLE,
            mpn="CABLE-1",
            manufacturer="Test",
            cores=[
                CableCore(1, awg=18, color=WireColor.RED),
                CableCore(2, awg=18, color=WireColor.BLACK),
            ],
        )
        core_ref = cable.core(2)
        assert isinstance(core_ref, CoreRef)
        assert core_ref.core == 2

    def test_cable_to_dict(self, empty_harness):
        """Test cable serialization."""
        cable = empty_harness.add_component(
            kind=ComponentType.CABLE,
            mpn="CABLE-2C",
            manufacturer="Test",
            cores=[
                CableCore(1, awg=18, color=WireColor.RED, label="PWR"),
                CableCore(2, awg=18, color=WireColor.BLACK, label="GND"),
            ],
            position=(150, 250),
        )
        data = cable.to_dict()

        assert data["kind"] == "cable"
        assert data["mpn"] == "CABLE-2C"
        assert len(data["cores"]) == 2
        assert data["cores"][0]["number"] == 1
        assert data["cores"][0]["color"] == "red"
        assert data["cores"][0]["label"] == "PWR"


class TestWireInstance:
    """Tests for WireInstance class."""

    def test_create_wire_instance(self, empty_harness):
        """Test creating a wire instance."""
        wire = empty_harness.add_component(
            kind=ComponentType.WIRE,
            mpn="20AWG-RED",
            manufacturer="Generic",
            awg=20,
            color=WireColor.RED,
        )
        assert isinstance(wire, WireInstance)
        assert wire.kind == ComponentType.WIRE
        assert wire.awg == 20
        assert wire.color == WireColor.RED.value

    def test_wire_with_string_color(self, empty_harness):
        """Test wire with custom string color."""
        wire = empty_harness.add_component(
            kind=ComponentType.WIRE,
            mpn="CUSTOM-WIRE",
            manufacturer="Test",
            awg=18,
            color="cyan",
        )
        assert wire.color == "cyan"

    def test_wire_to_dict(self, empty_harness):
        """Test wire serialization."""
        wire = empty_harness.add_component(
            kind=ComponentType.WIRE,
            mpn="18AWG-GRN",
            manufacturer="Test",
            awg=18,
            color=WireColor.GREEN,
        )
        data = wire.to_dict()

        assert data["kind"] == "wire"
        assert data["awg"] == 18
        assert data["color"] == "green"


class TestCableCore:
    """Tests for CableCore class."""

    def test_create_basic_core(self):
        """Test creating a basic cable core."""
        core = CableCore(number=1, awg=18, color=WireColor.RED)
        assert core.number == 1
        assert core.awg == 18
        assert core.color == WireColor.RED

    def test_core_with_label(self):
        """Test cable core with label."""
        core = CableCore(number=1, awg=18, color=WireColor.RED, label="PWR+")
        assert core.label == "PWR+"

    def test_core_with_conductor_type(self):
        """Test cable core with conductor type."""
        core = CableCore(
            number=1,
            awg=18,
            color=WireColor.RED,
            conductor_type=ConductorType.SOLID,
        )
        assert core.conductor_type == ConductorType.SOLID

    def test_core_invalid_number_raises(self):
        """Test that invalid core number raises ValueError."""
        with pytest.raises(ValueError):
            CableCore(number=0, awg=18, color=WireColor.RED)

        with pytest.raises(ValueError):
            CableCore(number=-1, awg=18, color=WireColor.RED)

    def test_core_to_dict(self):
        """Test cable core serialization."""
        core = CableCore(
            number=2,
            awg=16,
            color=WireColor.BLACK,
            label="GND",
            conductor_type=ConductorType.STRANDED,
        )
        data = core.to_dict()

        assert data["number"] == 2
        assert data["awg"] == 16
        assert data["color"] == "black"
        assert data["label"] == "GND"
        assert data["conductor_type"] == "stranded"


class TestWirePart:
    """Tests for Wire part class."""

    def test_create_basic_wire(self):
        """Test creating a basic wire."""
        wire = Wire(
            mpn="20AWG-RED",
            manufacturer="Generic",
            awg=20,
            color=WireColor.RED,
        )
        assert wire.mpn == "20AWG-RED"
        assert wire.awg == 20
        assert wire.color == WireColor.RED

    def test_wire_with_description(self):
        """Test wire with description."""
        wire = Wire(
            mpn="20AWG-RED",
            manufacturer="Generic",
            awg=20,
            color=WireColor.RED,
            description="Hook-up wire",
        )
        assert wire.description == "Hook-up wire"

    def test_wire_with_string_color(self):
        """Test wire with custom string color."""
        wire = Wire(
            mpn="CUSTOM",
            manufacturer="Test",
            awg=18,
            color="turquoise",
        )
        assert wire.color == "turquoise"

    def test_wire_to_dict(self):
        """Test wire serialization."""
        wire = Wire(
            mpn="18AWG-BLU",
            manufacturer="Generic",
            awg=18,
            color=WireColor.BLUE,
            description="Blue wire",
            conductor_type=ConductorType.STRANDED,
        )
        data = wire.to_dict()

        assert data["mpn"] == "18AWG-BLU"
        assert data["manufacturer"] == "Generic"
        assert data["awg"] == 18
        assert data["color"] == "blue"
        assert data["description"] == "Blue wire"
        assert data["conductor_type"] == "stranded"
