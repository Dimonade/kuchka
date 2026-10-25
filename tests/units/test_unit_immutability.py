"""A unit definition is written once: its fields cannot be rebound or replaced."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from kuchka.dimensions import VOLTAGE
from kuchka.quantities.base import AffineUnitDef
from kuchka.quantities.base import LogarithmicUnitDef
from kuchka.quantities.base import UnitDef
from kuchka.units import logarithmic
from kuchka.units import thermal
from kuchka.units.electromagnetics import voltage

if TYPE_CHECKING:
    from kuchka.quantities.base.units import _Unit

FIELDS = {
    UnitDef: ["name", "symbol", "scale", "dimension", "aliases", "words"],
    AffineUnitDef: ["name", "symbol", "scale", "offset", "aliases", "words"],
    LogarithmicUnitDef: ["name", "symbol", "scale", "aliases", "words"],
}


FIELD_CASES = [
    (unit, field)
    for unit, fields in (
        (voltage.VOLT, FIELDS[UnitDef]),
        (thermal.CELSIUS, FIELDS[AffineUnitDef]),
        (logarithmic.DECIBEL, FIELDS[LogarithmicUnitDef]),
    )
    for field in fields
]


@pytest.mark.parametrize(
    ("unit", "field"),
    FIELD_CASES,
    ids=[f"{unit.name}-{field}" for unit, field in FIELD_CASES],
)
def test_a_field_cannot_be_rebound_or_deleted(unit: _Unit, field: str) -> None:
    before = getattr(unit, field)
    with pytest.raises(AttributeError, match="immutable"):
        setattr(unit, field, before)
    with pytest.raises(AttributeError, match="immutable"):
        delattr(unit, field)
    assert getattr(unit, field) == before


@pytest.mark.parametrize(
    "unit", [voltage.VOLT, thermal.CELSIUS, logarithmic.DECIBEL], ids=lambda u: u.name
)
def test_a_new_attribute_cannot_be_added(unit: _Unit) -> None:
    with pytest.raises(AttributeError):
        unit.extra = 1


REINIT = [
    pytest.param(voltage.VOLT, ("x", "x", 5, VOLTAGE), id="linear"),
    pytest.param(thermal.CELSIUS, ("x", "x", 5, 5), id="affine"),
    pytest.param(logarithmic.DECIBEL, ("x", "x", 5), id="logarithmic"),
]


@pytest.mark.parametrize(("unit", "arguments"), REINIT)
def test_init_cannot_be_called_again_to_replace_the_fields(
    unit: _Unit, arguments: tuple[object, ...]
) -> None:
    before = unit._fields()
    with pytest.raises(AttributeError, match="immutable"):
        type(unit).__init__(unit, *arguments)
    assert unit._fields() == before
