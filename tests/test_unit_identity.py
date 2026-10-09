"""A unit definition is an immutable value that copies to itself and pickles by name.

`UnitDef`, `AffineUnitDef`, and `LogarithmicUnitDef` describe a unit: its name, symbol,
scale, and spellings.
Two with the same fields are equal and hash alike, and their state is written once.
Copying returns the same object, so `copy.deepcopy(Volt(5)).unit is VOLT`, and
pickling stores only the name `kuchka.units` publishes the unit under, so a restored
unit is the same constant and the pickle holds no internal fields.
A unit that `kuchka.units` does not publish copies normally and cannot be pickled.
"""

from __future__ import annotations

import copy
import pickle
from fractions import Fraction

import pytest

import kuchka.units as published
from kuchka import Celsius
from kuchka import Decibel
from kuchka import Volt
from kuchka.dimensions import CURRENT
from kuchka.dimensions import VOLTAGE
from kuchka.internal.typing import override
from kuchka.quantities.base import AffineUnitDef
from kuchka.quantities.base import LogarithmicUnitDef
from kuchka.quantities.base import UnitDef
from kuchka.quantities.base.units import _published
from kuchka.quantities.base.units import _published_unit
from kuchka.quantities.base.units import _Unit
from kuchka.units import CELSIUS
from kuchka.units import DECIBEL
from kuchka.units import MILLIVOLT
from kuchka.units import VOLT

PUBLISHED = {
    name: getattr(published, name)
    for name in published.__all__
    if isinstance(getattr(published, name), _Unit)
}
PUBLISHED_NAMES = list(PUBLISHED)
PROTOCOLS = list(range(pickle.HIGHEST_PROTOCOL + 1))


def _linear(**changes: object) -> UnitDef:
    fields: dict[str, object] = {
        "name": "volt",
        "symbol": "V",
        "scale": 1,
        "dimension": VOLTAGE,
        "aliases": ("v",),
        "words": ("volts",),
    }
    fields.update(changes)
    return UnitDef(
        str(fields["name"]),
        str(fields["symbol"]),
        fields["scale"],  # type: ignore[arg-type]
        fields["dimension"],  # type: ignore[arg-type]
        aliases=fields["aliases"],  # type: ignore[arg-type]
        words=fields["words"],  # type: ignore[arg-type]
    )


# Value equality and hashing.


def test_units_with_the_same_fields_are_equal_and_hash_alike() -> None:
    assert _linear() == _linear()
    assert hash(_linear()) == hash(_linear())


@pytest.mark.parametrize(
    "change",
    [
        {"name": "other"},
        {"symbol": "W"},
        {"scale": 2},
        {"dimension": CURRENT},
        {"aliases": ("x",)},
        {"words": ("volty",)},
    ],
    ids=["name", "symbol", "scale", "dimension", "aliases", "words"],
)
def test_a_unit_differing_in_any_field_is_not_equal(change: dict[str, object]) -> None:
    assert _linear() != _linear(**change)


def test_a_scale_given_in_another_form_is_the_same_unit() -> None:
    assert _linear(scale=1) == _linear(scale=Fraction(1))


def test_affine_units_compare_by_every_field() -> None:
    def build(**changes: object) -> AffineUnitDef:
        fields: dict[str, object] = {"scale": 1, "offset": 273}
        fields.update(changes)
        return AffineUnitDef("c", "C", fields["scale"], fields["offset"])  # type: ignore[arg-type]

    assert build() == build()
    assert hash(build()) == hash(build())
    assert build() != build(offset=274)
    assert build() != build(scale=2)


def test_logarithmic_units_compare_by_every_field() -> None:
    assert LogarithmicUnitDef("d", "dB", 1) == LogarithmicUnitDef("d", "dB", 1)
    assert LogarithmicUnitDef("d", "dB", 1) != LogarithmicUnitDef("d", "dB", 10)


SPELLING_CHANGES = [
    pytest.param({"aliases": ("a",)}, id="aliases"),
    pytest.param({"words": ("w",)}, id="words"),
]
BUILDERS = [
    pytest.param(lambda **kw: UnitDef("u", "u", 1, VOLTAGE, **kw), id="linear"),
    pytest.param(lambda **kw: AffineUnitDef("u", "u", 1, 0, **kw), id="affine"),
    pytest.param(lambda **kw: LogarithmicUnitDef("u", "u", 1, **kw), id="logarithmic"),
]


@pytest.mark.parametrize("build", BUILDERS)
@pytest.mark.parametrize("change", SPELLING_CHANGES)
def test_every_unit_type_compares_its_spellings(
    build, change: dict[str, object]
) -> None:
    assert build() != build(**change)
    assert build(**change) == build(**change)
    assert hash(build(**change)) == hash(build(**change))


def test_units_of_different_types_are_never_equal() -> None:
    assert UnitDef("a", "a", 1, VOLTAGE) != AffineUnitDef("a", "a", 1, 0)
    assert AffineUnitDef("a", "a", 1, 0) != LogarithmicUnitDef("a", "a", 1)


@pytest.mark.parametrize("other", [None, 5, "V", object()], ids=repr)
def test_a_unit_is_not_equal_to_a_non_unit(other: object) -> None:
    assert other != VOLT


def test_units_work_as_dictionary_keys_and_set_members() -> None:
    assert {_linear(): "a"}[_linear()] == "a"
    assert len({_linear(), _linear(), _linear(symbol="W")}) == 2  # noqa: PLR2004


