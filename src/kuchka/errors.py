"""The measurement system's exception hierarchy.

Every error a user is likely to hit -- a dimension mismatch, a naked float where a
measurement was expected, an unrecognised conversion target -- is a subclass of
:class:`MeasurementError`, so application code can catch the whole family with one
except clause if it wants to.
"""

from __future__ import annotations


class MeasurementError(Exception):
    """Base class for all measurement-system errors."""


class InvalidMeasurementError(MeasurementError):
    """A value could not be turned into, or combined with, a measurement.

    Raised at construction time, e.g. passing a string, or a measurement of the wrong
    dimension, into a unit constructor, and at arithmetic boundaries where a naked
    number was used where a measurement was expected.
    """


_HINTS: dict[tuple[type, type], str] = {}
"""Advice for a refused pair of types, keyed by the operand types in either order."""


def _register_hint(left: type, right: type, hint: str) -> None:
    """Attach `hint` to every `IncompatibleDimensionError` between two types."""
    _HINTS[left, right] = hint
    _HINTS[right, left] = hint


class IncompatibleDimensionError(MeasurementError):
    """An operation was attempted between two incompatible dimensions or types.

    Every raise site for this error tests for a *type* mismatch
    (`type(self) is not type(other)`), not a dimension mismatch directly, since two
    different types can share a dimension on purpose.

    The message below is built accordingly:
    - when the operands' dimensions actually differ, it names both.
    - when they coincide, names them as different concepts within identical dimension.
    """

    def __init__(
        self,
        operation: str,
        left: object,
        right: object,
        *,
        hint: str | None = None,
    ) -> None:
        """Build the error message from the operands' runtime types and dimensions.

        A `hint` is appended as a last line, for a refusal that has a better route.
        Without one, the advice registered for the operand types is used.
        """
        if hint is None:
            hint = _HINTS.get((type(left), type(right)))
        left_name = type(left).__name__
        right_name = type(right).__name__
        left_dim = getattr(left, "dimension", None)
        right_dim = getattr(right, "dimension", None)
        if left_dim == right_dim:
            message = (
                f"Cannot {operation} `{left_name}` and `{right_name}`.\n"
                f"Both share dimension [{left_dim!r}], but `kuchka` treats them as "
                f"distinct concepts, not interchangeable quantities.\n"
                f"Convert explicitly if you mean to treat one as the other."
            )
        else:
            message = (
                f"Cannot {operation} `{left_name}` and `{right_name}`.\n"
                f"`{left_name}` has dimension [{left_dim!r}].\n"
                f"`{right_name}` has dimension [{right_dim!r}]."
            )
        if hint is not None:
            message = f"{message}\n{hint}"
        super().__init__(message)
        self.operation = operation
        self.left = left
        self.right = right


class DivisionByZeroError(MeasurementError, ZeroDivisionError):
    """A measurement was divided by zero, or the reciprocal of zero was taken.

    Also a `ZeroDivisionError`, so code that catches either one handles it.
    `dividend` and `divisor` are the operands as given.
    """

    def __init__(self, dividend: object, divisor: object) -> None:
        """Build the message from both operands."""
        super().__init__(f"cannot divide {dividend} by {divisor}: the divisor is zero.")
        self.dividend = dividend
        self.divisor = divisor


class InvalidConversionError(MeasurementError):
    """``.to(...)`` was given something that is not a valid conversion target."""


class ParseError(InvalidMeasurementError, ValueError):
    """Text could not be read as a measurement of the quantity type asked for.

    Raised by `parse` for text without a number or without a unit, for a number
    written in a form `parse` does not read, and for a unit text that two units claim.
    Also a `ValueError`, so code that catches either one handles it.
    """


class UnknownUnitError(ParseError):
    """The unit in the text is no unit of the quantity type asked for.

    `unit` is the unit text as written and `quantity` the type `parse` was given.
    """

    def __init__(self, message: str, *, unit: str, quantity: type) -> None:
        """Keep the unit text and the quantity type beside the message."""
        super().__init__(message)
        self.unit = unit
        self.quantity = quantity


class UnrepresentableDimensionError(MeasurementError):
    """Arithmetic produced a dimension with no registered engineering type.

    This is a scope boundary: each released version of the library registers a
    specific, deliberately limited vocabulary of engineering quantities
    (see ``kuchka.quantities``).

    An operation that mathematically produces something outside that vocabulary,
    e.g. Resistance times Resistance, is rejected clearly here rather than silently
    returning an untyped number.
    """

    def __init__(self, dimension: object) -> None:
        """Build the error message from the unregistered dimension."""
        super().__init__(
            f"the result of this operation has dimension [{dimension!r}], "
            "which has no registered engineering type in this version of "
            "the library.",
        )
        self.dimension = dimension


class PlannedDimensionError(UnrepresentableDimensionError):
    """Arithmetic produced a dimension this library already has a name for.

    Raised instead of the more general `UnrepresentableDimensionError` so the message
    can say what the result actually is, on top of printing the exponent vector.
    A subclass of :class:`UnrepresentableDimensionError`, so code that catches the
    general error still catches this one too.
    """

    def __init__(self, dimension: object, planned_name: str) -> None:
        """Build the error message from the dimension and its planned quantity name."""
        MeasurementError.__init__(
            self,
            f"the result of this operation has dimension [{dimension!r}], "
            f"which corresponds to {planned_name} -- planned but not yet "
            "implemented in this version of the library.",
        )
        self.dimension = dimension
        self.planned_name = planned_name


class AmbiguousKindError(UnrepresentableDimensionError):
    """Arithmetic produced a dimension that several kinds share on equal footing.

    No one of them is the general name for the dimension, so the library does not pick
    one for the caller.
    `candidates` holds the kinds the result could be.
    A subclass of :class:`UnrepresentableDimensionError`, so code that catches the
    general error still catches this one too.
    """

    def __init__(self, dimension: object, candidates: tuple[type, ...]) -> None:
        """Build the error message from the dimension and the kinds sharing it."""
        names = ", ".join(kind.__name__ for kind in candidates)
        MeasurementError.__init__(
            self,
            f"the result of this operation has dimension [{dimension!r}], "
            f"which several kinds share equally: {names}; construct the one you "
            f"mean explicitly, such as {candidates[0].__name__}(...).",
        )
        self.dimension = dimension
        self.candidates = candidates


__all__ = [
    "AmbiguousKindError",
    "DivisionByZeroError",
    "IncompatibleDimensionError",
    "InvalidConversionError",
    "InvalidMeasurementError",
    "MeasurementError",
    "ParseError",
    "PlannedDimensionError",
    "UnknownUnitError",
    "UnrepresentableDimensionError",
]
