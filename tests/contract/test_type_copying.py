"""Every quantity type copies, deep-copies, and pickles to an equal value.

The copy keeps the display unit and stays immutable, and a state restored into a blank
instance gives an equal value.
Restoring is validated like construction; see `test_state_restoring`.
"""

from __future__ import annotations

import copy
import pickle

import pytest

from tests.support.kinds import QUANTITY_TYPES
from tests.support.kinds import TYPE_IDS
from tests.support.kinds import UNIT_TABLES
from tests.support.kinds import sample_of


@pytest.mark.parametrize("cls", QUANTITY_TYPES, ids=TYPE_IDS)
def test_a_value_copies_and_pickles_to_an_equal_value(cls: type) -> None:
    original = sample_of(cls)
    for clone in (
        copy.copy(original),
        copy.deepcopy(original),
        pickle.loads(pickle.dumps(original)),
    ):
        assert clone == original
        assert clone.unit is original.unit


@pytest.mark.parametrize("cls", QUANTITY_TYPES, ids=TYPE_IDS)
def test_a_copy_is_as_immutable_as_the_original(cls: type) -> None:
    clone = copy.deepcopy(sample_of(cls))
    with pytest.raises(AttributeError, match="immutable"):
        clone._magnitude = 1  # type: ignore[assignment]  # noqa: SLF001


@pytest.mark.parametrize("cls", QUANTITY_TYPES, ids=TYPE_IDS)
def test_a_valid_state_restores_an_equal_value(cls: type) -> None:
    original = sample_of(cls)
    blank = cls.__new__(cls)
    blank.__setstate__(original.__getstate__())
    assert blank == original
    assert blank.unit is original.unit


@pytest.mark.parametrize("name", UNIT_TABLES)
def test_a_value_keeps_its_display_unit_through_copy_and_pickle(name: str) -> None:
    for constructor in UNIT_TABLES[name].values():
        original = constructor(7)
        for clone in (
            copy.copy(original),
            copy.deepcopy(original),
            pickle.loads(pickle.dumps(original)),
        ):
            assert clone == original
            assert clone.unit is original.unit
