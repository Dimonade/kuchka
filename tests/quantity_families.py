"""Shared fixtures describing every `LinearQuantity` family, plus shared strategies.

Each `QuantityFamily` bundles a quantity's canonical constructor with the `*_UNITS`
table `kuchka.units` already maintains for that dimension, so a single property
("addition is commutative") can run against every registered quantity type,
and every unit that dimension has, at once.

Only linear quantities appear here: multiplying by a plain scalar and combining two
instances behave the same way for each of them, which is what makes one shared property
suite possible.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction
from typing import TYPE_CHECKING

from hypothesis import strategies as st

from kuchka.internal import symbols
from kuchka.quantities import LinearQuantity
from kuchka.quantities.base.storage import _ScalarStorage
from kuchka.units import acceleration
from kuchka.units import amount
from kuchka.units import area
from kuchka.units import baud_rate
from kuchka.units import charge
from kuchka.units import conductance
from kuchka.units import current
from kuchka.units import density
from kuchka.units import energy
from kuchka.units import force
from kuchka.units import frequency
from kuchka.units import length
from kuchka.units import luminous_intensity
from kuchka.units import mass
from kuchka.units import power
from kuchka.units import pressure
from kuchka.units import proportion
from kuchka.units import resistance
from kuchka.units import sample_rate
from kuchka.units import sampling_period
from kuchka.units import thermal
from kuchka.units import time
from kuchka.units import velocity
from kuchka.units import voltage
from kuchka.units import volume

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Iterator
    from collections.abc import Mapping

    from kuchka.numeric import Numeric
    from kuchka.quantities.base import UnitDef


@dataclass(frozen=True)
class QuantityFamily:
    """One `LinearQuantity` dimension, plus everything needed to test it generically.

    `units` is the same `*_UNITS` table `kuchka.units` exports for this dimension
    (e.g. `VOLTAGE_UNITS`), keyed by symbol.

    Iterating it gives tests every constructor this dimension actually has.
    """

    id: str
    canonical: Callable[[Numeric], LinearQuantity]
    canonical_unit: UnitDef
    units: Mapping[str, Callable[[Numeric], LinearQuantity]]


FAMILIES: list[QuantityFamily] = [
    QuantityFamily("voltage", voltage.Volt, voltage.VOLT, voltage.VOLTAGE_UNITS),
    QuantityFamily("current", current.Ampere, current.AMPERE, current.CURRENT_UNITS),
    QuantityFamily("power", power.Watt, power.WATT, power.POWER_UNITS),
    QuantityFamily(
        "resistance", resistance.Ohm, resistance.OHM, resistance.RESISTANCE_UNITS
    ),
    QuantityFamily("time", time.Second, time.SECOND, time.TIME_UNITS),
    QuantityFamily(
        "frequency", frequency.Hertz, frequency.HERTZ, frequency.FREQUENCY_UNITS
    ),
    QuantityFamily("length", length.Metre, length.METRE, length.LENGTH_UNITS),
    QuantityFamily(
        "proportion", proportion.Ratio, proportion.RATIO, proportion.PROPORTION_UNITS
    ),
    QuantityFamily(
        "temperature_delta",
        thermal.DeltaKelvin,
        thermal.DELTA_KELVIN,
        thermal.TEMPERATURE_DELTA_UNITS,
    ),
    QuantityFamily(
        "sampling_period",
        lambda v: time.Second(v).as_sampling_period(),
        time.SECOND,
        sampling_period.SAMPLING_PERIOD_UNITS,
    ),
    QuantityFamily(
        "sample_rate",
        sample_rate.SamplesPerSecond,
        sample_rate.SAMPLES_PER_SECOND,
        sample_rate.SAMPLE_RATE_UNITS,
    ),
    QuantityFamily(
        "baud_rate", baud_rate.Baud, baud_rate.BAUD, baud_rate.BAUD_RATE_UNITS
    ),
    QuantityFamily("mass", mass.Kilogram, mass.KILOGRAM, mass.MASS_UNITS),
    QuantityFamily(
        "amount_of_substance",
        amount.Mole,
        amount.MOLE,
        amount.AMOUNT_OF_SUBSTANCE_UNITS,
    ),
    QuantityFamily(
        "luminous_intensity",
        luminous_intensity.Candela,
        luminous_intensity.CANDELA,
        luminous_intensity.LUMINOUS_INTENSITY_UNITS,
    ),
    QuantityFamily(
        "velocity",
        velocity.MetrePerSecond,
        velocity.METRE_PER_SECOND,
        velocity.VELOCITY_UNITS,
    ),
    QuantityFamily("charge", charge.Coulomb, charge.COULOMB, charge.CHARGE_UNITS),
    QuantityFamily("energy", energy.Joule, energy.JOULE, energy.ENERGY_UNITS),
    QuantityFamily("area", area.SquareMetre, area.SQUARE_METRE, area.AREA_UNITS),
    QuantityFamily(
        "volume", volume.CubicMetre, volume.CUBIC_METRE, volume.VOLUME_UNITS
    ),
    QuantityFamily(
        "conductance",
        conductance.Siemens,
        conductance.SIEMENS,
        conductance.CONDUCTANCE_UNITS,
    ),
    QuantityFamily(
        "acceleration",
        acceleration.MetrePerSecondSquared,
        acceleration.METRE_PER_SECOND_SQUARED,
        acceleration.ACCELERATION_UNITS,
    ),
    QuantityFamily("force", force.Newton, force.NEWTON, force.FORCE_UNITS),
    QuantityFamily(
        "density",
        density.KilogramPerCubicMetre,
        density.KILOGRAM_PER_CUBIC_METRE,
        density.DENSITY_UNITS,
    ),
    QuantityFamily(
        "pressure", pressure.Pascal, pressure.PASCAL, pressure.PRESSURE_UNITS
    ),
]

FAMILY_IDS: list[str] = [family.id for family in FAMILIES]

ALL_UNIT_CASES: list[tuple[QuantityFamily, Callable[[Numeric], LinearQuantity]]] = [
    (family, constructor)
    for family in FAMILIES
    for constructor in family.units.values()
]
"""Every (family, constructor) pair every `*_UNITS` table registers, paired with a
matching id list -- one entry per unit a dimension has.
"""

ALL_UNIT_CASE_IDS: list[str] = [
    f"{family.id}-{symbol}" for family in FAMILIES for symbol in family.units
]

EXACT_DIVISION_EXCLUSIONS: dict[str, frozenset[str]] = {
    "length": frozenset({"in"}),
    "area": frozenset({"ac", f"in{symbols.SUPERSCRIPT_TWO}"}),
    "energy": frozenset(
        {
            "mWh",
            "Wh",
            f"{symbols.MICRO}eV",
            "meV",
            "eV",
            "keV",
            "MeV",
            "GeV",
            "TeV",
            "PeV",
            "kcal",
            "cal_th",
        }
    ),
    "charge": frozenset({"mAh", "Ah"}),
    "velocity": frozenset({"km/h"}),
    "force": frozenset({"lbf", "kgf"}),
    "pressure": frozenset({"psi"}),
    "temperature_delta": frozenset({"dF"}),
    "time": frozenset(
        {
            "min",
            "h",
            "d",
            "wk",
            "fortnight",
            "a",
        }
    ),
    "power": frozenset({"hp", "PS"}),
}
"""Units excluded from properties that require finite Decimal reciprocals.

