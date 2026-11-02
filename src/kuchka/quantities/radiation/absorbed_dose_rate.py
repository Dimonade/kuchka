"""Absorbed dose rate: the absorbed dose a radiation field delivers per unit time."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Self
from typing import overload

from kuchka.dimensions import SPECIFIC_POWER
from kuchka.errors import IncompatibleDimensionError
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register
from kuchka.quantities.base.registry import _rule
from kuchka.quantities.mechanics.specific_power import SpecificPower
from kuchka.quantities.radiation.absorbed_dose import AbsorbedDose
from kuchka.quantities.temporal import Time

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.proportion import Proportion


class AbsorbedDoseRate(LinearQuantity):
    """The absorbed dose delivered per unit time, in gray per second, hour, or minute.

        field = MicrograyPerHour(0.09)
        shift = field * Hour(8)   # an AbsorbedDose

    Dimensionally identical to `SpecificPower`: one gray per second is one watt per
    kilogram.
    A dose rate times a `Time` is an `AbsorbedDose`, an `AbsorbedDose` over a `Time` is
    a dose rate, and an `AbsorbedDose` over a dose rate is a `Time`.
    Any other product goes through `to_specific_power()` first, and
    `from_specific_power` goes the other way.
    `EquivalentDoseRate.from_absorbed_dose_rate` weights it by the kind of radiation.
    """

    dimension: ClassVar[Dimension] = SPECIFIC_POWER
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Proportion) -> AbsorbedDoseRate: ...
    @overload
    def __mul__(self, other: Time) -> AbsorbedDose: ...
    @overload
    def __mul__(self, other: Numeric) -> AbsorbedDoseRate: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: AbsorbedDoseRate) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> AbsorbedDoseRate: ...
    @overload
    def __truediv__(self, other: Numeric) -> AbsorbedDoseRate: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)

    @classmethod
    def from_specific_power(cls, specific_power: SpecificPower) -> Self:
        """Return the absorbed dose rate of a `SpecificPower` deposited in a material.

            AbsorbedDoseRate.from_specific_power(Watt(3) / Kilogram(2))

        The gray per second and the watt per kilogram are the same quantity, and the
        value is carried over unchanged.
        """
        if not isinstance(specific_power, SpecificPower):
            raise IncompatibleDimensionError(
                "build an absorbed dose rate from", specific_power, specific_power
            )
        return cls(specific_power._magnitude, cls._canonical_unit)  # noqa: SLF001 -- same-package retag of canonical magnitudes

    def to_specific_power(self) -> SpecificPower:
        """View this dose rate as a `SpecificPower`, in watts per kilogram.

        The gray per second is one watt per kilogram, and the value is carried over
        unchanged.
        """
        return SpecificPower(self._magnitude, SpecificPower._canonical_unit)  # noqa: SLF001 -- SpecificPower's own canonical unit


_register(SPECIFIC_POWER, AbsorbedDoseRate, specialisation_of=SpecificPower)
_rule(AbsorbedDoseRate, "*", Time, AbsorbedDose)
_rule(AbsorbedDose, "/", Time, AbsorbedDoseRate)
_rule(AbsorbedDose, "/", AbsorbedDoseRate, Time)

__all__ = ["AbsorbedDoseRate"]
