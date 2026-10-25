"""The caller's decimal context has no effect on rendering."""

from __future__ import annotations

import decimal
from decimal import Context
from decimal import Decimal
from decimal import localcontext
from fractions import Fraction

import pytest

from kuchka.internal.display import render
from kuchka.units.electromagnetics import voltage
from tests.support.kinds import QUANTITY_TYPES
from tests.support.kinds import sample_of

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
        assert repr(voltage.Volt(ONE_THIRD)) == "0.3333333333333333333333333333 V"
        assert f"{voltage.Volt(Decimal('2.675')):.2f}" == "2.68 V"


@pytest.mark.parametrize("cls", QUANTITY_TYPES, ids=lambda cls: cls.__name__)
def test_every_quantity_type_displays_independently_of_the_context(cls) -> None:
    value = sample_of(cls)
    expected = repr(value)
    hostile = Context(prec=3, rounding=decimal.ROUND_DOWN, traps=[decimal.Inexact])
    with localcontext(hostile):
        assert repr(value) == expected
        assert f"{value}" == expected


def test_the_active_contexts_flags_are_left_alone() -> None:
    with localcontext(Context()) as context:
        repr(voltage.Volt(ONE_THIRD))
        f"{voltage.Volt(ONE_THIRD):.4f}"
        assert not any(context.flags.values())
