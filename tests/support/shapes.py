"""The four shapes a quantity type can have."""

from __future__ import annotations

from kuchka.quantities.base import AffineQuantity
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base import ModularQuantity
from kuchka.quantities.base import PureLogarithmicQuantity

SHAPES = [
    LinearQuantity,
    AffineQuantity,
    ModularQuantity,
    PureLogarithmicQuantity,
]


SHAPE_IDS = [shape.__name__ for shape in SHAPES]
