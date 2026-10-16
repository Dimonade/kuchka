"""A motor and its shaft: speed, torque, power, work, and the mains frequency.

Rotation is where the angle axis matters: a shaft speed in rpm, a torque in
newton-metres, and a power in kilowatts are related by exact products, and a frequency
in hertz is not an angular velocity until it is converted by name.
"""

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
from kuchka.units import angular_velocity
from kuchka.units import energy
from kuchka.units import force
from kuchka.units import frequency
from kuchka.units import length
from kuchka.units import power
from kuchka.units import temporal
from kuchka.units import torque

SPEED = angular_velocity.RevolutionPerMinute(3000)
SHAFT = torque.NewtonMetre(20)


def test_shaft_power_is_torque_times_speed_exactly() -> None:
    delivered = SHAFT * SPEED
    assert type(delivered) is Power
    assert delivered == power.Watt(2000 * PI)
    assert delivered / SPEED == SHAFT
    assert delivered / SHAFT == SPEED


def test_the_turns_in_a_minute_run_at_the_speed_given() -> None:
    swept = SPEED * temporal.Minute(1)
    assert type(swept) is AngularDisplacement
    assert swept == angular.TurnDisplacement(3000)
    assert swept.to(angular.TURN).value_in(angular.TURN) == Fraction(3000)


def test_the_work_done_over_a_quarter_turn() -> None:
    work = SHAFT * angular.TurnDisplacement(Fraction(1, 4))
    assert type(work) is Energy
    assert work == energy.Joule(10 * PI)


def test_a_force_on_a_lever_arm_is_a_torque_by_name_and_not_by_product() -> None:
    lever = length.Metre(Fraction(1, 5))
    pull = force.Newton(100)
    assert Torque.from_force(pull, lever) == SHAFT
    assert type(pull * lever) is Energy


def test_the_mains_frequency_becomes_a_speed_only_by_conversion() -> None:
    mains = frequency.Hertz(50)
    with pytest.raises(IncompatibleDimensionError):
        mains + SPEED  # type: ignore[operator]
    speed = mains.to_angular_velocity()
    assert type(speed) is AngularVelocity
    assert speed == angular_velocity.RevolutionPerMinute(3000)
    assert speed.to_frequency() == mains


def test_a_gearbox_scales_speed_and_torque_inversely() -> None:
    ratio = Fraction(5)
    output_speed = SPEED / ratio
    output_torque = SHAFT * ratio
    assert output_speed == angular_velocity.RevolutionPerMinute(600)
    assert output_torque * output_speed == SHAFT * SPEED


def test_results_read_in_the_units_an_engineer_reads() -> None:
    assert str(SHAFT * SPEED).endswith(" W")
    assert str(power.Kilowatt(2) / SPEED).endswith(" N\u00b7m")
    assert str(SPEED * temporal.Second(1)).endswith(" rad")
