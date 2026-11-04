"""Specific heat capacity: the energy per mass for one degree of temperature change."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import SPECIFIC_HEAT_CAPACITY
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register
from kuchka.quantities.base.registry import _rule
from kuchka.quantities.mass import Mass
from kuchka.quantities.thermodynamics.heat_capacity import Entropy

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.chemistry.molality import Molality
    from kuchka.quantities.chemistry.molar_heat_capacity import MolarHeatCapacity
    from kuchka.quantities.chemistry.molar_mass import MolarMass
    from kuchka.quantities.mechanics.specific_energy import SpecificEnergy
    from kuchka.quantities.mechanics.specific_power import SpecificPower
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.thermal import TemperatureDelta
    from kuchka.quantities.thermodynamics.heat_capacity import HeatCapacity
    from kuchka.quantities.thermodynamics.heating_rate import HeatingRate


class SpecificHeatCapacity(LinearQuantity):
    """The energy per unit mass that changes a temperature by one degree, in J/(kg K).

        water = KilojoulePerKilogramKelvin(4.184)
        heat = water * Kilogram(2) * DeltaKelvin(30)   # an Energy

    `SpecificHeatCapacity * Mass` is a `HeatCapacity`, and `SpecificHeatCapacity *
    TemperatureDelta` is a `SpecificEnergy`.
    `SpecificEnergy / TemperatureDelta` and `HeatCapacity / Mass` are specific heat
    capacities, and `SpecificEnergy / SpecificHeatCapacity` is a `TemperatureDelta`.
    So the heat `Q = m * c * dT` comes out as an `Energy` however it is grouped.
    A joule per kilogram degree Celsius is a joule per kilogram kelvin, because a
    Celsius degree is a difference.
    `to_specific_entropy()` reads it as a `SpecificEntropy`, the other quantity measured
    in joules per kilogram kelvin.
    """

    dimension: ClassVar[Dimension] = SPECIFIC_HEAT_CAPACITY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: HeatingRate) -> SpecificPower: ...
    @overload
    def __mul__(self, other: Mass) -> HeatCapacity: ...
    @overload
    def __mul__(self, other: MolarMass) -> MolarHeatCapacity: ...
    @overload
    def __mul__(self, other: Proportion) -> SpecificHeatCapacity: ...
    @overload
    def __mul__(self, other: TemperatureDelta) -> SpecificEnergy: ...
    @overload
    def __mul__(self, other: Numeric) -> SpecificHeatCapacity: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Molality) -> MolarHeatCapacity: ...
    @overload
    def __truediv__(self, other: MolarHeatCapacity) -> Molality: ...
    @overload
    def __truediv__(self, other: Proportion) -> SpecificHeatCapacity: ...
    @overload
    def __truediv__(self, other: SpecificHeatCapacity) -> Proportion: ...
    @overload
    def __truediv__(self, other: Numeric) -> SpecificHeatCapacity: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)

    def to_specific_entropy(self) -> SpecificEntropy:
        """View this as a `SpecificEntropy`, in the same joules per kilogram kelvin.

        Specific entropy and specific heat capacity share a unit and are different
        quantities, so the conversion is a statement of meaning.
        The display unit carries through.
        """
        return SpecificEntropy(self._magnitude, self._display_unit)


class SpecificEntropy(LinearQuantity):
    """The entropy per unit mass, in joules per kilogram kelvin.

        steam = JoulePerKilogramKelvin(7000).to_specific_entropy()
        total = steam * Kilogram(2)   # an Entropy

    Dimensionally identical to `SpecificHeatCapacity`, and a different quantity, so it
    is a role of it with the closed arithmetic of `Entropy`.
    `SpecificEntropy * Mass` is an `Entropy`, `Entropy / Mass` is a `SpecificEntropy`,
    and `Entropy / SpecificEntropy` is a `Mass`.
    The gas constant of one gas, in joules per kilogram kelvin, is another quantity of
    this dimension.
    `to_specific_heat_capacity()` and `SpecificHeatCapacity.to_specific_entropy()` move
    between the two.
    """

    dimension: ClassVar[Dimension] = SPECIFIC_HEAT_CAPACITY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Mass) -> Entropy: ...
    @overload
    def __mul__(self, other: Proportion) -> SpecificEntropy: ...
    @overload
    def __mul__(self, other: Numeric) -> SpecificEntropy: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Proportion) -> SpecificEntropy: ...
    @overload
    def __truediv__(self, other: SpecificEntropy) -> Proportion: ...
    @overload
    def __truediv__(self, other: Numeric) -> SpecificEntropy: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)

    def to_specific_heat_capacity(self) -> SpecificHeatCapacity:
        """View this as a `SpecificHeatCapacity`, in the same J/(kg K).

        Use it when the product is meant, and not to read a change of entropy as a heat.
        The display unit carries through.
        """
        return SpecificHeatCapacity(self._magnitude, self._display_unit)


_register(SPECIFIC_HEAT_CAPACITY, SpecificHeatCapacity)
_register(
    SPECIFIC_HEAT_CAPACITY, SpecificEntropy, specialisation_of=SpecificHeatCapacity
)
_rule(Entropy, "/", Mass, SpecificEntropy)
_rule(SpecificEntropy, "*", Mass, Entropy)
_rule(Entropy, "/", SpecificEntropy, Mass)

__all__ = ["SpecificEntropy", "SpecificHeatCapacity"]
