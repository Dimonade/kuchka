"""Angular displacement, angular velocity, and torque: counting the angle axis.

Angle is a position on a circle and wraps, so it takes no part in arithmetic.
`AngularDisplacement` is the angle swept, which does not wrap, and with the angle axis
counted torque is energy per angle and angular velocity is angle per time, both distinct
from energy and from the hertz.
Generic algebraic properties are covered once for every registered quantity family
elsewhere; this module covers what is specific to these three kinds.
"""

from __future__ import annotations

import operator
from fractions import Fraction

import pytest

from kuchka import Angle
from kuchka import AngularDisplacement
from kuchka import AngularVelocity
from kuchka import Degree
from kuchka import DegreeDisplacement
from kuchka import DegreePerSecond
from kuchka import Energy
from kuchka import Force
from kuchka import Frequency
from kuchka import Hertz
from kuchka import IncompatibleDimensionError
from kuchka import InvalidConversionError
from kuchka import InvalidMeasurementError
from kuchka import Joule
from kuchka import JoulePerTurn
from kuchka import Metre
from kuchka import Newton
from kuchka import NewtonMetre
from kuchka import PoundForceFoot
from kuchka import PoundForceInch
from kuchka import Power
from kuchka import Radian
from kuchka import RadianDisplacement
from kuchka import RadianPerSecond
from kuchka import RevolutionPerMinute
from kuchka import Second
from kuchka import Time
from kuchka import Torque
from kuchka import TurnDisplacement
from kuchka import TurnPerSecond
from kuchka import Watt
from kuchka.dimensions import ANGLE
from kuchka.dimensions import ANGULAR_VELOCITY
from kuchka.dimensions import ENERGY
from kuchka.dimensions import FREQUENCY
from kuchka.dimensions import TIME
from kuchka.dimensions import TORQUE
from kuchka.internal.constants import PI
from kuchka.units import ANGULAR_DISPLACEMENT_UNITS
from kuchka.units import ANGULAR_VELOCITY_UNITS
from kuchka.units import DEGREE
from kuchka.units import HERTZ
from kuchka.units import JOULE
from kuchka.units import NEWTON_METRE
from kuchka.units import RADIAN
from kuchka.units import RADIAN_PER_SECOND
from kuchka.units import TORQUE_UNITS

# The dimensions.


def test_torque_is_energy_per_angle_and_angular_velocity_is_angle_per_time() -> None:
    assert TORQUE == ENERGY / ANGLE
    assert ANGULAR_VELOCITY == ANGLE / TIME


def test_torque_and_angular_velocity_differ_from_energy_and_frequency() -> None:
    assert TORQUE != ENERGY
    assert ANGULAR_VELOCITY != FREQUENCY


# `AngularDisplacement` is the unwrapped angle.


def test_an_angular_displacement_keeps_the_turns_it_swept() -> None:
    swept = DegreeDisplacement(370)
    assert swept.value_in(DEGREE) == Fraction(370)
    assert swept != DegreeDisplacement(10)


def test_an_angle_wraps_where_a_displacement_does_not() -> None:
    assert Degree(370) == Degree(10)
    assert DegreeDisplacement(370) != DegreeDisplacement(10)


def test_a_displacement_adds_and_subtracts_without_wrapping() -> None:
    assert DegreeDisplacement(270) + DegreeDisplacement(270) == DegreeDisplacement(540)
    assert DegreeDisplacement(10) - DegreeDisplacement(20) == DegreeDisplacement(-10)


def test_the_displacement_units_are_exact_for_degrees_and_turns() -> None:
    assert TurnDisplacement(1) == DegreeDisplacement(360)
    assert RadianDisplacement(PI * 2) == TurnDisplacement(1)


def test_angle_does_not_take_part_in_arithmetic() -> None:
    with pytest.raises(TypeError):
        Joule(1) / Radian(1)  # type: ignore[operator]
    with pytest.raises(TypeError):
        Radian(1) / Second(1)  # type: ignore[operator]


