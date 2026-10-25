"""ApparentPower and ReactivePower: the two powers of an alternating-current circuit.

An AC circuit has three powers that share the watt's dimension and differ in what
they say: the active power `P` that does work (watts), the reactive power `Q` that
swings back and forth (var), and the apparent power `S` that the source has to supply
(volt-amperes).

`Power` is the active one.
`ApparentPower` and `ReactivePower` are roles of it, each with its own units, so a
`VoltAmpere` and a `Watt` never add by accident, and the product of an apparent power
and a time is not taken for an energy.
`to_power()` takes either as a plain `Power` when the number is what matters.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import POWER
from kuchka.internal.typing import override
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register
from kuchka.quantities.mechanics.power import Power

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.proportion import Proportion


class ApparentPower(LinearQuantity):
    """The power a source supplies to a load, in volt-amperes: `S = V I` in RMS.

        supply = KilovoltAmpere(5)
        headroom = supply - VoltAmpere(3200)

    It adds and subtracts with another `ApparentPower`, scales by a plain number or a
    `Proportion`, and divides by another `ApparentPower` into a `Proportion`.
    `to_power()` takes it as a `Power` for any other arithmetic.
    """

    dimension: ClassVar[Dimension] = POWER
    __slots__ = ()

    @overload
    def __mul__(self, other: Proportion) -> ApparentPower: ...
    @overload
    def __mul__(self, other: Numeric) -> ApparentPower: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: ApparentPower) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> ApparentPower: ...
    @overload
    def __truediv__(self, other: Numeric) -> ApparentPower: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)

    def to_power(self) -> Power:
        """View this apparent power as an ordinary `Power`, as a number of watts.

            KilovoltAmpere(5).to_power() == Kilowatt(5)

        The volt-ampere and the watt are the same quantity of joules per second, and
        the value is carried over unchanged.
        """
        return Power(self._magnitude, Power._canonical_unit)  # noqa: SLF001 -- Power's own canonical unit


class ReactivePower(LinearQuantity):
    """The power that swings between source and load, in var: `Q = V I sin(phi)`.

        capacitor = Kilovar(2)
        net = capacitor - Kilovar(3.5)   # -1.5 kvar, an inductive load

    It adds and subtracts with another `ReactivePower`, scales by a plain number or a
    `Proportion`, and divides by another `ReactivePower` into a `Proportion`.
    The sign says whether the load is capacitive or inductive.
    `to_power()` takes it as a `Power` for any other arithmetic.
    """

    dimension: ClassVar[Dimension] = POWER
    __slots__ = ()

    @overload
    def __mul__(self, other: Proportion) -> ReactivePower: ...
    @overload
    def __mul__(self, other: Numeric) -> ReactivePower: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: ReactivePower) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> ReactivePower: ...
    @overload
    def __truediv__(self, other: Numeric) -> ReactivePower: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)

    def to_power(self) -> Power:
        """View this reactive power as an ordinary `Power`, as a number of watts.

            Kilovar(2).to_power() == Kilowatt(2)

        The var and the watt are the same quantity of joules per second, and the
        value is carried over unchanged.
        """
        return Power(self._magnitude, Power._canonical_unit)  # noqa: SLF001 -- Power's own canonical unit


_register(POWER, ApparentPower, specialisation_of=Power)
_register(POWER, ReactivePower, specialisation_of=Power)

__all__ = ["ApparentPower", "ReactivePower"]
