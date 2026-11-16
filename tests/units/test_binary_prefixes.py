"""The IEC binary prefixes: powers of two, held exactly, beside the SI powers of ten.

The names, symbols, exponents, and factors are hand-written from IEC 80000-13.
The SI prefix table is tested in `test_prefixes`.
"""

from __future__ import annotations

from decimal import Decimal

import pytest

from kuchka.internal import prefixes
from kuchka.internal.prefixes import Prefix
from kuchka.internal.prefixes import with_prefix
from kuchka.units.information import data

BINARY_PREFIXES = [
    (prefixes.KIBI, "kibi", "Ki", 10, "1024"),
    (prefixes.MEBI, "mebi", "Mi", 20, "1048576"),
    (prefixes.GIBI, "gibi", "Gi", 30, "1073741824"),
    (prefixes.TEBI, "tebi", "Ti", 40, "1099511627776"),
    (prefixes.PEBI, "pebi", "Pi", 50, "1125899906842624"),
    (prefixes.EXBI, "exbi", "Ei", 60, "1152921504606846976"),
    (prefixes.ZEBI, "zebi", "Zi", 70, "1180591620717411303424"),
    (prefixes.YOBI, "yobi", "Yi", 80, "1208925819614629174706176"),
]
BINARY_BASE = 2
IDS = [name for _, name, _, _, _ in BINARY_PREFIXES]


@pytest.mark.parametrize(
    ("prefix", "name", "symbol", "exponent", "factor"), BINARY_PREFIXES, ids=IDS
)
def test_a_binary_prefix_is_a_power_of_two_with_its_standard_name(
    prefix: Prefix, name: str, symbol: str, exponent: int, factor: str
) -> None:
    assert (prefix.name, prefix.symbol, prefix.base, prefix.exponent) == (
        name,
        symbol,
        2,
        exponent,
    )
    assert prefix.factor == Decimal(factor)


@pytest.mark.parametrize("prefix", [row[0] for row in BINARY_PREFIXES], ids=IDS)
def test_the_factor_of_a_binary_prefix_is_a_decimal_without_a_fraction(
    prefix: Prefix,
) -> None:
    assert isinstance(prefix.factor, Decimal)
    assert prefix.factor == prefix.factor.to_integral_value()


def test_the_factor_does_not_depend_on_the_arithmetic_context() -> None:
    """Quebi, 2**100, has 31 digits, more than the default context keeps."""
    quebi = Prefix("quebi", "Qi", 100, base=2)
    assert quebi.factor == Decimal(1267650600228229401496703205376)


def test_a_prefix_is_decimal_unless_it_names_another_base() -> None:
    assert Prefix("kilo", "k", 3).base == 10  # noqa: PLR2004 -- the base of every SI prefix


def test_no_symbol_is_shared_by_a_metric_and_a_binary_prefix() -> None:
    metric = [
        p.symbol
        for p in vars(prefixes).values()
        if isinstance(p, Prefix) and p.base != BINARY_BASE
    ]
    binary = [p.symbol for p, *_ in BINARY_PREFIXES]
    assert not set(metric) & set(binary)


def test_with_prefix_builds_a_binary_multiple_of_a_unit() -> None:
    kibibyte = with_prefix(prefixes.KIBI, data.BYTE)
    assert (kibibyte.name, kibibyte.symbol) == ("kibibyte", "KiB")
    assert kibibyte.scale == 8 * 1024


def test_a_binary_prefix_pairs_with_the_aliases_of_its_unit() -> None:
    """The bit is also `b`, so the kibibit is also `Kib`."""
    kibibit = with_prefix(prefixes.KIBI, data.BIT)
    assert "Kib" in kibibit.aliases
