"""Levels compare, hash, and order by their exact value."""

from __future__ import annotations

import pytest

from kuchka import IncompatibleDimensionError
from kuchka.units import logarithmic
from kuchka.units import proportion


def test_equality_compares_the_level_across_units():
    assert logarithmic.Bel(0.3) == logarithmic.Decibel(3)
    assert logarithmic.Decibel(3) != logarithmic.Decibel(3.001)


def test_equal_levels_hash_equally():
    assert hash(logarithmic.Bel(1)) == hash(logarithmic.Decibel(10))
    assert {logarithmic.Bel(1), logarithmic.Decibel(10), logarithmic.Decibel(20)} == {
        logarithmic.Decibel(10),
        logarithmic.Decibel(20),
    }


def test_a_level_never_equals_a_linear_ratio():
    assert logarithmic.Decibel(0) != proportion.Ratio(1)
    assert logarithmic.Decibel(3) != proportion.Ratio(3)
    plain_number = 3
    assert logarithmic.Decibel(3) != plain_number


def test_ordering_follows_the_level():
    assert logarithmic.Decibel(-3) < logarithmic.Decibel(0) < logarithmic.Decibel(3)
    assert logarithmic.Bel(1) > logarithmic.Decibel(9)
    assert logarithmic.Bel(1) >= logarithmic.Decibel(10)
    assert logarithmic.Decibel(-10) <= logarithmic.Bel(-1)
    assert sorted(
        [logarithmic.Decibel(3), logarithmic.Decibel(-6), logarithmic.Bel(0.5)]
    ) == [
        logarithmic.Decibel(-6),
        logarithmic.Decibel(3),
        logarithmic.Decibel(5),
    ]


def test_comparing_with_a_linear_ratio_is_a_dimension_error():
    with pytest.raises(IncompatibleDimensionError, match="distinct concepts"):
        logarithmic.Decibel(3) < proportion.Ratio(2)  # noqa: B015  # type: ignore[operator]
