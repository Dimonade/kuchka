"""Activity: the becquerel and the curie, a role of Frequency.

The generic role behaviour (refusals, scaling) is covered once for every role in
`test_role_kinds`; this module covers what is specific to activity and its units.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka import Activity
from kuchka import Frequency
from kuchka import IncompatibleDimensionError
from kuchka import Proportion
from kuchka.units import proportion
from kuchka.units.radiation import activity
from kuchka.units.temporal import frequency
from kuchka.units.temporal import time


def test_a_curie_is_exactly_37_billion_becquerel() -> None:
    assert activity.Curie(1) == activity.Becquerel(37_000_000_000)


def test_the_prefixed_curies_are_exact_multiples_of_the_becquerel() -> None:
    assert activity.Millicurie(1) == activity.Megabecquerel(37)
    assert activity.Microcurie(1) == activity.Kilobecquerel(37)
    assert activity.Picocurie(1) == activity.Millibecquerel(37)


def test_a_radon_reading_converts_exactly() -> None:
    reading = activity.Picocurie(4).to(activity.BECQUEREL)
    assert reading == activity.Millibecquerel(148)
    assert repr(reading) == "0.148 Bq"


def test_to_frequency_carries_the_value_over() -> None:
    taken = activity.Kilobecquerel(3).to_frequency()
    assert isinstance(taken, Frequency)
    assert taken == frequency.Kilohertz(3)


def test_the_decays_over_a_time_go_through_the_frequency() -> None:
    source = activity.Becquerel(5)
    with pytest.raises(IncompatibleDimensionError, match="to_frequency"):
        source * time.Second(10)
    assert source.to_frequency() * time.Second(10) == Fraction(50)


def test_an_activity_and_a_frequency_do_not_mix() -> None:
    with pytest.raises(IncompatibleDimensionError):
        activity.Becquerel(1) + frequency.Hertz(1)  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_an_activity_has_no_hertz_and_a_frequency_has_no_becquerel() -> None:
    assert "Hz" not in activity.ACTIVITY_UNITS
    assert "Bq" not in frequency.FREQUENCY_UNITS


def test_after_one_half_life_half_of_the_activity_is_left() -> None:
    remaining = activity.Megabecquerel(37) * proportion.Percent(50)
    assert isinstance(remaining, Activity)
    assert remaining == activity.Megabecquerel(18.5)


def test_the_ratio_of_two_activities_is_a_proportion() -> None:
    ratio = activity.Millicurie(1) / activity.Megabecquerel(74)
    assert isinstance(ratio, Proportion)
    assert ratio == proportion.Ratio(Fraction(1, 2))
