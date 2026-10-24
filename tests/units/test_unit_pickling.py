"""A unit pickles by the name `kuchka.units` publishes it under, and only so."""

from __future__ import annotations

import pickle

import pytest

from kuchka.internal.typing import override
from kuchka.quantities.base import UnitDef
from kuchka.quantities.base.units import _published
from kuchka.quantities.base.units import _published_unit
from kuchka.units import logarithmic
from kuchka.units import thermal
from kuchka.units import voltage
from tests.support.values import PICKLE_PROTOCOLS
from tests.units.helpers import PUBLISHED
from tests.units.helpers import _linear


@pytest.mark.parametrize("protocol", PICKLE_PROTOCOLS)
def test_a_pickled_quantity_keeps_the_library_unit(protocol: int) -> None:
    restored = pickle.loads(pickle.dumps(voltage.Volt(5), protocol=protocol))
    assert restored == voltage.Volt(5)
    assert restored.unit is voltage.VOLT
    assert restored.unit == voltage.VOLT


@pytest.mark.parametrize("protocol", PICKLE_PROTOCOLS)
@pytest.mark.parametrize(
    "quantity", [thermal.Celsius(20), logarithmic.Decibel(3)], ids=["affine", "log"]
)
def test_a_pickled_quantity_of_every_shape_keeps_its_unit(
    quantity: object, protocol: int
) -> None:
    restored = pickle.loads(pickle.dumps(quantity, protocol=protocol))
    assert restored == quantity
    assert restored.unit is quantity.unit  # type: ignore[attr-defined]  # ty: ignore[unresolved-attribute]


def test_a_pickled_unit_holds_its_name_and_no_fields() -> None:
    payload = pickle.dumps(voltage.VOLT)
    assert b"VOLT" in payload
    assert b"Dimension" not in payload
    assert b"Fraction" not in payload
    assert len(payload) < 150  # noqa: PLR2004


def test_a_pickled_quantity_holds_no_unit_fields() -> None:
    payload = pickle.dumps(voltage.Volt(5))
    assert b"VOLT" in payload
    assert b"Dimension" not in payload
    assert b"volt" not in payload


def test_a_unit_published_under_two_names_pickles_under_the_first() -> None:
    by_name, by_unit = _published()
    twins = [name for name, unit in by_name.items() if by_unit[unit] != name]
    assert twins
    for name in twins:
        unit = by_name[name]
        assert pickle.loads(pickle.dumps(unit)) is unit
        assert by_unit[unit].encode() in pickle.dumps(unit)


def test_a_custom_unit_cannot_be_pickled() -> None:
    with pytest.raises(pickle.PicklingError, match="only the units published"):
        pickle.dumps(_linear(name="custom", symbol="cu"))


def test_a_unit_equal_to_a_published_one_pickles_as_the_published_unit() -> None:
    twin = UnitDef(
        voltage.VOLT.name,
        voltage.VOLT.symbol,
        voltage.VOLT.scale,
        voltage.VOLT.dimension,
        aliases=voltage.VOLT.aliases,
        words=voltage.VOLT.words,
    )
    assert twin == voltage.VOLT
    assert twin is not voltage.VOLT
    assert pickle.loads(pickle.dumps(twin)) is voltage.VOLT


# Unpickling accepts only published units.


def test_unpickling_resolves_a_published_name() -> None:
    assert _published_unit("VOLT") is voltage.VOLT


@pytest.mark.parametrize(
    "name",
    ["print", "VOLTAGE_UNITS", "__all__", "Volt", "NOPE", "", "units"],
)
def test_unpickling_refuses_a_name_that_is_not_a_unit(name: str) -> None:
    with pytest.raises(pickle.UnpicklingError, match="not a unit published"):
        _published_unit(name)


def test_a_forged_payload_naming_a_non_unit_is_refused() -> None:
    forged = b"\x80\x04\x95\x00\x00\x00\x00\x00\x00\x00\x00"  # not used: built below
    del forged

    class Forge:
        @override
        def __reduce__(self) -> tuple[object, ...]:
            return (_published_unit, ("VOLTAGE_UNITS",))

    with pytest.raises(pickle.UnpicklingError):
        pickle.loads(pickle.dumps(Forge()))


def test_every_published_unit_is_indexed_both_ways() -> None:
    by_name, by_unit = _published()
    assert set(by_name) == set(PUBLISHED)
    assert set(by_unit) == set(PUBLISHED.values())
    assert len(by_name) > 150  # noqa: PLR2004 -- a floor, so discovery cannot silently empty
