"""Specific tests for `kuchka.prefixes`.

Includes the `Prefix` dataclass itself, and the `prefixed_unit()` and `with_prefix()`
helpers.

Every expected scale is hand written as an independent decimal literal to avoid
testing against the implementation of itself, which would always be true.
"""

from __future__ import annotations

import dataclasses
from decimal import Decimal
from fractions import Fraction
from typing import TYPE_CHECKING

import pytest

from kuchka.dimensions import LENGTH
from kuchka.dimensions import MASS
from kuchka.dimensions import VOLTAGE
from kuchka.internal import prefixes
from kuchka.internal import symbols
from kuchka.internal.prefixes import prefixed_unit
from kuchka.internal.prefixes import with_prefix
from kuchka.quantities.base import AffineUnitDef
from kuchka.quantities.base import UnitDef
from kuchka.units import length
from kuchka.units import mass
from kuchka.units import thermal
from kuchka.units.electromagnetics import voltage

if TYPE_CHECKING:
    from kuchka.internal.prefixes import Prefix

PREFIX_TABLE_CASES = [
    (prefixes.QUECTO, -30, Decimal("0.000000000000000000000000000001"), "quecto", "q"),
    (prefixes.RONTO, -27, Decimal("0.000000000000000000000000001"), "ronto", "r"),
    (prefixes.YOCTO, -24, Decimal("0.000000000000000000000001"), "yocto", "y"),
    (prefixes.ZEPTO, -21, Decimal("0.000000000000000000001"), "zepto", "z"),
    (prefixes.ATTO, -18, Decimal("0.000000000000000001"), "atto", "a"),
    (prefixes.FEMTO, -15, Decimal("0.000000000000001"), "femto", "f"),
    (prefixes.PICO, -12, Decimal("0.000000000001"), "pico", "p"),
    (prefixes.NANO, -9, Decimal("0.000000001"), "nano", "n"),
    (prefixes.MICRO, -6, Decimal("0.000001"), "micro", symbols.MICRO),
    (prefixes.MILLI, -3, Decimal("0.001"), "milli", "m"),
    (prefixes.CENTI, -2, Decimal("0.01"), "centi", "c"),
    (prefixes.DECI, -1, Decimal("0.1"), "deci", "d"),
    (prefixes.UNIT, 0, Decimal(1), "", ""),
    (prefixes.DECA, 1, Decimal(10), "deca", "da"),
    (prefixes.HECTO, 2, Decimal(100), "hecto", "h"),
    (prefixes.KILO, 3, Decimal(1_000), "kilo", "k"),
    (prefixes.MEGA, 6, Decimal(1_000_000), "mega", "M"),
    (prefixes.GIGA, 9, Decimal(1_000_000_000), "giga", "G"),
    (prefixes.TERA, 12, Decimal(1_000_000_000_000), "tera", "T"),
    (prefixes.PETA, 15, Decimal(1_000_000_000_000_000), "peta", "P"),
    (prefixes.EXA, 18, Decimal(1_000_000_000_000_000_000), "exa", "E"),
    (prefixes.ZETTA, 21, Decimal(1_000_000_000_000_000_000_000), "zetta", "Z"),
    (prefixes.YOTTA, 24, Decimal(1_000_000_000_000_000_000_000_000), "yotta", "Y"),
    (prefixes.RONNA, 27, Decimal(1_000_000_000_000_000_000_000_000_000), "ronna", "R"),
    (
        prefixes.QUETTA,
        30,
        Decimal(1_000_000_000_000_000_000_000_000_000_000),
        "quetta",
        "Q",
    ),
]

PREFIX_TABLE_IDS = [name for _, _, _, name, _ in PREFIX_TABLE_CASES]
PREFIX_TABLE_IDS[7] = "unit"  # UNIT's own name is "", give it a readable test id.

ALL_PREFIXES = [prefix for prefix, *_ in PREFIX_TABLE_CASES]


@pytest.mark.parametrize(
    ("prefix", "exponent", "factor", "name", "symbol"),
    PREFIX_TABLE_CASES,
    ids=PREFIX_TABLE_IDS,
)
def test_prefix_matches_its_independently_known_value(
    prefix: Prefix, exponent: int, factor: Decimal, name: str, symbol: str
) -> None:
    assert prefix.exponent == exponent
    assert prefix.factor == factor
    assert prefix.name == name
    assert prefix.symbol == symbol


def test_micro_symbol_is_the_micro_sign_not_greek_mu():
    """Test that the U+00B5 vs U+03BC symbols render identically."""
    assert prefixes.MICRO.symbol == symbols.MICRO
    assert prefixes.MICRO.symbol != symbols.SMALL_MICRO


def test_factor_is_always_a_decimal_not_a_float():
    assert isinstance(prefixes.PICO.factor, Decimal)
    assert isinstance(prefixes.PETA.factor, Decimal)


def test_extreme_factors_agree_with_integer_exponentiation():
    """A second, independently-computed check on the two widest prefixes."""
    assert prefixes.FEMTO.factor == Decimal(1) / Decimal(10) ** 15
    assert prefixes.PETA.factor == Decimal(10) ** 15


def test_prefix_exponents_are_all_distinct():
    exponents = [prefix.exponent for prefix in ALL_PREFIXES]
    assert len(exponents) == len(set(exponents))


def test_prefix_symbols_are_all_distinct():
    symbols = [prefix.symbol for prefix in ALL_PREFIXES]
    assert len(symbols) == len(set(symbols))


def test_prefix_names_are_all_distinct():
    names = [prefix.name for prefix in ALL_PREFIXES]
    assert len(names) == len(set(names))


