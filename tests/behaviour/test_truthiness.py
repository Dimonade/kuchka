"""A quantity has no truth value, whatever its shape and whatever its magnitude."""

from __future__ import annotations

import pytest

from kuchka import Celsius
from kuchka import Decibel
from kuchka import Degree
from kuchka import Second
from tests.support.families import FAMILIES
from tests.support.families import FAMILY_IDS

OTHER_SHAPES = [
    pytest.param(Celsius, id="Temperature"),
    pytest.param(lambda value: Second(value).to_instant(), id="Instant"),
    pytest.param(Degree, id="Angle"),
    pytest.param(Decibel, id="LogarithmicRatio"),
]


@pytest.mark.parametrize("family", FAMILIES, ids=FAMILY_IDS)
def test_a_linear_quantity_has_no_truth_value(family) -> None:
    with pytest.raises(TypeError, match="is None"):
        bool(family.canonical(0))


@pytest.mark.parametrize("make", OTHER_SHAPES)
@pytest.mark.parametrize("value", [0, 1])
def test_a_quantity_of_another_shape_has_no_truth_value(make, value) -> None:
    with pytest.raises(TypeError, match="ambiguous"):
        bool(make(value))