def test_every_published_unit_is_equal_only_to_itself_or_a_twin() -> None:
    by_value: dict[object, str] = {}
    for name, unit in PUBLISHED.items():
        twin = by_value.setdefault(unit, name)
        assert PUBLISHED[twin] is unit, (twin, name)


# Immutability.

FIELDS = {
    UnitDef: ["name", "symbol", "scale", "dimension", "aliases", "words"],
    AffineUnitDef: ["name", "symbol", "scale", "offset", "aliases", "words"],
    LogarithmicUnitDef: ["name", "symbol", "scale", "aliases", "words"],
}


FIELD_CASES = [
    (unit, field)
    for unit, fields in (
        (VOLT, FIELDS[UnitDef]),
        (CELSIUS, FIELDS[AffineUnitDef]),
        (DECIBEL, FIELDS[LogarithmicUnitDef]),
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


@pytest.mark.parametrize("unit", [VOLT, CELSIUS, DECIBEL], ids=lambda u: u.name)
def test_a_new_attribute_cannot_be_added(unit: _Unit) -> None:
    with pytest.raises(AttributeError):
        unit.extra = 1


REINIT = [
    pytest.param(VOLT, ("x", "x", 5, VOLTAGE), id="linear"),
    pytest.param(CELSIUS, ("x", "x", 5, 5), id="affine"),
    pytest.param(DECIBEL, ("x", "x", 5), id="logarithmic"),
]


@pytest.mark.parametrize(("unit", "arguments"), REINIT)
def test_init_cannot_be_called_again_to_replace_the_fields(
    unit: _Unit, arguments: tuple[object, ...]
) -> None:
    before = unit._fields()
    with pytest.raises(AttributeError, match="immutable"):
        type(unit).__init__(unit, *arguments)
    assert unit._fields() == before


# Copying returns the same unit.


@pytest.mark.parametrize("name", PUBLISHED_NAMES)
def test_copy_and_deepcopy_of_a_published_unit_return_it(name: str) -> None:
    unit = PUBLISHED[name]
    assert copy.copy(unit) is unit
    assert copy.deepcopy(unit) is unit


def test_a_copied_quantity_keeps_the_library_unit() -> None:
    value = Volt(5)
    assert copy.copy(value).unit is VOLT
    assert copy.deepcopy(value).unit is VOLT
    assert copy.deepcopy(value).unit == VOLT


def test_a_copied_quantity_in_a_prefixed_unit_keeps_that_unit() -> None:
    assert copy.deepcopy(Volt(5).to(MILLIVOLT)).unit is MILLIVOLT


@pytest.mark.parametrize("quantity", [Celsius(20), Decibel(3)], ids=["affine", "log"])
def test_copying_keeps_the_unit_of_every_shape(quantity: object) -> None:
    assert copy.deepcopy(quantity).unit is quantity.unit  # type: ignore[attr-defined]  # ty: ignore[unresolved-attribute]


def test_a_custom_unit_copies_to_itself() -> None:
    unit = _linear(name="custom", symbol="cu")
    assert copy.copy(unit) is unit
    assert copy.deepcopy(unit) is unit


def test_deepcopy_of_a_container_of_units_keeps_each_unit() -> None:
    holder = {"units": [VOLT, MILLIVOLT, VOLT]}
    copied = copy.deepcopy(holder)
    assert copied["units"][0] is VOLT
    assert copied["units"][1] is MILLIVOLT
    assert copied["units"][2] is VOLT


# Pickling is by published name.


@pytest.mark.parametrize("protocol", PROTOCOLS)
@pytest.mark.parametrize("name", PUBLISHED_NAMES)
def test_a_published_unit_pickles_to_itself(name: str, protocol: int) -> None:
    unit = PUBLISHED[name]
    assert pickle.loads(pickle.dumps(unit, protocol=protocol)) is unit


@pytest.mark.parametrize("protocol", PROTOCOLS)
def test_a_pickled_quantity_keeps_the_library_unit(protocol: int) -> None:
    restored = pickle.loads(pickle.dumps(Volt(5), protocol=protocol))
    assert restored == Volt(5)
    assert restored.unit is VOLT
    assert restored.unit == VOLT


@pytest.mark.parametrize("protocol", PROTOCOLS)
@pytest.mark.parametrize("quantity", [Celsius(20), Decibel(3)], ids=["affine", "log"])
def test_a_pickled_quantity_of_every_shape_keeps_its_unit(
    quantity: object, protocol: int
) -> None:
    restored = pickle.loads(pickle.dumps(quantity, protocol=protocol))
    assert restored == quantity
    assert restored.unit is quantity.unit  # type: ignore[attr-defined]  # ty: ignore[unresolved-attribute]


def test_a_pickled_unit_holds_its_name_and_no_fields() -> None:
    payload = pickle.dumps(VOLT)
    assert b"VOLT" in payload
    assert b"Dimension" not in payload
    assert b"Fraction" not in payload
    assert len(payload) < 150  # noqa: PLR2004


def test_a_pickled_quantity_holds_no_unit_fields() -> None:
    payload = pickle.dumps(Volt(5))
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
        VOLT.name,
        VOLT.symbol,
        VOLT.scale,
        VOLT.dimension,
        aliases=VOLT.aliases,
        words=VOLT.words,
    )
    assert twin == VOLT
    assert twin is not VOLT
    assert pickle.loads(pickle.dumps(twin)) is VOLT


# Unpickling accepts only published units.


def test_unpickling_resolves_a_published_name() -> None:
    assert _published_unit("VOLT") is VOLT


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
