"""Unit prefixes: every constructor must scale into its canonical unit correctly.

Rather than writing one test per constructor per dimension, this
parametrizes over `(prefixed_constructor, canonical_constructor, scale)`
triples so that adding a new prefix or a new dimension later means adding
a row to a table, not writing a new test function.
"""

from decimal import Decimal

import pytest
from kuchka import Ampere
from kuchka import Kiloampere
from kuchka import Kiloohm
from kuchka import Kilovolt
from kuchka import Kilowatt
from kuchka import Megaohm
from kuchka import Microampere
from kuchka import Microvolt
from kuchka import Milliampere
from kuchka import Milliohm
from kuchka import Millivolt
from kuchka import Milliwatt
from kuchka import Ohm
from kuchka import Volt
from kuchka import Watt

# (prefixed constructor, canonical constructor for the same dimension, scale factor)
PREFIX_CASES = [
    (Microvolt, Volt, Decimal("0.000001")),
    (Millivolt, Volt, Decimal("0.001")),
    (Kilovolt, Volt, Decimal(1000)),
    (Microampere, Ampere, Decimal("0.000001")),
    (Milliampere, Ampere, Decimal("0.001")),
    (Kiloampere, Ampere, Decimal(1000)),
    (Milliohm, Ohm, Decimal("0.001")),
    (Kiloohm, Ohm, Decimal(1000)),
    (Megaohm, Ohm, Decimal(1_000_000)),
    (Milliwatt, Watt, Decimal("0.001")),
    (Kilowatt, Watt, Decimal(1000)),
]


@pytest.mark.parametrize(("prefixed", "canonical", "scale"), PREFIX_CASES)
def test_prefix_scales_into_the_canonical_unit(prefixed, canonical, scale):
    assert prefixed(1) == canonical(scale)


@pytest.mark.parametrize(("prefixed", "canonical", "scale"), PREFIX_CASES)
def test_prefix_scale_is_exact_for_a_range_of_magnitudes(prefixed, canonical, scale):
    for magnitude in (0, 1, -1, 7, 250, Decimal("0.5")):
        assert prefixed(magnitude) == canonical(Decimal(magnitude) * scale)


@pytest.mark.parametrize(("prefixed", "canonical", "scale"), PREFIX_CASES)
def test_round_trip_conversion_through_to(prefixed, canonical, scale):
    """Converting a canonical-unit value down and back up preserves the value."""
    original = canonical(1)
    converted = original.to(prefixed(0).unit)
    assert converted == original
    assert converted.value_in(prefixed(0).unit) == 1 / scale


def test_unit_def_repr_shows_name_and_symbol():
    assert repr(Volt(1).unit) == "UnitDef('volt', 'V')"
