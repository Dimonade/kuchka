"""Heat capacity: the energy a body needs to change its temperature by one degree."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Self
from typing import overload

from kuchka.dimensions import HEAT_CAPACITY
from kuchka.errors import IncompatibleDimensionError
from kuchka.errors import InvalidMeasurementError
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register
from kuchka.quantities.thermal import Temperature

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.amount import AmountOfSubstance
    from kuchka.quantities.chemistry.entities_per_amount import EntitiesPerAmount
    from kuchka.quantities.chemistry.molar_heat_capacity import MolarEntropy
    from kuchka.quantities.chemistry.molar_heat_capacity import MolarHeatCapacity
    from kuchka.quantities.mass import Mass
    from kuchka.quantities.mechanics.energy import Energy
    from kuchka.quantities.mechanics.power import Power
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.thermal import TemperatureDelta
    from kuchka.quantities.thermodynamics.heating_rate import HeatingRate
    from kuchka.quantities.thermodynamics.specific_heat_capacity import SpecificEntropy
    from kuchka.quantities.thermodynamics.specific_heat_capacity import (
        SpecificHeatCapacity,
    )


class HeatCapacity(LinearQuantity):
    """The energy that changes a body's temperature by one degree, in joules per kelvin.

        kettle = KilojoulePerKelvin(1.2)
        heat = kettle * DeltaKelvin(80)   # an Energy

    It is the quotient `Energy / TemperatureDelta`.
    `HeatCapacity * TemperatureDelta` is an `Energy`: the heat `Q = C * dT`.
    `Energy / HeatCapacity` is a `TemperatureDelta`, and `Power / HeatCapacity` is a
    `HeatingRate`.
    `HeatCapacity / Mass` is a `SpecificHeatCapacity`, and `SpecificHeatCapacity * Mass`
    is a `HeatCapacity`.
    A joule per degree Celsius is a joule per kelvin, because a Celsius degree is a
    difference.
    `to_entropy()` reads it as an `Entropy`, the other quantity measured in joules per
    kelvin.
    """

    dimension: ClassVar[Dimension] = HEAT_CAPACITY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: EntitiesPerAmount) -> MolarHeatCapacity: ...
    @overload
    def __mul__(self, other: HeatingRate) -> Power: ...
    @overload
    def __mul__(self, other: Proportion) -> HeatCapacity: ...
    @overload
    def __mul__(self, other: TemperatureDelta) -> Energy: ...
    @overload
    def __mul__(self, other: Numeric) -> HeatCapacity: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: AmountOfSubstance) -> MolarHeatCapacity: ...
    @overload
    def __truediv__(self, other: HeatCapacity) -> Proportion: ...
    @overload
    def __truediv__(self, other: Mass) -> SpecificHeatCapacity: ...
    @overload
    def __truediv__(self, other: MolarHeatCapacity) -> AmountOfSubstance: ...
    @overload
    def __truediv__(self, other: Proportion) -> HeatCapacity: ...
    @overload
    def __truediv__(self, other: SpecificHeatCapacity) -> Mass: ...
    @overload
    def __truediv__(self, other: Numeric) -> HeatCapacity: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)

    def to_entropy(self) -> Entropy:
        """View this heat capacity as an `Entropy`, in the same joules per kelvin.

            Calorimeter = KilojoulePerKelvin(1.2).to_entropy()

        Entropy and heat capacity share a unit and are different quantities, so the
        conversion is a statement of meaning, and the display unit carries through.
        """
        return Entropy(self._magnitude, self._display_unit)


class Entropy(LinearQuantity):
    """The measure of a system's disorder, in joules per kelvin.

        change = JoulePerKelvin(5).to_entropy()
        molar_scale = change * 2

    Dimensionally identical to `HeatCapacity`, and a different quantity: the heat that
    changes a temperature by one degree is not an entropy.
    So it is a role of `HeatCapacity`: it adds and subtracts with another `Entropy`,
    scales by a plain number or a `Proportion`, and divides by another `Entropy` into
    a `Proportion`.
    Multiplying it by a temperature difference is refused, because a joule per kelvin
    times a kelvin of difference is not an energy.
    `Entropy / Mass` is a `SpecificEntropy`, and `SpecificEntropy * Mass` is an
    `Entropy`.
    `to_heat_capacity()` and `HeatCapacity.to_entropy()` move between the two, for the
    products that are real, such as the thermal energy `k * T`.
    `Entropy.from_heat(heat, temperature)` is the entropy a heat carries at an absolute
    temperature, `dS = Q / T`.
    """

    dimension: ClassVar[Dimension] = HEAT_CAPACITY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: EntitiesPerAmount) -> MolarEntropy: ...
    @overload
    def __mul__(self, other: Proportion) -> Entropy: ...
    @overload
    def __mul__(self, other: Numeric) -> Entropy: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: AmountOfSubstance) -> MolarEntropy: ...
    @overload
    def __truediv__(self, other: Entropy) -> Proportion: ...
    @overload
    def __truediv__(self, other: Mass) -> SpecificEntropy: ...
    @overload
    def __truediv__(self, other: MolarEntropy) -> AmountOfSubstance: ...
    @overload
    def __truediv__(self, other: Proportion) -> Entropy: ...
    @overload
    def __truediv__(self, other: SpecificEntropy) -> Mass: ...
    @overload
    def __truediv__(self, other: Numeric) -> Entropy: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)

    @classmethod
    def from_heat(cls, heat: Energy, temperature: Temperature) -> Self:
        """Return the entropy a heat carries at an absolute temperature.

            Entropy.from_heat(Joule(300), Kelvin(300)) == JoulePerKelvin(1).to_entropy()

        This is `dS = Q / T` for heat exchanged reversibly at one temperature.
        The temperature is a reading on any scale, taken from absolute zero, so
        `Celsius(27)` and `Kelvin(300.15)` give the same entropy.
        `Energy / Temperature` alone has no result, because a temperature is a point
        and not an interval.

        Raises
        ------
        IncompatibleDimensionError
            If `heat` is not an `Energy` or `temperature` is not a `Temperature`.
        InvalidMeasurementError
            If the temperature is at absolute zero, where `Q / T` has no value.

        """
        from kuchka.quantities.mechanics.energy import Energy  # noqa: PLC0415 -- Energy's module reaches this one through SpecificEnergy

        if not isinstance(heat, Energy) or not isinstance(temperature, Temperature):
            raise IncompatibleDimensionError("build an entropy from", heat, temperature)
        kelvin = temperature.kelvin
        if kelvin <= 0:
            msg = (
                f"cannot build an entropy at a temperature of {float(kelvin)} K: "
                "Q / T has no value at absolute zero."
            )
            raise InvalidMeasurementError(msg)
        return cls(heat._magnitude / kelvin, cls._canonical_unit)  # noqa: SLF001 -- same-package arithmetic on canonical magnitudes

    def to_heat_capacity(self) -> HeatCapacity:
        """View this entropy as a `HeatCapacity`, in the same joules per kelvin.

            thermal = Entropy.to_heat_capacity(change) * DeltaKelvin(300)

        Use it when the product is meant, such as the energy `k * T` of a constant, and
        not to read a change of entropy as a heat.
        The display unit carries through.
        """
        return HeatCapacity(self._magnitude, self._display_unit)


_register(HEAT_CAPACITY, HeatCapacity)
_register(HEAT_CAPACITY, Entropy, specialisation_of=HeatCapacity)

__all__ = ["Entropy", "HeatCapacity"]
