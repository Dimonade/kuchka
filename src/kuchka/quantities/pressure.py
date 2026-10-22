"""Pressure and Stress: force per unit area, and the force per area inside a material.

Defined alongside two relationships:
- `Force / Area -> Pressure`, and its two inverses, `Pressure * Area -> Force` and
  `Force / Pressure -> Area`, whose other overload halves live on `Force` and
  `Area` themselves.
- `Pressure * Volume -> Energy`, the P-V work relationship, and its inverse
  `Energy / Pressure -> Volume`, whose other overload halves live on `Volume` and
  `Energy` themselves.

`Pressure` shares its dimension with `EnergyDensity`, so the two are contested and
`Force / Area` is declared to be a `Pressure` (see `EnergyDensity`).

`Stress` is a role of `Pressure`: the same dimension, read as the force per area a
material carries.
It is reached with `Pressure.to_stress()`, gives back a `Pressure` with
`Stress.to_pressure()`, and shares every unit of `Pressure`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import overload

from kuchka.dimensions import PRESSURE
from kuchka.internal.typing import override
from kuchka.quantities.area import Area
from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base.registry import _register
from kuchka.quantities.base.registry import _rule
from kuchka.quantities.kinematics import Force

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric
    from kuchka.quantities.energy import Energy
    from kuchka.quantities.energy_density import EnergyDensity
    from kuchka.quantities.proportion import Proportion
    from kuchka.quantities.volume import Volume


class Pressure(LinearQuantity):
    """Force per unit area: how concentrated a push or pull is over a surface."""

    dimension: ClassVar[Dimension] = PRESSURE
    __slots__ = ()

    @overload
    def __mul__(self, other: Area) -> Force: ...
    @overload
    def __mul__(self, other: Volume) -> Energy: ...
    @overload
    def __mul__(self, other: Proportion) -> Pressure: ...
    @overload
    def __mul__(self, other: Numeric) -> Pressure: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: Pressure) -> Proportion: ...
    @overload
    def __truediv__(self, other: EnergyDensity) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> Pressure: ...
    @overload
    def __truediv__(self, other: Numeric) -> Pressure: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)

    def to_stress(self) -> Stress:
        """View this pressure as a `Stress`, e.g. for the load a section carries.

            Megapascal(250).to_stress()

        `Stress` shares the units of `Pressure`, and the unit this value displays in
        carries over.
        """
        return Stress(self._magnitude, self._display_unit)


class Stress(LinearQuantity):
    """The force per unit area a material carries, e.g. a yield or a tensile strength.

        yield_strength = Megapascal(250).to_stress()
        load = yield_strength.to_pressure() * SquareMillimetre(100)   # -> Force

    Dimensionally identical to `Pressure`.
    `Force / Area` is a `Pressure`, and a `Stress` comes from `Pressure.to_stress()`.
    It adds and subtracts with another `Stress`, scales by a plain number or a
    `Proportion`, and divides by another `Stress` into a `Proportion`.
    `to_pressure()` takes it as a `Pressure` for any other arithmetic, such as the
    `Force` it carries over an `Area`.
    """

    dimension: ClassVar[Dimension] = PRESSURE
    __slots__ = ()

    @overload
    def __mul__(self, other: Proportion) -> Stress: ...
    @overload
    def __mul__(self, other: Numeric) -> Stress: ...
    @overload
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction: ...

    @override
    def __mul__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: Stress) -> Proportion: ...
    @overload
    def __truediv__(self, other: Proportion) -> Stress: ...
    @overload
    def __truediv__(self, other: Numeric) -> Stress: ...
    @overload
    def __truediv__(
        self, other: LinearQuantity | Numeric
    ) -> LinearQuantity | Fraction: ...

    @override
    def __truediv__(self, other: LinearQuantity | Numeric) -> LinearQuantity | Fraction:
        return super().__truediv__(other)

    def to_pressure(self) -> Pressure:
        """View this stress as an ordinary `Pressure`, e.g. to multiply it by an area.

            Megapascal(250).to_stress().to_pressure() == Megapascal(250)

        The unit it displays in carries over, and `Pressure.to_stress()` takes the
        value back.
        """
        return Pressure(self._magnitude, self._display_unit)


_register(PRESSURE, Pressure)
_register(PRESSURE, Stress, specialisation_of=Pressure)
_rule(Force, "/", Area, Pressure)

__all__ = ["Pressure", "Stress"]
