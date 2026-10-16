"""The format-spec surface of every quantity."""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka.units import thermal
from kuchka.units import voltage

ONE_THIRD = Fraction(1, 3)


def test_empty_spec_equals_repr_and_str() -> None:
    value = voltage.Volt(ONE_THIRD)
    assert f"{value}" == repr(value) == str(value)


def test_the_unit_symbol_follows_the_formatted_magnitude() -> None:
    assert f"{thermal.Celsius(20.5):.1f}".startswith("20.5 ")


def test_an_absurd_precision_raises_value_error() -> None:
    with pytest.raises(ValueError, match="too large"):
        f"{voltage.Volt(ONE_THIRD):.99999999999999999999f}"


def test_an_invalid_spec_raises_value_error() -> None:
    with pytest.raises(ValueError, match="format"):
        f"{voltage.Volt(1):.2x}"
