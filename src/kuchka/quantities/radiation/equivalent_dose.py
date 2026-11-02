"""Equivalent dose: absorbed dose weighted by what the radiation does to tissue."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Self
from typing import overload

from kuchka.dimensions import SPECIFIC_ENERGY
from kuchka.errors import IncompatibleDimensionError
from kuchka.errors import InvalidMeasurementError
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register
from kuchka.quantities.mechanics.specific_energy import SpecificEnergy
from kuchka.quantities.proportion import Proportion
from kuchka.quantities.radiation.absorbed_dose import AbsorbedDose

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.radiation.equivalent_dose_rate import EquivalentDoseRate
    from kuchka.quantities.temporal import Time


class EquivalentDose(LinearQuantity):
    """A dose weighted for its biological effect, in sievert or rem.

        reading = Microsievert(0.12)
        annual = reading * Percent(50)

    A sievert is a joule per kilogram, like a gray, but it measures risk to a person
    and not energy deposited: the same absorbed dose of alpha particles is worth twenty
    times that of gamma rays.
    So it is a role of `SpecificEnergy` with no way back to one: it adds and subtracts
    with another `EquivalentDose`, scales by a plain number or a `Proportion`, and
    divides by another `EquivalentDose` into a `Proportion`.
    Multiplying it by a mass is refused, because a sievert times a kilogram is not an
    energy.
    `EquivalentDose.from_absorbed_dose` is the one way in from an `AbsorbedDose`.

    The type covers the protection quantities measured in sieverts: equivalent dose,
    effective dose, and the ambient and personal dose equivalents an instrument reads.
    """

    dimension: ClassVar[Dimension] = SPECIFIC_ENERGY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Proportion) -> EquivalentDose: ...
    @overload
    def __mul__(self, other: Numeric) -> EquivalentDose: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: EquivalentDose) -> Proportion: ...
    @overload
    def __truediv__(self, other: EquivalentDoseRate) -> Time: ...
    @overload
    def __truediv__(self, other: Proportion) -> EquivalentDose: ...
    @overload
    def __truediv__(self, other: Time) -> EquivalentDoseRate: ...
    @overload
    def __truediv__(self, other: Numeric) -> EquivalentDose: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)

    @classmethod
    def from_absorbed_dose(
        cls, dose: AbsorbedDose, weighting_factor: Proportion
    ) -> Self:
        """Return the equivalent dose of an absorbed dose of one kind of radiation.

            EquivalentDose.from_absorbed_dose(Milligray(3), Ratio(20))
            # 60 mSv: alpha particles, at the weighting factor of ICRP 103

        The weighting factor is a plain `Proportion`.
        `kuchka.constants.icrp_103` has the values the ICRP recommends, such as
        `ALPHA_PARTICLES`.
        A field of several kinds of radiation is the sum of one such dose for each.

        Raises
        ------
        InvalidMeasurementError
            The weighting factor is negative.

        """
        if not isinstance(dose, AbsorbedDose) or not isinstance(
            weighting_factor, Proportion
        ):
            raise IncompatibleDimensionError(
                "build an equivalent dose from", dose, weighting_factor
            )
        if weighting_factor._magnitude < 0:  # noqa: SLF001 -- same-package read of the canonical magnitude
            msg = f"a radiation weighting factor is not negative: {weighting_factor!r}."
            raise InvalidMeasurementError(msg)
        return cls(dose._magnitude * weighting_factor._magnitude, cls._canonical_unit)  # noqa: SLF001 -- same-package arithmetic on canonical magnitudes


_register(SPECIFIC_ENERGY, EquivalentDose, specialisation_of=SpecificEnergy)

__all__ = ["EquivalentDose"]