def test_an_angle_becomes_a_displacement_within_one_turn() -> None:
    swept = Degree(370).to_angular_displacement()
    assert type(swept) is AngularDisplacement
    assert swept == DegreeDisplacement(10)


def test_a_displacement_wraps_into_the_angle_it_ends_at() -> None:
    angle = DegreeDisplacement(370).to_angle()
    assert type(angle) is Angle
    assert angle.value_in(DEGREE) == Fraction(10)
    assert DegreeDisplacement(-10).to_angle().value_in(DEGREE) == Fraction(350)


def test_the_conversions_keep_the_unit_they_were_shown_in() -> None:
    assert Degree(90).to_angular_displacement().unit is DEGREE
    assert RadianDisplacement(1).to_angle().unit is RADIAN


# Torque.


def test_energy_per_angle_is_torque() -> None:
    result = Joule(1) / RadianDisplacement(1)
    assert type(result) is Torque
    assert result == NewtonMetre(1)


def test_torque_times_angular_displacement_is_energy_exactly() -> None:
    work = NewtonMetre(10) * RadianDisplacement(2)
    assert type(work) is Energy
    assert work == Joule(20)
    assert RadianDisplacement(2) * NewtonMetre(10) == Joule(20)


def test_energy_per_torque_is_angular_displacement() -> None:
    result = Joule(20) / NewtonMetre(10)
    assert type(result) is AngularDisplacement
    assert result == RadianDisplacement(2)


def test_torque_times_angular_velocity_is_power_exactly() -> None:
    power = NewtonMetre(2) * RadianPerSecond(5)
    assert type(power) is Power
    assert power == Watt(10)
    assert RadianPerSecond(5) * NewtonMetre(2) == Watt(10)


def test_power_per_angular_velocity_is_torque_and_per_torque_is_velocity() -> None:
    assert Watt(10) / RadianPerSecond(5) == NewtonMetre(2)
    assert type(Watt(10) / RadianPerSecond(5)) is Torque
    assert Watt(10) / NewtonMetre(2) == RadianPerSecond(5)
    assert type(Watt(10) / NewtonMetre(2)) is AngularVelocity


def test_a_force_at_a_distance_is_a_torque_by_name() -> None:
    torque = Torque.from_force(Newton(50), Metre(Fraction(1, 5)))
    assert type(torque) is Torque
    assert torque == NewtonMetre(10)


def test_a_force_times_a_length_is_energy_not_torque() -> None:
    assert type(Newton(5) * Metre(2)) is Energy


def test_a_torque_is_built_from_a_force_and_a_length() -> None:
    with pytest.raises(IncompatibleDimensionError, match="build a torque from"):
        Torque.from_force(Metre(1), Newton(1))  # type: ignore[arg-type]
    with pytest.raises(IncompatibleDimensionError):
        Torque.from_force(Newton(1), Newton(1))  # type: ignore[arg-type]


def test_torque_units_scale_exactly() -> None:
    assert NewtonMetre(1) == JoulePerTurn(2 * PI)
    assert PoundForceFoot(12) == PoundForceInch(144)
    pound_force = Newton(Fraction("4.4482216152605"))
    foot = Metre(Fraction("0.3048"))
    assert PoundForceFoot(1) == Torque.from_force(pound_force, foot)


# AngularVelocity.


def test_angle_per_time_is_angular_velocity_and_back() -> None:
    velocity = DegreeDisplacement(90) / Second(1)
    assert type(velocity) is AngularVelocity
    assert velocity == DegreePerSecond(90)
    swept = RadianPerSecond(5) * Second(2)
    assert type(swept) is AngularDisplacement
    assert swept == RadianDisplacement(10)
    assert Second(2) * RadianPerSecond(5) == RadianDisplacement(10)
    assert type(RadianDisplacement(10) / RadianPerSecond(5)) is Time


def test_the_revolution_per_minute_is_exact() -> None:
    assert RevolutionPerMinute(60) == TurnPerSecond(1)
    assert RevolutionPerMinute(3000).value_in(RADIAN_PER_SECOND) == 3000 * 2 * PI / 60


