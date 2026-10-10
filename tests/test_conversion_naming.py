"""Conversions between quantity types are named `to_*` and `from_*`.

`.to(unit)` changes the unit a value is shown in.
A conversion between types is `to_x()` on the value or `from_x()` on the class, and a
conversion that has a domain raises `InvalidMeasurementError` outside it.
"""

from __future__ import annotations

import inspect
from fractions import Fraction

import pytest

from kuchka import Decibel
from kuchka import Frequency
from kuchka import Hertz
from kuchka import Instant
from kuchka import InvalidMeasurementError
from kuchka import LogarithmicRatio
from kuchka import Millisecond
from kuchka import Ratio
from kuchka import SampleRate
from kuchka import Second
from tests.quantity_families import CONCRETE_QUANTITY_TYPES


def _public_callables(cls: type) -> list[str]:
    return [
        name
        for name, member in inspect.getmembers(cls, callable)
        if not name.startswith("_")
    ]


@pytest.mark.parametrize("cls", CONCRETE_QUANTITY_TYPES, ids=lambda cls: cls.__name__)
def test_no_conversion_uses_a_retired_prefix(cls: type) -> None:
    retired = [
        name
        for name in _public_callables(cls)
        if name.startswith(("as_", "try_")) and name != "as_tuple"
    ]
    assert retired == []


@pytest.mark.parametrize("cls", CONCRETE_QUANTITY_TYPES, ids=lambda cls: cls.__name__)
def test_a_from_conversion_is_a_classmethod(cls: type) -> None:
    for name in _public_callables(cls):
        if name.startswith("from_"):
            assert inspect.ismethod(getattr(cls, name)), name


def test_the_conversions_between_types_exist_under_their_new_names() -> None:
    assert Millisecond(2).to_sampling_period().magnitude == Fraction(1, 500)
    assert isinstance(Second(1).to_instant(), Instant)
    rate = SampleRate(Fraction(8), SampleRate._canonical_unit)  # noqa: SLF001
    assert rate.to_frequency().magnitude == Fraction(8)
    assert Frequency.to_frequency(Hertz(3)).magnitude == Fraction(3)
    assert Decibel(30).to_power_ratio() == Ratio(1000)
    assert Decibel(40).to_field_ratio() == Ratio(100)


@pytest.mark.parametrize("name", ["from_power_ratio", "from_field_ratio"])
def test_a_ratio_without_a_logarithm_raises_invalid_measurement(name: str) -> None:
    convert = getattr(LogarithmicRatio, name)
    for ratio in (Ratio(0), Ratio(-1)):
        with pytest.raises(InvalidMeasurementError, match="positive"):
            convert(ratio)
