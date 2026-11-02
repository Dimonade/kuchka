"""Exposure: the ionisation an X-ray or gamma beam leaves in a mass of air."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Self
from typing import overload

from kuchka.dimensions import SPECIFIC_CHARGE
from kuchka.errors import IncompatibleDimensionError
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register
from kuchka.quantities.electromagnetics.specific_charge import SpecificCharge

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.proportion import Proportion


class Exposure(LinearQuantity):
    """The charge of the ions a photon beam frees in air, per kilogram: coulomb per kg.

        survey = Milliroentgen(5)
        beam = CoulombPerKilogram(0.0001)

    Dimensionally identical to `SpecificCharge`, and the roentgen is its customary unit.
    It adds and subtracts with another `Exposure`, scales by a plain number or a
    `Proportion`, and divides by another `Exposure` into a `Proportion`.
    `to_specific_charge()` takes it as a `SpecificCharge` for any other arithmetic, such
    as the charge freed in a mass of air, and `from_specific_charge` goes the other way.
    Exposure is defined for photons in air only: it is not an absorbed dose.
    """

    dimension: ClassVar[Dimension] = SPECIFIC_CHARGE
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Proportion) -> Exposure: ...
    @overload
    def __mul__(self, other: Numeric) -> Exposure: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: Exposure) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> Exposure: ...
    @overload
    def __truediv__(self, other: Numeric) -> Exposure: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)

    @classmethod
    def from_specific_charge(cls, specific_charge: SpecificCharge) -> Self:
        """Return the exposure that frees `specific_charge` in air.

            Exposure.from_specific_charge(Coulomb(3) / Kilogram(2))

        The value is carried over unchanged, in coulombs per kilogram.
        """
        if not isinstance(specific_charge, SpecificCharge):
            raise IncompatibleDimensionError(
                "build an exposure from", specific_charge, specific_charge
            )
        return cls(specific_charge._magnitude, cls._canonical_unit)  # noqa: SLF001 -- same-package retag of canonical magnitudes

    def to_specific_charge(self) -> SpecificCharge:
        """View this exposure as a `SpecificCharge`, in coulombs per kilogram.

            CoulombPerKilogram(2).to_specific_charge() * Kilogram(3) == Coulomb(6)

        The value is carried over unchanged.
        """
        return SpecificCharge(self._magnitude, SpecificCharge._canonical_unit)  # noqa: SLF001 -- SpecificCharge's own canonical unit


_register(SPECIFIC_CHARGE, Exposure, specialisation_of=SpecificCharge)

__all__ = ["Exposure"]