A unit is excluded when its exact scale factor has a reciprocal whose denominator
contains a prime factor other than 2 or 5.
Such a reciprocal cannot be represented by a finite `Decimal`.

`in` (inch), `ac` (acre), and `in²` (square inch) are excluded because their exact
reciprocal scales are non-terminating decimals.

`min`, `h`, `d`, `wk`, `fortnight`, and `a` are excluded for the same reason:
their exact scales in seconds contain factors other than 2 and 5.

`km/h`, `dF`, and similar rational scales are excluded when their reduced fractional
representation itself has a denominator containing a prime factor other than 2 or 5.

A unit does not need to have a power-of-ten scale to be accepted.
For example, `mph` has an exact scale of `0.44704`, and its reciprocal also terminates,
so it does not require an exclusion.

The physics `jiffy` is another example of a non-power-of-ten scale that does not
require exclusion: its exact scale is the reciprocal of an integer, so its own
reciprocal is an integer.
"""

EXACT_DIVISION_UNIT_CASES: list[
    tuple[QuantityFamily, Callable[[Numeric], LinearQuantity]]
] = [
    (family, constructor)
    for family in FAMILIES
    for symbol, constructor in family.units.items()
    if symbol not in EXACT_DIVISION_EXCLUSIONS.get(family.id, frozenset())
]
EXACT_DIVISION_UNIT_CASE_IDS: list[str] = [
    f"{family.id}-{symbol}"
    for family in FAMILIES
    for symbol in family.units
    if symbol not in EXACT_DIVISION_EXCLUSIONS.get(family.id, frozenset())
]

ALL_UNITDEF_CASES: list[tuple[QuantityFamily, UnitDef]] = [
    (family, constructor(1).unit) for family, constructor in ALL_UNIT_CASES
]
"""The `UnitDef` each constructor carries.

