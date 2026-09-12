"""Tests for resistor_network.py.

This directory is documentation, not part of the installed `kuchka` package, so
`resistor_network` is imported by adding this directory to `sys.path`, not through a
package import.

Run with `pytest docs/examples/unrepresentable_dimensions` from the repository root,
or `pytest` from inside this directory.
"""

from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pytest
from resistor_network import parallel
from resistor_network import power_dissipation
from resistor_network import series

from kuchka import Ohm
from kuchka import Power
from kuchka import Resistance
from kuchka import Volt
from kuchka import Watt


def test_parallel_of_two_equal_resistors_halves_the_value() -> None:
    assert parallel(Ohm(100), Ohm(100)) == Ohm(50)


def test_parallel_of_two_unequal_resistors() -> None:
    assert parallel(Ohm(60), Ohm(30)) == Ohm(20)


def test_parallel_of_three_resistors() -> None:
    assert parallel(Ohm(10), Ohm(20), Ohm(20)) == Ohm(5)


def test_parallel_of_a_single_resistor_is_itself() -> None:
    assert parallel(Ohm(42)) == Ohm(42)


def test_parallel_result_is_a_resistance() -> None:
    assert isinstance(parallel(Ohm(60), Ohm(30)), Resistance)


def test_parallel_with_no_resistors_raises_zero_division_error() -> None:
    with pytest.raises(ZeroDivisionError):
        parallel()


def test_parallel_with_a_short_circuit_raises_zero_division_error() -> None:
    with pytest.raises(ZeroDivisionError):
        parallel(Ohm(0), Ohm(100))


def test_series_of_resistors_is_ordinary_addition() -> None:
    assert series(Ohm(60), Ohm(30)) == Ohm(90)


def test_series_of_a_single_resistor_is_itself() -> None:
    assert series(Ohm(42)) == Ohm(42)


def test_series_with_no_resistors_is_zero() -> None:
    assert series() == Ohm(0)


def test_parallel_scale_is_exact_not_approximate() -> None:
    """Two equal resistors of any magnitude halve exactly, not to 28 rounded digits."""
    assert parallel(Ohm(Decimal("3.3")), Ohm(Decimal("3.3"))) == Ohm(Decimal("1.65"))


def test_power_dissipation_matches_the_textbook_formula() -> None:
    power = power_dissipation(Volt(10), Ohm(5))
    assert isinstance(power, Power)
    assert power == power.to(power.unit)  # sanity: a real, comparable Power
    assert power == Watt(20)


def test_power_dissipation_scales_with_the_square_of_voltage() -> None:
    assert power_dissipation(Volt(20), Ohm(5)) == Watt(80)  # 4x the power at 2x V
