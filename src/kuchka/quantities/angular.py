"""Angle: a plane angle -- a bearing, a phase, a joint rotation.

NOT YET USABLE. Nothing about `Angle` works yet, including construction. This module
is not imported by `kuchka.quantities`'s wildcard aggregation and is not part of the
public API -- it exists in `develop` so the type has a stable home to build on, not
because it is ready to use.

The SI-coherent unit for plane angle is the radian, and one of this library's own
design commitments is that a `UnitDef` scale factor is always exact -- no unit
conversion in kuchka silently approximates. The degree-radian relationship is
pi/180: genuinely irrational, with no exact finite representation in `Decimal`, and
no exact representation in `Fraction` either, unlike the already-solved non-power-of-
ten cases elsewhere in this library (`Inch`, `Minute`/`Hour`, ...), whose scale
factors are all exact rationals even when their reciprocals do not terminate in base
10.

Declaring `Degree` the canonical unit to sidestep that would misrepresent the
physically correct SI-coherent unit as a workaround -- exactly the kind of quiet
inaccuracy this library exists to prevent. So `Angle` ships as a named, importable
type with a correctly distinct `dimension` (see `kuchka.dimensions.ANGLE`), but
`_period` and `_canonical_unit` are deliberately left unset below, and
`kuchka.units.angular.Degree`/`Radian` both unconditionally raise
`PlannedDimensionError`.

This is blocked on a decision broader than `Angle` alone: kuchka's internal exact-
value model currently assumes every stored magnitude is a `Decimal`. Supporting
`Angle` correctly needs that model to also represent exact rationals (`Fraction`)
and exact symbolic constants (pi) natively, with `Decimal`/`float` extraction as an
explicit, opt-in materialization step rather than the storage format itself. Once
that representation question is settled, the same fix very likely also unblocks
`KilometrePerHour` and any other unit whose conversion factor is a non-power-of-ten
rational or an irrational constant. `Angle` will be finished then, not before --
see `CHANGELOG.md`.
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

    # NOTE: `_period` and `_canonical_unit` are deliberately left unset. There is
    # no exact value for one full turn expressed in radians (2 * pi) under kuchka's
    # current `Decimal`-only storage model, so this class cannot yet honor
    # `ModularQuantity`'s contract at all -- setting either attribute to a rounded
    # approximation would silently violate kuchka's own exactness guarantee instead
    # of failing loudly. `kuchka.units.angular.Degree`/`Radian`, the only intended
    # entry points for constructing an `Angle`, raise `PlannedDimensionError`
    # unconditionally rather than relying on these being unset to fail naturally,
    # so the reason is clear at the call site instead of an `AttributeError` from
    # deep inside `ModularQuantity`.


__all__ = ["Angle"]
"""Declared normally, matching every other leaf module's convention.

Not wired into `kuchka.quantities`'s wildcard aggregation, though -- that omission,
not this list, is what actually keeps `Angle` off the public API for now. See the
module docstring.
"""
