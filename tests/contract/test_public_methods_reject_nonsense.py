"""No public method of a quantity leaks an internal error for an argument of no sense.

A method that is given a dinosaur raises a kuchka error or a `TypeError` that says what
was expected, and never an `AttributeError`, a `KeyError`, or a number: the person who
passes the wrong thing has to learn that from the message.
Every public method of one quantity of every type, with every parameter it has, is given
nonsense.
"""

from __future__ import annotations

import inspect
from fractions import Fraction

import pytest

from kuchka import Decibel
from kuchka import Millivolt
from kuchka import Ratio
from kuchka import Volt
from kuchka.quantities import LogarithmicRatio
from tests.support.kinds import UNIT_TABLES


class Dinosaur:
    """Nothing a quantity method should take."""


NONSENSE = {
    "a string": "five",
    "None": None,
    "a bool": True,
    "a list": [1],
    "a dinosaur": Dinosaur(),
    "nan": float("nan"),
    "infinity": float("inf"),
    "a complex": 1 + 2j,
    "a class": Dinosaur,
}
LEAKS = (
    AttributeError,
    KeyError,
    IndexError,
    UnboundLocalError,
    ZeroDivisionError,
    RecursionError,
    OverflowError,
    NameError,
    AssertionError,
    StopIteration,
)


@pytest.mark.parametrize("name", list(UNIT_TABLES))
def test_no_public_method_leaks_an_internal_error(name: str) -> None:
    sample = next(iter(UNIT_TABLES[name].values()))(Fraction(1))
    for method_name, method in inspect.getmembers(sample, inspect.ismethod):
        if method_name.startswith("_"):
            continue
        parameters = [
            p
            for p in inspect.signature(method).parameters.values()
            if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD, p.KEYWORD_ONLY)
        ]
        required = [p for p in parameters if p.default is p.empty]
        for parameter in parameters:
            if required and parameter is not required[0]:
                continue
            for what, value in NONSENSE.items():
                try:
                    method(**{parameter.name: value})
                except LEAKS as error:
                    pytest.fail(
                        f"{name}.{method_name}({parameter.name}={what}) "
                        f"leaked {type(error).__name__}: {error}"
                    )
                except Exception:  # noqa: BLE001, S110 -- a refusal is what is wanted
                    pass


@pytest.mark.parametrize("what", list(NONSENSE))
def test_a_level_is_made_from_a_proportion_and_nothing_else(what: str) -> None:
    for make in (LogarithmicRatio.from_power_ratio, LogarithmicRatio.from_field_ratio):
        with pytest.raises(TypeError, match="Proportion"):
            make(NONSENSE[what])  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
    assert LogarithmicRatio.from_power_ratio(Ratio(1000)) == Decibel(30)


@pytest.mark.parametrize("spec", [None, 5, 1.5, b".2f", [".2f"], Dinosaur()])
def test_a_format_specification_is_a_string(spec: object) -> None:
    with pytest.raises(TypeError, match="must be str"):
        Volt(1).format_parts(spec)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
    with pytest.raises(TypeError):
        format(Volt(1), spec)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_the_empty_specification_and_a_width_are_strings_that_are_taken() -> None:
    assert Millivolt(2800).format_parts("") == ("2800", "mV")
    assert Millivolt(2800).format_parts("6") == ("  2800", "mV")
