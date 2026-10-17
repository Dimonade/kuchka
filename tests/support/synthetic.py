"""Quantity types made up for a test, and the registry state it runs against."""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.quantities.base import LinearQuantity
from kuchka.quantities.base import ModularQuantity
from kuchka.quantities.base import registry

if TYPE_CHECKING:
    from kuchka.dimensions import Dimension

REGISTRY_TABLES = (
    "_KINDS_BY_DIMENSION",
    "_DIMENSION_REGISTRY",
    "_CONTESTED",
    "_SPECIALISATIONS",
    "_RULES",
    "_RATIO_KIND",
    "_RECIPROCALS",
)
"""The registry tables a registration or a rule writes to."""


def linear_kind(name: str, dimension: Dimension) -> type[LinearQuantity]:
    """Return a new linear quantity type of `dimension`, named `name`."""
    return type(name, (LinearQuantity,), {"dimension": dimension, "__slots__": ()})


def modular_kind(name: str, dimension: Dimension) -> type[ModularQuantity]:
    """Return a new modular quantity type of `dimension`, named `name`."""
    return type(name, (ModularQuantity,), {"dimension": dimension, "__slots__": ()})


def registry_state() -> tuple[object, ...]:
    """Return a snapshot of every registry table, to compare before and after."""
    return tuple(dict(getattr(registry, name)) for name in REGISTRY_TABLES)
