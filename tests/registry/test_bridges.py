"""Declaring a bridge, a rule that crosses the angle axis."""

from __future__ import annotations

import pytest

from kuchka import Acceleration
from kuchka import AngularAcceleration
from kuchka import AngularDisplacement
from kuchka import AngularVelocity
from kuchka import AngularVelocitySquared
from kuchka import Area
from kuchka import Current
from kuchka import FirstMomentOfMass
from kuchka import Force
from kuchka import Frequency
from kuchka import Length
from kuchka import Mass
from kuchka import MomentOfInertia
from kuchka import Momentum
from kuchka import Power
from kuchka import Proportion
from kuchka import SampleRate
from kuchka import Time
from kuchka import Torque
from kuchka import Velocity
from kuchka import Voltage
from kuchka.dimensions import Dimension
from kuchka.internal.constants import PI
from kuchka.quantities.base import registry
from kuchka.units import length
from kuchka.units.kinematics import angular_velocity
from kuchka.units.kinematics import velocity
from tests.support.synthetic import linear_kind
from tests.support.synthetic import registry_state

SHIPPED_BRIDGES: dict[tuple[type, str, type], tuple[type, str]] = {
    (AngularVelocity, "*", Length): (
        Velocity,
        "the speed of a point turning at a radius",
    ),
    (Velocity, "/", AngularVelocity): (Length, "the radius turning at a rim speed"),
    (AngularAcceleration, "*", Length): (
        Acceleration,
        "the tangential acceleration of a point at a radius",
    ),
    (Acceleration, "/", AngularAcceleration): (
        Length,
        "the radius at a tangential acceleration",
    ),
    (AngularVelocitySquared, "*", Length): (
        Acceleration,
        "the centripetal acceleration of a point turning at a squared rate",
    ),
    (Acceleration, "/", AngularVelocitySquared): (
        Length,
        "the radius at a centripetal acceleration and a squared rate",
    ),
    (Mass, "*", Area): (MomentOfInertia, "a mass at a radius, times that radius"),
    (FirstMomentOfMass, "*", Length): (
        MomentOfInertia,
        "an unbalance, times its radius",
    ),
    (MomentOfInertia, "/", Mass): (Area, "the square of the radius of gyration"),
    (MomentOfInertia, "/", Area): (Mass, "the mass at the radius of gyration"),
    (MomentOfInertia, "/", Length): (
        FirstMomentOfMass,
        "the unbalance at a radius",
    ),
    (MomentOfInertia, "/", FirstMomentOfMass): (Length, "the radius of an unbalance"),
    (Torque, "/", Force): (Length, "the lever arm of a force"),
    (Torque, "/", Length): (Force, "the force at a lever arm"),
    (AngularVelocity, "*", Velocity): (
        Acceleration,
        "the centripetal acceleration of a point turning at a rim speed",
    ),
    (Acceleration, "/", AngularVelocity): (
        Velocity,
        "the rim speed at a centripetal acceleration",
    ),
    (AngularVelocity, "*", Momentum): (
        Force,
        "the centripetal force on a body turning with a momentum",
    ),
    (Force, "/", AngularVelocity): (
        Momentum,
        "the momentum a centripetal force turns",
    ),
    (FirstMomentOfMass, "*", AngularVelocity): (
        Momentum,
        "the momentum of an unbalance turning on its circle",
    ),
    (Momentum, "/", AngularVelocity): (
        FirstMomentOfMass,
        "the unbalance that turns with a momentum",
    ),
    (AngularDisplacement, "*", Length): (Length, "the arc an angle sweeps at a radius"),
    (Length, "/", AngularDisplacement): (Length, "the radius of an arc"),
}
"""Every bridge the library declares, with its result and the one reading of it."""


def test_a_bridge_after_the_close_is_refused() -> None:
    with pytest.raises(RuntimeError, match="closed"):
        registry._bridge(AngularVelocity, "*", Length, Velocity)  # noqa: SLF001


@pytest.mark.usefixtures("open_registry")
def test_a_product_bridge_holds_in_both_operand_orders() -> None:
    registry._bridge(AngularVelocity, "*", Length, Velocity)  # noqa: SLF001
    speed = velocity.MetrePerSecond(0.6)
    rate = angular_velocity.RadianPerSecond(3)
    assert rate * length.Metre(0.2) == speed
    assert length.Metre(0.2) * rate == speed


@pytest.mark.usefixtures("open_registry")
def test_a_value_across_a_bridge_and_back_is_unchanged() -> None:
    registry._bridge(AngularVelocity, "*", Length, Velocity)  # noqa: SLF001
    registry._bridge(Velocity, "/", AngularVelocity, Length)  # noqa: SLF001
    rate = angular_velocity.RadianPerSecond(3)
    radius = length.Metre(0.2)
    assert (rate * radius) / rate == radius
    assert type((rate * radius) / rate) is Length


