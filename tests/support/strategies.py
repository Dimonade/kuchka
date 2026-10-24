"""Hypothesis strategies shared by the property tests."""

from __future__ import annotations

from decimal import Decimal

from hypothesis import strategies as st

from tests.support.families import FAMILIES
from tests.support.families import UNIT_CASES

FINITE_DECIMALS = st.decimals(
    allow_nan=False,
    allow_infinity=False,
    min_value=Decimal("-1E9"),
    max_value=Decimal("1E9"),
    places=9,
)
"""Bounded, finite decimals: real arithmetic, with exactly representable digits."""

SCALARS = st.integers(min_value=-1000, max_value=1000)
NONZERO_SCALARS = SCALARS.filter(lambda value: value != 0)

FAMILY_STRATEGY = st.sampled_from(FAMILIES)
"""A family drawn at random: one property test covers every linear type."""

UNIT_CASE_STRATEGY = st.sampled_from(UNIT_CASES)
"""A unit of a family drawn at random: one property test covers every unit."""
