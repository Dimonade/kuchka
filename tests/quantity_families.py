"""Shared fixtures describing every `LinearQuantity` family, plus shared strategies.

This is what lets `tests/test_properties.py` express one property ("addition
is commutative") once and run it against every registered quantity type.
Each `QuantityFamily` bundles a quantity's canonical constructor with a second,
differently scaled constructor for the same dimension, so conversion and cross-prefix
properties have something to convert between.

NOTE: `Temperature` is deliberately absent: it is affine, not linear (see
`kuchka.temperature`), so "scalar multiplication" and "additive identity"
are not meaningful questions for it.
It gets its own, smaller set of affine-specific properties in `test_properties.py`.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import TYPE_CHECKING

from hypothesis import strategies as st
from kuchka import Ampere
from kuchka import Baud
from kuchka import DeltaCelsius
from kuchka import DeltaKelvin
from kuchka import Hertz
from kuchka import Kilobaud
from kuchka import Kilohertz
from kuchka import Kiloohm
from kuchka import KilosamplesPerSecond
from kuchka import Meter
from kuchka import Milliampere
from kuchka import Millimeter
from kuchka import Millisecond
from kuchka import MillisecondSamplingPeriod
from kuchka import Millivolt
from kuchka import Milliwatt
from kuchka import Ohm
from kuchka import Percent
from kuchka import Ratio
from kuchka import SamplesPerSecond
from kuchka import Second
from kuchka import SecondSamplingPeriod
from kuchka import Volt
from kuchka import Watt
from kuchka.quantities import LinearQuantity
from kuchka.temperature import DELTA_CELSIUS
from kuchka.temperature import DELTA_KELVIN
from kuchka.units import AMPERE
from kuchka.units import BAUD
from kuchka.units import HERTZ
from kuchka.units import KILOBAUD
from kuchka.units import KILOHERTZ
from kuchka.units import KILOOHM
from kuchka.units import KILOSAMPLE_PER_SECOND
from kuchka.units import METER
from kuchka.units import MILLIAMPERE
from kuchka.units import MILLIMETER
from kuchka.units import MILLISECOND
from kuchka.units import MILLIVOLT
from kuchka.units import MILLIWATT
from kuchka.units import OHM
from kuchka.units import PERCENT
from kuchka.units import RATIO
from kuchka.units import SAMPLE_PER_SECOND
from kuchka.units import SAMPLING_PERIOD_MILLISECOND
from kuchka.units import SAMPLING_PERIOD_SECOND
from kuchka.units import SECOND
from kuchka.units import VOLT
from kuchka.units import WATT

if TYPE_CHECKING:
    from collections.abc import Callable

    from kuchka.numeric import Numeric
    from kuchka.quantities.base import UnitDef


@dataclass(frozen=True)
class QuantityFamily:
    """One `LinearQuantity` dimension, plus everything needed to test it generically.

    `canonical` and `alt` construct the same physical quantity at two different scales
    (e.g. `Volt`/`Millivolt`); `canonical_unit` and `alt_unit` are the
    `UnitDef`s those two constructors carry, so tests can convert between them with
    `.to(...)` without a hand-written per-dimension conversion table.
    """

    id: str
    canonical: Callable[[Numeric], LinearQuantity]
    alt: Callable[[Numeric], LinearQuantity]
    canonical_unit: UnitDef
    alt_unit: UnitDef


FAMILIES: list[QuantityFamily] = [
    QuantityFamily("voltage", Volt, Millivolt, VOLT, MILLIVOLT),
    QuantityFamily("current", Ampere, Milliampere, AMPERE, MILLIAMPERE),
    QuantityFamily("power", Watt, Milliwatt, WATT, MILLIWATT),
    QuantityFamily("resistance", Ohm, Kiloohm, OHM, KILOOHM),
    QuantityFamily("time", Second, Millisecond, SECOND, MILLISECOND),
    QuantityFamily("frequency", Hertz, Kilohertz, HERTZ, KILOHERTZ),
    QuantityFamily("length", Meter, Millimeter, METER, MILLIMETER),
    QuantityFamily("proportion", Ratio, Percent, RATIO, PERCENT),
    QuantityFamily(
        "temperature_delta",
        DeltaKelvin,
        DeltaCelsius,
        DELTA_KELVIN,
        DELTA_CELSIUS,
    ),
    QuantityFamily(
        "sampling_period",
        SecondSamplingPeriod,
        MillisecondSamplingPeriod,
        SAMPLING_PERIOD_SECOND,
        SAMPLING_PERIOD_MILLISECOND,
    ),
    QuantityFamily(
        "sample_rate",
        SamplesPerSecond,
        KilosamplesPerSecond,
        SAMPLE_PER_SECOND,
        KILOSAMPLE_PER_SECOND,
    ),
    QuantityFamily("baud_rate", Baud, Kilobaud, BAUD, KILOBAUD),
]

FAMILY_IDS: list[str] = [family.id for family in FAMILIES]


def scale_by(quantity: LinearQuantity, factor: int) -> LinearQuantity:
    """Multiply a `LinearQuantity` by a plain scalar, narrowing back from the union.

    `LinearQuantity.__mul__`'s statically visible signature on the base class returns
    `LinearQuantity | Decimal`, because from the base class's own perspective a
    multiplication can also be quantity-times-quantity, which is sometimes
    dimensionless (see `_promote` in `quantities/base.py`).

    Multiplying by a plain scalar never produces a bare `Decimal` at runtime --
    only quantity-times-quantity does -- so this narrows the result back down for tests
    that stay on the abstract `LinearQuantity` interface, where mypy has no way to know
    that on its own.
    """
    result = quantity * factor
    assert isinstance(result, LinearQuantity)
    return result


"""Bounded, finite decimals.

