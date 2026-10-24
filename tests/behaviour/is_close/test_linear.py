"""`is_close` on linear quantities."""

from __future__ import annotations

import pytest

from kuchka import IncompatibleDimensionError
from kuchka.units import baud_rate
from kuchka.units import frequency
from kuchka.units import length
from kuchka.units import voltage


def test_linear_readings_within_the_tolerance_are_close() -> None:
    assert voltage.Volt(1).is_close(
        voltage.Volt(1.0004), tolerance=voltage.Millivolt(1)
    )


def test_linear_readings_outside_the_tolerance_are_not_close() -> None:
    assert not voltage.Volt(1).is_close(
        voltage.Volt(1.01), tolerance=voltage.Millivolt(1)
    )


def test_the_tolerance_boundary_is_inclusive_and_exact() -> None:
    assert length.Metre(1).is_close(length.Metre(1.001), tolerance=length.Millimetre(1))
    assert not length.Metre(1).is_close(
        length.Metre(1.0010000000000001), tolerance=length.Millimetre(1)
    )


def test_linear_readings_in_different_units_compare_by_value() -> None:
    assert length.Kilometre(1).is_close(
        length.Metre(1000.4), tolerance=length.Metre(0.5)
    )


def test_the_float_sum_is_close_to_its_ideal_value_but_not_equal() -> None:
    reading = voltage.Volt(0.1 + 0.2)
    assert reading != voltage.Volt(0.3)
    assert reading.is_close(voltage.Volt(0.3), tolerance=voltage.Volt(1e-12))


def test_linear_closeness_is_symmetric() -> None:
    a, b, tolerance = voltage.Volt(1), voltage.Volt(1.5), voltage.Volt(0.5)
    assert a.is_close(b, tolerance=tolerance) is b.is_close(a, tolerance=tolerance)


def test_a_zero_tolerance_means_exactly_equal() -> None:
    assert voltage.Volt(1).is_close(voltage.Millivolt(1000), tolerance=voltage.Volt(0))
    assert not voltage.Volt(0.1 + 0.2).is_close(
        voltage.Volt(0.3), tolerance=voltage.Volt(0)
    )


def test_closeness_is_not_transitive() -> None:
    a, b, c, tolerance = (
        voltage.Volt(0),
        voltage.Volt(0.8),
        voltage.Volt(1.6),
        voltage.Volt(1),
    )
    assert a.is_close(b, tolerance=tolerance)
    assert b.is_close(c, tolerance=tolerance)
    assert not a.is_close(c, tolerance=tolerance)


def test_two_types_that_share_a_dimension_are_not_comparable() -> None:
    with pytest.raises(IncompatibleDimensionError):
        frequency.Hertz(1).is_close(baud_rate.Baud(1), tolerance=frequency.Hertz(1))  # type: ignore[arg-type]
