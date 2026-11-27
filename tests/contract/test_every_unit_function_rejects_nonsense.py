"""Every function of the flat API refuses what it was not made for.

`Volt`, `Celsius`, `Degree`, and the rest of the unit functions each take a number, and
`kuchka.__all__` lists them with the other functions; none of them takes a string, a
`None`, a `bool`, a dinosaur, or a number that is no finite number, and none leaks an
internal error for one.
"""

from __future__ import annotations

import inspect
from decimal import Decimal

import pytest

import kuchka
from kuchka import MeasurementError


class Dinosaur:
    """Nothing a unit function takes."""


NONSENSE = {
    "a string": "5",
    "None": None,
    "a bool": True,
    "a list": [1],
    "a dinosaur": Dinosaur(),
    "nan": float("nan"),
    "infinity": float("inf"),
    "a Decimal nan": Decimal("NaN"),
    "a complex": 1 + 2j,
    "bytes": b"5",
    "a class": Dinosaur,
}
FUNCTIONS = [
    name for name in kuchka.__all__ if inspect.isfunction(getattr(kuchka, name, None))
]
LEAKS = (AttributeError, KeyError, IndexError, UnboundLocalError, RecursionError)


def test_the_flat_api_has_its_unit_functions() -> None:
    assert len(FUNCTIONS) > len(NONSENSE) * 50


@pytest.mark.parametrize("name", FUNCTIONS)
def test_a_unit_function_refuses_nonsense(name: str) -> None:
    function = getattr(kuchka, name)
    for what, value in NONSENSE.items():
        try:
            result = function(value)
        except MeasurementError:
            continue
        except LEAKS as error:
            pytest.fail(f"{name}({what}) leaked {type(error).__name__}: {error}")
        except TypeError:
            continue
        pytest.fail(f"{name}({what}) took it, and returned {result!r}")
