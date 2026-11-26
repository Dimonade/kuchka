"""Immutable storage, pickling, and text rendering shared by every scalar quantity.

Does not implement any operator at all.
Algebraic shape (linear, affine, modular, ...) decides equality and ordering;
added by the mixins and concrete bases built on top of this one, in sibling modules
of this package.
"""

from __future__ import annotations

import importlib
import pickle
from fractions import Fraction
from types import MappingProxyType
from typing import TYPE_CHECKING
from typing import Any
from typing import ClassVar
from typing import Generic
from typing import NoReturn
from typing import Self
from typing import TypeVar

from kuchka.dimensions import Dimension
from kuchka.errors import IncompatibleDimensionError
from kuchka.errors import InvalidConversionError
from kuchka.errors import InvalidMeasurementError
from kuchka.internal.display import render
from kuchka.internal.typing import override
from kuchka.quantities.base.units import _DisplayUnit

_UnitT = TypeVar("_UnitT", bound=_DisplayUnit)

_STATE_LENGTH = 2
"""A pickled state is a (magnitude, display unit) pair."""

if TYPE_CHECKING:
    from collections.abc import Iterator
    from collections.abc import Mapping

    from kuchka.internal.unit_table import UnitTable


def _concrete_types(base: type | None = None) -> Iterator[type]:
    """Yield every concrete quantity type: one that names its own `dimension`."""
    parent: type = base or _ScalarStorage
    subclass: type
    for subclass in parent.__subclasses__():
        if "dimension" in vars(subclass):
            yield subclass
        yield from _concrete_types(subclass)


def _owners_of(unit: object) -> str:
    """Name the quantity types `unit` belongs to, as a sentence; empty if none."""
    owners = sorted(
        candidate.__name__
        for candidate in _concrete_types()
        if unit in getattr(candidate, "_applicable_units", ())
    )
    return f" It is a unit of {', '.join(owners)}." if owners else ""


