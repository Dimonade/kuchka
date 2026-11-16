"""Instant: a point in time, reached from any Time value, and its arithmetic with Time.

Instant is the affine counterpart to Time.
It is a reading on a scale, similar to the relationship between Temperature and
TemperatureDelta.
"""

from decimal import Decimal

import pytest

from kuchka import IncompatibleDimensionError
from kuchka import Instant
from kuchka import MeasurementError
from kuchka import Time
from kuchka.units.temporal import instant
from kuchka.units.temporal import time


def test_time_as_instant_returns_an_instant():
    reading = time.Second(1_700_000_000).to_instant()
    assert isinstance(reading, Instant)


def test_instant_plus_time_is_an_instant():
    later = time.Second(100).to_instant() + time.Second(42)
    assert isinstance(later, Instant)
    assert later == time.Second(142).to_instant()


def test_instant_minus_instant_is_a_time():
    elapsed = time.Second(142).to_instant() - time.Second(100).to_instant()
    assert isinstance(elapsed, Time)
    assert elapsed == time.Second(42)


def test_time_plus_instant_also_works_reflected():
    assert (
        time.Second(42) + time.Second(100).to_instant() == time.Second(142).to_instant()
    )


def test_any_time_prefix_reaches_the_same_instant():
    """Millisecond, Second, and Hour all read into the same Instant scale."""
    assert time.Millisecond(1000).to_instant() == time.Second(1).to_instant()
    assert time.Hour(1).to_instant() == time.Second(3600).to_instant()


def test_adding_two_instants_is_rejected_with_a_physical_explanation():
    with pytest.raises(MeasurementError, match="point on a scale"):
        time.Second(100).to_instant() + time.Second(1).to_instant()  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_rejection_message_has_correct_article_agreement():
    """A regression check for the a/an article-agreement bug the base class had."""
    with pytest.raises(MeasurementError) as excinfo:
        time.Second(100).to_instant() + time.Second(1).to_instant()  # type: ignore[operator]  # ty: ignore[unsupported-operator]
    assert "a `Instant`" not in str(excinfo.value)
    assert "an `Instant`" not in str(excinfo.value)


def test_instant_before_the_callers_own_zero_point_is_valid():
    """Unlike Temperature, an Instant has no absolute-zero-style lower bound."""
    before = time.Second(-100).to_instant()
    assert before.value_in(time.Second(0).to_instant().unit) == Decimal(-100)


def test_instant_ordering():
    assert time.Second(1).to_instant() < time.Second(2).to_instant()
    assert time.Second(2).to_instant() > time.Second(1).to_instant()


def test_instant_minus_time_shifts_the_reading_down():
    assert (
        time.Second(100).to_instant() - time.Second(42) == time.Second(58).to_instant()
    )


def test_instant_plus_millisecond_time_stays_exact():
    shifted = time.Second(1).to_instant() + time.Millisecond(500)
    assert shifted == time.Second(2).to_instant() - time.Millisecond(500)


def test_instant_is_incompatible_with_a_different_affine_type():
    from kuchka import Celsius

    with pytest.raises(IncompatibleDimensionError):
        time.Second(1).to_instant() + Celsius(5)  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_repr_shows_the_display_unit_symbol():
    assert repr(time.Second(42).to_instant()) == "42 s"


def test_instant_units_table_resolves_seconds():
    assert (
        instant.INSTANT_UNITS["s"](1_700_000_000)
        == time.Second(1_700_000_000).to_instant()
    )
