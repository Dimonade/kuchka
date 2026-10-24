"""Data and DataRate: the arithmetic that relates them to time, and their units.

Generic algebraic properties and the scale of every unit are covered once for all
quantities elsewhere; this module covers what is specific to information:
`Data / Time`, `DataRate * Time`, and the decimal and binary sizes that differ.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka import Data
from kuchka import DataRate
from kuchka import Frequency
from kuchka import IncompatibleDimensionError
from kuchka import Proportion
from kuchka import Time
from kuchka.units import data
from kuchka.units import data_rate
from kuchka.units import frequency
from kuchka.units import proportion
from kuchka.units import time


def test_data_over_time_is_a_data_rate() -> None:
    rate = data.Mebibyte(300) / time.Second(60)
    assert isinstance(rate, DataRate)
    assert rate == data_rate.MebibytePerSecond(5)


def test_a_data_rate_over_a_period_is_data_in_both_orders() -> None:
    link = data_rate.GigabitPerSecond(1)
    assert isinstance(link * time.Second(1), Data)
    assert link * time.Second(8) == data.Gigabyte(1)
    assert time.Second(8) * link == data.Gigabyte(1)


def test_data_over_a_data_rate_is_the_time_it_takes() -> None:
    duration = data.Gibibyte(4) / data_rate.MegabytePerSecond(100)
    assert isinstance(duration, Time)
    assert duration == time.Second(Fraction(4 * 1024**3, 100 * 10**6))


def test_a_data_rate_over_a_frequency_is_the_data_of_each_cycle() -> None:
    frame = data_rate.KibibytePerSecond(4000) / frequency.Hertz(1000)
    assert isinstance(frame, Data)
    assert frame == data.Kibibyte(4)


def test_data_times_a_frequency_is_a_data_rate() -> None:
    rate = frequency.Hertz(1000) * data.Kibibyte(4)
    assert isinstance(rate, DataRate)
    assert rate == data_rate.KibibytePerSecond(4000)


def test_a_data_rate_over_data_is_a_frequency() -> None:
    blocks = data_rate.MebibytePerSecond(8) / data.Mebibyte(2)
    assert isinstance(blocks, Frequency)
    assert blocks == frequency.Hertz(4)


def test_data_over_data_is_a_proportion() -> None:
    ratio = data.Megabyte(1) / data.Kibibyte(1)
    assert isinstance(ratio, Proportion)
    assert ratio.magnitude == Fraction(10**6, 1024)


def test_a_proportion_scales_data_and_keeps_its_type() -> None:
    assert proportion.Percent(50) * data.Kibibyte(2) == data.Kibibyte(1)
    assert data.Kibibyte(2) * proportion.Percent(50) == data.Kibibyte(1)
    assert isinstance(proportion.Percent(50) * data_rate.BitPerSecond(8), DataRate)


def test_a_marketed_terabyte_holds_less_than_a_tebibyte() -> None:
    assert data.Terabyte(1) < data.Tebibyte(1)
    assert data.Terabyte(1) == data.Gigabyte(1000)
    assert data.Tebibyte(1) == data.Gibibyte(1024)


def test_the_sizes_in_the_two_families_never_coincide_above_the_byte() -> None:
    assert data.Kilobyte(1) != data.Kibibyte(1)
    assert data.Megabit(1) != data.Mebibit(1)


def test_a_byte_is_eight_bits_and_a_bit_is_not_a_byte() -> None:
    assert data.Byte(1) == data.Bit(8)
    assert data.Bit(1) != data.Byte(1)


def test_data_displays_in_the_unit_it_was_built_in() -> None:
    assert repr(data.Kibibyte(2)) == "2 KiB"
    assert repr(data_rate.MegabitPerSecond(100)) == "100 Mbit/s"


def test_conversion_between_the_families_is_exact() -> None:
    assert data.Kibibyte(1).to(data.KILOBYTE) == data.Kilobyte(Fraction(128, 125))
    assert data.Megabyte(1).to(data.MEBIBYTE) == data.Mebibyte(Fraction(10**6, 1024**2))


def test_a_data_rate_is_not_a_frequency() -> None:
    with pytest.raises(IncompatibleDimensionError):
        data_rate.BitPerSecond(1) + frequency.Hertz(1)  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_data_is_incompatible_with_a_data_rate_and_with_time() -> None:
    with pytest.raises(IncompatibleDimensionError):
        data.Byte(1) + data_rate.BytePerSecond(1)  # type: ignore[operator]  # ty: ignore[unsupported-operator]
    with pytest.raises(IncompatibleDimensionError):
        data.Byte(1) + time.Second(1)  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_a_unit_of_data_does_not_build_a_data_rate() -> None:
    assert isinstance(data.Byte(1), Data)
    assert not isinstance(data.Byte(1), DataRate)
