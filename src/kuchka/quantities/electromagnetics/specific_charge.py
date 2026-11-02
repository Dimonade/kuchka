"""Specific charge: electric charge per unit mass."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import SPECIFIC_CHARGE
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.chemistry.molality import Molality
    from kuchka.quantities.chemistry.molar_charge import MolarCharge
    from kuchka.quantities.chemistry.molar_mass import MolarMass
    from kuchka.quantities.current import Current
    from kuchka.quantities.electromagnetics.charge import Charge
    from kuchka.quantities.electromagnetics.magnetic_flux_density import (
        MagneticFluxDensity,
    )
    from kuchka.quantities.mass import Mass
    from kuchka.quantities.mechanics.mass_flow_rate import MassFlowRate
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.temporal import Frequency


class SpecificCharge(LinearQuantity):
    """Electric charge per unit mass, in coulombs per kilogram.

        cell = AmpereHourPerKilogram(0.25)
        charge = cell * Kilogram(0.045)   # a Charge

    It is the quotient `Charge / Mass`, and `SpecificCharge * Mass` is a `Charge`.
    Gravimetric battery capacity and the charge-to-mass ratio of a particle are both
    specific charges.
    `Exposure` is a role of it: the ionisation an X-ray or gamma beam leaves in air.
    """

    dimension: ClassVar[Dimension] = SPECIFIC_CHARGE
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: MagneticFluxDensity) -> Frequency: ...
    @overload
    def __mul__(self, other: Mass) -> Charge: ...
    @overload
    def __mul__(self, other: MassFlowRate) -> Current: ...
    @overload
    def __mul__(self, other: MolarMass) -> MolarCharge: ...
    @overload
    def __mul__(self, other: Proportion) -> SpecificCharge: ...
    @overload
    def __mul__(self, other: Numeric) -> SpecificCharge: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Molality) -> MolarCharge: ...
    @overload
    def __truediv__(self, other: MolarCharge) -> Molality: ...
    @overload
    def __truediv__(self, other: Proportion) -> SpecificCharge: ...
    @overload
    def __truediv__(self, other: SpecificCharge) -> Proportion: ...
    @overload
    def __truediv__(self, other: Numeric) -> SpecificCharge: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)


_register(SPECIFIC_CHARGE, SpecificCharge)

__all__ = ["SpecificCharge"]
