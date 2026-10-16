"""Acquiring a signal: sample rate, record length, serial link, and gain in decibels.

A capture is described with a sampling rate, a record length in time, and a serial link
in baud; the analogue front end is a chain of gains in decibels.
The roles of the rates stay apart, and the conversions between them are by name.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka import BaudRate
from kuchka import Frequency
from kuchka import IncompatibleDimensionError
from kuchka import LogarithmicRatio
from kuchka import SampleRate
from kuchka import SamplingPeriod
from kuchka.units import baud_rate
from kuchka.units import frequency
from kuchka.units import logarithmic
from kuchka.units import proportion
from kuchka.units import sample_rate
from kuchka.units import sampling_period
from kuchka.units import temporal
from kuchka.units import voltage

RATE = sample_rate.KilosamplesPerSecond(48)


def test_a_rate_and_its_period_are_reciprocal_roles() -> None:
    period = 1 / RATE
    assert type(period) is SamplingPeriod
    assert type(1 / period) is SampleRate
    assert 1 / period == RATE


def test_the_samples_in_a_record_are_a_plain_count() -> None:
    samples = RATE * temporal.Second(2)
    assert samples == Fraction(96_000)
    assert type(samples) is Fraction


def test_a_sample_rate_is_not_a_frequency_until_it_is_viewed_as_one() -> None:
    carrier = frequency.Kilohertz(48)
    with pytest.raises(IncompatibleDimensionError):
        RATE + carrier  # type: ignore[operator]
    viewed = RATE.to_frequency()
    assert type(viewed) is Frequency
    assert viewed == carrier


def test_a_baud_rate_has_no_frequency_to_view_as() -> None:
    link = baud_rate.Baud(115_200)
    assert type(link) is BaudRate
    assert not hasattr(link, "to_frequency")
    with pytest.raises(IncompatibleDimensionError):
        link + frequency.Hertz(115_200)  # type: ignore[operator]


def test_a_sampling_period_prints_in_the_unit_it_is_given() -> None:
    period = sampling_period.SAMPLING_PERIOD_UNITS["us"](Fraction(125, 6))
    assert period.to(temporal.MICROSECOND).value_in(temporal.MICROSECOND) == Fraction(
        125, 6
    )
    assert type(1 / period) is SampleRate


def test_gain_stages_add_in_decibels_and_multiply_as_ratios() -> None:
    preamp = logarithmic.Decibel(20)
    filter_loss = logarithmic.Decibel(-6)
    total = preamp + filter_loss
    assert type(total) is LogarithmicRatio
    assert total == logarithmic.Decibel(14)
    assert preamp.to_power_ratio() == proportion.Ratio(100)
    assert preamp.to_field_ratio() == proportion.Ratio(10)


def test_a_voltage_ratio_becomes_a_level() -> None:
    gain = logarithmic.LogarithmicRatio.from_field_ratio(proportion.Ratio(10))
    assert gain == logarithmic.Decibel(20)
    assert voltage.Volt(1) * proportion.Ratio(10) == voltage.Volt(10)
