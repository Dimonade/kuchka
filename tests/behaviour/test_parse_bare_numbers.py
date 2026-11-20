"""`parse` reads a number with no unit where the quantity's table names a bare unit.

A proportion is a pure number, so `"0.25"` says everything `"0.25 1"` does, and
requiring the `1` is a surprise for the people who write the configuration.
Every other quantity needs its unit, because a bare `2.8` does not say whether it is
volts.
"""

from __future__ import annotations

from fractions import Fraction

import pytest
from hypothesis import given
from hypothesis import strategies as st

from kuchka import ParseError
from kuchka import Proportion
from kuchka import UnknownUnitError
from kuchka import Voltage
from kuchka import parse
from kuchka.dimensions import DIMENSIONLESS
from kuchka.units import proportion
from tests.support.kinds import QUANTITY_TYPES
from tests.support.kinds import UNIT_TABLES


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("0.25", Fraction(1, 4)),
        (".25", Fraction(1, 4)),
        ("1/4", Fraction(1, 4)),
        ("-0.5", Fraction(-1, 2)),
        ("\u22120.5", Fraction(-1, 2)),
        ("+5", Fraction(5)),
        ("1e-2", Fraction(1, 100)),
        ("  0.25  ", Fraction(1, 4)),
        ("0.25\u00a0", Fraction(1, 4)),
        ("\uff10.\uff12\uff15", Fraction(1, 4)),
        ("0", Fraction(0)),
    ],
)
def test_a_proportion_reads_without_a_unit_as_a_ratio(
    text: str, expected: Fraction
) -> None:
    result = parse(text, Proportion)
    assert result == proportion.Ratio(expected)
    assert result.unit is proportion.RATIO


def test_a_proportion_reads_the_same_with_the_unit_written() -> None:
    assert parse("0.25 1", Proportion) == parse("0.25", Proportion)
    assert parse("0.25 1", Proportion).unit is proportion.RATIO


def test_a_percent_keeps_its_unit() -> None:
    result = parse("25 %", Proportion)
    assert result == parse("0.25", Proportion)
    assert result.unit is proportion.PERCENT


def test_a_bare_number_is_a_ratio_and_not_a_percent() -> None:
    assert parse("25", Proportion) == proportion.Percent(2500)


@pytest.mark.parametrize("text", ["0.25 V", "0.25 x", "0.25 percentage", "0.25 %%"])
def test_a_proportion_with_any_other_unit_is_refused(text: str) -> None:
    with pytest.raises(UnknownUnitError):
        parse(text, Proportion)


@pytest.mark.parametrize("text", ["", "   ", "%", "abc", "nan", "inf", "0,25", "1_0"])
def test_text_that_is_no_number_is_refused_for_a_proportion(text: str) -> None:
    with pytest.raises(ParseError):
        parse(text, Proportion)


@pytest.mark.parametrize("text", ["5", "1/3", "5   ", "-5.5e3"])
def test_a_quantity_with_no_bare_unit_refuses_a_number_with_no_unit(text: str) -> None:
    with pytest.raises(ParseError, match="no unit"):
        parse(text, Voltage)


def test_only_the_proportion_names_a_bare_unit() -> None:
    named = {name for name, table in UNIT_TABLES.items() if table.bare is not None}
    assert named == {"PROPORTION_UNITS"}


def test_a_bare_unit_is_the_coherent_unit_of_a_dimensionless_quantity() -> None:
    for table in UNIT_TABLES.values():
        if table.bare is None:
            continue
        unit = table.bare[0]
        assert unit.dimension == DIMENSIONLESS  # type: ignore[attr-defined]
        assert unit.scale == 1  # type: ignore[attr-defined]


def test_every_other_quantity_type_refuses_a_number_with_no_unit() -> None:
    checked = []
    for quantity in QUANTITY_TYPES:
        table = vars(quantity).get("_unit_table")
        if table is None or table.bare is not None:
            continue
        with pytest.raises(ParseError, match="no unit"):
            parse("5", quantity)
        checked.append(quantity)
    assert Voltage in checked


@given(value=st.fractions(min_value=-1000, max_value=1000, max_denominator=10**6))
def test_a_ratio_reads_back_from_the_fraction_that_writes_it(value: Fraction) -> None:
    text = f"{value.numerator}/{value.denominator}"
    assert parse(text, Proportion) == proportion.Ratio(value)