def test_prefixes_are_ordered_smallest_to_largest():
    exponents = [prefix.exponent for prefix in ALL_PREFIXES]
    assert exponents == sorted(exponents)


def test_prefix_is_immutable():
    with pytest.raises(dataclasses.FrozenInstanceError):
        prefixes.PICO.exponent = -6  # type: ignore[misc]  # ty: ignore[invalid-assignment]


def test_prefixed_unit_builds_the_expected_unitdef():
    unit = prefixed_unit(prefixes.MILLI, "volt", "V", VOLTAGE)
    assert isinstance(unit, UnitDef)
    assert unit.name == "millivolt"
    assert unit.symbol == "mV"
    assert unit.scale == Decimal("0.001")
    assert unit.dimension is VOLTAGE


def test_prefixed_unit_with_no_prefix_is_a_pass_through():
    unit = prefixed_unit(prefixes.UNIT, "volt", "V", VOLTAGE)
    assert unit.name == "volt"
    assert unit.symbol == "V"
    assert unit.scale == Decimal(1)


def test_prefixed_unit_micro_symbol_concatenates_correctly():
    unit = prefixed_unit(prefixes.MICRO, "volt", "V", VOLTAGE)
    assert unit.symbol == f"{symbols.MICRO}V"


def test_coherent_offset_reproduces_mass_s_existing_nanogram_scale():
    unit = prefixed_unit(prefixes.NANO, "gram", "g", MASS, coherent_offset=-3)
    assert unit.scale == Decimal("0.000000000001")


def test_coherent_offset_defaults_to_zero() -> None:
    with_default = prefixed_unit(prefixes.KILO, "volt", "V", VOLTAGE)
    explicit_zero = prefixed_unit(
        prefixes.KILO, "volt", "V", VOLTAGE, coherent_offset=0
    )
    assert with_default.scale == explicit_zero.scale == Decimal(1000)


def test_coherent_offset_composes_additively_with_the_prefix_exponent():
    unit = prefixed_unit(prefixes.KILO, "x", "x", VOLTAGE, coherent_offset=-2)
    assert unit.scale == Decimal(10)  # 10³ * 10⁻² = 10¹


SHELL = UnitDef(
    "shell", "shell", Fraction(3, 100), LENGTH, aliases=("sh",), words=("shells",)
)

PUBLISHED_PREFIXED_CASES = [
    (prefixes.MILLI, length.METRE, length.MILLIMETRE),
    (prefixes.KILO, length.METRE, length.KILOMETRE),
    (prefixes.KILO, mass.GRAM, mass.KILOGRAM),
    (prefixes.MILLI, voltage.VOLT, voltage.MILLIVOLT),
]


def test_with_prefix_multiplies_the_scale_of_a_base_that_is_not_an_si_unit() -> None:
    unit = with_prefix(prefixes.KILO, SHELL)
    assert unit.name == "kiloshell"
    assert unit.symbol == "kshell"
    assert unit.scale == Fraction(30)
    assert unit.dimension is LENGTH


def test_with_prefix_keeps_a_fractional_scale_exact() -> None:
    assert with_prefix(prefixes.MICRO, SHELL).scale == Fraction(3, 100_000_000)


def test_with_prefix_pairs_the_spellings_of_prefix_and_base() -> None:
    unit = with_prefix(prefixes.MICRO, SHELL)
    assert set(unit.aliases) == {"ush", f"{symbols.MICRO}sh", "ushell"}
    assert unit.words == ("microshells",)


def test_with_prefix_adds_the_extra_spellings_it_is_given() -> None:
    unit = with_prefix(prefixes.KILO, SHELL, aliases=("ks",), words=("shellthousand",))
    assert "ks" in unit.aliases
    assert "shellthousand" in unit.words


def test_with_prefix_with_no_prefix_is_a_pass_through() -> None:
    assert with_prefix(prefixes.UNIT, length.METRE) == length.METRE


@pytest.mark.parametrize(
    ("prefix", "base", "published"), PUBLISHED_PREFIXED_CASES, ids=str
)
def test_with_prefix_reproduces_the_published_prefixed_unit(
    prefix: Prefix, base: UnitDef, published: UnitDef
) -> None:
    assert with_prefix(prefix, base) == published


def test_with_prefix_of_an_affine_unit_scales_the_unit_and_keeps_its_zero() -> None:
    unit = with_prefix(prefixes.MILLI, thermal.CELSIUS)
    assert isinstance(unit, AffineUnitDef)
    assert unit.name == "millicelsius"
    assert unit.symbol == f"m{symbols.DEGREE}C"
    assert unit.scale == Fraction(1, 1000)
    assert unit.offset == Fraction(27315, 100)


def test_with_prefix_pairs_every_alias_of_the_base_by_default() -> None:
    unit = with_prefix(prefixes.MILLI, thermal.CELSIUS)
    assert "mC" in unit.aliases


def test_with_prefix_pairs_only_the_aliases_it_is_told_to() -> None:
    unit = with_prefix(
        prefixes.MILLI, thermal.CELSIUS, paired_aliases=(f"{symbols.DEGREE} C",)
    )
    assert unit.aliases == (f"m{symbols.DEGREE} C",)


def test_with_prefix_pairs_only_the_words_it_is_told_to() -> None:
    unit = with_prefix(
        prefixes.MILLI, thermal.CELSIUS, paired_words=("degrees celsius",)
    )
    assert unit.words == ("millidegrees celsius",)
    assert with_prefix(prefixes.MILLI, thermal.KELVIN, paired_words=()).words == ()
