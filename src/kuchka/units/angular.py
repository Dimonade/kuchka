"""Unit constructors for Angle: Degree and Radian.

NEITHER CONSTRUCTOR WORKS YET.
Both raise `PlannedDimensionError` unconditionally.
Not imported by any wildcard aggregation; not part of the public API.

The degree-radian conversion factor is pi/180: pi is irrational, with no exact
rational representation.
kuchka's magnitude storage is `Fraction`, which holds every exact rational value but
cannot hold pi.
Shipping either constructor with a rounded approximation would violate the exactness
guarantee every other unit constructor in this library holds.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import ANGLE
from kuchka.errors import PlannedDimensionError

if TYPE_CHECKING:
    from kuchka.numeric import Numeric
    from kuchka.quantities.angular import Angle

_PLANNED_NAME = "Angle"


def Degree(value: Numeric) -> Angle:  # noqa: ARG001 -- signature kept stable for when this is implemented.
    """Raise `PlannedDimensionError` unconditionally. Not implemented."""
    raise PlannedDimensionError(ANGLE, _PLANNED_NAME)


def Radian(value: Numeric) -> Angle:  # noqa: ARG001 -- signature kept stable for when this is implemented.
    """Raise `PlannedDimensionError` unconditionally. Not implemented."""
    raise PlannedDimensionError(ANGLE, _PLANNED_NAME)


__all__ = ["Degree", "Radian"]
"""Declared normally, matching every other leaf module's convention.

Not wired into a wildcard aggregation, kept off the public API.
"""
