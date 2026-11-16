"""Activity concentration: the activity in each unit of volume of a fluid."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import ACTIVITY_CONCENTRATION
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register
from kuchka.quantities.base.registry import _rule
from kuchka.quantities.geometry.volume import Volume
from kuchka.quantities.radiation.activity import Activity

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.length import Length
    from kuchka.quantities.mechanics.density import Density
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.radiation.specific_activity import SpecificActivity
    from kuchka.quantities.radiation.surface_activity import SurfaceActivity


class ActivityConcentration(LinearQuantity):
    """The activity in each unit of volume, in becquerels per cubic metre or litre.

        radon = PicocuriePerLitre(4)
        room = radon * CubicMetre(60)   # an Activity

    What a radon monitor or a water assay reports.
    `Activity / Volume` is an `ActivityConcentration`, `ActivityConcentration * Volume`
    is an `Activity`, and `Activity / ActivityConcentration` is a `Volume`.
    Dimensionally it is any frequency per volume, and `Frequency / Volume` is one too.
    """

    dimension: ClassVar[Dimension] = ACTIVITY_CONCENTRATION
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Length) -> SurfaceActivity: ...
    @overload
    def __mul__(self, other: Proportion) -> ActivityConcentration: ...
    @overload
    def __mul__(self, other: Volume) -> Activity: ...
    @overload
    def __mul__(self, other: Numeric) -> ActivityConcentration: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: ActivityConcentration) -> Proportion: ...
    @overload
    def __truediv__(self, other: Density) -> SpecificActivity: ...
    @overload
    def __truediv__(self, other: Proportion) -> ActivityConcentration: ...
    @overload
    def __truediv__(self, other: SpecificActivity) -> Density: ...
    @overload
    def __truediv__(self, other: Numeric) -> ActivityConcentration: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(ACTIVITY_CONCENTRATION, ActivityConcentration)
_rule(Activity, "/", Volume, ActivityConcentration)
_rule(ActivityConcentration, "*", Volume, Activity)
_rule(Activity, "/", ActivityConcentration, Volume)

__all__ = ["ActivityConcentration"]
