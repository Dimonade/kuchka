"""Molar heat capacity and molar entropy: the heat capacity and entropy of one mole."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import MOLAR_HEAT_CAPACITY
from kuchka.internal.typing import override
from kuchka.quantities.amount import AmountOfSubstance
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register
from kuchka.quantities.base.registry import _rule
from kuchka.quantities.chemistry.entities_per_amount import EntitiesPerAmount
from kuchka.quantities.thermodynamics.heat_capacity import Entropy

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.chemistry.molality import Molality
    from kuchka.quantities.chemistry.molar_energy import MolarEnergy
    from kuchka.quantities.chemistry.molar_mass import MolarMass
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.thermal import TemperatureDelta
    from kuchka.quantities.thermodynamics.heat_capacity import HeatCapacity
    from kuchka.quantities.thermodynamics.specific_heat_capacity import (
        SpecificHeatCapacity,
    )


class MolarHeatCapacity(LinearQuantity):
    """The energy that changes the temperature of one mole by one degree, in J/(mol K).

        helium = JoulePerMoleKelvin(12.47)
        heat = helium * AmountOfSubstance(2) * DeltaKelvin(10)   # an Energy

    It is the quotient `HeatCapacity / AmountOfSubstance`, and
    `MolarHeatCapacity * AmountOfSubstance` is a `HeatCapacity`.
    `MolarEnergy / TemperatureDelta` is a `MolarHeatCapacity`, and
    `MolarHeatCapacity * TemperatureDelta` is a `MolarEnergy`.
    A joule per mole degree Celsius is a joule per mole kelvin, because a Celsius degree
    is a difference.
    `to_molar_entropy()` reads it as a `MolarEntropy`, the other quantity measured in
    joules per mole kelvin.
    """

    dimension: ClassVar[Dimension] = MOLAR_HEAT_CAPACITY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: AmountOfSubstance) -> HeatCapacity: ...
    @overload
    def __mul__(self, other: Molality) -> SpecificHeatCapacity: ...
    @overload
    def __mul__(self, other: Proportion) -> MolarHeatCapacity: ...
    @overload
    def __mul__(self, other: TemperatureDelta) -> MolarEnergy: ...
    @overload
    def __mul__(self, other: Numeric) -> MolarHeatCapacity: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: EntitiesPerAmount) -> HeatCapacity: ...
    @overload
    def __truediv__(self, other: HeatCapacity) -> EntitiesPerAmount: ...
    @overload
    def __truediv__(self, other: MolarHeatCapacity) -> Proportion: ...
    @overload
    def __truediv__(self, other: MolarMass) -> SpecificHeatCapacity: ...
    @overload
    def __truediv__(self, other: Proportion) -> MolarHeatCapacity: ...
    @overload
    def __truediv__(self, other: SpecificHeatCapacity) -> MolarMass: ...
    @overload
    def __truediv__(self, other: Numeric) -> MolarHeatCapacity: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)

    def to_molar_entropy(self) -> MolarEntropy:
        """View this as a `MolarEntropy`, in the same joules per mole kelvin.

        Molar entropy and molar heat capacity share a unit and are different
        quantities, so the conversion is a statement of meaning.
        The display unit carries through.
        """
        return MolarEntropy(self._magnitude, self._display_unit)


class MolarEntropy(LinearQuantity):
    """The entropy of one mole, in joules per mole kelvin.

        standard = JoulePerMoleKelvin(188.8).to_molar_entropy()
        total = standard * AmountOfSubstance(2)   # an Entropy

    Dimensionally identical to `MolarHeatCapacity`, and a different quantity, so it is
    a role of it with the closed arithmetic of `Entropy`.
    `MolarEntropy * AmountOfSubstance` is an `Entropy`, `Entropy / AmountOfSubstance` is
    a `MolarEntropy`, and `Entropy / MolarEntropy` is an `AmountOfSubstance`.
    `EntitiesPerAmount * Entropy` is a `MolarEntropy` too: the molar gas constant is the
    Avogadro constant times the Boltzmann constant, `R = N_A * k`.
    `to_molar_heat_capacity()` and `MolarHeatCapacity.to_molar_entropy()` move between
    the two.
    """

    dimension: ClassVar[Dimension] = MOLAR_HEAT_CAPACITY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: AmountOfSubstance) -> Entropy: ...
    @overload
    def __mul__(self, other: Proportion) -> MolarEntropy: ...
    @overload
    def __mul__(self, other: Numeric) -> MolarEntropy: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: EntitiesPerAmount) -> Entropy: ...
    @overload
    def __truediv__(self, other: Entropy) -> EntitiesPerAmount: ...
    @overload
    def __truediv__(self, other: MolarEntropy) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> MolarEntropy: ...
    @overload
    def __truediv__(self, other: Numeric) -> MolarEntropy: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)

    def to_molar_heat_capacity(self) -> MolarHeatCapacity:
        """View this as a `MolarHeatCapacity`, in the same joules per mole kelvin.

        Use it when the product is meant, and not to read a change of entropy as a heat.
        The display unit carries through.
        """
        return MolarHeatCapacity(self._magnitude, self._display_unit)


_register(MOLAR_HEAT_CAPACITY, MolarHeatCapacity)
_register(MOLAR_HEAT_CAPACITY, MolarEntropy, specialisation_of=MolarHeatCapacity)
_rule(Entropy, "/", AmountOfSubstance, MolarEntropy)
_rule(MolarEntropy, "*", AmountOfSubstance, Entropy)
_rule(Entropy, "/", MolarEntropy, AmountOfSubstance)
_rule(EntitiesPerAmount, "*", Entropy, MolarEntropy)
_rule(MolarEntropy, "/", EntitiesPerAmount, Entropy)
_rule(MolarEntropy, "/", Entropy, EntitiesPerAmount)

__all__ = ["MolarEntropy", "MolarHeatCapacity"]