A constructor always displays the same unit regardless of the magnitude it's called
with, so calling it to read `.unit` back is only worth doing a single time per case.
"""

EXACT_DIVISION_UNITDEF_CASES: list[tuple[QuantityFamily, UnitDef]] = [
    (family, constructor(1).unit) for family, constructor in EXACT_DIVISION_UNIT_CASES
]


def scale_by(quantity: LinearQuantity, factor: int) -> LinearQuantity:
    """Multiply a `LinearQuantity` by a plain scalar and return the typed result.

    A scalar multiplication always produces another quantity of the same type, so the
    runtime `isinstance` check here always holds;
    it exists to give tests a value typed as `LinearQuantity` to keep working with.
    """
    result = quantity * factor
    assert isinstance(result, LinearQuantity)
    return result


FINITE_DECIMALS = st.decimals(
    allow_nan=False,
    allow_infinity=False,
    min_value=Decimal("-1E9"),
    max_value=Decimal("1E9"),
    places=9,
)
"""Bounded, finite decimals.

Large enough to exercise real arithmetic, small enough in both magnitude and decimal
places to stay well under Decimal's default 28-significant-digit context precision
even after two or three quantities get combined.
"""

NONZERO_FINITE_DECIMALS = FINITE_DECIMALS.filter(lambda value: value != 0)
"""Excludes zero, for tests exercising division by a generated value."""

SCALARS = st.integers(min_value=-1000, max_value=1000)
NONZERO_SCALARS = SCALARS.filter(lambda value: value != 0)

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
"""Extreme magnitude collection.

Round numbers spanning many orders of magnitude, from the smallest a quantity's own
prefix vocabulary needs out to far beyond it.
"""

BINARY_IMPRECISE_TRIPLES: list[tuple[Decimal, Decimal, Decimal]] = [
    (Decimal("0.1"), Decimal("0.2"), Decimal("0.3")),
    (Decimal("0.1"), Decimal("0.7"), Decimal("0.8")),
    (Decimal("1.1"), Decimal("2.2"), Decimal("3.3")),
    (Decimal("0.01"), Decimal("0.02"), Decimal("0.03")),
]
"""Values where binary float arithmetic and decimal arithmetic disagree.

0.1 + 0.2 prints as 0.30000000000000004 in `float`, exactly 0.3 in `Decimal`.
"""


def _concrete_quantity_types(base: type = _ScalarStorage) -> Iterator[type]:
    """Yield every quantity type that declares its own dimension."""
    for subclass in base.__subclasses__():
        if "dimension" in vars(subclass):
            yield subclass
        yield from _concrete_quantity_types(subclass)


CONCRETE_QUANTITY_TYPES: list[type] = sorted(
    _concrete_quantity_types(), key=lambda cls: cls.__name__
)
"""Every concrete quantity type, discovered from the class hierarchy.

A type added later joins the list without any edit here.
"""


def sample_of(cls: type) -> _ScalarStorage:
    """Build one valid value of a concrete quantity type, in its canonical unit."""
    unit = getattr(cls, "_canonical_unit", thermal.KELVIN)
    return cls(Fraction(5), unit)  # type: ignore[no-any-return]
