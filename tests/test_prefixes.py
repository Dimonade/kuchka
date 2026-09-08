"""Specific tests for `kuchka.prefixes`.

Includes the `Prefix` dataclass itself, and the `prefixed_unit()` helper.

Every expected scale is hand written as an independent decimal literal to avoid
testing against the implementation of itself, which would always be true.
"""

from __future__ import annotations

import dataclasses
from decimal import Decimal

import pytest

from kuchka.dimensions import MASS
from kuchka.dimensions import VOLTAGE
from kuchka.prefixes import CENTI
from kuchka.prefixes import DECA
from kuchka.prefixes import DECI
from kuchka.prefixes import FEMTO
from kuchka.prefixes import GIGA
from kuchka.prefixes import HECTO
from kuchka.prefixes import KILO
from kuchka.prefixes import MEGA
from kuchka.prefixes import MICRO
from kuchka.prefixes import MILLI
from kuchka.prefixes import NANO
from kuchka.prefixes import PETA
from kuchka.prefixes import PICO
from kuchka.prefixes import TERA
from kuchka.prefixes import UNIT
from kuchka.prefixes import Prefix
from kuchka.prefixes import prefixed_unit
from kuchka.quantities.base import UnitDef

PREFIX_TABLE_CASES = [
    (FEMTO, -15, Decimal("0.000000000000001"), "femto", "f"),
    (PICO, -12, Decimal("0.000000000001"), "pico", "p"),
    (NANO, -9, Decimal("0.000000001"), "nano", "n"),
    (MICRO, -6, Decimal("0.000001"), "micro", "\u00b5"),
    (MILLI, -3, Decimal("0.001"), "milli", "m"),
    (CENTI, -2, Decimal("0.01"), "centi", "c"),
    (DECI, -1, Decimal("0.1"), "deci", "d"),
    (UNIT, 0, Decimal(1), "", ""),
    (DECA, 1, Decimal(10), "deca", "da"),
    (HECTO, 2, Decimal(100), "hecto", "h"),
    (KILO, 3, Decimal(1_000), "kilo", "k"),
    (MEGA, 6, Decimal(1_000_000), "mega", "M"),
    (GIGA, 9, Decimal(1_000_000_000), "giga", "G"),
    (TERA, 12, Decimal(1_000_000_000_000), "tera", "T"),
    (PETA, 15, Decimal(1_000_000_000_000_000), "peta", "P"),
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
    assert MICRO.symbol == "\u00b5"
    assert MICRO.symbol != "\u03bc"


def test_factor_is_always_a_decimal_not_a_float():
    assert isinstance(PICO.factor, Decimal)
    assert isinstance(PETA.factor, Decimal)


def test_extreme_factors_agree_with_integer_exponentiation():
    """A second, independently-computed check on the two widest prefixes."""
    assert FEMTO.factor == Decimal(1) / Decimal(10) ** 15
    assert PETA.factor == Decimal(10) ** 15


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
        PICO.exponent = -6  # type: ignore[misc]  # ty: ignore[invalid-assignment]


def test_prefixed_unit_builds_the_expected_unitdef():
    unit = prefixed_unit(MILLI, "volt", "V", VOLTAGE)
    assert isinstance(unit, UnitDef)
    assert unit.name == "millivolt"
    assert unit.symbol == "mV"
    assert unit.scale == Decimal("0.001")
    assert unit.dimension is VOLTAGE


def test_prefixed_unit_with_no_prefix_is_a_pass_through():
    unit = prefixed_unit(UNIT, "volt", "V", VOLTAGE)
    assert unit.name == "volt"
    assert unit.symbol == "V"
    assert unit.scale == Decimal(1)


def test_prefixed_unit_micro_symbol_concatenates_correctly():
    unit = prefixed_unit(MICRO, "volt", "V", VOLTAGE)
    assert unit.symbol == "\u00b5V"


def test_coherent_offset_reproduces_mass_s_existing_nanogram_scale():
    unit = prefixed_unit(NANO, "gram", "g", MASS, coherent_offset=-3)
    assert unit.scale == Decimal("0.000000000001")


def test_coherent_offset_defaults_to_zero() -> None:
    with_default = prefixed_unit(KILO, "volt", "V", VOLTAGE)
    explicit_zero = prefixed_unit(KILO, "volt", "V", VOLTAGE, coherent_offset=0)
    assert with_default.scale == explicit_zero.scale == Decimal(1000)


def test_coherent_offset_composes_additively_with_the_prefix_exponent():
    unit = prefixed_unit(KILO, "x", "x", VOLTAGE, coherent_offset=-2)
    assert unit.scale == Decimal(10)  # 10^3 * 10^-2 = 10^1
