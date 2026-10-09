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

import functools
import importlib
import pickle
from typing import TYPE_CHECKING
from typing import Any
from typing import Protocol

from kuchka.errors import InvalidMeasurementError
from kuchka.internal.typing import override
from kuchka.numeric import to_exact

if TYPE_CHECKING:
    from collections.abc import Iterable
    from collections.abc import Mapping
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


class _Unit:
    """Behaviour shared by the unit-definition types.

    A unit definition is an immutable value:
    two with the same fields are equal and hash alike, and its state is written once,
    by `__init__`.
    Copying returns the same object, and pickling stores only the name under which
    `kuchka.units` publishes an equal unit, so a restored unit is the published
    constant and a stored reference does not depend on the fields behind it.
    """

    __slots__ = ()

    def _fields(self) -> tuple[object, ...]:
        """Return every field that makes this unit what it is."""
        raise NotImplementedError

    def _store(self, **fields: object) -> None:
        """Write the fields of a unit that has none yet."""
        if hasattr(self, "name"):
            raise AttributeError(f"{type(self).__name__} is immutable")
        for name, value in fields.items():
            object.__setattr__(self, name, value)

    @override
    def __setattr__(self, name: str, value: object) -> None:
        raise AttributeError(f"{type(self).__name__} is immutable")

    @override
    def __delattr__(self, name: str) -> None:
        raise AttributeError(f"{type(self).__name__} is immutable")

    @override
    def __eq__(self, other: object) -> bool:
        if type(other) is not type(self):
            return NotImplemented
        return self._fields() == other._fields()

    @override
    def __hash__(self) -> int:
        return hash((type(self), self._fields()))

    def __copy__(self) -> _Unit:
        """Return this unit: a unit definition is its own copy."""
        return self

    def __deepcopy__(self, memo: dict[int, object]) -> _Unit:
        """Return this unit: a unit definition is its own deep copy."""
        return self

    @override
    def __reduce__(self) -> tuple[object, ...]:
        """Pickle by the name `kuchka.units` publishes an equal unit under."""
        name = _published()[1].get(self)
        if name is None:
            msg = (
                f"cannot pickle {self!r}: only the units published by kuchka.units "
                "can be pickled, by name."
            )
            raise pickle.PicklingError(msg)
        return (_published_unit, (name,))


@functools.cache
def _published() -> tuple[Mapping[str, _Unit], Mapping[_Unit, str]]:
    """Index the unit constants of `kuchka.units`: by name, and by value."""
    package = importlib.import_module("kuchka.units")
    by_name: dict[str, _Unit] = {}
    by_unit: dict[_Unit, str] = {}
    for name in package.__all__:
        value = getattr(package, name)
        if isinstance(value, _Unit):
            by_name[name] = value
            by_unit.setdefault(value, name)
    return by_name, by_unit


def bind_units(quantity_type: type[Any], units: Iterable[_Unit]) -> None:
    """Bind the units `quantity_type` displays in.

    This is called once per quantity type.

    Every unit must be of the kind the type displays (`_unit_type`) and, when it has a
    dimension, of the type's dimension.
    Several types may bind the same unit.
    For example, the `second` is a unit of both `Time` and `SamplingPeriod`.

    Raises `TypeError` for a type that is bound already or a unit that does not fit,
    since either is a defect in `kuchka`'s own unit modules.
    """
    if "_applicable_units" in vars(quantity_type):
        msg = f"{quantity_type.__name__} already has its units bound."
        raise TypeError(msg)
    bound = frozenset(units)
    if not bound:
        msg = f"{quantity_type.__name__} needs at least one unit."
        raise TypeError(msg)
    for unit in bound:
        if not isinstance(unit, quantity_type._unit_type):  # noqa: SLF001
            msg = (
                f"{unit!r} is not a {quantity_type._unit_type.__name__}, "  # noqa: SLF001
                f"the kind of unit {quantity_type.__name__} displays in."
            )
            raise TypeError(msg)
        dimension = getattr(unit, "dimension", None)
        if dimension is not None and dimension != quantity_type.dimension:
            msg = (
                f"{unit.name} ({unit.symbol}) has dimension [{dimension!r}] but "
                f"{quantity_type.__name__} has [{quantity_type.dimension!r}]."
            )
            raise TypeError(msg)
    quantity_type._applicable_units = bound  # noqa: SLF001


def _published_unit(name: str) -> _Unit:
    """Return the unit published as `name` by `kuchka.units`; unpickling calls this."""
    try:
        return _published()[0][name]
    except KeyError:
        msg = f"{name!r} is not a unit published by kuchka.units."
        raise pickle.UnpicklingError(msg) from None


class UnitDef(_Unit):
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
    aliases: tuple[str, ...]
    dimension: Dimension
    name: str
    scale: Fraction
    symbol: str
    words: tuple[str, ...]

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
        self._store(
            name=name,
            symbol=symbol,
            scale=_positive_scale("unit", name, scale),
            dimension=dimension,
            aliases=_checked_spellings("unit", name, aliases),
            words=_checked_spellings("unit", name, words),
        )

    @override
    def _fields(self) -> tuple[object, ...]:
        return (
            self.name,
            self.symbol,
            self.scale,
            self.dimension,
            self.aliases,
            self.words,
        )

    @override
    def __repr__(self) -> str:
        return f"UnitDef({self.name!r}, {self.symbol!r})"


class AffineUnitDef(_Unit):
    """A unit with a scale and an offset, e.g. Celsius relative to Kelvin.

    The affine counterpart to `UnitDef`.
    `scale` and `offset` are normalized to exact `Fraction`s at construction.
    Application code never constructs one directly.
    It imports the unit constants (`KELVIN`, `CELSIUS`, ...) from `kuchka.units`.
    """

    __slots__ = ("aliases", "name", "offset", "scale", "symbol", "words")
    aliases: tuple[str, ...]
    name: str
    offset: Fraction
    scale: Fraction
    symbol: str
    words: tuple[str, ...]

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
        self._store(
            name=name,
            symbol=symbol,
            scale=_positive_scale("unit", name, scale),
            offset=to_exact(offset),
            aliases=_checked_spellings("unit", name, aliases),
            words=_checked_spellings("unit", name, words),
        )

    @override
    def _fields(self) -> tuple[object, ...]:
        return (
            self.name,
            self.symbol,
            self.scale,
            self.offset,
            self.aliases,
            self.words,
        )

    @override
    def __repr__(self) -> str:
        return f"AffineUnitDef({self.name!r}, {self.symbol!r})"


class LogarithmicUnitDef(_Unit):
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
    aliases: tuple[str, ...]
    name: str
    scale: Fraction
    symbol: str
    words: tuple[str, ...]

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
        self._store(
            name=name,
            symbol=symbol,
            scale=_positive_scale("unit", name, scale),
            aliases=_checked_spellings("unit", name, aliases),
            words=_checked_spellings("unit", name, words),
        )

    @override
    def _fields(self) -> tuple[object, ...]:
        return (self.name, self.symbol, self.scale, self.aliases, self.words)

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
