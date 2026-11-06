"""Velocity squared: a velocity times a velocity."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Self
from typing import overload

from kuchka.dimensions import VELOCITY_SQUARED
from kuchka.errors import IncompatibleDimensionError
from kuchka.errors import _register_hint
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register
from kuchka.quantities.base.registry import _rule
from kuchka.quantities.kinematics.velocity import Velocity
from kuchka.quantities.mechanics.density import Density
from kuchka.quantities.mechanics.pressure import Pressure
from kuchka.quantities.mechanics.specific_energy import SpecificEnergy

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.chemistry.molality import Molality
    from kuchka.quantities.chemistry.molar_energy import MolarEnergy
    from kuchka.quantities.chemistry.molar_mass import MolarMass
    from kuchka.quantities.electromagnetics.magnetic_flux import MagneticFlux
    from kuchka.quantities.electromagnetics.specific_charge import SpecificCharge
    from kuchka.quantities.electromagnetics.specific_current import SpecificCurrent
    from kuchka.quantities.electromagnetics.voltage import Voltage
    from kuchka.quantities.geometry.area import Area
    from kuchka.quantities.kinematics.acceleration import Acceleration
    from kuchka.quantities.kinematics.time_squared import TimeSquared
    from kuchka.quantities.length import Length
    from kuchka.quantities.mass import Mass
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.mechanics.mass_flow_rate import MassFlowRate
    from kuchka.quantities.mechanics.power import Power
    from kuchka.quantities.mechanics.specific_power import SpecificPower
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency
    from kuchka.quantities.temporal import Time
    from kuchka.quantities.thermal import TemperatureDelta
    from kuchka.quantities.thermodynamics.specific_heat_capacity import (
        SpecificHeatCapacity,
    )


class VelocitySquared(LinearQuantity):
    """A velocity times a velocity, in square metres per second squared.

        orbital = SquareKilometrePerSecondSquared(62.5)
        dynamic = KilogramPerCubicMetre(1.2) * (speed * speed) / 2   # a Pressure

    It appears in many formulas: `Density * VelocitySquared` is a `Pressure`,
    `VelocitySquared / Length` an `Acceleration`, and `VelocitySquared * Mass` an
    `Energy`.
    It shares its dimension with `SpecificEnergy`, and the two are contested: the
    kinetic energy per mass of a velocity is half its square, which is
    `VelocitySquared.to_specific_energy()`, and `VelocitySquared.from_specific_energy`
    goes the other way.
    """

    dimension: ClassVar[Dimension] = VELOCITY_SQUARED
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Density) -> Pressure: ...
    @overload
    def __mul__(self, other: Frequency) -> SpecificPower: ...
    @overload
    def __mul__(self, other: Mass) -> Energy: ...
    @overload
    def __mul__(self, other: MassFlowRate) -> Power: ...
    @overload
    def __mul__(self, other: MolarMass) -> MolarEnergy: ...
    @overload
    def __mul__(self, other: Proportion) -> VelocitySquared: ...
    @overload
    def __mul__(self, other: TimeSquared) -> Area: ...
    @overload
    def __mul__(self, other: Numeric) -> VelocitySquared: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Acceleration) -> Length: ...
    @overload
    def __truediv__(self, other: Length) -> Acceleration: ...
    @overload
    def __truediv__(self, other: MagneticFlux) -> SpecificCurrent: ...
    @overload
    def __truediv__(self, other: Molality) -> MolarEnergy: ...
    @overload
    def __truediv__(self, other: MolarEnergy) -> Molality: ...
    @overload
    def __truediv__(self, other: Proportion) -> VelocitySquared: ...
    @overload
    def __truediv__(self, other: SpecificCharge) -> Voltage: ...
    @overload
    def __truediv__(self, other: SpecificCurrent) -> MagneticFlux: ...
    @overload
    def __truediv__(self, other: SpecificEnergy) -> Proportion: ...
    @overload
    def __truediv__(self, other: SpecificHeatCapacity) -> TemperatureDelta: ...
    @overload
    def __truediv__(self, other: SpecificPower) -> Time: ...
    @overload
    def __truediv__(self, other: TemperatureDelta) -> SpecificHeatCapacity: ...
    @overload
    def __truediv__(self, other: Time) -> SpecificPower: ...
    @overload
    def __truediv__(self, other: Velocity) -> Velocity: ...
    @overload
    def __truediv__(self, other: VelocitySquared) -> Proportion: ...
    @overload
    def __truediv__(self, other: Voltage) -> SpecificCharge: ...
    @overload
    def __truediv__(self, other: Numeric) -> VelocitySquared: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)

    @classmethod
    def from_specific_energy(cls, specific_energy: SpecificEnergy) -> Self:
        """Return the squared velocity at which a body carries `specific_energy`.

            VelocitySquared.from_specific_energy(JoulePerKilogram(8))

        The kinetic energy per mass of a velocity `v` is `v² / 2`, so the square is
        twice the specific energy.
        """
        if not isinstance(specific_energy, SpecificEnergy):
            raise IncompatibleDimensionError(
                "build a squared velocity from", specific_energy, specific_energy
            )
        return cls(2 * specific_energy._magnitude, cls._canonical_unit)  # noqa: SLF001 -- same-package retag of canonical magnitudes

    def to_specific_energy(self) -> SpecificEnergy:
        """Return half of this square: the kinetic energy per mass of the velocity.

        (MetrePerSecond(4) * MetrePerSecond(4)).to_specific_energy()
        """
        return SpecificEnergy(self._magnitude / 2, SpecificEnergy._canonical_unit)  # noqa: SLF001 -- same-package retag of canonical magnitudes


_register(VELOCITY_SQUARED, VelocitySquared, contested_with=SpecificEnergy)
_rule(Velocity, "*", Velocity, VelocitySquared)
_rule(Density, "*", VelocitySquared, Pressure)
_register_hint(
    VelocitySquared,
    SpecificEnergy,
    "A squared velocity is twice a kinetic energy per mass: convert with "
    "`VelocitySquared.to_specific_energy()` (the half) or "
    "`VelocitySquared.from_specific_energy(...)` (the double).",
)

__all__ = ["VelocitySquared"]
