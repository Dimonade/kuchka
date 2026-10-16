"""Defining a concrete quantity type checks what is known at class creation.

A type that names its own `dimension` is a concrete quantity.
It declares `__slots__`, so its instances have no `__dict__`, and its `dimension` is a
`Dimension`; the guard applies to every shape.
"""

from __future__ import annotations

from typing import Any

import pytest

from kuchka import Voltage
from kuchka.dimensions import VOLTAGE
from kuchka.quantities.base import LinearQuantity
from tests.support.shapes import SHAPE_IDS
from tests.support.shapes import SHAPES


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
