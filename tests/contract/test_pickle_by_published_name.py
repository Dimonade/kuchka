"""A quantity pickles by the name `kuchka.quantities` publishes its class under."""

from __future__ import annotations

import pickle
import pickletools

import pytest

from kuchka import Metre
from kuchka.quantities import Length
from kuchka.quantities.base.storage import _new_published


class Unpublished(Length):
    """A subclass that `kuchka.quantities` does not publish."""


def _strings(payload: bytes) -> set[str]:
    return {
        argument
        for _, argument, _ in pickletools.genops(payload)
        if isinstance(argument, str)
    }


def test_a_class_that_is_not_published_pickles_by_reference() -> None:
    original = Unpublished.__new__(Unpublished)
    original.__setstate__(Metre(2).__getstate__())
    payload = pickle.dumps(original)
    restored = pickle.loads(payload)
    assert type(restored) is Unpublished
    assert restored == original
    assert __name__ in _strings(payload)


@pytest.mark.parametrize("name", ["Fraction", "UnitDef", "NoSuchQuantity", "__all__"])
def test_unpickling_a_name_that_is_no_published_quantity_is_refused(name: str) -> None:
    with pytest.raises(pickle.UnpicklingError, match="publishes no such quantity"):
        _new_published(name)
