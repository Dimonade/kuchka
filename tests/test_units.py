"""Unit prefixes: every constructor must scale into its canonical unit correctly.

Tests parametrize over `PrefixCase`, which provides a comfortable interface to add
new units and quantities to.

`PrefixCase.prefixed_unit` and `.canonical_unit` are the actual `UnitDef` instances
each constructor carries (`MILLIVOLT`, `VOLT`, ...), imported directly from
`kuchka.units`.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import TYPE_CHECKING

import pytest
from hypothesis import given
from kuchka import Ampere
from kuchka import Gram
from kuchka import Hertz
from kuchka import Inch
from kuchka import Kiloampere
from kuchka import Kilogram
from kuchka import Kilohertz
from kuchka import Kilometer
from kuchka import Kiloohm
from kuchka import KilosamplesPerSecond
from kuchka import Kilovolt
from kuchka import Kilowatt
from kuchka import Megagram
from kuchka import Megahertz
from kuchka import Megaohm
from kuchka import MegasamplesPerSecond
from kuchka import Meter
from kuchka import Microampere
from kuchka import Microgram
from kuchka import Micrometer
from kuchka import Microsecond
from kuchka import MicrosecondSamplingPeriod
from kuchka import Microvolt
from kuchka import Milliampere
from kuchka import Milligram
from kuchka import Millimeter
from kuchka import Milliohm
from kuchka import Millisecond
from kuchka import MillisecondSamplingPeriod
from kuchka import Millivolt
from kuchka import Milliwatt
from kuchka import Nanogram
from kuchka import Nanometer
from kuchka import Ohm
from kuchka import SamplesPerSecond
from kuchka import Second
from kuchka import SecondSamplingPeriod
from kuchka import Tonne
from kuchka import Volt
from kuchka import Watt
from kuchka.units import AMPERE
from kuchka.units import GRAM
from kuchka.units import HERTZ
from kuchka.units import INCH
from kuchka.units import KILOAMPERE
from kuchka.units import KILOGRAM
from kuchka.units import KILOHERTZ
from kuchka.units import KILOMETER
from kuchka.units import KILOOHM
from kuchka.units import KILOSAMPLE_PER_SECOND
from kuchka.units import KILOVOLT
from kuchka.units import KILOWATT
from kuchka.units import MEGAGRAM
from kuchka.units import MEGAHERTZ
from kuchka.units import MEGAOHM
from kuchka.units import MEGASAMPLE_PER_SECOND
from kuchka.units import METER
from kuchka.units import MICROAMPERE
from kuchka.units import MICROGRAM
from kuchka.units import MICROMETER
from kuchka.units import MICROSECOND
from kuchka.units import MICROVOLT
from kuchka.units import MILLIAMPERE
from kuchka.units import MILLIGRAM
from kuchka.units import MILLIMETER
from kuchka.units import MILLIOHM
from kuchka.units import MILLISECOND
from kuchka.units import MILLIVOLT
from kuchka.units import MILLIWATT
from kuchka.units import NANOGRAM
from kuchka.units import NANOMETER
from kuchka.units import OHM
from kuchka.units import SAMPLE_PER_SECOND
from kuchka.units import SAMPLING_PERIOD_MICROSECOND
from kuchka.units import SAMPLING_PERIOD_MILLISECOND
from kuchka.units import SAMPLING_PERIOD_SECOND
from kuchka.units import SECOND
from kuchka.units import VOLT
from kuchka.units import WATT

from tests.quantity_families import FINITE_DECIMALS

if TYPE_CHECKING:
    from collections.abc import Callable

    from kuchka.numeric import Numeric
    from kuchka.quantities import LinearQuantity
    from kuchka.quantities.base import UnitDef


@dataclass(frozen=True)
class PrefixCase:
    """One prefix constructor paired with its canonical constructor and both units."""

    id: str
    prefixed: Callable[[Numeric], LinearQuantity]
    canonical: Callable[[Numeric], LinearQuantity]
    scale: Decimal
    prefixed_unit: UnitDef
    canonical_unit: UnitDef


PREFIX_CASES: list[PrefixCase] = [
    PrefixCase("Microvolt", Microvolt, Volt, Decimal("0.000001"), MICROVOLT, VOLT),
    PrefixCase("Millivolt", Millivolt, Volt, Decimal("0.001"), MILLIVOLT, VOLT),
    PrefixCase("Kilovolt", Kilovolt, Volt, Decimal(1000), KILOVOLT, VOLT),
    PrefixCase(
        "Microampere", Microampere, Ampere, Decimal("0.000001"), MICROAMPERE, AMPERE
    ),
    PrefixCase(
        "Milliampere", Milliampere, Ampere, Decimal("0.001"), MILLIAMPERE, AMPERE
    ),
    PrefixCase("Kiloampere", Kiloampere, Ampere, Decimal(1000), KILOAMPERE, AMPERE),
    PrefixCase("Milliohm", Milliohm, Ohm, Decimal("0.001"), MILLIOHM, OHM),
    PrefixCase("Kiloohm", Kiloohm, Ohm, Decimal(1000), KILOOHM, OHM),
    PrefixCase("Megaohm", Megaohm, Ohm, Decimal(1_000_000), MEGAOHM, OHM),
    PrefixCase("Milliwatt", Milliwatt, Watt, Decimal("0.001"), MILLIWATT, WATT),
    PrefixCase("Kilowatt", Kilowatt, Watt, Decimal(1000), KILOWATT, WATT),
    PrefixCase(
        "Microsecond", Microsecond, Second, Decimal("0.000001"), MICROSECOND, SECOND
    ),
    PrefixCase(
        "Millisecond", Millisecond, Second, Decimal("0.001"), MILLISECOND, SECOND
    ),
    PrefixCase("Kilohertz", Kilohertz, Hertz, Decimal(1000), KILOHERTZ, HERTZ),
    PrefixCase("Megahertz", Megahertz, Hertz, Decimal(1_000_000), MEGAHERTZ, HERTZ),
    PrefixCase(
        "MicrosecondSamplingPeriod",
        MicrosecondSamplingPeriod,
        SecondSamplingPeriod,
        Decimal("0.000001"),
        SAMPLING_PERIOD_MICROSECOND,
        SAMPLING_PERIOD_SECOND,
    ),
    PrefixCase(
        "MillisecondSamplingPeriod",
        MillisecondSamplingPeriod,
        SecondSamplingPeriod,
        Decimal("0.001"),
        SAMPLING_PERIOD_MILLISECOND,
        SAMPLING_PERIOD_SECOND,
    ),
    PrefixCase(
        "KilosamplesPerSecond",
        KilosamplesPerSecond,
        SamplesPerSecond,
        Decimal(1000),
        KILOSAMPLE_PER_SECOND,
        SAMPLE_PER_SECOND,
    ),
    PrefixCase(
        "MegasamplesPerSecond",
        MegasamplesPerSecond,
        SamplesPerSecond,
        Decimal(1_000_000),
        MEGASAMPLE_PER_SECOND,
        SAMPLE_PER_SECOND,
    ),
    PrefixCase("Nanometer", Nanometer, Meter, Decimal("0.000000001"), NANOMETER, METER),
    PrefixCase("Micrometer", Micrometer, Meter, Decimal("0.000001"), MICROMETER, METER),
    PrefixCase("Millimeter", Millimeter, Meter, Decimal("0.001"), MILLIMETER, METER),
    PrefixCase("Kilometer", Kilometer, Meter, Decimal(1000), KILOMETER, METER),
    PrefixCase("Inch", Inch, Meter, Decimal("0.0254"), INCH, METER),
    PrefixCase(
        "Nanogram", Nanogram, Kilogram, Decimal("0.000000000001"), NANOGRAM, KILOGRAM
    ),
    PrefixCase(
        "Microgram", Microgram, Kilogram, Decimal("0.000000001"), MICROGRAM, KILOGRAM
    ),
    PrefixCase(
        "Milligram", Milligram, Kilogram, Decimal("0.000001"), MILLIGRAM, KILOGRAM
    ),
    PrefixCase("Gram", Gram, Kilogram, Decimal("0.001"), GRAM, KILOGRAM),
    PrefixCase("Megagram", Megagram, Kilogram, Decimal(1000), MEGAGRAM, KILOGRAM),
    PrefixCase("Tonne", Tonne, Kilogram, Decimal(1000), MEGAGRAM, KILOGRAM),
]

PREFIX_CASE_IDS: list[str] = [case.id for case in PREFIX_CASES]


@pytest.mark.parametrize("case", PREFIX_CASES, ids=PREFIX_CASE_IDS)
def test_prefix_scales_into_the_canonical_unit(case: PrefixCase) -> None:
    assert case.prefixed(1) == case.canonical(case.scale)
    assert case.prefixed(1).unit is case.prefixed_unit
    assert case.canonical(1).unit is case.canonical_unit


@pytest.mark.parametrize("case", PREFIX_CASES, ids=PREFIX_CASE_IDS)
@given(magnitude=FINITE_DECIMALS)
def test_prefix_scale_is_exact_across_a_range_of_magnitudes(
    case: PrefixCase,
    magnitude: Decimal,
) -> None:
    assert case.prefixed(magnitude) == case.canonical(magnitude * case.scale)


@pytest.mark.parametrize("case", PREFIX_CASES, ids=PREFIX_CASE_IDS)
def test_round_trip_conversion_through_to(case: PrefixCase) -> None:
    """Converting a canonical-unit value down and back up preserves the value."""
    original = case.canonical(1)
    converted = original.to(case.prefixed_unit)
    assert converted == original
    assert converted.unit is case.prefixed_unit
    assert converted.value_in(case.prefixed_unit) == 1 / case.scale
    assert converted.to(case.canonical_unit) == original


def test_unit_def_repr_shows_name_and_symbol() -> None:
    assert repr(Volt(1).unit) == "UnitDef('volt', 'V')"
