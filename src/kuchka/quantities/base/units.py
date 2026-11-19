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
from itertools import pairwise
from types import MappingProxyType
from typing import TYPE_CHECKING
from typing import Any
from typing import Protocol

from kuchka.errors import InvalidMeasurementError
from kuchka.internal.typing import override
from kuchka.internal.unit_table import UnitTable
from kuchka.numeric import to_exact

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Iterable
    from collections.abc import Mapping
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.numeric import Numeric


_MINIMUM_LADDER = 2
"""A ladder with one unit has nothing to move along."""


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
        if not isinstance(other, type(self)) or type(other) is not type(self):
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


def _check_fits(quantity_type: type[Any], unit: object) -> None:
    """Raise `TypeError` unless `unit` is of the kind and dimension of the type."""
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


def bind_units(quantity_type: type[Any], units: Iterable[Any]) -> None:
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
        _check_fits(quantity_type, unit)
    quantity_type._applicable_units = bound  # noqa: SLF001


def bind_table(
    quantity_type: type[Any], table: Mapping[str, Callable[..., Any]]
) -> None:
    """Bind the table that reads the text of a unit into a `quantity_type`.

    This is called once per quantity type, with the table of that type's units.
    `parse` reads the type's table from here.

    Raises `TypeError` for a type that has its table bound already or for a table not
    built by `unit_table`, since either is a defect in `kuchka`'s own unit modules.
    """
    if "_unit_table" in vars(quantity_type):
        msg = f"{quantity_type.__name__} already has its table bound."
        raise TypeError(msg)
    if not isinstance(table, UnitTable):
        msg = f"{table!r} is not a table built by unit_table."
        raise TypeError(msg)
    quantity_type._unit_table = table  # noqa: SLF001


def extend_units(
    quantity_type: type[Any], units: Iterable[Any] | UnitTable[Any]
) -> None:
    """Add units to those a bound `quantity_type` displays in.

    A collection of units that lives outside `kuchka.units`, such as the archaic
    units, calls this when its module is imported, so a quantity type displays in
    those units exactly when the application has imported them.
    The units pass the same kind and dimension checks as bound ones.
    The added units are recorded apart from the bound ones (`_extension_units`), so
    the published set a type binds stays recoverable.
    A `UnitTable` stands for its units, and the type records the table too
    (`_extension_tables`), which is how `parse` reads the spellings of the units an
    application has imported.
    Extending with a unit the type already displays in changes nothing, which makes
    importing the same module twice harmless.

    Raises `TypeError` for a type that has no bound units yet, no unit, or a unit
    that does not fit.
    """
    if "_applicable_units" not in vars(quantity_type):
        msg = f"{quantity_type.__name__} has no bound units to extend."
        raise TypeError(msg)
    table = units if isinstance(units, UnitTable) else None
    added = frozenset(units.units if isinstance(units, UnitTable) else units)
    if not added:
        msg = f"{quantity_type.__name__} needs at least one unit to extend with."
        raise TypeError(msg)
    for unit in added:
        _check_fits(quantity_type, unit)
    already = quantity_type._applicable_units  # noqa: SLF001
    extension = getattr(quantity_type, "_extension_units", frozenset[object]())
    quantity_type._extension_units = extension | (added - already)  # noqa: SLF001
    quantity_type._applicable_units = already | added  # noqa: SLF001
    if table is not None:
        recorded = vars(quantity_type).get("_extension_tables", ())
        if not any(known is table for known in recorded):
            quantity_type._extension_tables = (*recorded, table)  # noqa: SLF001


def _check_ladder(
    quantity_type: type[Any], ladder: tuple[Any, ...], claimed: Mapping[object, object]
) -> None:
    """Raise `TypeError` unless `ladder` is a run of bound units that grow in size."""
    name = quantity_type.__name__
    if len(ladder) < _MINIMUM_LADDER:
        msg = f"a ladder of {name} needs at least two units, got {ladder!r}."
        raise TypeError(msg)
    for unit in ladder:
        if unit not in quantity_type._applicable_units:  # noqa: SLF001
            msg = f"{unit!r} is not a unit of {name}, so it cannot be on its ladder."
            raise TypeError(msg)
        if getattr(unit, "offset", 0) != 0:
            msg = (
                f"{unit!r} starts its scale away from zero, so the size of a reading "
                f"in it is no size of the {name}: it cannot be on a ladder."
            )
            raise TypeError(msg)
        if unit in claimed:
            msg = f"{unit!r} is on more than one ladder of {name}."
            raise TypeError(msg)
    for smaller, larger in pairwise(ladder):
        if smaller.scale >= larger.scale:
            msg = (
                f"a ladder of {name} grows from each unit to the next, but "
                f"{smaller!r} is followed by {larger!r}."
            )
            raise TypeError(msg)


