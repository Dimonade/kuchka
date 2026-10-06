"""A concrete quantity type is set up completely, whichever module is imported first.

A type that names its own `dimension` is a concrete quantity.
Defining one checks, at class creation, what is known then: it declares `__slots__`, so
its instances have no `__dict__`, and its `dimension` is a `Dimension`.
The canonical unit is bound afterwards by the unit module that defines the unit, so
these tests check the assembled package: every concrete type has a canonical unit of
its own, of the right kind and dimension, stored with scale 1 and offset 0, and
importing any entry point of the package leaves every type complete.
"""

from __future__ import annotations

import os
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

import kuchka
from kuchka import Voltage
from kuchka.dimensions import VOLTAGE
from kuchka.quantities.base import AffineQuantity
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base import ModularQuantity
from kuchka.quantities.base import PureLogarithmicQuantity
from tests.quantity_families import CONCRETE_QUANTITY_TYPES
from tests.quantity_families import sample_of

SHAPES = [
    LinearQuantity,
    AffineQuantity,
    ModularQuantity,
    PureLogarithmicQuantity,
]
SHAPE_IDS = [shape.__name__ for shape in SHAPES]


def _type_id(cls: type) -> str:
    return cls.__name__


# --- The guard at class creation ------------------------------------------------------


@pytest.mark.parametrize("shape", SHAPES, ids=SHAPE_IDS)
def test_a_concrete_type_without_slots_is_rejected(shape: type[Any]) -> None:
    with pytest.raises(TypeError, match="must declare `__slots__ = \\(\\)`"):

        class NoSlots(shape):  # type: ignore[misc]  # ty: ignore[invalid-base]
            dimension = VOLTAGE


@pytest.mark.parametrize("shape", SHAPES, ids=SHAPE_IDS)
def test_a_concrete_type_with_slots_is_accepted(shape: type[Any]) -> None:
    class WithSlots(shape):  # type: ignore[misc]  # ty: ignore[invalid-base]
        dimension = VOLTAGE
        __slots__ = ()

    assert "__dict__" not in dir(WithSlots) or WithSlots.__dictoffset__ == 0


@pytest.mark.parametrize("bad", [None, "voltage", 3, VOLTAGE.__class__])
def test_a_dimension_that_is_not_a_dimension_is_rejected(bad: object) -> None:
    with pytest.raises(TypeError, match="must be a Dimension"):

        class BadDimension(LinearQuantity):
            dimension = bad  # type: ignore[assignment]  # ty: ignore[invalid-assignment]
            __slots__ = ()


@pytest.mark.parametrize("shape", SHAPES, ids=SHAPE_IDS)
def test_a_shape_that_names_no_dimension_needs_neither(shape: type[Any]) -> None:
    class Intermediate(shape):  # type: ignore[misc]  # ty: ignore[invalid-base]
        pass

    assert issubclass(Intermediate, shape)


def test_a_subclass_of_a_concrete_type_that_names_no_dimension_is_accepted() -> None:
    class Calibrated(Voltage):
        pass

    assert Calibrated.dimension == VOLTAGE


def test_the_guard_passes_extra_class_keywords_on() -> None:
    class Marked(LinearQuantity):
        def __init_subclass__(cls, *, flag: bool = False, **kwargs: object) -> None:
            super().__init_subclass__(**kwargs)
            cls.flag = flag  # type: ignore[attr-defined]  # ty: ignore[unresolved-attribute]

    class Child(Marked, flag=True):
        pass

    assert Child.flag is True  # type: ignore[attr-defined]  # ty: ignore[unresolved-attribute]


# --- Every concrete type, as assembled ------------------------------------------------


def test_the_concrete_types_are_discovered() -> None:
    assert len(CONCRETE_QUANTITY_TYPES) > 25  # noqa: PLR2004 -- a floor, so discovery cannot silently empty


@pytest.mark.parametrize("cls", CONCRETE_QUANTITY_TYPES, ids=_type_id)
def test_instances_have_no_per_instance_dictionary(cls: type[Any]) -> None:
    assert cls.__dictoffset__ == 0
    assert not hasattr(sample_of(cls), "__dict__")


@pytest.mark.parametrize("cls", CONCRETE_QUANTITY_TYPES, ids=_type_id)
def test_every_concrete_type_declares_its_own_slots(cls: type[Any]) -> None:
    assert "__slots__" in vars(cls)


@pytest.mark.parametrize("cls", CONCRETE_QUANTITY_TYPES, ids=_type_id)
def test_every_concrete_type_binds_a_canonical_unit_of_its_own(cls: type[Any]) -> None:
    assert "_canonical_unit" in vars(cls), (
        f"{cls.__name__} has no canonical unit bound by its unit module"
    )


@pytest.mark.parametrize("cls", CONCRETE_QUANTITY_TYPES, ids=_type_id)
def test_the_canonical_unit_is_of_the_kind_the_shape_displays(cls: type[Any]) -> None:
    assert isinstance(cls._canonical_unit, cls._unit_type)


@pytest.mark.parametrize("cls", CONCRETE_QUANTITY_TYPES, ids=_type_id)
def test_the_canonical_unit_has_the_dimension_of_the_type(cls: type[Any]) -> None:
    unit = cls._canonical_unit
    if hasattr(unit, "dimension"):
        assert unit.dimension == cls.dimension


@pytest.mark.parametrize("cls", CONCRETE_QUANTITY_TYPES, ids=_type_id)
def test_the_canonical_unit_stores_the_magnitude_unscaled(cls: type[Any]) -> None:
    unit = cls._canonical_unit
    assert unit.scale == Fraction(1)
    assert getattr(unit, "offset", Fraction(0)) == Fraction(0)


@pytest.mark.parametrize("cls", CONCRETE_QUANTITY_TYPES, ids=_type_id)
def test_a_value_in_the_canonical_unit_reads_back_its_magnitude(cls: type[Any]) -> None:
    value = cls(Fraction(7, 3), cls._canonical_unit)
    assert value.value_in(cls._canonical_unit) == Fraction(7, 3)
    assert value.unit is cls._canonical_unit


# --- Independent of which module is imported first ------------------------------------

ENTRY_POINTS = [
    "kuchka",
    "kuchka.errors",
    "kuchka.constants",
    "kuchka.quantities",
    "kuchka.quantities.base",
    "kuchka.quantities.base.registry",
    "kuchka.units",
    "kuchka.units.voltage",
    "kuchka.units.temporal.time",
]

CHECK = """
import importlib, sys
importlib.import_module(sys.argv[1])
from kuchka.quantities.base.storage import _ScalarStorage

def concrete(base):
    for sub in base.__subclasses__():
        if "dimension" in vars(sub):
            yield sub
        yield from concrete(sub)

unbound = (c for c in concrete(_ScalarStorage) if "_canonical_unit" not in vars(c))
missing = sorted(c.__name__ for c in unbound)
print(",".join(missing) or "complete")
"""


@pytest.mark.parametrize("module", ENTRY_POINTS)
def test_importing_any_entry_point_leaves_every_type_complete(module: str) -> None:
    location = str(Path(kuchka.__file__).resolve().parent.parent)
    environment = {**os.environ, "PYTHONPATH": location}
    result = subprocess.run(
        [sys.executable, "-c", CHECK, module],
        capture_output=True,
        text=True,
        check=True,
        env=environment,
    )
    assert result.stdout.strip() == "complete"
