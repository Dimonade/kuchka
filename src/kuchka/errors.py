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


class IncompatibleDimensionError(MeasurementError):
    """An operation was attempted between two incompatible dimensions."""

    def __init__(self, operation: str, left: object, right: object) -> None:
        """Build the error message from the operands' runtime types and dimensions."""
        left_name = type(left).__name__
        right_name = type(right).__name__
        left_dim = getattr(left, "dimension", None)
        right_dim = getattr(right, "dimension", None)
        message = (
            f"Cannot {operation} {left_name} and {right_name}.\n"
            f"{left_name} has dimension [{left_dim!r}].\n"
            f"{right_name} has dimension [{right_dim!r}]."
        )
        super().__init__(message)
        self.operation = operation
        self.left = left
        self.right = right


class InvalidConversionError(MeasurementError):
    """``.to(...)`` was given something that is not a valid conversion target."""


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


__all__ = [
    "IncompatibleDimensionError",
    "InvalidConversionError",
    "InvalidMeasurementError",
    "MeasurementError",
    "PlannedDimensionError",
    "UnrepresentableDimensionError",
]