def test_a_frequency_times_an_angle_is_an_angular_velocity() -> None:
    result = Hertz(2) * TurnDisplacement(1)
    assert type(result) is AngularVelocity
    assert result == RadianPerSecond(4 * PI)
    assert type(TurnDisplacement(1) * Hertz(2)) is AngularVelocity
    assert type(RadianPerSecond(4 * PI) / Hertz(2)) is AngularDisplacement


def test_one_hertz_is_not_an_angular_velocity() -> None:
    with pytest.raises(IncompatibleDimensionError):
        Hertz(1) + TurnPerSecond(1)  # type: ignore[operator]
    assert Hertz(1) != TurnPerSecond(1)
    with pytest.raises(IncompatibleDimensionError):
        operator.lt(Hertz(1), TurnPerSecond(1))


def test_a_frequency_converts_to_an_angular_velocity_by_name() -> None:
    velocity = Hertz(50).to_angular_velocity()
    assert type(velocity) is AngularVelocity
    assert velocity == RadianPerSecond(100 * PI)


def test_an_angular_velocity_converts_to_a_frequency_by_name() -> None:
    frequency = RevolutionPerMinute(3000).to_frequency()
    assert type(frequency) is Frequency
    assert frequency == Hertz(50)
    assert Hertz(50).to_angular_velocity().to_frequency() == Hertz(50)


# Units belong to their kind.


def test_a_torque_unit_is_not_an_energy_unit() -> None:
    with pytest.raises(InvalidConversionError):
        NewtonMetre(1).to(JOULE)
    with pytest.raises(InvalidConversionError):
        Joule(1).to(NEWTON_METRE)
    with pytest.raises(InvalidMeasurementError):
        Energy(Fraction(1), NEWTON_METRE)
    with pytest.raises(InvalidMeasurementError):
        Torque(Fraction(1), JOULE)


def test_hertz_is_not_an_angular_velocity_unit() -> None:
    with pytest.raises(InvalidConversionError):
        TurnPerSecond(1).to(HERTZ)
    with pytest.raises(InvalidMeasurementError):
        AngularVelocity(Fraction(1), HERTZ)


def test_angle_and_displacement_share_their_units() -> None:
    assert Radian(1).unit is RADIAN
    assert RadianDisplacement(1).unit is RADIAN
    assert RadianDisplacement(1).to(DEGREE).unit is DEGREE


def test_the_tables_list_the_units_by_symbol() -> None:
    assert set(ANGULAR_DISPLACEMENT_UNITS) >= {"tr", "rad", "\u00b0"}
    assert set(ANGULAR_VELOCITY_UNITS) == {"tr/s", "rad/s", "\u00b0/s", "rpm"}
    assert set(TORQUE_UNITS) == {
        "J/tr",
        "N\u00b7m",
        "mN\u00b7m",
        "kN\u00b7m",
        "lbf\u00b7ft",
        "lbf\u00b7in",
    }


# What arithmetic displays.


def test_results_display_in_the_units_people_read() -> None:
    assert str(Joule(1) / RadianDisplacement(1)) == "1 N\u00b7m"
    assert str(RadianPerSecond(5) * Second(2)) == "10 rad"
    assert str(DegreeDisplacement(90) / Second(1)).endswith(" rad/s")
    assert str(Torque.from_force(Newton(50), Metre(Fraction(1, 5)))) == "10 N\u00b7m"


def test_the_canonical_unit_is_what_magnitude_reads_in() -> None:
    assert JoulePerTurn(3).magnitude == Fraction(3)
    assert TurnPerSecond(3).magnitude == Fraction(3)
    assert TurnDisplacement(3).magnitude == Fraction(3)


# Protocols.


def test_an_angular_velocity_can_be_viewed_as_a_frequency() -> None:
    from kuchka import BaudRate
    from kuchka import ConvertibleToFrequency

    assert isinstance(TurnPerSecond(1), ConvertibleToFrequency)
    assert not issubclass(BaudRate, ConvertibleToFrequency)


def test_force_stays_a_force() -> None:
    assert isinstance(Newton(1), Force)
