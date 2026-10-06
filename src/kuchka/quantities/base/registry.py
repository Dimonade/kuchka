"""The dimension registry: what arithmetic hands back for a given exponent vector.

NOTE: Kept separate from `linear.py` even though `_promote` only ever constructs
`LinearQuantity` subclasses, because the dependency runs the other way at import
time: `LinearQuantity.__mul__`/`__truediv__` call `_promote`, so this module cannot
import `linear.py` at runtime without creating a cycle.
The `LinearQuantity` import below is therefore `TYPE_CHECKING`-only -- needed for
accurate annotations, not needed to actually run `register()` or `_promote()`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import DIMENSIONLESS
from kuchka.errors import PlannedDimensionError
from kuchka.errors import UnrepresentableDimensionError

if TYPE_CHECKING:
    from fractions import Fraction

    from kuchka.dimensions import Dimension
    from kuchka.quantities.base.linear import LinearQuantity

_DIMENSION_REGISTRY: dict[Dimension, type[LinearQuantity]] = {}
"""Maps a dimension signature back to the named type that represents it, so that e.g.
``Volt(5) * Ampere(2)`` produces a real ``Power`` instance.

Each quantity module populates this via ``_register`` as a side effect of being
imported, so this module needs no list of the types in advance.
The registry is closed when the package finishes importing (see ``_close``): the named
dimensions are part of the library, and arithmetic hands back the library's own types.

NOTE: LOAD-BEARING RULE: at most one type may ever be registered per dimension, and it
must always be the general SI/physics name for that dimension
(``Voltage`` for M L^2 T^-3 I^-1, ``Frequency`` for T^-1, and so on), never a
domain-specific vocabulary type.

This matters once more than one type can share a dimension:
``SampleRate`` and ``BaudRate`` are both T^-1, the same as ``Frequency``, but neither
of them registers.
They stay reachable only by explicit construction, exactly like ``Temperature`` --
``_register`` enforces this by refusing a second type for a dimension that already has
one, rather than silently overwriting it.
"""

_PLANNED_DIMENSIONS: dict[Dimension, str] = {}
"""Maps a dimension signature to the name of a quantity this library intends to
implement but does not yet.

Lets `_promote` raise `PlannedDimensionError` for a dimension this library already has
a name for, naming the result instead of only printing its exponent vector.

Curated by hand, the same way the `@overload` tables are: adding an entry here improves
the error message, and is a marker for what to implement next.

Emptied out as each named dimension gets a real registered type.
"""


_closed = False


def _register(dimension: Dimension, quantity_type: type[LinearQuantity]) -> None:
    """Associate a dimension signature with the type that represents it.

    Called once per quantity type, at import time, by the module that defines that type.

    Raises `TypeError` if another type already claimed this dimension, and
    `RuntimeError` once the registry is closed.
    Both are defects in kuchka's own quantity modules, not something a caller of the
    public API can trigger, so neither is part of the `MeasurementError` hierarchy that
    application code handles.
    """
    if _closed:
        msg = (
            f"cannot register {quantity_type.__name__}: the dimension registry is "
            "closed once `kuchka` has finished importing."
        )
        raise RuntimeError(msg)
    existing = _DIMENSION_REGISTRY.get(dimension)
    if existing is not None and existing is not quantity_type:
        msg = (
            f"dimension {dimension!r} is already registered to "
            f"{existing.__name__}; only one type per dimension may be the "
            f"canonical, arithmetic-derived type for it (see the note "
            f"above `_DIMENSION_REGISTRY`). {quantity_type.__name__} "
            f"should stay unregistered and reachable only by explicit "
            f"construction, the way `SampleRate` and `Temperature` are."
        )
        raise TypeError(msg)
    _DIMENSION_REGISTRY[dimension] = quantity_type


def _close() -> None:
    """Close the registry: later registrations raise `RuntimeError`.

    Called once, when the package has imported every quantity module.
    """
    global _closed  # noqa: PLW0603 -- one-way switch, set once at the end of the import
    _closed = True


def _promote(dimension: Dimension, magnitude: Fraction) -> LinearQuantity | Fraction:
    """Build the correctly-typed result of a multiplication or division.

    A dimensionless result (e.g. Resistance / Resistance) is returned as a plain
    ``Fraction`` ratio, matching ordinary physics convention.
    """
    if dimension == DIMENSIONLESS:
        return magnitude
    try:
        quantity_type = _DIMENSION_REGISTRY[dimension]
    except KeyError:
        planned_name = _PLANNED_DIMENSIONS.get(dimension)
        if planned_name is not None:
            raise PlannedDimensionError(dimension, planned_name) from None
        raise UnrepresentableDimensionError(dimension) from None
    return quantity_type(magnitude, quantity_type._canonical_unit)  # noqa: SLF001 -- accessing the registered type's own canonical unit, not a foreign instance's internals


__all__: list[str] = []
