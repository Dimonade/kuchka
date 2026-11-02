"""Surface activity: the activity on each unit of area of a surface."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import SURFACE_ACTIVITY
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register
from kuchka.quantities.base.registry import _rule
from kuchka.quantities.geometry.area import Area
from kuchka.quantities.radiation.activity import Activity

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.geometry.volume import Volume
    from kuchka.quantities.kinematics.acceleration import Acceleration
    from kuchka.quantities.kinematics.velocity import Velocity
    from kuchka.quantities.length import Length
    from kuchka.quantities.mechanics.volumetric_flow_rate import VolumetricFlowRate
    from kuchka.quantities.photometry.illuminance import Illuminance
    from kuchka.quantities.photometry.luminous_energy import LuminousEnergy
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.radiation.activity_concentration import ActivityConcentration


class SurfaceActivity(LinearQuantity):
    """The activity on each unit of area, in becquerels per square metre or centimetre.

        wipe = BecquerelPerSquareCentimetre(4)
        bench = wipe * SquareMetre(2)   # an Activity

    What a contamination monitor or a wipe test reports, and what a fallout map shows.
    `Activity / Area` is a `SurfaceActivity`, `SurfaceActivity * Area` is an `Activity`,
    and `Activity / SurfaceActivity` is an `Area`.
    Dimensionally it is any frequency per area, and `Frequency / Area` is one too.
    """

    dimension: ClassVar[Dimension] = SURFACE_ACTIVITY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Area) -> Activity: ...
    @overload
    def __mul__(self, other: LuminousEnergy) -> Illuminance: ...
    @overload
    def __mul__(self, other: Proportion) -> SurfaceActivity: ...
    @overload
    def __mul__(self, other: Volume) -> Velocity: ...
    @overload
    def __mul__(self, other: VolumetricFlowRate) -> Acceleration: ...
    @overload
    def __mul__(self, other: Numeric) -> SurfaceActivity: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: ActivityConcentration) -> Length: ...
    @overload
    def __truediv__(self, other: Length) -> ActivityConcentration: ...
    @overload
    def __truediv__(self, other: Proportion) -> SurfaceActivity: ...
    @overload
    def __truediv__(self, other: SurfaceActivity) -> Proportion: ...
    @overload
    def __truediv__(self, other: Numeric) -> SurfaceActivity: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(SURFACE_ACTIVITY, SurfaceActivity)
_rule(Activity, "/", Area, SurfaceActivity)
_rule(SurfaceActivity, "*", Area, Activity)
_rule(Activity, "/", SurfaceActivity, Area)

__all__ = ["SurfaceActivity"]
