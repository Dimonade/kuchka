"""Exposure rate: the exposure a photon beam delivers in air per unit time."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Self
from typing import overload

from kuchka.dimensions import SPECIFIC_CURRENT
from kuchka.errors import IncompatibleDimensionError
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register
from kuchka.quantities.base.registry import _rule
from kuchka.quantities.electromagnetics.specific_current import SpecificCurrent
from kuchka.quantities.radiation.exposure import Exposure
from kuchka.quantities.temporal import Time

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.proportion import Proportion


class ExposureRate(LinearQuantity):
    """The exposure delivered per unit time, in roentgen per hour or minute.

        reading = MilliroentgenPerHour(2.5)
        visit = reading * Minute(30)   # an Exposure

    What a survey meter calibrated in roentgens displays.
    Dimensionally identical to `SpecificCurrent`: coulombs per kilogram per second are
    amperes per kilogram.
    An exposure rate times a `Time` is an `Exposure`, an `Exposure` over a `Time` is an
    exposure rate, and an `Exposure` over an exposure rate is a `Time`.
    Any other product goes through `to_specific_current()` first, and
    `from_specific_current` goes the other way.
    Like `Exposure`, it is defined for photons in air: it is not a dose rate.
    """

    dimension: ClassVar[Dimension] = SPECIFIC_CURRENT
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Proportion) -> ExposureRate: ...
    @overload
    def __mul__(self, other: Time) -> Exposure: ...
    @overload
    def __mul__(self, other: Numeric) -> ExposureRate: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: ExposureRate) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> ExposureRate: ...
    @overload
    def __truediv__(self, other: Numeric) -> ExposureRate: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)

    @classmethod
    def from_specific_current(cls, specific_current: SpecificCurrent) -> Self:
        """Return the exposure rate that frees `specific_current` in air.

            ExposureRate.from_specific_current(Ampere(3) / Kilogram(2))

        The value is carried over unchanged, in amperes per kilogram.
        """
        if not isinstance(specific_current, SpecificCurrent):
            raise IncompatibleDimensionError(
                "build an exposure rate from", specific_current, specific_current
            )
        return cls(specific_current._magnitude, cls._canonical_unit)  # noqa: SLF001 -- same-package retag of canonical magnitudes

    def to_specific_current(self) -> SpecificCurrent:
        """View this exposure rate as a `SpecificCurrent`, in amperes per kilogram.

        The value is carried over unchanged.
        """
        return SpecificCurrent(self._magnitude, SpecificCurrent._canonical_unit)  # noqa: SLF001 -- SpecificCurrent's own canonical unit


_register(SPECIFIC_CURRENT, ExposureRate, specialisation_of=SpecificCurrent)
_rule(ExposureRate, "*", Time, Exposure)
_rule(Exposure, "/", Time, ExposureRate)
_rule(Exposure, "/", ExposureRate, Time)

__all__ = ["ExposureRate"]
