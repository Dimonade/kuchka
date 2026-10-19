"""The static overloads of `*` and `/` agree with what the operators do.

A type checker trusts the `@overload` declarations, and the runtime ignores them, so
nothing but a test keeps the two together.
Every declared overload is run, and every pair of linear types that the runtime
multiplies or divides into another quantity, a `Proportion` included, must have been
declared.
"""

from __future__ import annotations

import operator
from fractions import Fraction

import pytest

from kuchka import MeasurementError
from tests.support.families import FAMILIES
from tests.support.overloads import FAMILY_OF
from tests.support.overloads import OVERLOAD_IDS
from tests.support.overloads import OVERLOADS
from tests.support.overloads import SYMBOL
from tests.support.overloads import Overload

OPERATOR = {"__mul__": operator.mul, "__truediv__": operator.truediv}


def operands(left: type, right: type) -> tuple:
    """Return one value of each type, in their canonical units."""
    return FAMILY_OF[left].canonical(12), FAMILY_OF[right].canonical(3)


@pytest.mark.parametrize("overload", OVERLOADS, ids=OVERLOAD_IDS)
def test_a_declared_overload_is_what_the_operator_returns(overload: Overload) -> None:
    left, right = operands(overload.left, overload.right)
    result = OPERATOR[overload.operation](left, right)
    if overload.result is None:
        assert type(result) is Fraction
        return
    assert type(result) is overload.result
    expected = 36 if overload.operation == "__mul__" else 4
    assert result == FAMILY_OF[overload.result].canonical(expected)


def runtime_pairs() -> set[tuple[str, str, str, str]]:
    """Return every pair the runtime combines into a quantity or a fraction."""
    found = set()
    for left in FAMILIES:
        for right in FAMILIES:
            for operation, apply in OPERATOR.items():
                try:
                    result = apply(left.canonical(12), right.canonical(3))
                except (MeasurementError, TypeError):
                    continue
                found.add(
                    (
                        left.quantity.__name__,
                        SYMBOL[operation],
                        right.quantity.__name__,
                        type(result).__name__,
                    )
                )
    return found


def declared_pairs() -> set[tuple[str, str, str, str]]:
    """Return every pair the overloads declare, in the same form."""
    return {
        (
            o.left.__name__,
            SYMBOL[o.operation],
            o.right.__name__,
            "Fraction" if o.result is None else o.result.__name__,
        )
        for o in OVERLOADS
    }


def test_every_product_the_runtime_allows_is_declared() -> None:
    assert runtime_pairs() - declared_pairs() == set()
