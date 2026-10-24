"""Digits and the significant-figure limit."""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction

from kuchka.internal.display import DISPLAY_DIGITS
from kuchka.units.electromagnetics import voltage

ONE_THIRD = Fraction(1, 3)


def test_the_default_shows_twenty_eight_significant_digits() -> None:
    assert DISPLAY_DIGITS == 28  # noqa: PLR2004 -- the pinned default
    assert repr(voltage.Volt(ONE_THIRD)).removesuffix(" V") == "0." + "3" * 28


def test_an_exact_value_shows_exactly_with_no_padding() -> None:
    assert repr(voltage.Volt(4.2)) == "4.2 V"
    assert repr(voltage.Kilovolt(1).to(voltage.MILLIVOLT)) == "1000000 mV"


def test_a_precision_beyond_the_default_digits_is_honoured() -> None:
    assert f"{voltage.Volt(ONE_THIRD):.40f}" == "0." + "3" * 40 + " V"


def test_a_large_integer_part_is_never_cut_by_the_requested_precision() -> None:
    value = 10**2000 + 1
    assert f"{voltage.Volt(value):.2f}" == f"{value}.00 V"


def test_a_value_far_below_the_precision_rounds_to_zero() -> None:
    assert f"{voltage.Volt(Decimal('1E-30')):.2f}" == "0.00 V"
