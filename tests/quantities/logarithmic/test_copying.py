"""A level copies and pickles to an equal level."""

from __future__ import annotations

import copy
import pickle
from fractions import Fraction

import pytest

from kuchka.units import logarithmic


def test_copy_and_pickle_round_trip_and_keep_the_display_unit():
    original = logarithmic.Bel(2)
    for restored in (
        copy.copy(original),
        copy.deepcopy(original),
        pickle.loads(pickle.dumps(original)),
    ):
        assert restored == original
        assert restored.unit.symbol == "B"


def test_instances_are_immutable():
    level = logarithmic.Decibel(3)
    with pytest.raises(AttributeError, match="immutable"):
        level._magnitude = Fraction(4)  # noqa: SLF001  # type: ignore[misc]
