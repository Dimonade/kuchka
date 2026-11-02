"""Specific activity: the activity in each unit of mass of a material."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import SPECIFIC_ACTIVITY
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register
from kuchka.quantities.base.registry import _rule
from kuchka.quantities.mass import Mass
from kuchka.quantities.radiation.activity import Activity

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.electromagnetics.charge import Charge
    from kuchka.quantities.electromagnetics.specific_current import SpecificCurrent
    from kuchka.quantities.kinematics.acceleration import Acceleration
    from kuchka.quantities.mechanics.density import Density
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.mechanics.impulse import Impulse
    from kuchka.quantities.mechanics.momentum import Momentum
    from kuchka.quantities.mechanics.specific_power import SpecificPower
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.radiation.activity_concentration import ActivityConcentration


class SpecificActivity(LinearQuantity):
    """The activity in each unit of mass, in becquerels per kilogram or gram.

        soil = BecquerelPerKilogram(400)
        sample = soil * Kilogram(0.5)   # an Activity

    What a food, soil, or material measurement reports.
    `Activity / Mass` is a `SpecificActivity`, `SpecificActivity * Mass` is an
    `Activity`, and `Activity / SpecificActivity` is a `Mass`.
    Dimensionally it is any frequency per mass, and `Frequency / Mass` is one too.
    """

    dimension: ClassVar[Dimension] = SPECIFIC_ACTIVITY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Charge) -> SpecificCurrent: ...
    @overload
    def __mul__(self, other: Density) -> ActivityConcentration: ...
    @overload
    def __mul__(self, other: Energy) -> SpecificPower: ...
    @overload
    def __mul__(self, other: Impulse) -> Acceleration: ...
    @overload
    def __mul__(self, other: Mass) -> Activity: ...
    @overload
    def __mul__(self, other: Momentum) -> Acceleration: ...
    @overload
    def __mul__(self, other: Proportion) -> SpecificActivity: ...
    @overload
    def __mul__(self, other: Numeric) -> SpecificActivity: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Proportion) -> SpecificActivity: ...
    @overload
    def __truediv__(self, other: SpecificActivity) -> Proportion: ...
    @overload
    def __truediv__(self, other: Numeric) -> SpecificActivity: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(SPECIFIC_ACTIVITY, SpecificActivity)
_rule(Activity, "/", Mass, SpecificActivity)
_rule(SpecificActivity, "*", Mass, Activity)
_rule(Activity, "/", SpecificActivity, Mass)

__all__ = ["SpecificActivity"]
