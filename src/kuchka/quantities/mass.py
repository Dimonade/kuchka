"""Mass: how much matter something contains."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import MASS
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.amount import AmountOfSubstance
    from kuchka.quantities.chemistry.entities_per_amount import EntitiesPerAmount
    from kuchka.quantities.chemistry.molality import Molality
    from kuchka.quantities.chemistry.molar_mass import MolarMass
    from kuchka.quantities.current import Current
    from kuchka.quantities.electromagnetics.charge import Charge
    from kuchka.quantities.electromagnetics.specific_charge import SpecificCharge
    from kuchka.quantities.electromagnetics.specific_current import SpecificCurrent
    from kuchka.quantities.geometry.area import Area
    from kuchka.quantities.geometry.volume import Volume
    from kuchka.quantities.kinematics.acceleration import Acceleration
    from kuchka.quantities.kinematics.velocity import Velocity
    from kuchka.quantities.length import Length
    from kuchka.quantities.mechanics.density import Density
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.mechanics.first_moment_of_mass import FirstMomentOfMass
    from kuchka.quantities.mechanics.force import Force
    from kuchka.quantities.mechanics.mass_flow_rate import MassFlowRate
    from kuchka.quantities.mechanics.moment_of_inertia import MomentOfInertia
    from kuchka.quantities.mechanics.momentum import Momentum
    from kuchka.quantities.mechanics.power import Power
    from kuchka.quantities.mechanics.specific_energy import SpecificEnergy
    from kuchka.quantities.mechanics.specific_power import SpecificPower
    from kuchka.quantities.mechanics.velocity_squared import VelocitySquared
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.radiation.activity import Activity
    from kuchka.quantities.radiation.specific_activity import SpecificActivity
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time
    from kuchka.quantities.thermodynamics.heat_capacity import Entropy
    from kuchka.quantities.thermodynamics.heat_capacity import HeatCapacity
    from kuchka.quantities.thermodynamics.specific_heat_capacity import SpecificEntropy
    from kuchka.quantities.thermodynamics.specific_heat_capacity import (
        SpecificHeatCapacity,
    )


class Mass(LinearQuantity):
    """How much matter something contains."""

    dimension: ClassVar[Dimension] = MASS
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Acceleration) -> Force: ...
    @overload
    def __mul__(self, other: Area) -> MomentOfInertia: ...
    @overload
    def __mul__(self, other: EntitiesPerAmount) -> MolarMass: ...
    @overload
    def __mul__(self, other: Frequency) -> MassFlowRate: ...
    @overload
    def __mul__(self, other: Length) -> FirstMomentOfMass: ...
    @overload
    def __mul__(self, other: Molality) -> AmountOfSubstance: ...
    @overload
    def __mul__(self, other: Proportion) -> Mass: ...
    @overload
    def __mul__(self, other: SpecificActivity) -> Activity: ...
    @overload
    def __mul__(self, other: SpecificCharge) -> Charge: ...
    @overload
    def __mul__(self, other: SpecificCurrent) -> Current: ...
    @overload
    def __mul__(self, other: SpecificEnergy) -> Energy: ...
    @overload
    def __mul__(self, other: SpecificEntropy) -> Entropy: ...
    @overload
    def __mul__(self, other: SpecificHeatCapacity) -> HeatCapacity: ...
    @overload
    def __mul__(self, other: SpecificPower) -> Power: ...
    @overload
    def __mul__(self, other: Velocity) -> Momentum: ...
    @overload
    def __mul__(self, other: VelocitySquared) -> Energy: ...
    @overload
    def __mul__(self, other: Numeric) -> Mass: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: AmountOfSubstance) -> MolarMass: ...
    @overload
    def __truediv__(self, other: Density) -> Volume: ...
    @overload
    def __truediv__(self, other: Mass) -> Proportion: ...
    @overload
    def __truediv__(self, other: MassFlowRate) -> Time: ...
    @overload
    def __truediv__(self, other: MolarMass) -> AmountOfSubstance: ...
    @overload
    def __truediv__(self, other: Proportion) -> Mass: ...
    @overload
    def __truediv__(self, other: Time) -> MassFlowRate: ...
    @overload
    def __truediv__(self, other: Volume) -> Density: ...
    @overload
    def __truediv__(self, other: Numeric) -> Mass: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(MASS, Mass)

__all__ = ["Mass"]
