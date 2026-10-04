"""Unit-definition types: the data behind every unit constructor.

`UnitDef`, `AffineUnitDef`, and `LogarithmicUnitDef` are internal machinery.
Application code never constructs any of them directly -- see each class's own
docstring.

`_DisplayUnit` is the structural shape a `_ScalarStorage` display unit must have
(`kuchka.quantities.base.storage`).
It lives here, next to the concrete types that satisfy it, so this module has no
dependency on anything else in the `base` package.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Protocol

from kuchka.errors import InvalidMeasurementError
from kuchka.internal.typing import override
from kuchka.numeric import to_exact

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric


def _checked_spellings(
    kind: str, name: str, spellings: tuple[str, ...]
) -> tuple[str, ...]:
    """Return `spellings` unchanged, which must be a tuple of non-empty strings."""
    if not isinstance(spellings, tuple) or not all(
        isinstance(spelling, str) and spelling.strip() for spelling in spellings
    ):
        msg = f"{kind} {name!r} needs a tuple of non-empty strings, got {spellings!r}."
        raise InvalidMeasurementError(msg)
    return spellings


def _positive_scale(kind: str, name: str, scale: Numeric) -> Fraction:
    """Return `scale` as an exact `Fraction`, which must be positive.

    A unit's scale divides every value read back in that unit, so zero would make
    each reading a division by zero.
    """
    exact = to_exact(scale)
    if exact <= 0:
        msg = f"{kind} {name!r} needs a positive scale, got {scale!r}."
        raise InvalidMeasurementError(msg)
    return exact


class UnitDef:
    """A named, purely multiplicative unit.

    Builds constructors like `Volt`.
    `scale` is normalized to an exact `Fraction` at construction, regardless of which
    `Numeric` type it is given.
    `symbol` is the display notation.
    `aliases` are further symbols the unit is known by, and `words` further names; see
    `kuchka.internal.unit_table` for how each is matched.
    Application code never constructs one directly, it imports the constructor
    functions instead.
    """

    __slots__ = ("aliases", "dimension", "name", "scale", "symbol", "words")

    def __init__(  # noqa: PLR0913 -- the two spelling lists are keyword-only extras
        self,
        name: str,
        symbol: str,
        scale: Numeric,
        dimension: Dimension,
        *,
        aliases: tuple[str, ...] = (),
        words: tuple[str, ...] = (),
    ) -> None:
        """Store name, symbol, scale, dimension, and the other accepted spellings."""
        self.name = name
        self.symbol = symbol
        self.scale: Fraction = _positive_scale("unit", name, scale)
        self.dimension = dimension
        self.aliases = _checked_spellings("unit", name, aliases)
        self.words = _checked_spellings("unit", name, words)

    @override
    def __repr__(self) -> str:
        return f"UnitDef({self.name!r}, {self.symbol!r})"


class AffineUnitDef:
    """A unit with a scale and an offset, e.g. Celsius relative to Kelvin.

    The affine counterpart to `UnitDef`.
    `scale` and `offset` are normalized to exact `Fraction`s at construction.
    Application code never constructs one directly.
    It imports the unit constants (`KELVIN`, `CELSIUS`, ...) from `kuchka.units`.
    """

    __slots__ = ("aliases", "name", "offset", "scale", "symbol", "words")

    def __init__(  # noqa: PLR0913 -- the two spelling lists are keyword-only extras
        self,
        name: str,
        symbol: str,
        scale: Numeric,
        offset: Numeric,
        *,
        aliases: tuple[str, ...] = (),
        words: tuple[str, ...] = (),
    ) -> None:
        """Store name, symbol, scale/offset (as ``Fraction``), and other spellings."""
        self.name = name
        self.symbol = symbol
        self.scale: Fraction = _positive_scale("unit", name, scale)
        self.offset: Fraction = to_exact(offset)
        self.aliases = _checked_spellings("unit", name, aliases)
        self.words = _checked_spellings("unit", name, words)

    @override
    def __repr__(self) -> str:
        return f"AffineUnitDef({self.name!r}, {self.symbol!r})"


class LogarithmicUnitDef:
    """A named unit of logarithmic level, e.g. the decibel or the bel.

    The logarithmic counterpart to `UnitDef`.
    `scale` is the size of one of these units in decibels (10 for the bel), normalized
    to an exact `Fraction` at construction.
    Being its own type makes a logarithmic unit the only thing
    `PureLogarithmicQuantity.to()` accepts.
    Application code never constructs one directly.
    It imports the unit constants (`DECIBEL`, `BEL`) from `kuchka.units`.
    """

    __slots__ = ("aliases", "name", "scale", "symbol", "words")

    def __init__(
        self,
        name: str,
        symbol: str,
        scale: Numeric,
        *,
        aliases: tuple[str, ...] = (),
        words: tuple[str, ...] = (),
    ) -> None:
        """Store name, symbol, scale (as ``Fraction``), and other spellings."""
        self.name = name
        self.symbol = symbol
        self.scale: Fraction = _positive_scale("unit", name, scale)
        self.aliases = _checked_spellings("unit", name, aliases)
        self.words = _checked_spellings("unit", name, words)

    @override
    def __repr__(self) -> str:
        return f"LogarithmicUnitDef({self.name!r}, {self.symbol!r})"


class _DisplayUnit(Protocol):  # noqa: PYI046 -- bound for the scalar-storage generic parameter, not used within this file.
    """Structural shape a scalar-storage display unit must have.

    A name, a display symbol, and the other spellings the unit is known by.
    `UnitDef`, `AffineUnitDef`, and `LogarithmicUnitDef` satisfy this without declaring
    it explicitly.
    """

    name: str
    symbol: str
    aliases: tuple[str, ...]
    words: tuple[str, ...]


__all__ = ["AffineUnitDef", "LogarithmicUnitDef", "UnitDef"]
