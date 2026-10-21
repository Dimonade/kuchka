"""The units of rotation belong to their kind, and results display in them."""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka import AngularVelocity
from kuchka import Energy
from kuchka import Force
from kuchka import InvalidConversionError
from kuchka import InvalidMeasurementError
from kuchka import Torque
from kuchka.internal import symbols
from kuchka.units import angular
from kuchka.units import angular_velocity as angvel
from kuchka.units import energy
from kuchka.units import force
from kuchka.units import frequency
from kuchka.units import length
from kuchka.units import time
from kuchka.units import torque


def test_a_torque_unit_is_not_an_energy_unit() -> None:
    with pytest.raises(InvalidConversionError):
        torque.NewtonMetre(1).to(energy.JOULE)
    with pytest.raises(InvalidConversionError):
        energy.Joule(1).to(torque.NEWTON_METRE)
    with pytest.raises(InvalidMeasurementError):
        Energy(Fraction(1), torque.NEWTON_METRE)
    with pytest.raises(InvalidMeasurementError):
        Torque(Fraction(1), energy.JOULE)


def test_hertz_is_not_an_angular_velocity_unit() -> None:
    with pytest.raises(InvalidConversionError):
        angvel.TurnPerSecond(1).to(frequency.HERTZ)
    with pytest.raises(InvalidMeasurementError):
        AngularVelocity(Fraction(1), frequency.HERTZ)


def test_angle_and_displacement_share_their_units() -> None:
    assert angular.Radian(1).unit is angular.RADIAN
    assert angular.RadianDisplacement(1).unit is angular.RADIAN
    assert angular.RadianDisplacement(1).to(angular.DEGREE).unit is angular.DEGREE


def test_the_tables_list_the_units_by_symbol() -> None:
    assert set(angular.ANGULAR_DISPLACEMENT_UNITS) >= {"tr", "rad", symbols.DEGREE}
    assert set(angvel.ANGULAR_VELOCITY_UNITS) == {"tr/s", "rad/s", f"{symbols.DEGREE}/s", "rpm"}
    assert set(torque.TORQUE_UNITS) == {
        "J/tr",
        f"N{symbols.MIDDLE_DOT}m",
        f"mN{symbols.MIDDLE_DOT}m",
        f"kN{symbols.MIDDLE_DOT}m",
        f"lbf{symbols.MIDDLE_DOT}ft",
        f"lbf{symbols.MIDDLE_DOT}in",
    }


def test_results_display_in_the_units_people_read() -> None:
    assert str(energy.Joule(1) / angular.RadianDisplacement(1)) == f"1 N{symbols.MIDDLE_DOT}m"
    assert str(angvel.RadianPerSecond(5) * time.Second(2)) == "10 rad"
    assert str(angular.DegreeDisplacement(90) / time.Second(1)).endswith(" rad/s")
    assert (
        str(Torque.from_force(force.Newton(50), length.Metre(Fraction(1, 5))))
        == f"10 N{symbols.MIDDLE_DOT}m"
    )


def test_the_canonical_unit_is_what_magnitude_reads_in() -> None:
    assert torque.JoulePerTurn(3).magnitude == Fraction(3)
    assert angvel.TurnPerSecond(3).magnitude == Fraction(3)
    assert angular.TurnDisplacement(3).magnitude == Fraction(3)


def test_an_angular_velocity_can_be_viewed_as_a_frequency() -> None:
    from kuchka import BaudRate
    from kuchka import ConvertibleToFrequency

    assert isinstance(angvel.TurnPerSecond(1), ConvertibleToFrequency)
    assert not issubclass(BaudRate, ConvertibleToFrequency)


def test_force_stays_a_force() -> None:
    assert isinstance(force.Newton(1), Force)
