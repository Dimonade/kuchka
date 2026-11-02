"""Equivalent dose rate: the reading of a dosimeter, in sieverts per unit time."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Self
from typing import overload

from kuchka.dimensions import SPECIFIC_POWER
from kuchka.errors import IncompatibleDimensionError
from kuchka.errors import InvalidMeasurementError
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register
from kuchka.quantities.base.registry import _rule
from kuchka.quantities.mechanics.specific_power import SpecificPower
from kuchka.quantities.proportion import Proportion
from kuchka.quantities.radiation.absorbed_dose_rate import AbsorbedDoseRate
from kuchka.quantities.radiation.equivalent_dose import EquivalentDose
from kuchka.quantities.temporal import Time

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric


class EquivalentDoseRate(LinearQuantity):
    """A dose rate weighted for its biological effect, in sievert per hour or second.

        reading = Microsievert(0.12) / Hour(1)
        shift = reading * Hour(8)   # an EquivalentDose

    What a survey meter or an area dosimeter displays: the ambient dose equivalent rate,
    usually in microsieverts per hour.
    A dose rate times a `Time` is an `EquivalentDose`, an `EquivalentDose` over a `Time`
    is a dose rate, and an `EquivalentDose` over a dose rate is a `Time`.
    Like `EquivalentDose`, it has no way into `SpecificPower`: a sievert per second is
    not a watt per kilogram, and multiplying it by a mass is refused.
    `EquivalentDoseRate.from_absorbed_dose_rate` is the one way in from an
    `AbsorbedDoseRate`.
    """

    dimension: ClassVar[Dimension] = SPECIFIC_POWER
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Proportion) -> EquivalentDoseRate: ...
    @overload
    def __mul__(self, other: Time) -> EquivalentDose: ...
    @overload
    def __mul__(self, other: Numeric) -> EquivalentDoseRate: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: EquivalentDoseRate) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> EquivalentDoseRate: ...
    @overload
    def __truediv__(self, other: Numeric) -> EquivalentDoseRate: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)

    @classmethod
    def from_absorbed_dose_rate(
        cls, dose_rate: AbsorbedDoseRate, weighting_factor: Proportion
    ) -> Self:
        """Return the equivalent dose rate of an absorbed dose rate of one radiation.

            EquivalentDoseRate.from_absorbed_dose_rate(
                MilligrayPerHour(3), icrp_103.ALPHA_PARTICLES
            )   # 60 mSv/h

        The weighting factor is a plain `Proportion`, as for
        `EquivalentDose.from_absorbed_dose`.

        Raises
        ------
        InvalidMeasurementError
            The weighting factor is negative.

        """
        if not isinstance(dose_rate, AbsorbedDoseRate) or not isinstance(
            weighting_factor, Proportion
        ):
            raise IncompatibleDimensionError(
                "build an equivalent dose rate from", dose_rate, weighting_factor
            )
        if weighting_factor._magnitude < 0:  # noqa: SLF001 -- same-package read of the canonical magnitude
            msg = f"a radiation weighting factor is not negative: {weighting_factor!r}."
            raise InvalidMeasurementError(msg)
        magnitude = dose_rate._magnitude * weighting_factor._magnitude  # noqa: SLF001 -- same-package arithmetic on canonical magnitudes
        return cls(magnitude, cls._canonical_unit)


_register(SPECIFIC_POWER, EquivalentDoseRate, specialisation_of=SpecificPower)
_rule(EquivalentDoseRate, "*", Time, EquivalentDose)
_rule(EquivalentDose, "/", Time, EquivalentDoseRate)
_rule(EquivalentDose, "/", EquivalentDoseRate, Time)

__all__ = ["EquivalentDoseRate"]
