"""Display: the text of a measurement depends on its value and the format spec alone.

`repr()`, `str()`, and `format()` turn an exact `Fraction` into text in a `Decimal`
context built for the purpose.
The precision, rounding mode, traps, and exponent range of the caller's active context
have no effect on the result, and the caller's flags are left as they were.
A tie rounds away from zero (`2.665` shows as `2.67` at two places), and the value is
rounded once, from its exact form.
"""

from __future__ import annotations

import decimal
from decimal import Context
from decimal import Decimal
from decimal import localcontext
from fractions import Fraction

import pytest

from kuchka import Celsius
from kuchka import Kilovolt
from kuchka import Volt
from kuchka.internal.display import DISPLAY_DIGITS
from kuchka.internal.display import DISPLAY_ROUNDING
from kuchka.internal.display import render
from kuchka.units import MILLIVOLT
from tests.quantity_families import CONCRETE_QUANTITY_TYPES
from tests.quantity_families import sample_of

ONE_THIRD = Fraction(1, 3)
TWO_THIRDS = Fraction(2, 3)

ROUNDING_MODES = [
    decimal.ROUND_UP,
    decimal.ROUND_DOWN,
    decimal.ROUND_CEILING,
    decimal.ROUND_FLOOR,
    decimal.ROUND_HALF_UP,
    decimal.ROUND_HALF_DOWN,
    decimal.ROUND_HALF_EVEN,
    decimal.ROUND_05UP,
]

HOSTILE_CONTEXTS = [
    pytest.param(Context(prec=1), id="precision_1"),
    pytest.param(Context(prec=5), id="precision_5"),
    pytest.param(Context(prec=100), id="precision_100"),
    pytest.param(Context(traps=[decimal.Inexact]), id="traps_inexact"),
    pytest.param(Context(traps=[decimal.Rounded, decimal.Inexact]), id="traps_rounded"),
    pytest.param(Context(Emax=10, Emin=-10), id="narrow_exponent_range"),
    *[pytest.param(Context(rounding=mode), id=mode.lower()) for mode in ROUNDING_MODES],
]

# (exact value, format spec, expected text)
RENDERINGS = [
    (ONE_THIRD, "f", "0.3333333333333333333333333333"),
    (TWO_THIRDS, "f", "0.6666666666666666666666666667"),
    (Fraction(21, 5), "f", "4.2"),
    (Fraction(1000000), "f", "1000000"),
    (Fraction(0), "f", "0"),
    (Fraction(-21, 5), "f", "-4.2"),
    (ONE_THIRD, ".2f", "0.33"),
    (TWO_THIRDS, ".2f", "0.67"),
    (Fraction(107, 40), ".2f", "2.68"),
    (Fraction(533, 200), ".2f", "2.67"),
    (Fraction(1, 8), ".2f", "0.13"),
    (Fraction(-107, 40), ".2f", "-2.68"),
    (Fraction(-1, 8), ".2f", "-0.13"),
    (Fraction(1, 200), ".2f", "0.01"),
    (Fraction(201, 200), ".2f", "1.01"),
    (Fraction(5, 2), ".0f", "3"),
    (Fraction(7, 2), ".0f", "4"),
    (TWO_THIRDS, ".5e", "6.66667e-1"),
    (TWO_THIRDS, ".5g", "0.66667"),
    (TWO_THIRDS, ".1%", "66.7%"),
    (Fraction(1234567891, 1000), "*>16,.1f", "*****1,234,567.9"),
    (Fraction(3), "+08.2f", "+0003.00"),
    (ONE_THIRD, ".30f", "0.333333333333333333333333333333"),
]
RENDERING_IDS = [f"{value}-{spec}" for value, spec, _ in RENDERINGS]


# The caller's decimal context has no effect.


@pytest.mark.parametrize("context", HOSTILE_CONTEXTS)
@pytest.mark.parametrize(("value", "spec", "expected"), RENDERINGS, ids=RENDERING_IDS)
def test_rendering_ignores_the_active_context(
    context: Context, value: Fraction, spec: str, expected: str
) -> None:
    with localcontext(context):
        assert render(value, spec) == expected


@pytest.mark.parametrize("context", HOSTILE_CONTEXTS)
def test_repr_and_format_ignore_the_active_context(context: Context) -> None:
    with localcontext(context):
        assert repr(Volt(ONE_THIRD)) == "0.3333333333333333333333333333 V"
        assert f"{Volt(Decimal('2.675')):.2f}" == "2.68 V"


