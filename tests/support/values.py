"""Magnitudes the contract tests probe with."""

from __future__ import annotations

import pickle
from decimal import Decimal

EXTREME_MAGNITUDES: tuple[Decimal, ...] = (
    Decimal("1E-100"),
    Decimal("1E-50"),
    Decimal("1E-20"),
    Decimal("1E-9"),
    Decimal("-1E-9"),
    Decimal(0),
    Decimal(1),
    Decimal(-1),
    Decimal("1E9"),
    Decimal("1E20"),
    Decimal("1E50"),
    Decimal("1E100"),
)
"""Round numbers from far below any prefix to far above it, in both signs."""

BINARY_IMPRECISE_TRIPLES: tuple[tuple[Decimal, Decimal, Decimal], ...] = (
    (Decimal("0.1"), Decimal("0.2"), Decimal("0.3")),
    (Decimal("0.1"), Decimal("0.7"), Decimal("0.8")),
    (Decimal("1.1"), Decimal("2.2"), Decimal("3.3")),
    (Decimal("0.01"), Decimal("0.02"), Decimal("0.03")),
)
"""Sums where binary float arithmetic and decimal arithmetic disagree."""

PICKLE_PROTOCOLS: tuple[int, ...] = tuple(range(pickle.HIGHEST_PROTOCOL + 1))
"""Every pickle protocol the running interpreter supports."""