These are fitting for:
- large enough to exercise real arithmetic,
- small enough in both magnitude and decimal places to stay well under Decimal's
    default 28-significant-digit context precision even after two or three quantities
    get combined.

Extreme magnitudes get their own dedicated, explicit test cases (see EXTREME_MAGNITUDES).
"""
FINITE_DECIMALS = st.decimals(
    allow_nan=False,
    allow_infinity=False,
    min_value=Decimal("-1E9"),
    max_value=Decimal("1E9"),
    places=9,
)

"""Deliberate zero excluded finite decimals.

Division by a hypothesis-generated zero is a separate concern (see test_arithmetic.py's
ZeroDivisionError tests), not something every property test needs to special-case.
"""
NONZERO_FINITE_DECIMALS = FINITE_DECIMALS.filter(lambda value: value != 0)

SCALARS = st.integers(min_value=-1000, max_value=1000)
NONZERO_SCALARS = SCALARS.filter(lambda value: value != 0)

"""Deliberate round numbers of varying magnitude.

These include the smallest quantity's own prefix vocabulary ever needs (1E-9, for a
nanometer expressed in meters) out to far beyond it.

This is used specifically for a "huge and tiny exponents" sweep.
"""
EXTREME_MAGNITUDES: list[Decimal] = [
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
]

"""A handful of hand-picked binary-float traps.

This is the category of `0.1 + 0.2 != 0.3` in `float`, by design, because none of the
three has an exact binary fraction.

`Decimal` (and therefore every `kuchka` quantity) must not inherit that surprise.
"""
BINARY_IMPRECISE_TRIPLES: list[tuple[Decimal, Decimal, Decimal]] = [
    (Decimal("0.1"), Decimal("0.2"), Decimal("0.3")),
    (Decimal("0.1"), Decimal("0.7"), Decimal("0.8")),
    (Decimal("1.1"), Decimal("2.2"), Decimal("3.3")),
    (Decimal("0.01"), Decimal("0.02"), Decimal("0.03")),
]