@pytest.mark.parametrize(
    ("key", "factor"),
    [
        ((Mass, "*", Area), (2 * PI) ** 2),
        ((AngularVelocity, "*", Length), 2 * PI),
        ((Velocity, "/", AngularVelocity), 1 / (2 * PI)),
        ((Torque, "/", Force), 1 / (2 * PI)),
        ((AngularVelocitySquared, "*", Length), (2 * PI) ** 2),
        ((Acceleration, "/", AngularVelocitySquared), 1 / (2 * PI) ** 2),
    ],
    ids=[
        "inertia",
        "rim-speed",
        "radius",
        "lever-arm",
        "rim-acceleration",
        "rim-radius-squared",
    ],
)
def test_the_factor_follows_from_the_angle_exponents(
    key: tuple[type, str, type], factor: object
) -> None:
    assert registry._BRIDGES[key][1] == factor  # noqa: SLF001  # type: ignore[index]


@pytest.mark.usefixtures("open_registry")
@pytest.mark.parametrize(
    ("left", "operation", "right", "result", "match"),
    [
        (AngularVelocity, "+", Length, Velocity, "'\\*' or '/'"),
        (SampleRate, "*", AngularDisplacement, AngularVelocity, "take part"),
        (Proportion, "*", AngularVelocity, AngularVelocity, "take part"),
        (Frequency, "*", Time, AngularDisplacement, "does not fit"),
        (AngularVelocity, "*", Length, Frequency, "does not fit"),
        (Voltage, "*", Current, Power, "does not fit"),
    ],
    ids=["operation", "role", "dimensionless", "cycles", "other-axis", "no-angle"],
)
def test_a_bridge_that_does_not_fit_is_refused(
    left: type, operation: str, right: type, result: type, match: str
) -> None:
    before = registry_state()
    with pytest.raises(TypeError, match=match):
        registry._bridge(left, operation, right, result)  # type: ignore[arg-type]  # noqa: SLF001
    assert registry_state() == before


@pytest.mark.usefixtures("open_registry")
def test_a_bridge_contradicting_another_is_refused() -> None:
    other = linear_kind("Other", Dimension(length=1, time=-1, angle=-1))
    registry._register(other.dimension, other)  # noqa: SLF001
    registry._bridge(AngularVelocity, "*", Length, Velocity)  # noqa: SLF001
    with pytest.raises(TypeError, match="already Velocity"):
        registry._bridge(Length, "*", AngularVelocity, other)  # noqa: SLF001


@pytest.mark.usefixtures("open_registry")
def test_a_rule_contradicting_a_bridge_is_refused() -> None:
    plain = linear_kind("Plain", AngularVelocity.dimension * Length.dimension)
    registry._register(plain.dimension, plain)  # noqa: SLF001
    registry._bridge(AngularVelocity, "*", Length, Velocity)  # noqa: SLF001
    with pytest.raises(TypeError, match="already Velocity"):
        registry._rule(AngularVelocity, "*", Length, plain)  # noqa: SLF001


@pytest.mark.usefixtures("open_registry")
def test_a_kind_for_the_plain_dimension_conflicts_with_the_bridge() -> None:
    registry._bridge(AngularVelocity, "*", Length, Velocity)  # noqa: SLF001
    plain = linear_kind("Plain", AngularVelocity.dimension * Length.dimension)
    registry._register(plain.dimension, plain)  # noqa: SLF001
    with pytest.raises(TypeError, match="conflicts with Plain"):
        registry._check_bridges()  # noqa: SLF001


def test_the_shipped_bridges_are_the_known_ones() -> None:
    expected = {
        key: result
        for (left, operation, right), (result, _) in SHIPPED_BRIDGES.items()
        for key in {(left, operation, right), (right, operation, left)}
        if operation == "*" or key == (left, operation, right)
    }
    shipped = {key: result for key, (result, _) in registry._BRIDGES.items()}  # noqa: SLF001
    assert shipped == expected


def test_every_shipped_bridge_crosses_the_angle_axis_into_a_gap() -> None:
    for (left, operation, right), (result, _) in registry._BRIDGES.items():  # noqa: SLF001
        plain = registry._plain_dimension(left, operation, right)  # noqa: SLF001
        assert registry._differs_in_angle_alone(plain, result.dimension)  # noqa: SLF001
        assert not registry._arithmetic_roots(plain)  # noqa: SLF001
