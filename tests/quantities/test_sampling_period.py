"""SamplingPeriod: reached from any Time value, and shared with Time's own units.

SamplingPeriod is dimensionally identical to Time, reciprocal to SampleRate, and
reached through Time.to_sampling_period().
"""

from decimal import Decimal

import pytest

from kuchka import IncompatibleDimensionError
from kuchka import InvalidMeasurementError
from kuchka import SampleRate
from kuchka import SamplingPeriod
from kuchka.units import sample_rate
from kuchka.units import sampling_period as sp
from kuchka.units import time
from kuchka.units import voltage


def test_time_as_sampling_period_returns_a_sampling_period():
    period = time.Millisecond(2).to_sampling_period()
    assert isinstance(period, SamplingPeriod)


def test_any_time_prefix_reaches_the_same_sampling_period():
    """Millisecond, Second, and Hour all read into the same SamplingPeriod scale."""
    assert (
        time.Millisecond(1000).to_sampling_period()
        == time.Second(1).to_sampling_period()
    )
    assert time.Hour(1).to_sampling_period() == time.Second(3600).to_sampling_period()


def test_sampling_period_addition_and_prefix_conversion():
    total = (
        time.Second(1).to_sampling_period() + time.Millisecond(500).to_sampling_period()
    )
    assert total == time.Second(Decimal("1.5")).to_sampling_period()


def test_sampling_period_is_incompatible_with_time():
    """A SamplingPeriod and a Time share a dimension but stay different concepts."""
    with pytest.raises(IncompatibleDimensionError):
        time.Second(1).to_sampling_period() + time.Second(1)  # type: ignore[operator]

    assert (time.Second(1).to_sampling_period() == time.Second(1)) is False


def test_sampling_period_reciprocal_is_sample_rate():
    rate = 1 / time.Millisecond(2).to_sampling_period()
    assert isinstance(rate, SampleRate)
    assert rate == sample_rate.SamplesPerSecond(500)


def test_sample_rate_reciprocal_is_sampling_period():
    period = 1 / sample_rate.KilosamplesPerSecond(2)
    assert isinstance(period, SamplingPeriod)
    assert period == time.Millisecond(Decimal("0.5")).to_sampling_period()


def test_naked_number_addition_is_rejected():
    with pytest.raises(InvalidMeasurementError, match="wrap it in a unit constructor"):
        time.Second(1).to_sampling_period() + 4.2  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_sampling_period_is_incompatible_with_voltage():
    with pytest.raises(IncompatibleDimensionError):
        time.Second(1).to_sampling_period() + voltage.Volt(1)  # type: ignore[operator]  # not (yet) flagged by ty across sibling quantity types


def test_scalar_multiplication_and_division():
    period = time.Second(2).to_sampling_period()
    assert period * 3 == time.Second(6).to_sampling_period()
    assert (period * 3) / 3 == period


def test_ordering_within_sampling_period():
    assert (
        time.Millisecond(500).to_sampling_period() < time.Second(1).to_sampling_period()
    )


def test_repr_shows_the_display_unit_symbol():
    assert repr(time.Second(42).to_sampling_period()) == "42 s"


def test_sampling_period_units_table_resolves_every_symbol():
    assert sp.SAMPLING_PERIOD_UNITS["ms"](2) == time.Millisecond(2).to_sampling_period()
    assert sp.SAMPLING_PERIOD_UNITS["s"](1) == time.Second(1).to_sampling_period()