@pytest.mark.parametrize("cls", CONCRETE_QUANTITY_TYPES, ids=lambda cls: cls.__name__)
def test_every_quantity_type_displays_independently_of_the_context(cls) -> None:
    value = sample_of(cls)
    expected = repr(value)
    hostile = Context(prec=3, rounding=decimal.ROUND_DOWN, traps=[decimal.Inexact])
    with localcontext(hostile):
        assert repr(value) == expected
        assert f"{value}" == expected


def test_the_active_contexts_flags_are_left_alone() -> None:
    with localcontext(Context()) as context:
        repr(Volt(ONE_THIRD))
        f"{Volt(ONE_THIRD):.4f}"
        assert not any(context.flags.values())


# Rounding: ties away from zero, applied once.


def test_the_display_rounding_mode_is_half_up() -> None:
    assert DISPLAY_ROUNDING == decimal.ROUND_HALF_UP


@pytest.mark.parametrize(
    ("literal", "expected"),
    [
        ("2.675", "2.68 V"),
        ("2.665", "2.67 V"),
        ("0.125", "0.13 V"),
        ("-2.675", "-2.68 V"),
        ("-2.665", "-2.67 V"),
        ("-0.125", "-0.13 V"),
    ],
)
def test_a_tie_rounds_away_from_zero(literal: str, expected: str) -> None:
    assert f"{Volt(Decimal(literal)):.2f}" == expected


def test_a_value_just_below_a_tie_rounds_down() -> None:
    value = Volt(Fraction(1, 8) - Fraction(1, 10**40))
    assert f"{value:.2f}" == "0.12 V"


def test_a_value_just_above_a_tie_rounds_up() -> None:
    value = Volt(Fraction(1, 8) + Fraction(1, 10**40))
    assert f"{value:.2f}" == "0.13 V"


def test_a_value_just_below_a_tie_of_the_negative_side_rounds_toward_zero() -> None:
    value = Volt(-(Fraction(1, 8) - Fraction(1, 10**40)))
    assert f"{value:.2f}" == "-0.12 V"


def test_rounding_to_the_display_digits_happens_once() -> None:
    # 0.5 - 10**-40 rounds to 0.5000000000000000000000000000 at 28 digits, a value
    # that then looks like a tie at one place.
    below = Volt(Fraction(1, 2) - Fraction(1, 10**40))
    assert f"{below:.0f}" == "0 V"
    assert f"{Volt(Fraction(1, 2)):.0f}" == "1 V"


# Digits.


def test_the_default_shows_twenty_eight_significant_digits() -> None:
    assert DISPLAY_DIGITS == 28  # noqa: PLR2004 -- the pinned default
    assert repr(Volt(ONE_THIRD)).removesuffix(" V") == "0." + "3" * 28


def test_an_exact_value_shows_exactly_with_no_padding() -> None:
    assert repr(Volt(4.2)) == "4.2 V"
    assert repr(Kilovolt(1).to(MILLIVOLT)) == "1000000 mV"


def test_a_precision_beyond_the_default_digits_is_honoured() -> None:
    assert f"{Volt(ONE_THIRD):.40f}" == "0." + "3" * 40 + " V"


def test_a_large_integer_part_is_never_cut_by_the_requested_precision() -> None:
    value = 10**2000 + 1
    assert f"{Volt(value):.2f}" == f"{value}.00 V"


def test_a_value_far_below_the_precision_rounds_to_zero() -> None:
    assert f"{Volt(Decimal('1E-30')):.2f}" == "0.00 V"


# Format spec surface.


def test_empty_spec_equals_repr_and_str() -> None:
    value = Volt(ONE_THIRD)
    assert f"{value}" == repr(value) == str(value)


def test_the_unit_symbol_follows_the_formatted_magnitude() -> None:
    assert f"{Celsius(20.5):.1f}".startswith("20.5 ")


def test_an_absurd_precision_raises_value_error() -> None:
    with pytest.raises(ValueError, match="too large"):
        f"{Volt(ONE_THIRD):.99999999999999999999f}"


def test_an_invalid_spec_raises_value_error() -> None:
    with pytest.raises(ValueError, match="format"):
        f"{Volt(1):.2x}"
