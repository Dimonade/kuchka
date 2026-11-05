"""A point turning at a radius moves along its rim, and the radius reads back."""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka import Acceleration
from kuchka import AngularDisplacement
from kuchka import AngularVelocity
from kuchka import DivisionByZeroError
from kuchka import FirstMomentOfMass
from kuchka import Force
from kuchka import Frequency
from kuchka import IncompatibleDimensionError
from kuchka import Length
from kuchka import Momentum
from kuchka import Torque
from kuchka import Velocity
from kuchka.internal.constants import PI
from kuchka.units import angular
from kuchka.units import length
from kuchka.units import mass
from kuchka.units.kinematics import acceleration
from kuchka.units.kinematics import angular_acceleration as angacc
from kuchka.units.kinematics import angular_velocity as angvel
from kuchka.units.kinematics import velocity
from kuchka.units.mechanics import first_moment_of_mass as unbalance
from kuchka.units.mechanics import force
from kuchka.units.mechanics import momentum
from kuchka.units.mechanics import torque


@pytest.mark.parametrize(
    "build",
    [lambda w, r: w * r, lambda w, r: r * w],
    ids=["w*r", "r*w"],
)
def test_an_angular_velocity_at_a_radius_is_a_rim_speed(build) -> None:
    rim = build(angvel.RadianPerSecond(300), length.Metre(Fraction(1, 5)))
    assert type(rim) is Velocity
    assert rim == velocity.MetrePerSecond(60)


def test_a_turn_rate_at_a_radius_moves_a_circumference_per_turn() -> None:
    rim = angvel.RevolutionPerMinute(60) * length.Metre(1)
    assert rim == velocity.MetrePerSecond(2 * PI)


def test_a_rim_speed_per_angular_velocity_is_the_radius() -> None:
    radius = velocity.MetrePerSecond(60) / angvel.RadianPerSecond(300)
    assert type(radius) is Length
    assert radius == length.Metre(Fraction(1, 5))


def test_the_centripetal_acceleration_reads_from_the_rim_speed() -> None:
    radius = length.Metre(Fraction(1, 5))
    rim = angvel.RadianPerSecond(300) * radius
    centripetal = rim**2 / radius
    assert type(centripetal) is Acceleration
    assert centripetal == acceleration.MetrePerSecondSquared(18_000)


def test_a_velocity_per_radius_stays_a_frequency() -> None:
    rate = velocity.MetrePerSecond(60) / length.Metre(Fraction(1, 5))
    assert type(rate) is Frequency


@pytest.mark.parametrize(
    "build",
    [lambda a, r: a * r, lambda a, r: r * a],
    ids=["a*r", "r*a"],
)
def test_an_angular_acceleration_at_a_radius_is_tangential(build) -> None:
    tangential = build(angacc.RadianPerSecondSquared(150), length.Metre(Fraction(1, 5)))
    assert type(tangential) is Acceleration
    assert tangential == acceleration.MetrePerSecondSquared(30)


def test_a_tangential_acceleration_per_angular_acceleration_is_the_radius() -> None:
    radius = acceleration.MetrePerSecondSquared(30) / angacc.RadianPerSecondSquared(150)
    assert type(radius) is Length
    assert radius == length.Metre(Fraction(1, 5))


def test_a_torque_per_force_is_the_lever_arm() -> None:
    arm = torque.NewtonMetre(10) / force.Newton(50)
    assert type(arm) is Length
    assert arm == length.Metre(Fraction(1, 5))


def test_a_torque_per_lever_arm_is_the_force() -> None:
    push = torque.NewtonMetre(10) / length.Metre(Fraction(1, 5))
    assert type(push) is Force
    assert push == force.Newton(50)


def test_a_force_at_a_lever_arm_round_trips() -> None:
    turning = Torque.from_force(force.Newton(50), length.Metre(Fraction(1, 5)))
    assert turning / length.Metre(Fraction(1, 5)) == force.Newton(50)
    assert turning / force.Newton(50) == length.Metre(Fraction(1, 5))


@pytest.mark.parametrize(
    "build",
    [
        lambda w, r: w * (w * r),
        lambda w, r: (w * r) * w,
        lambda w, r: r * w * w,
    ],
    ids=["w*(w*r)", "(w*r)*w", "r*w*w"],
)
def test_an_angular_velocity_times_its_rim_speed_is_centripetal(build) -> None:
    centripetal = build(angvel.RadianPerSecond(300), length.Metre(Fraction(1, 5)))
    assert type(centripetal) is Acceleration
    assert centripetal == acceleration.MetrePerSecondSquared(18_000)


def test_a_centripetal_acceleration_per_angular_velocity_is_the_rim_speed() -> None:
    rim = acceleration.MetrePerSecondSquared(18_000) / angvel.RadianPerSecond(300)
    assert type(rim) is Velocity
    assert rim == velocity.MetrePerSecond(60)


@pytest.mark.parametrize(
    "build",
    [lambda w, p: w * p, lambda w, p: p * w],
    ids=["w*p", "p*w"],
)
def test_an_angular_velocity_times_a_momentum_is_centripetal_force(build) -> None:
    pull = build(angvel.RadianPerSecond(300), momentum.KilogramMetrePerSecond(120))
    assert type(pull) is Force
    assert pull == force.Newton(36_000)


