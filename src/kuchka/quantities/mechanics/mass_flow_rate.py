"""Mass flow rate: the mass that passes a section per unit of time."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import MASS_FLOW_RATE
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.chemistry.molality import Molality
    from kuchka.quantities.chemistry.molar_flow_rate import MolarFlowRate
    from kuchka.quantities.chemistry.molar_mass import MolarMass
    from kuchka.quantities.current import Current
    from kuchka.quantities.electromagnetics.charge import Charge
    from kuchka.quantities.electromagnetics.magnetic_flux_density import (
        MagneticFluxDensity,
    )
    from kuchka.quantities.electromagnetics.specific_charge import SpecificCharge
    from kuchka.quantities.kinematics.velocity import Velocity
    from kuchka.quantities.mass import Mass
    from kuchka.quantities.mechanics.density import Density
    from kuchka.quantities.mechanics.force import Force
    from kuchka.quantities.mechanics.power import Power
    from kuchka.quantities.mechanics.specific_energy import SpecificEnergy
    from kuchka.quantities.mechanics.velocity_squared import VelocitySquared
    from kuchka.quantities.mechanics.volumetric_flow_rate import VolumetricFlowRate
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time


class MassFlowRate(LinearQuantity):
    """The mass that passes a section per unit of time: kilograms per second."""

    dimension: ClassVar[Dimension] = MASS_FLOW_RATE
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Molality) -> MolarFlowRate: ...
    @overload
    def __mul__(self, other: Proportion) -> MassFlowRate: ...
    @overload
    def __mul__(self, other: SpecificCharge) -> Current: ...
    @overload
    def __mul__(self, other: SpecificEnergy) -> Power: ...
    @overload
    def __mul__(self, other: Time) -> Mass: ...
    @overload
    def __mul__(self, other: Velocity) -> Force: ...
    @overload
    def __mul__(self, other: VelocitySquared) -> Power: ...
    @overload
    def __mul__(self, other: Numeric) -> MassFlowRate: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Charge) -> MagneticFluxDensity: ...
    @overload
    def __truediv__(self, other: Density) -> VolumetricFlowRate: ...
    @overload
    def __truediv__(self, other: Frequency) -> Mass: ...
    @overload
    def __truediv__(self, other: MagneticFluxDensity) -> Charge: ...
    @overload
    def __truediv__(self, other: Mass) -> Frequency: ...
    @overload
    def __truediv__(self, other: MassFlowRate) -> Proportion: ...
    @overload
    def __truediv__(self, other: MolarFlowRate) -> MolarMass: ...
    @overload
    def __truediv__(self, other: MolarMass) -> MolarFlowRate: ...
    @overload
    def __truediv__(self, other: Proportion) -> MassFlowRate: ...
    @overload
    def __truediv__(self, other: VolumetricFlowRate) -> Density: ...
    @overload
    def __truediv__(self, other: Numeric) -> MassFlowRate: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(MASS_FLOW_RATE, MassFlowRate)

__all__ = ["MassFlowRate"]
