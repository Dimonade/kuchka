"""`Torque` is energy per angle."""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka import AngularDisplacement
from kuchka import AngularVelocity
from kuchka import Energy
from kuchka import IncompatibleDimensionError
from kuchka import Power
from kuchka import Torque
from kuchka.internal.constants import PI
from kuchka.units import angular
from kuchka.units import angular_velocity as angvel
from kuchka.units import energy
from kuchka.units import force
from kuchka.units import length
from kuchka.units import power as power_units
from kuchka.units import torque as torque_units


def test_energy_per_angle_is_torque() -> None:
    result = energy.Joule(1) / angular.RadianDisplacement(1)
    assert type(result) is Torque
    assert result == torque_units.NewtonMetre(1)


def test_torque_times_angular_displacement_is_energy_exactly() -> None:
    work = torque_units.NewtonMetre(10) * angular.RadianDisplacement(2)
    assert type(work) is Energy
    assert work == energy.Joule(20)
    assert angular.RadianDisplacement(2) * torque_units.NewtonMetre(10) == energy.Joule(
        20
    )


def test_energy_per_torque_is_angular_displacement() -> None:
    result = energy.Joule(20) / torque_units.NewtonMetre(10)
    assert type(result) is AngularDisplacement
    assert result == angular.RadianDisplacement(2)


def test_torque_times_angular_velocity_is_power_exactly() -> None:
    power = torque_units.NewtonMetre(2) * angvel.RadianPerSecond(5)
    assert type(power) is Power
    assert power == power_units.Watt(10)
    assert angvel.RadianPerSecond(5) * torque_units.NewtonMetre(2) == power_units.Watt(
        10
    )


def test_power_per_angular_velocity_is_torque_and_per_torque_is_velocity() -> None:
    assert power_units.Watt(10) / angvel.RadianPerSecond(5) == torque_units.NewtonMetre(
        2
    )
    assert type(power_units.Watt(10) / angvel.RadianPerSecond(5)) is Torque
    assert power_units.Watt(10) / torque_units.NewtonMetre(2) == angvel.RadianPerSecond(
        5
    )
    assert type(power_units.Watt(10) / torque_units.NewtonMetre(2)) is AngularVelocity


def test_a_force_at_a_distance_is_a_torque_by_name() -> None:
    torque = Torque.from_force(force.Newton(50), length.Metre(Fraction(1, 5)))
    assert type(torque) is Torque
    assert torque == torque_units.NewtonMetre(10)


def test_a_force_times_a_length_is_energy_not_torque() -> None:
    assert type(force.Newton(5) * length.Metre(2)) is Energy


def test_a_torque_is_built_from_a_force_and_a_length() -> None:
    with pytest.raises(IncompatibleDimensionError, match="build a torque from"):
        Torque.from_force(length.Metre(1), force.Newton(1))  # type: ignore[arg-type]
    with pytest.raises(IncompatibleDimensionError):
        Torque.from_force(force.Newton(1), force.Newton(1))  # type: ignore[arg-type]


def test_torque_units_scale_exactly() -> None:
    assert torque_units.NewtonMetre(1) == torque_units.JoulePerTurn(2 * PI)
    assert torque_units.PoundForceFoot(12) == torque_units.PoundForceInch(144)
    pound_force = force.Newton(Fraction("4.4482216152605"))
    foot = length.Metre(Fraction("0.3048"))
    assert torque_units.PoundForceFoot(1) == Torque.from_force(pound_force, foot)
