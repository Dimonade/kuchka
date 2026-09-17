"""Angle: a plane angle -- a bearing, a phase, a joint rotation.

NOT YET USABLE.
Nothing about `Angle` works yet, including construction.
This module is not imported by `kuchka.quantities`'s wildcard aggregation and is not
part of the public API -- it exists in `develop` so the type has a stable home to
build on, not because it is ready to use.

The SI-coherent unit for plane angle is the radian, and one of this library's own
design commitments is that a `UnitDef` scale factor is always exact -- no unit
conversion in kuchka silently approximates.
The degree-radian relationship is pi/180: genuinely irrational, with no exact
representation in `Decimal` or `Fraction`.
The already-solved non-power-of-ten cases elsewhere in this library
(`Inch`, `Minute`/`Hour`, ...) have scale factors that are exact rationals, even when
their reciprocals do not terminate in base 10; pi is not rational at all.

Declaring `Degree` the canonical unit to sidestep that would misrepresent the
physically correct SI-coherent unit as a workaround -- exactly the kind of quiet
inaccuracy this library exists to prevent.
So `Angle` ships as a named, importable type with a correctly distinct `dimension`
(see `kuchka.dimensions.ANGLE`), but `_period` and `_canonical_unit` are deliberately
left unset below, and `kuchka.units.angular.Degree`/`Radian` both unconditionally raise
`PlannedDimensionError`.

This is blocked on a decision broader than `Angle` alone: representing pi exactly.
kuchka's internal magnitude storage is `Fraction`, which holds every exact rational
value -- the rational relationships between `Degree`, `Turn`, `Gradian`, `ArcMinute`,
and `ArcSecond` are all representable this way, with no symbolic machinery needed.
`Radian` specifically needs an exact symbolic constant for pi, which `Fraction` cannot
express (no rational number equals pi).
`Angle` will be finished once that representation exists.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar

from kuchka.dimensions import ANGLE
from kuchka.quantities.base import ModularQuantity

if TYPE_CHECKING:
    from kuchka.dimensions import Dimension


class Angle(ModularQuantity):
    """A plane angle. NOT YET USABLE -- see this module's docstring."""

    dimension: ClassVar[Dimension] = ANGLE
    __slots__ = ()

    # NOTE: `_period` and `_canonical_unit` are deliberately left unset.
    # There is no exact value for one full turn expressed in radians (2 * pi):
    # `Fraction` holds exact rationals, and pi is irrational, so this class cannot yet
    # honor `ModularQuantity`'s contract at all.
    # Setting either attribute to a rounded approximation would silently violate
    # kuchka's own exactness guarantee instead of failing loudly.
    # `kuchka.units.angular.Degree`/`Radian`, the only intended entry points for
    # constructing an `Angle`, raise `PlannedDimensionError` unconditionally, so the
    # reason is clear at the call site instead of an `AttributeError` from deep inside
    # `ModularQuantity`.


__all__ = ["Angle"]
"""Declared normally, matching every other leaf module's convention.

Not wired into `kuchka.quantities`'s wildcard aggregation, though -- that omission,
not this list, is what actually keeps `Angle` off the public API for now. See the
module docstring.
"""
