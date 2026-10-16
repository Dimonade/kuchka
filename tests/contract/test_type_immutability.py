"""A quantity is born with its state and keeps it.

State is written once, through construction or a validated restore.
After that the magnitude and display unit cannot be rebound, deleted, or replaced by
calling `__init__` or `__setstate__` again.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from tests.support.kinds import QUANTITY_TYPES
from tests.support.kinds import TYPE_IDS
from tests.support.kinds import sample_of

STATE_ATTRIBUTES = ("_magnitude", "_display_unit", "anything_else")


def state_of(value) -> tuple[Fraction, object]:
    """Return the magnitude in the display unit, plus that unit."""
    return (value.value_in(value.unit), value.unit)


@pytest.mark.parametrize("cls", QUANTITY_TYPES, ids=TYPE_IDS)
def test_attributes_cannot_be_rebound_or_deleted(cls: type) -> None:
    value = sample_of(cls)
    before = state_of(value)
    for attribute in STATE_ATTRIBUTES:
        with pytest.raises(AttributeError, match="immutable"):
            setattr(value, attribute, 1)
        with pytest.raises(AttributeError, match="immutable"):
            delattr(value, attribute)
    assert state_of(value) == before


@pytest.mark.parametrize("cls", QUANTITY_TYPES, ids=TYPE_IDS)
def test_the_state_cannot_be_replaced_by_initialising_or_restoring_again(
    cls: type,
) -> None:
    value = sample_of(cls)
    before = state_of(value)
    with pytest.raises(AttributeError, match="immutable"):
        value.__init__(Fraction(9), value.unit)
    with pytest.raises(AttributeError, match="immutable"):
        value.__setstate__((Fraction(9), value.unit))
    assert state_of(value) == before