class _ScalarStorage(Generic[_UnitT]):
    """State every scalar quantity needs, independent of algebraic shape.

    A `Fraction` magnitude in this quantity's own canonical frame (volts for Voltage,
    kelvin for Temperature, ...), plus the unit it currently displays as.
    `Fraction`, not `Decimal`: an exact rational input (`Litre(Fraction(5, 18))`) stays
    exact through storage; approximation happens only at `repr()`/`__format__`, via
    `kuchka.internal.display.render`.

    The class itself is part of the public surface (`Voltage`, ...), so its
    constructor is a validation boundary just like the unit constructors are:
    it accepts only an exact `Fraction` and a display unit of the right kind and
    dimension, and rejects everything else instead of storing it.
    Plain numbers in a particular unit are what the unit constructors (`Volt`,
    `Celsius`, ...) are for.
    """

    _magnitude: Fraction
    _display_unit: _UnitT
    dimension: ClassVar[Dimension]
    _canonical_unit: ClassVar[Any]
    """The unit the magnitude is stored in; each algebraic shape narrows its type."""
    _unit_type: ClassVar[type]
    """The kind of unit definition this algebraic shape displays in.

    Assigned by each algebraic base (`LinearQuantity`, `AffineQuantity`, ...).
    """
    __slots__ = ("_display_unit", "_magnitude")

    _applicable_units: ClassVar[frozenset[object]]
    """The units this quantity type displays in, bound by `bind_units`.

    `extend_units` adds the units of an imported collection, such as the archaic ones.
    """

    _scales_by_size: ClassVar[bool] = False
    """Whether the size of the magnitude says which unit reads best.

    A shape sets it where the zero of a unit is the absence of the quantity, so that a
    larger magnitude is a larger quantity; modular and logarithmic shapes do not.
    """

    _ladders: ClassVar[tuple[tuple[Any, ...], ...]] = ()
    """The runs of units `auto_scale` moves along, bound by `bind_ladders`."""

    _ladder_of: ClassVar[Mapping[object, tuple[Any, ...]]] = MappingProxyType({})
    """The ladder each of the units on a ladder stands on."""

    _extension_units: ClassVar[frozenset[object]]
    """The units `extend_units` added to those `bind_units` bound; absent until then."""

    _unit_table: ClassVar[UnitTable[Any]]
    """The table that reads the text of a unit into a value of this type.

    Bound by `bind_table`, and read by `parse`.
    """

    _extension_tables: ClassVar[tuple[UnitTable[Any], ...]]
    """The tables `extend_units` was given, in the order added; absent until then."""

    def __init_subclass__(cls, **kwargs: object) -> None:
        """Check that a concrete quantity type is set up completely.

        A type that names its own `dimension` is a concrete quantity, and has to be a
        value object with no `__dict__`: it declares `__slots__` and a `Dimension`.
        The shape bases (`LinearQuantity`, ...) only annotate `dimension`, so they
        pass without declaring one.
        The canonical unit is bound later, by the unit module that defines the unit,
        so completeness of that binding is a property of the assembled package.
        """
        super().__init_subclass__(**kwargs)
        if "dimension" not in vars(cls):
            return
        if not isinstance(vars(cls)["dimension"], Dimension):
            msg = f"{cls.__name__}.dimension must be a Dimension."
            raise TypeError(msg)
        if "__slots__" not in vars(cls):
            msg = (
                f"{cls.__name__} must declare `__slots__ = ()`: a quantity is an "
                "immutable value with no per-instance `__dict__`."
            )
            raise TypeError(msg)

    def __init__(self, magnitude: Fraction, display_unit: _UnitT) -> None:
        """Store `magnitude` (canonical unit) and `display_unit`, validating both."""
        self._store(magnitude, display_unit)

    @classmethod
    def _validate(cls, magnitude: object, display_unit: object) -> None:
        """Raise `InvalidMeasurementError` unless the pair is a valid state.

        Construction, unpickling, and copying all pass through this check.
        A concrete type with a domain restriction of its own extends it.
        """
        if not isinstance(magnitude, Fraction):
            msg = (
                f"{cls.__name__} takes an exact `Fraction` magnitude in its "
                f"canonical unit, got {type(magnitude).__name__} ({magnitude!r}). "
                "To build a measurement from a plain number, use one of the unit "
                "constructors in `kuchka.units` instead."
            )
            raise InvalidMeasurementError(msg)
        if not isinstance(display_unit, cls._unit_type):
            msg = (
                f"{cls.__name__} needs a {cls._unit_type.__name__} as its display "
                f"unit, got {display_unit!r}."
            )
            raise InvalidMeasurementError(msg)
        # NOTE: Affine and logarithmic unit definitions carry no dimension of
        # their own; their `_unit_type` check above is the whole contract.
        unit_dimension = getattr(display_unit, "dimension", None)
        if (
            unit_dimension is not None
            and unit_dimension is not cls.dimension
            and unit_dimension != cls.dimension
        ):
            name = getattr(display_unit, "name", "?")
            symbol = getattr(display_unit, "symbol", "?")
            msg = (
                f"cannot construct a {cls.__name__} displayed in "
                f"{name} ({symbol}): "
                f"incompatible dimensions - "
                f"[{cls.dimension!r}] and [{unit_dimension!r}]."
            )
            raise InvalidMeasurementError(msg)
        # The units are bound once the unit modules have loaded.
        # Until then (only while the package imports) the kind and dimension checks
        # above apply.
        applicable = getattr(cls, "_applicable_units", None)
        if applicable is not None and display_unit not in applicable:
            msg = (
                f"{getattr(display_unit, 'name', '?')} "
                f"({getattr(display_unit, 'symbol', '?')}) is not a unit of "
                f"{cls.__name__}.{_owners_of(display_unit)}"
            )
            raise InvalidMeasurementError(msg)

    def _store(self, magnitude: Fraction, display_unit: _UnitT) -> None:
        """Validate and set the state of a value that has none yet.

        The only place state is written: a value is born with its state and keeps it.
        """
        if hasattr(self, "_magnitude"):
            raise AttributeError(f"{type(self).__name__} is immutable")
        self._validate(magnitude, display_unit)
        object.__setattr__(self, "_magnitude", magnitude)
        object.__setattr__(self, "_display_unit", display_unit)

    @override
    def __setattr__(self, name: str, value: object) -> None:
        raise AttributeError(f"{type(self).__name__} is immutable")

    @override
    def __delattr__(self, name: str) -> None:
        raise AttributeError(f"{type(self).__name__} is immutable")

    def _reject_foreign_unit(self, unit: object) -> None:
        """Raise `InvalidConversionError` unless `unit` is a unit of this type."""
        applicable = getattr(type(self), "_applicable_units", None)
        if applicable is not None and unit not in applicable:
            msg = (
                f"cannot convert {self.unit.name} ({self.unit.symbol}) to "
                f"{getattr(unit, 'name', '?')} ({getattr(unit, 'symbol', '?')}): "
                f"it is not a unit of {type(self).__name__}.{_owners_of(unit)}"
            )
            raise InvalidConversionError(msg)

    def _tolerance_limit(
        self, other: object, tolerance: object, tolerance_type: type
    ) -> Fraction:
        """Validate the operands of `is_close` and return the tolerance's magnitude.

        `other` must be the same type as `self`, and `tolerance` an instance of
        `tolerance_type` that is not negative.
        A plain number is no tolerance: it has no unit to say what is being allowed.
        """
        if type(other) is not type(self):
            raise IncompatibleDimensionError("compare", self, other)
        if type(tolerance) is not tolerance_type or not isinstance(
            tolerance, _ScalarStorage
        ):
            msg = (
                f"the tolerance for comparing {type(self).__name__} values must be a "
                f"{tolerance_type.__name__}, got {tolerance!r}."
            )
            raise InvalidMeasurementError(msg)
        limit = tolerance._magnitude  # noqa: SLF001 -- same class family, same storage
        if limit < 0:
            msg = f"the tolerance must not be negative, got {tolerance!r}."
            raise InvalidMeasurementError(msg)
        return limit

    @property
    def unit(self) -> _UnitT:
        """Unit this measurement currently displays as."""
        return self._display_unit

    @override
    def __getstate__(self) -> tuple[Fraction, _UnitT]:
        """Pickle/copy state: magnitude and display unit.

        `__setattr__` blocks the default slot-restoring path `pickle`/`copy` use for
        `__slots__`-only classes, since that path calls plain `setattr()`.
        `object.__setattr__`, the same way `__init__` does it, restores state without
        going through the guard.
        """
        return (self._magnitude, self._display_unit)

    @override
    def __reduce__(self) -> tuple[object, ...]:
        """Pickle by the name `kuchka.quantities` publishes this class under.

        A published class is named rather than located, so a pickle does not depend on
        the module that defines the class and still loads when the class moves.
        A class that is not published is pickled by reference, as `object` does.
        """
        name = _published_name(type(self))
        if name is None:
            return (_new_instance, (type(self),), self.__getstate__())
        return (_new_published, (name,), self.__getstate__())

    def __setstate__(self, state: tuple[Fraction, _UnitT]) -> None:
        """Restore a pickled/copied instance, validating it like construction."""
        if not isinstance(state, tuple) or len(state) != _STATE_LENGTH:
            msg = (
                f"cannot restore a {type(self).__name__} from {state!r}: "
                "expected a (magnitude, display unit) pair."
            )
            raise InvalidMeasurementError(msg)
        magnitude, display_unit = state
        self._store(magnitude, display_unit)

    def value_in(self, unit: _UnitT) -> Fraction:
        """Exact magnitude expressed in `unit`, which has to be a unit of this type.

        Overridden per algebraic base: a pure scale (`LinearQuantity`) vs. a
        scale-plus-offset (`AffineQuantity`), each of which refuses a unit that is no
        unit of its quantity.
        """
        raise NotImplementedError

    def _magnitude_in(self, unit: _UnitT) -> Fraction:
        """Exact magnitude expressed in `unit`, which the caller knows is a unit of it.

        `value_in` without the check, for the code that passes the display unit of the
        measurement itself or a unit taken from its own ladder.
        """
        raise NotImplementedError

    def auto_scale(self) -> Self:
        """Return an equal measurement in the unit of its ladder that suits its size.

        A ladder is the run of decimal-prefixed units of a quantity, such as the
        picoampere to the megaampere, and a measurement moves along the ladder of the
        unit it displays in.
        It is shown in the largest unit of the ladder in which its size is at least 1,
        or in the smallest unit when it is under 1 in all of them.
        The sign is left out of the size, and zero keeps the unit it has.
        The value is the same exact value, so `q.auto_scale() == q`.

        Returns
        -------
        Self
            This measurement when the display unit is already the one chosen, when it
            is zero, when its unit is on no ladder, or when its type has none, and
            otherwise the same value in the chosen unit.

        Notes
        -----
        A unit on no ladder keeps its display unit: `Inch(100_000).auto_scale()` still
        shows inches, and `Celsius(0.5)` still shows degrees Celsius, since the size of
        a reading on a scale with an offset is no size of the quantity.
        A unit stands on one ladder, so a kibibyte moves along the binary ladder and a
        kilobyte along the decimal one.

        The unit is chosen from the exact value, and the digits are rounded when the
        value is shown, so a value just under a step can round up to the step of the
        unit below it, as the last example shows.

        Examples
        --------
        A small current is shown in the unit that reads best:

        >>> from kuchka import Ampere
        >>> Ampere(0.000045).auto_scale()
        45 µA

        The value is unchanged, and only the display unit differs:

        >>> Ampere(0.000045).auto_scale() == Ampere(0.000045)
        True

        A large frequency, and a negative voltage, move the same way:

        >>> from kuchka import Hertz
        >>> from kuchka import Volt
        >>> Hertz(2_400_000_000).auto_scale()
        2.4 GHz
        >>> Volt(-0.025).auto_scale()
        -25 mV

        A value at a step moves up to it, and zero keeps its unit:

        >>> from kuchka import Milliampere
        >>> Milliampere(1000).auto_scale()
        1 A
        >>> Milliampere(0).auto_scale()
        0 mA

        The unit is picked before the digits are rounded, so 999.9999 µA shown to one
        decimal reads as 1000.0 µA:

        >>> f"{Milliampere(0.9999999).auto_scale():.1f}"
        '1000.0 µA'

        """
        ladder = self._ladder_of.get(self._display_unit)
        if ladder is None or self._magnitude == 0:
            return self
        chosen = next(
            (unit for unit in reversed(ladder) if abs(self._magnitude_in(unit)) >= 1),
            ladder[0],
        )
        if chosen == self._display_unit:
            return self
        return type(self)(self._magnitude, chosen)

    def __bool__(self) -> NoReturn:
        """Raise: a quantity has no truth value.

        Zero is a measurement and not an absence, so `if not voltage:` cannot tell a
        missing reading from `Volt(0)`.
        A zero depends on the shape: `Celsius(0)` is not `Kelvin(0)`, `Degree(360)` is
        `Degree(0)`, and `Decibel(0)` is a ratio of one.
        Test for a missing value with `is None`, and for zero with an equality.
        """
        msg = (
            f"the truth value of a {type(self).__name__} is ambiguous: compare it "
            "with `is None` for a missing value, or with a zero of its own type."
        )
        raise TypeError(msg)

    def _reject_naked_number(self, operation: str, other: object) -> None:
        """Raise `InvalidMeasurementError` for a plain number met in arithmetic.

        A plain `0` added to a quantity is what `sum()` starts from, so that case
        names the `start=` that `sum()` needs.
        """
        unit_name = self._canonical_unit.name.capitalize()
        msg = (
            f"cannot {operation} a plain number ({other!r}) to a "
            f"{type(self).__name__}; wrap it in a unit constructor first, "
            f"e.g. {unit_name}({other!r})"
        )
        if operation == "add" and type(other) is int and other == 0:
            msg += (
                f". If this came from `sum()`, which starts from 0, give it a start "
                f"of the same type: `sum(values, start={unit_name}(0))`"
            )
        raise InvalidMeasurementError(msg)

    def format_parts(self, spec: str = "") -> tuple[str, str]:
        """Return the formatted magnitude and the unit symbol, as two strings.

        For a table, a CSV column, or a protocol that renders the number and the unit
        apart, without splitting a formatted string on its space.
        `spec` is the format specification of `__format__`, and the two are one rule:
        `" ".join(voltage.format_parts(spec))` is `format(voltage, spec)`, so the
        magnitude is rounded once, from its exact value, a tie rounds away from zero,
        and an empty spec shows 28 significant digits for a value with no finite
        decimal form.

        Examples
        --------
        >>> from kuchka import Volt
        >>> Volt(1234.5).format_parts(".2f")
        ('1234.50', 'V')
        >>> Volt(1234.5).format_parts()
        ('1234.5', 'V')

        """
        unit = self._display_unit
        return render(self._magnitude_in(unit), spec or "f"), unit.symbol

    @override
    def __repr__(self) -> str:
        return " ".join(self.format_parts())

    @override
    def __format__(self, format_spec: str) -> str:
        """Format the magnitude in the display unit, e.g. `f"{Volt(4.2):.2f}"`.

        Empty `format_spec` (`f"{voltage}"`, `str(voltage)`) matches `repr()`.
        A non-empty spec is a `Decimal` format spec applied to the exact value, rounded
        once and independent of the active `Decimal` context; the unit symbol follows:
        `f"{Volt(4.2):.2f}"` reads `"4.20 V"`.
        `format_parts` returns the two parts apart.
        """
        return " ".join(self.format_parts(format_spec))


__all__ = ["_ScalarStorage"]


def _published_name(cls: type) -> str | None:
    """Return the name `kuchka.quantities` publishes `cls` under, or `None`."""
    package = importlib.import_module("kuchka.quantities")
    name = cls.__name__
    return name if name in package.__all__ and getattr(package, name) is cls else None


def _new_instance(cls: type[_ScalarStorage[Any]]) -> _ScalarStorage[Any]:
    """Return a blank instance of `cls`, to be restored from its pickled state."""
    return cls.__new__(cls)


def _new_published(name: str) -> _ScalarStorage[Any]:
    """Return a blank instance of the class `kuchka.quantities` publishes as `name`.

    Only names of published quantity types are accepted.
    """
    package = importlib.import_module("kuchka.quantities")
    cls = getattr(package, name, None) if name in package.__all__ else None
    if not (isinstance(cls, type) and issubclass(cls, _ScalarStorage)):
        msg = (
            f"cannot restore {name!r}: "
            "kuchka.quantities publishes no such quantity type."
        )
        raise pickle.UnpicklingError(msg)
    return cls.__new__(cls)
