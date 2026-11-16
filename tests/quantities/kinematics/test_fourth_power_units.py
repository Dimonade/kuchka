"""The units of a time to the fourth power are exact fourth powers of the durations."""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka.internal import symbols
from kuchka.units.kinematics import time_fourth_power as fourth
from kuchka.units.temporal import time as time_units


@pytest.mark.parametrize(
    ("duration", "powered"),
    [
        (time_units.Nanosecond, fourth.NanosecondFourthPower),
        (time_units.Microsecond, fourth.MicrosecondFourthPower),
        (time_units.Millisecond, fourth.MillisecondFourthPower),
        (time_units.Second, fourth.SecondFourthPower),
        (time_units.Minute, fourth.MinuteFourthPower),
        (time_units.Hour, fourth.HourFourthPower),
    ],
    ids=["ns", "us", "ms", "s", "min", "h"],
)
def test_a_duration_to_the_fourth_power_is_the_fourth_power_unit(
    duration, powered
) -> None:
    assert duration(2) ** 4 == powered(16)


@pytest.mark.parametrize(
    ("powered", "seconds_to_the_fourth"),
    [
        (fourth.NanosecondFourthPower, Fraction(1, 10**36)),
        (fourth.MicrosecondFourthPower, Fraction(1, 10**24)),
        (fourth.MillisecondFourthPower, Fraction(1, 10**12)),
        (fourth.MinuteFourthPower, 12_960_000),
        (fourth.HourFourthPower, 167_961_600_000_000),
    ],
    ids=["ns", "us", "ms", "min", "h"],
)
def test_each_fourth_power_unit_has_its_scale_in_seconds_to_the_fourth(
    powered, seconds_to_the_fourth
) -> None:
    assert powered(1) == fourth.SecondFourthPower(seconds_to_the_fourth)


def test_the_fourth_power_table_lists_the_units_by_symbol() -> None:
    assert set(fourth.TIME_FOURTH_POWER_UNITS) == {
        f"ns{symbols.SUPERSCRIPT_FOUR}",
        f"{symbols.MICRO}s{symbols.SUPERSCRIPT_FOUR}",
        f"ms{symbols.SUPERSCRIPT_FOUR}",
        f"s{symbols.SUPERSCRIPT_FOUR}",
        f"min{symbols.SUPERSCRIPT_FOUR}",
        f"h{symbols.SUPERSCRIPT_FOUR}",
    }
