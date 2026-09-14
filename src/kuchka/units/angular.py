"""Unit constructors for Angle: Degree and Radian.

NEITHER CONSTRUCTOR WORKS YET. Both raise `PlannedDimensionError` unconditionally.
This module is not imported by `kuchka.units`'s wildcard aggregation and is not part
of the public API -- see `kuchka.quantities.angular`'s module docstring for the full
reasoning: the degree-radian conversion factor is pi/180, an irrational value with no
exact representation under kuchka's current `Decimal`-only storage model. Shipping
either constructor with a rounded approximation would silently violate the exactness
guarantee every other unit constructor in this library actually holds.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import ANGLE
from kuchka.errors import PlannedDimensionError

if TYPE_CHECKING:
    from kuchka.numeric import Numeric
    from kuchka.quantities.angular import Angle

_PLANNED_NAME = "Angle"


def Degree(value: Numeric) -> Angle:  # noqa: ARG001 -- signature kept stable for when this is implemented; see the module docstring.
    """Not implemented yet: raises `PlannedDimensionError` unconditionally.

    Blocked on kuchka's exact-value model gaining a representation for irrational
    conversion factors -- see `kuchka.quantities.angular`'s module docstring.
    """
    raise PlannedDimensionError(ANGLE, _PLANNED_NAME)


def Radian(value: Numeric) -> Angle:  # noqa: ARG001 -- signature kept stable for when this is implemented; see the module docstring.
    """Not implemented yet: raises `PlannedDimensionError` unconditionally.

    Blocked the same way `Degree` is -- see that function's docstring.
    """
    raise PlannedDimensionError(ANGLE, _PLANNED_NAME)


__all__ = ["Degree", "Radian"]
"""Declared normally, matching every other leaf module's convention.

Not wired into `kuchka.units`'s wildcard aggregation, though -- see
`kuchka.quantities.angular`'s module docstring for why.
"""
