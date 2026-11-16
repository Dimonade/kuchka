"""Catalytic activity: the rate at which a catalyst converts a substrate."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import MOLAR_FLOW_RATE
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register
from kuchka.quantities.chemistry.molar_flow_rate import MolarFlowRate

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.proportion import Proportion


class CatalyticActivity(LinearQuantity):
    """The rate at which a catalyst converts a substrate, in katal or enzyme units.

        enzyme = Microkatal(2)
        dose = enzyme * Percent(50)

    Dimensionally identical to `MolarFlowRate`: one katal is one mole converted per
    second.
    It adds and subtracts with another `CatalyticActivity`, scales by a plain number or
    a `Proportion`, and divides by another `CatalyticActivity` into a `Proportion`.
    `to_molar_flow_rate()` takes it as a `MolarFlowRate` for any other arithmetic, such
    as the amount converted over a time.
    """

    dimension: ClassVar[Dimension] = MOLAR_FLOW_RATE
    __slots__ = ()

    # BEGIN GENERATED __mul__
    @overload
    def __mul__(self, other: Proportion) -> CatalyticActivity: ...
    @overload
    def __mul__(self, other: Numeric) -> CatalyticActivity: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    # BEGIN GENERATED __truediv__
    @overload
    def __truediv__(self, other: CatalyticActivity) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> CatalyticActivity: ...
    @overload
    def __truediv__(self, other: Numeric) -> CatalyticActivity: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    # END GENERATED

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)

    def to_molar_flow_rate(self) -> MolarFlowRate:
        """View this catalytic activity as a `MolarFlowRate`, in moles per second.

            Microkatal(3).to_molar_flow_rate() == MolePerSecond(0.000003)

        The katal and the mole per second are the same unit, and the value is carried
        over unchanged.
        """
        return MolarFlowRate(self._magnitude, MolarFlowRate._canonical_unit)  # noqa: SLF001 -- MolarFlowRate's own canonical unit


_register(MOLAR_FLOW_RATE, CatalyticActivity, specialisation_of=MolarFlowRate)

__all__ = ["CatalyticActivity"]
