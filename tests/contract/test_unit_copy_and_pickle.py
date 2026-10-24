"""Every published unit copies and pickles to itself, under every pickle protocol.

A unit is an immutable constant: copying returns the same object, and pickling stores
only the name `kuchka.units` publishes it under.
The cases are the published units, so a unit added to the library is covered without
an edit here.
"""

from __future__ import annotations

import copy
import pickle

import pytest

from tests.support.kinds import PUBLISHED_UNITS
from tests.support.values import PICKLE_PROTOCOLS


@pytest.mark.parametrize("name", PUBLISHED_UNITS)
def test_a_published_unit_copies_and_pickles_to_itself(name: str) -> None:
    unit = PUBLISHED_UNITS[name]
    assert copy.copy(unit) is unit
    assert copy.deepcopy(unit) is unit
    for protocol in PICKLE_PROTOCOLS:
        restored = pickle.loads(pickle.dumps(unit, protocol=protocol))
        assert restored is unit, protocol
