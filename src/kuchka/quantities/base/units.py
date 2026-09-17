"""Unit-definition types: the data behind every unit constructor.

`UnitDef` and `AffineUnitDef` are internal machinery.
Application code never constructs either directly -- see each class's own docstring.

`_DisplayUnit` is the structural shape a `_ScalarStorage` display unit must have
(`kuchka.quantities.base.storage`).
It lives here, next to the concrete types that satisfy it, so this module has no
dependency on anything else in the `base` package.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Protocol

from kuchka.numeric import to_exact

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric


class UnitDef:
    """A named, purely multiplicative unit.

    Builds constructors like `Volt`.
    `scale` is normalized to an exact `Fraction` at construction, regardless of which
    `Numeric` type it is given.
    Application code never constructs one directly, it imports the constructor
    functions instead.
    """

    __slots__ = ("dimension", "name", "scale", "symbol")

    def __init__(
        self,
        name: str,
        symbol: str,
        scale: Numeric,
        dimension: Dimension,
    ) -> None:
        """Store name, symbol, scale, and dimension."""
        self.name = name
        self.symbol = symbol
        self.scale: Fraction = to_exact(scale)
        self.dimension = dimension

    def __repr__(self) -> str:
        return f"UnitDef({self.name!r}, {self.symbol!r})"


class AffineUnitDef:
    """A unit with a scale and an offset, e.g. Celsius relative to Kelvin.

    The affine counterpart to `UnitDef`.
    `scale` and `offset` are normalized to exact `Fraction`s at construction.
    Application code never constructs one directly.
    It imports the unit constants (`KELVIN`, `CELSIUS`, ...) from `kuchka.units`.
    """

    __slots__ = ("name", "offset", "scale", "symbol")

    def __init__(
        self,
        name: str,
        symbol: str,
        scale: Numeric,
        offset: Numeric,
    ) -> None:
        """Store name, symbol, and scale/offset, both normalized to ``Fraction``."""
        self.name = name
        self.symbol = symbol
        self.scale: Fraction = to_exact(scale)
        self.offset: Fraction = to_exact(offset)

    def __repr__(self) -> str:
        return f"AffineUnitDef({self.name!r}, {self.symbol!r})"


class _DisplayUnit(Protocol):  # noqa: PYI046 -- bound for the scalar-storage generic parameter, not used within this file.
    """Structural shape a scalar-storage display unit must have: name and symbol.

    Both `UnitDef` and `AffineUnitDef` satisfy this without declaring it explicitly.
    """

    name: str
    symbol: str


__all__ = ["AffineUnitDef", "UnitDef"]
