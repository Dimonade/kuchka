"""Immutable storage, pickling, and text rendering shared by every scalar quantity.

Does not implement any operator at all.
Algebraic shape (linear, affine, modular, ...) decides equality and ordering;
added by the mixins and concrete bases built on top of this one, in sibling modules
of this package.
"""

from __future__ import annotations

from fractions import Fraction
from typing import TYPE_CHECKING
from typing import Any
from typing import ClassVar
from typing import Generic
from typing import NoReturn
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

    _extension_units: ClassVar[frozenset[object]]
    """The units `extend_units` added to those `bind_units` bound; absent until then."""

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
        """Exact magnitude expressed in `unit`.

        Overridden per algebraic base: a pure scale (`LinearQuantity`) vs. a
        scale-plus-offset (`AffineQuantity`).
        """
        raise NotImplementedError

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

    @override
    def __repr__(self) -> str:
        return (
            f"{render(self.value_in(self._display_unit))} {self._display_unit.symbol}"
        )

    @override
    def __format__(self, format_spec: str) -> str:
        """Format the magnitude in the display unit, e.g. `f"{Volt(4.2):.2f}"`.

        Empty `format_spec` (`f"{voltage}"`, `str(voltage)`) matches `repr()`.
        A non-empty spec is a `Decimal` format spec applied to the exact value, rounded
        once and independent of the active `Decimal` context; the unit symbol follows:
        `f"{Volt(4.2):.2f}"` reads `"4.20 V"`.
        """
        if not format_spec:
            return repr(self)
        text = render(self.value_in(self._display_unit), format_spec)
        return f"{text} {self._display_unit.symbol}"


__all__ = ["_ScalarStorage"]
