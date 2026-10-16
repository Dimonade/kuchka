"""Unit definitions with the same fields are equal and hash alike."""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka.dimensions import CURRENT
from kuchka.dimensions import VOLTAGE
from kuchka.quantities.base import AffineUnitDef
from kuchka.quantities.base import LogarithmicUnitDef
from kuchka.quantities.base import UnitDef
from kuchka.units import voltage
from tests.units.helpers import PUBLISHED
from tests.units.helpers import _linear


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
    assert other != voltage.VOLT


def test_units_work_as_dictionary_keys_and_set_members() -> None:
    assert {_linear(): "a"}[_linear()] == "a"
    assert len({_linear(), _linear(), _linear(symbol="W")}) == 2  # noqa: PLR2004


def test_every_published_unit_is_equal_only_to_itself_or_a_twin() -> None:
    by_value: dict[object, str] = {}
    for name, unit in PUBLISHED.items():
        twin = by_value.setdefault(unit, name)
        assert PUBLISHED[twin] is unit, (twin, name)
