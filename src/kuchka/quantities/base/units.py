"""Unit-definition types: the data behind every unit constructor.

`UnitDef` and `AffineUnitDef` are internal machinery, never constructed directly by
application code -- see each class's own docstring.

`_DisplayUnit` is the structural shape a `_ScalarStorage` display unit must have
(`kuchka.quantities.base.storage`); it lives here, next to the two concrete types
that satisfy it, rather than in `storage.py`, so this module has no dependency on
anything else in the `base` package.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import Protocol

if TYPE_CHECKING:
    from decimal import Decimal

    from kuchka.dimensions import Dimension


class UnitDef:
    """A named, purely multiplicative unit, e.g. the ``mV`` behind ``Millivolt``.

    This is internal machinery used by to build unit constructors like ``Volt`` and
    ``Millivolt``.

    Application code never constructs a ``UnitDef`` directly;
    it imports the constructor functions instead.
    """

    __slots__ = ("dimension", "name", "scale", "symbol")

    def __init__(
        self,
        name: str,
        symbol: str,
        scale: Decimal,
        dimension: Dimension,
    ) -> None:
        """Store the unit's display name, symbol, scale factor, and dimension."""
        self.name = name
        self.symbol = symbol
        self.scale = scale
        self.dimension = dimension

    def __repr__(self) -> str:
        return f"UnitDef({self.name!r}, {self.symbol!r})"


@dataclass(frozen=True, slots=True)
class AffineUnitDef:
    """A unit with both a scale and an offset, e.g. Celsius relative to Kelvin.

    The affine counterpart to `UnitDef`.
    Most physical quantities convert by a pure scale factor, but a quantity whose zero
    point is itself a convention, like absolute temperature, a point-in-time `Instant`
    needs an offset alongside the scale.

    Application code never constructs one directly;
    it imports the unit constants (`KELVIN`, `CELSIUS`, ...) from `kuchka.units`.
    """

    name: str
    symbol: str
    scale: Decimal
    offset: Decimal


class _DisplayUnit(Protocol):  # noqa: PYI046 -- used as the bound for storage.py's `_UnitT`, not within this file; kept here, not there, because it documents the shared shape `UnitDef`/`AffineUnitDef` satisfy, and both live in this module.
    """Structural shape a `_ScalarStorage` display unit must have: a name and a symbol.

    Both `UnitDef` and `AffineUnitDef` satisfy this without declaring it explicitly;
    it exists so `_ScalarStorage.__repr__`/`__format__` can read `.symbol` off a
    display unit whose exact type (`UnitDef` for `LinearQuantity`, `AffineUnitDef` for
    `AffineQuantity`) it does not otherwise know.

    Declared as read-only properties: `AffineUnitDef` is a frozen dataclass, so its
    `name`/`symbol` fields are read-only, and a Protocol with plain mutable attributes
    only matches types whose matching attributes are settable.
    """

    @property
    def name(self) -> str: ...
    @property
    def symbol(self) -> str: ...


__all__ = ["AffineUnitDef", "UnitDef"]
