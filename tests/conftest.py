"""
Pytest configuration and shared fixtures for splice-py tests.
"""

import pytest
from splice import (
    Harness,
    ComponentType,
    Wire,
    CableCore,
    FlyingLead,
    WireColor,
    ConnectorCategory,
    ConnectorGender,
    ConnectorShape,
    FlyingLeadType,
)


@pytest.fixture
def empty_harness():
    """Create an empty harness for testing."""
    return Harness("Test Harness", "Test description")


@pytest.fixture
def wire_red_20awg():
    """Create a standard red 20AWG wire."""
    return Wire(
        mpn="20AWG-RED",
        manufacturer="Generic",
        awg=20,
        color=WireColor.RED,
        description="20 AWG Red Hook-up Wire",
    )


@pytest.fixture
def wire_black_20awg():
    """Create a standard black 20AWG wire."""
    return Wire(
        mpn="20AWG-BLK",
        manufacturer="Generic",
        awg=20,
        color=WireColor.BLACK,
        description="20 AWG Black Hook-up Wire",
    )


@pytest.fixture
def wire_green_18awg():
    """Create a standard green 18AWG wire."""
    return Wire(
        mpn="18AWG-GRN",
        manufacturer="Generic",
        awg=18,
        color=WireColor.GREEN,
        description="18 AWG Green Hook-up Wire",
    )


@pytest.fixture
def basic_connector(empty_harness):
    """Create a basic 3-position connector."""
    return empty_harness.add_component(
        kind=ComponentType.CONNECTOR,
        mpn="43650-0300",
        manufacturer="Molex",
        positions=3,
        position=(100, 100),
    )


@pytest.fixture
def basic_cable(empty_harness):
    """Create a basic 4-core cable."""
    return empty_harness.add_component(
        kind=ComponentType.CABLE,
        mpn="CABLE-4C-18",
        manufacturer="Alpha Wire",
        cores=[
            CableCore(1, awg=18, color=WireColor.RED),
            CableCore(2, awg=18, color=WireColor.BLACK),
            CableCore(3, awg=18, color=WireColor.GREEN),
            CableCore(4, awg=18, color=WireColor.WHITE),
        ],
        position=(200, 200),
    )


@pytest.fixture
def flying_lead_tinned():
    """Create a tinned flying lead."""
    return FlyingLead(termination_type=FlyingLeadType.TINNED)


@pytest.fixture
def flying_lead_bare():
    """Create a bare flying lead."""
    return FlyingLead(termination_type=FlyingLeadType.BARE)


@pytest.fixture
def harness_with_components():
    """Create a harness with multiple components for testing."""
    harness = Harness("Test Harness", "Harness with components")

    # Add connectors
    x1 = harness.add_component(
        kind=ComponentType.CONNECTOR,
        mpn="43650-0300",
        manufacturer="Molex",
        positions=3,
        position=(100, 100),
    )

    x2 = harness.add_component(
        kind=ComponentType.CONNECTOR,
        mpn="43650-0400",
        manufacturer="Molex",
        positions=4,
        position=(400, 100),
    )

    # Add wire
    wire = Wire(
        mpn="20AWG-RED",
        manufacturer="Generic",
        awg=20,
        color=WireColor.RED,
    )

    # Add connection
    harness.connect(x1.pin(1), x2.pin(1), wire=wire, length_mm=300)

    return harness, x1, x2, wire


@pytest.fixture
def harness_with_cable():
    """Create a harness with a cable and connectors."""
    harness = Harness("Cable Test", "Harness with cable")

    # Add connectors
    x1 = harness.add_component(
        kind=ComponentType.CONNECTOR,
        mpn="43650-0200",
        manufacturer="Molex",
        positions=2,
        position=(100, 100),
    )

    x2 = harness.add_component(
        kind=ComponentType.CONNECTOR,
        mpn="43650-0200",
        manufacturer="Molex",
        positions=2,
        position=(500, 100),
    )

    # Add cable
    c1 = harness.add_component(
        kind=ComponentType.CABLE,
        mpn="CABLE-2C",
        manufacturer="Alpha Wire",
        cores=[
            CableCore(1, awg=18, color=WireColor.RED),
            CableCore(2, awg=18, color=WireColor.BLACK),
        ],
        position=(300, 100),
    )

    return harness, x1, x2, c1