def test_a_centripetal_force_per_angular_velocity_is_the_momentum() -> None:
    turned = force.Newton(36_000) / angvel.RadianPerSecond(300)
    assert type(turned) is Momentum
    assert turned == momentum.KilogramMetrePerSecond(120)


def test_a_mass_on_a_rim_needs_the_centripetal_force() -> None:
    rate = angvel.RadianPerSecond(300)
    rim = rate * length.Metre(Fraction(1, 5))
    assert mass.Kilogram(2) * rim * rate == force.Newton(36_000)


@pytest.mark.parametrize(
    "build",
    [
        lambda m, r, w: m * r * w * w,
        lambda m, r, w: r * m * w * w,
        lambda m, r, w: w * (m * r) * w,
    ],
    ids=["m*r*w*w", "r*m*w*w", "w*(m*r)*w"],
)
def test_an_unbalance_turning_pulls_the_axis(build) -> None:
    pull = build(
        mass.Kilogram(2), length.Metre(Fraction(1, 5)), angvel.RadianPerSecond(300)
    )
    assert type(pull) is Force
    assert pull == force.Newton(36_000)


def test_a_rotor_unbalance_in_gram_millimetres_reads_in_newtons() -> None:
    rate = angvel.RadianPerSecond(300)
    assert unbalance.GramMillimetre(30) * rate * rate == force.Newton(Fraction(27, 10))


def test_an_unbalance_turning_has_the_momentum_of_its_mass_on_the_rim() -> None:
    rate = angvel.RadianPerSecond(300)
    turning = unbalance.KilogramMetre(Fraction(2, 5)) * rate
    assert type(turning) is Momentum
    assert turning == momentum.KilogramMetrePerSecond(120)
    assert turning / rate == unbalance.KilogramMetre(Fraction(2, 5))
    assert type(turning / rate) is FirstMomentOfMass


@pytest.mark.parametrize(
    "build",
    [lambda a, r: a * r, lambda a, r: r * a],
    ids=["theta*r", "r*theta"],
)
def test_an_angle_at_a_radius_sweeps_an_arc(build) -> None:
    arc = build(angular.RadianDisplacement(2), length.Metre(Fraction(1, 4)))
    assert type(arc) is Length
    assert arc == length.Metre(Fraction(1, 2))


def test_a_full_turn_sweeps_the_circumference() -> None:
    assert angular.TurnDisplacement(1) * length.Metre(1) == length.Metre(2 * PI)


def test_an_arc_per_angle_is_the_radius() -> None:
    radius = length.Metre(Fraction(1, 2)) / angular.RadianDisplacement(2)
    assert type(radius) is Length
    assert radius == length.Metre(Fraction(1, 4))


def test_the_angle_of_an_arc_is_built_by_name() -> None:
    swept = AngularDisplacement.from_arc(
        length.Metre(Fraction(1, 2)), length.Metre(Fraction(1, 4))
    )
    assert type(swept) is AngularDisplacement
    assert swept == angular.RadianDisplacement(2)
    assert swept * length.Metre(Fraction(1, 4)) == length.Metre(Fraction(1, 2))


def test_the_angular_velocity_of_a_rim_speed_is_built_by_name() -> None:
    rate = AngularVelocity.from_tangential(
        velocity.MetrePerSecond(60), length.Metre(Fraction(1, 5))
    )
    assert type(rate) is AngularVelocity
    assert rate == angvel.RadianPerSecond(300)
    assert str(rate) == "300 rad/s"
    assert rate * length.Metre(Fraction(1, 5)) == velocity.MetrePerSecond(60)


def test_a_rim_speed_over_its_radius_viewed_as_turns_reads_two_pi_fast() -> None:
    rate = velocity.MetrePerSecond(60) / length.Metre(Fraction(1, 5))
    viewed = rate.to_angular_velocity()
    built = AngularVelocity.from_tangential(
        velocity.MetrePerSecond(60), length.Metre(Fraction(1, 5))
    )
    assert viewed == built * (2 * PI)


@pytest.mark.parametrize(
    ("build", "first", "second"),
    [
        (AngularVelocity.from_tangential, length.Metre(1), velocity.MetrePerSecond(1)),
        (
            AngularVelocity.from_tangential,
            velocity.MetrePerSecond(1),
            angvel.RadianPerSecond(1),
        ),
        (AngularDisplacement.from_arc, length.Metre(1), velocity.MetrePerSecond(1)),
        (AngularDisplacement.from_arc, angular.RadianDisplacement(1), length.Metre(1)),
    ],
    ids=[
        "tangential-swapped",
        "tangential-not-a-length",
        "arc-not-a-length",
        "arc-angle",
    ],
)
def test_a_named_relation_refuses_other_kinds(build, first, second) -> None:
    with pytest.raises(IncompatibleDimensionError, match="build an"):
        build(first, second)


@pytest.mark.parametrize(
    "build",
    [
        lambda: AngularVelocity.from_tangential(
            velocity.MetrePerSecond(1), length.Metre(0)
        ),
        lambda: AngularDisplacement.from_arc(length.Metre(1), length.Metre(0)),
    ],
    ids=["tangential", "arc"],
)
def test_a_named_relation_around_no_radius_is_a_division_by_zero(build) -> None:
    with pytest.raises(DivisionByZeroError, match="the divisor is zero"):
        build()
