"""Absorbed dose: the energy a radiation field deposits in each kilogram of matter."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Self
from typing import overload

from kuchka.dimensions import SPECIFIC_ENERGY
from kuchka.errors import IncompatibleDimensionError
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register
from kuchka.quantities.mechanics.specific_energy import SpecificEnergy

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.proportion import Proportion


class AbsorbedDose(LinearQuantity):
    """The energy deposited per unit mass of an irradiated material, in gray or rad.

        scan = Milligray(12)
        skin_limit = Gray(2)

    Dimensionally identical to `SpecificEnergy`: one gray is one joule per kilogram.
    It adds and subtracts with another `AbsorbedDose`, scales by a plain number or a
    `Proportion`, and divides by another `AbsorbedDose` into a `Proportion`.
    `to_specific_energy()` takes it as a `SpecificEnergy` for any other arithmetic, such
    as the energy a mass of tissue absorbed, and `from_specific_energy` goes the other
    way.
    `EquivalentDose.from_absorbed_dose` weights it by the kind of radiation.
    """

    dimension: ClassVar[Dimension] = SPECIFIC_ENERGY
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Proportion) -> AbsorbedDose: ...
    @overload
    def __mul__(self, other: Numeric) -> AbsorbedDose: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: AbsorbedDose) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> AbsorbedDose: ...
    @overload
    def __truediv__(self, other: Numeric) -> AbsorbedDose: ...
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
        """Return the absorbed dose of a `SpecificEnergy` deposited in a material.

            AbsorbedDose.from_specific_energy(Joule(3) / Kilogram(2)) == Gray(1.5)

        The gray and the joule per kilogram are the same quantity, and the value is
        carried over unchanged.
        """
        if not isinstance(specific_energy, SpecificEnergy):
            raise IncompatibleDimensionError(
                "build an absorbed dose from", specific_energy, specific_energy
            )
        return cls(specific_energy._magnitude, cls._canonical_unit)  # noqa: SLF001 -- same-package retag of canonical magnitudes

    def to_specific_energy(self) -> SpecificEnergy:
        """View this dose as a `SpecificEnergy`, in joules per kilogram.

            Gray(2).to_specific_energy() * Kilogram(3) == Joule(6)

        The gray is one joule per kilogram, and the value is carried over unchanged.
        """
        return SpecificEnergy(self._magnitude, SpecificEnergy._canonical_unit)  # noqa: SLF001 -- SpecificEnergy's own canonical unit


_register(SPECIFIC_ENERGY, AbsorbedDose, specialisation_of=SpecificEnergy)

__all__ = ["AbsorbedDose"]
