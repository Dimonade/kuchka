"""Pickling/copying, and `__format__` on `LinearQuantity` and `Temperature`.

`LinearQuantity` and `Temperature` block `__setattr__` for immutability, which also
blocks the default `pickle`/`copy` restore path for `__slots__`-only classes:
that path calls plain `setattr()`, and the immutability guard rejects it.

`__getstate__`/`__setstate__` (defined on both types, routing through
`object.__setattr__` the same way `__init__` already does) is what makes an immutable,
`__slots__`-only quantity still picklable and copyable.
"""

from __future__ import annotations

import copy
import pickle

import pytest

from kuchka import Celsius
from kuchka import Fahrenheit
from kuchka import Kelvin
from kuchka import Volt
from kuchka.units import MILLIVOLT
from tests.quantity_families import FAMILIES
from tests.quantity_families import FAMILY_IDS


@pytest.mark.parametrize("family", FAMILIES, ids=FAMILY_IDS)
def test_deepcopy_round_trips_every_family(family) -> None:
    original = family.canonical(5)
    assert copy.deepcopy(original) == original


@pytest.mark.parametrize("family", FAMILIES, ids=FAMILY_IDS)
def test_pickle_round_trips_every_family(family) -> None:
    original = family.canonical(5)
    assert pickle.loads(pickle.dumps(original)) == original


def test_deepcopy_preserves_display_unit() -> None:
    voltage = Volt(1).to(MILLIVOLT)
    copied = copy.deepcopy(voltage)
    assert copied == voltage
    assert copied.unit.symbol == MILLIVOLT.symbol


def test_pickle_preserves_display_unit() -> None:
    voltage = Volt(1).to(MILLIVOLT)
    restored = pickle.loads(pickle.dumps(voltage))
    assert restored == voltage
    assert restored.unit.symbol == MILLIVOLT.symbol


def test_temperature_deepcopy_round_trips() -> None:
    original = Celsius(20)
    assert copy.deepcopy(original) == original


def test_temperature_pickle_round_trips() -> None:
    original = Kelvin(300)
    assert pickle.loads(pickle.dumps(original)) == original


def test_fahrenheit_copy_and_pickle_round_trip() -> None:
    original = Fahrenheit(68)
    assert copy.deepcopy(original) == original
    assert pickle.loads(pickle.dumps(original)) == original


def test_copied_and_pickled_values_stay_immutable() -> None:
    copied = copy.deepcopy(Volt(5))
    with pytest.raises(AttributeError):
        copied._magnitude = 1  # type: ignore[assignment]  # ty: ignore[invalid-assignment]  # noqa: SLF001