def bind_ladders(quantity_type: type[Any], ladders: Iterable[Iterable[Any]]) -> None:
    """Bind the ladders `auto_scale` moves along for `quantity_type`.

    This is called once per quantity type, after `bind_units`.

    A ladder is a run of units of one family, such as the nanoampere to the megaampere,
    given smallest first.
    It has at least two units, each a bound unit of the type, and every unit is larger
    than the one before.
    A unit stands on one ladder of a type, and a quantity displayed in it moves along
    that ladder.
    A ladder holds only units that start at zero, since the size of a reading on a
    scale with an offset, such as the degree Celsius, says nothing about the size of
    the quantity.
    Only a type whose magnitude is a size can have ladders, which leaves out the
    modular and logarithmic shapes.

    Raises `TypeError` for a type that has its ladders bound already, a type without
    bound units or without a size, and a ladder that breaks the rules above, since each
    is a defect in `kuchka`'s own unit modules.
    """
    name = quantity_type.__name__
    if "_ladders" in vars(quantity_type):
        msg = f"{name} already has its ladders bound."
        raise TypeError(msg)
    if "_applicable_units" not in vars(quantity_type):
        msg = f"{name} has no bound units to build ladders from."
        raise TypeError(msg)
    if not quantity_type._scales_by_size:  # noqa: SLF001
        msg = f"{name} has no ladders: the size of its magnitude does not pick a unit."
        raise TypeError(msg)
    runs = tuple(tuple(ladder) for ladder in ladders)
    if not runs:
        msg = f"{name} needs at least one ladder."
        raise TypeError(msg)
    claimed: dict[object, tuple[Any, ...]] = {}
    for run in runs:
        _check_ladder(quantity_type, run, claimed)
        claimed.update(dict.fromkeys(run, run))
    quantity_type._ladders = runs  # noqa: SLF001
    quantity_type._ladder_of = MappingProxyType(claimed)  # noqa: SLF001


def bind_clock_units(quantity_type: type[Any], units: Iterable[Any]) -> None:
    """Bind the units `clock_parts` splits a measurement of `quantity_type` into.

    This is called once per quantity type, after `bind_units`.

    The units are given largest first, such as the day, the hour, and the minute down
    to the femtosecond.
    There are at least two, each a bound unit of the type that starts at zero, and
    every unit is smaller than the one before.

    Raises `TypeError` for a type that has its clock units bound already, a type
    without bound units, and units that break the rules above, since each is a defect
    in `kuchka`'s own unit modules.
    """
    name = quantity_type.__name__
    if "_clock_units" in vars(quantity_type):
        msg = f"{name} already has its clock units bound."
        raise TypeError(msg)
    if "_applicable_units" not in vars(quantity_type):
        msg = f"{name} has no bound units to split into."
        raise TypeError(msg)
    run = tuple(units)
    if len(run) < _MINIMUM_LADDER:
        msg = f"the clock units of {name} need at least two units, got {run!r}."
        raise TypeError(msg)
    for unit in run:
        if unit not in quantity_type._applicable_units:  # noqa: SLF001
            msg = f"{unit!r} is not a unit of {name}, so it cannot split one."
            raise TypeError(msg)
        if getattr(unit, "offset", 0) != 0:
            msg = f"{unit!r} starts its scale away from zero: it cannot split a {name}."
            raise TypeError(msg)
    for larger, smaller in pairwise(run):
        if larger.scale <= smaller.scale:
            msg = (
                f"the clock units of {name} shrink from each unit to the next, but "
                f"{larger!r} is followed by {smaller!r}."
            )
            raise TypeError(msg)
    quantity_type._clock_units = run  # noqa: SLF001


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
