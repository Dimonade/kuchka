"""The units of a time cubed are exact cubes of the duration units."""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka.internal import symbols
from kuchka.units.kinematics import time_cubed
from kuchka.units.temporal import time as time_units


@pytest.mark.parametrize(
    ("duration", "cubed"),
    [
        (time_units.Nanosecond, time_cubed.NanosecondCubed),
        (time_units.Microsecond, time_cubed.MicrosecondCubed),
        (time_units.Millisecond, time_cubed.MillisecondCubed),
        (time_units.Second, time_cubed.SecondCubed),
        (time_units.Minute, time_cubed.MinuteCubed),
        (time_units.Hour, time_cubed.HourCubed),
    ],
    ids=["ns", "us", "ms", "s", "min", "h"],
)
def test_a_duration_cubed_is_the_cubed_unit(duration, cubed) -> None:
    assert duration(3) ** 3 == cubed(27)


@pytest.mark.parametrize(
    ("cubed", "seconds_cubed"),
    [
        (time_cubed.NanosecondCubed, Fraction(1, 10**27)),
        (time_cubed.MicrosecondCubed, Fraction(1, 10**18)),
        (time_cubed.MillisecondCubed, Fraction(1, 10**9)),
        (time_cubed.MinuteCubed, 216_000),
        (time_cubed.HourCubed, 46_656_000_000),
    ],
    ids=["ns", "us", "ms", "min", "h"],
)
def test_each_time_cubed_unit_has_its_scale_in_seconds_cubed(
    cubed, seconds_cubed
) -> None:
    assert cubed(1) == time_cubed.SecondCubed(seconds_cubed)


def test_the_time_cubed_table_lists_the_units_by_symbol() -> None:
    assert set(time_cubed.TIME_CUBED_UNITS) == {
        f"ns{symbols.SUPERSCRIPT_THREE}",
        f"{symbols.MICRO}s{symbols.SUPERSCRIPT_THREE}",
        f"ms{symbols.SUPERSCRIPT_THREE}",
        f"s{symbols.SUPERSCRIPT_THREE}",
        f"min{symbols.SUPERSCRIPT_THREE}",
        f"h{symbols.SUPERSCRIPT_THREE}",
    }
