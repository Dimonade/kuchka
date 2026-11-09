"""Unit constructors for Exposure Rate: roentgens per second, minute, and hour.

    from kuchka import MilliroentgenPerHour, RoentgenPerHour

    reading = MilliroentgenPerHour(2.5)
    calibration_field = RoentgenPerHour(0.1)

`ExposureRate` describes how quickly exposure accumulates in air.
Its canonical, SI-coherent unit is the ampere per kilogram (A/kg), shared in dimension
with `SpecificCurrent`.
Arithmetic results display in roentgens per hour (R/h).

The available units cover several scales of radiological measurement:

* microroentgens per hour (µR/h) describe low-level photon fields and fine-resolution
    survey readings;
* milliroentgens per hour (mR/h) are common in survey-meter measurements and
    radiation-field characterization;
* roentgens per hour (R/h) express larger exposure rates and irradiation field
    strengths;
* roentgens per minute (R/min) describe exposure rates over shorter irradiation
    intervals;
* roentgens per second (R/s) are useful when describing brief, high-rate exposures and
    pulsed irradiation.

Examples
--------
An ionization chamber records an exposure rate of 2.5 mR/h in an X-ray field.
Express the reading in microroentgens per hour:

>>> reading = MilliroentgenPerHour(2.5)
>>> from kuchka.units import MICROROENTGEN_PER_HOUR
>>> reading.to(MICROROENTGEN_PER_HOUR)
2500 µR/h

Exposure rate multiplied by elapsed time gives the accumulated exposure when the rate
is constant over the interval.
A two-hour measurement at 2.5 mR/h accumulates 5 mR:

>>> from kuchka import Hour
>>> from kuchka.units import MILLIROENTGEN
>>> (reading * Hour(2)).to(MILLIROENTGEN)
5 mR

Exposure rate can also be expressed directly in its canonical SI unit.
The conversion from exposure rate to specific current is made explicit:

>>> from fractions import Fraction
>>> from kuchka import ExposureRate, AmperePerKilogram
>>> from kuchka.units import ROENTGEN_PER_HOUR
>>> current_per_mass = AmperePerKilogram(Fraction(43, 600_000_000))
>>> ExposureRate.from_specific_current(current_per_mass).to(ROENTGEN_PER_HOUR)
1 R/h

Instrument and archival records often use different spellings for the same unit.
`parse` reads the numeric value and unit together, including registered alternatives:

>>> from kuchka import parse
>>> from kuchka.quantities import ExposureRate
>>> parse("2.5 mR/hr", ExposureRate) == MilliroentgenPerHour(2.5)
True

The SI representation is accepted as well:

>>> parse("0.000258 A/kg", ExposureRate) == RoentgenPerSecond(1)
True

Notes
-----
Exposure, denoted by X, quantifies the electric charge of ions of one sign produced in
air by X-rays or gamma rays, per unit mass of air:

``X = dQ/dm``

Exposure rate is its time derivative:

``Ẋ = dX/dt``

Its SI-coherent unit follows directly:

``1 A/kg = 1 C/(kg·s)``

The roentgen is a non-SI unit of exposure:

``1 R = 2.58 x 10⁻⁴ C/kg``

Therefore:

``1 R/s = 2.58 x 10⁻⁴ A/kg``

``1 R/h = 43/600000000 A/kg``

For a constant exposure rate, the accumulated exposure over an interval is the product
of the rate and elapsed time.
For a varying rate, exposure is obtained by integrating the rate over time.

Exposure is distinct from absorbed dose, which measures energy deposited per unit mass,
and equivalent dose, which incorporates a radiation weighting factor.
Roentgen is specifically a unit of exposure to X- and gamma radiation, not a general
unit of absorbed energy.

`ExposureRate.from_specific_current()` explicitly constructs an exposure rate from a
`SpecificCurrent`.
Although the quantities share the dimension and SI unit A/kg, they retain distinct
meanings.

`parse` accepts complete measurements such as ``"2.5 mR/h"``, ``"0.1 R/hr"``,
``"250 µR/hr"``, and ``"0.000258 A/kg"``.
Alternative spellings registered by the unit definitions are accepted as well.

`EXPOSURE_RATE_UNITS` maps supported unit symbols, including ``"R/s"``, ``"R/min"``,
``"R/h"``, ``"mR/h"``, ``"µR/h"``, and ``"A/kg"``, to their constructors.
It is useful when an application already receives a numeric magnitude and a separate
unit symbol.

The roentgen definition is maintained in the IUPAC Compendium of Chemical Terminology:
https://goldbook.iupac.org/terms/view/R05404

See Also
--------
~kuchka.quantities.ExposureRate
    Quantity type representing exposure rate.

~kuchka.quantities.Exposure
    Exposure accumulated over an irradiation interval.

~kuchka.quantities.SpecificCurrent
    Electric current per unit mass, sharing the dimension of exposure rate.

~kuchka.quantities.AbsorbedDose
    Energy deposited per unit mass by ionizing radiation.

~kuchka.quantities.EquivalentDose
    Radiation-weighted dose quantity.

~kuchka.units.radiation.exposure
    Constructors for roentgens and other exposure units.

"""

from __future__ import annotations

from fractions import Fraction
from typing import TYPE_CHECKING

from kuchka.dimensions import SPECIFIC_CURRENT
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import ExposureRate
from kuchka.quantities import UnitDef
from kuchka.units.electromagnetics.specific_current import AMPERE_PER_KILOGRAM
from kuchka.units.electromagnetics.specific_current import AmperePerKilogram

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

ROENTGEN_PER_SECOND = UnitDef(
    "roentgen_per_second",
    "R/s",
    Fraction(129, 500000),
    SPECIFIC_CURRENT,
    words=("roentgens per second",),
)
ROENTGEN_PER_MINUTE = UnitDef(
    "roentgen_per_minute",
    "R/min",
    Fraction(43, 10000000),
    SPECIFIC_CURRENT,
    words=("roentgens per minute",),
)
ROENTGEN_PER_HOUR = UnitDef(
    "roentgen_per_hour",
    "R/h",
    Fraction(43, 600000000),
    SPECIFIC_CURRENT,
    aliases=("R/hr",),
    words=("roentgens per hour",),
)
MILLIROENTGEN_PER_HOUR = UnitDef(
    "milliroentgen_per_hour",
    "mR/h",
    Fraction(43, 600000000000),
    SPECIFIC_CURRENT,
    aliases=("mR/hr",),
    words=("milliroentgens per hour",),
)
MICROROENTGEN_PER_HOUR = UnitDef(
    "microroentgen_per_hour",
    "µR/h",
    Fraction(43, 600000000000000),
    SPECIFIC_CURRENT,
    aliases=("µR/hr", "uR/h", "uR/hr"),
    words=("microroentgens per hour",),
)

ExposureRate._canonical_unit = AMPERE_PER_KILOGRAM  # noqa: SLF001 -- this module owns ExposureRate's canonical unit
ExposureRate._result_unit = ROENTGEN_PER_HOUR  # noqa: SLF001 -- and the unit its arithmetic results display in


def _ampere_per_kilogram(value: Numeric) -> ExposureRate:
    """Interpret a specific current magnitude as an exposure rate."""
    return ExposureRate.from_specific_current(AmperePerKilogram(value))


def RoentgenPerSecond(value: Numeric) -> ExposureRate:
    """Construct an ExposureRate from a magnitude in roentgens per second.

    Parameters
    ----------
    value : Numeric
        Exposure rate magnitude in R/s.

    Returns
    -------
    ExposureRate
        Exposure rate represented in roentgens per second.

    Examples
    --------
    A pulsed X-ray imaging sequence produces an exposure rate of 0.02 R/s during a
    250 ms pulse.
    Calculate the accumulated exposure:

    >>> from kuchka import Second
    >>> from kuchka.units import MILLIROENTGEN
    >>> pulse_rate = RoentgenPerSecond(0.02)
    >>> (pulse_rate * Second(Fraction(1, 4))).to(MILLIROENTGEN)
    5 mR

    """
    return ExposureRate(
        to_exact(value) * ROENTGEN_PER_SECOND.scale, ROENTGEN_PER_SECOND
    )


def RoentgenPerMinute(value: Numeric) -> ExposureRate:
    """Construct an ExposureRate from a magnitude in roentgens per minute.

    Parameters
    ----------
    value : Numeric
        Exposure rate magnitude in R/min.

    Returns
    -------
    ExposureRate
        Exposure rate represented in roentgens per minute.

    Examples
    --------
    A reference ionization chamber measures an X-ray field at 0.05 R/min.
    Express the same exposure rate per hour:

    >>> from kuchka.units import ROENTGEN_PER_HOUR
    >>> RoentgenPerMinute(0.05).to(ROENTGEN_PER_HOUR)
    3 R/h

    """
    return ExposureRate(
        to_exact(value) * ROENTGEN_PER_MINUTE.scale, ROENTGEN_PER_MINUTE
    )


def RoentgenPerHour(value: Numeric) -> ExposureRate:
    """Construct an ExposureRate from a magnitude in roentgens per hour.

    Parameters
    ----------
    value : Numeric
        Exposure rate magnitude in R/h.

    Returns
    -------
    ExposureRate
        Exposure rate represented in roentgens per hour.

    Examples
    --------
    A gamma-field measurement is recorded as 0.1 R/h.
    Express the reading in milliroentgens per hour:

    >>> from kuchka.units.radiation.exposure_rate import MILLIROENTGEN_PER_HOUR
    >>> RoentgenPerHour(0.1).to(MILLIROENTGEN_PER_HOUR)
    100 mR/h

    """
    return ExposureRate(to_exact(value) * ROENTGEN_PER_HOUR.scale, ROENTGEN_PER_HOUR)


def MilliroentgenPerHour(value: Numeric) -> ExposureRate:
    """Construct an ExposureRate from a magnitude in milliroentgens per hour.

    Parameters
    ----------
    value : Numeric
        Exposure rate magnitude in mR/h.

    Returns
    -------
    ExposureRate
        Exposure rate represented in milliroentgens per hour.

    Examples
    --------
    A radiological survey records an exposure rate of 2.5 mR/h.
    Express the reading in microroentgens per hour:

    >>> from kuchka import Hour
    >>> from kuchka.units import MICROROENTGEN_PER_HOUR
    >>> from kuchka.units import MILLIROENTGEN
    >>> reading = MilliroentgenPerHour(2.5)
    >>> reading.to(MICROROENTGEN_PER_HOUR)
    2500 µR/h

    Over a two-hour interval at this constant rate, the accumulated exposure is:

    >>> (reading * Hour(2)).to(MILLIROENTGEN)
    5 mR

    """
    return ExposureRate(
        to_exact(value) * MILLIROENTGEN_PER_HOUR.scale, MILLIROENTGEN_PER_HOUR
    )


def MicroroentgenPerHour(value: Numeric) -> ExposureRate:
    """Construct an ExposureRate from a magnitude in microroentgens per hour.

    Parameters
    ----------
    value : Numeric
        Exposure rate magnitude in µR/h.

    Returns
    -------
    ExposureRate
        Exposure rate represented in microroentgens per hour.

    Examples
    --------
    A long-duration gamma-field survey records an exposure rate of 850 µR/h.
    Express the reading in milliroentgens per hour:

    >>> from kuchka.units import MILLIROENTGEN_PER_HOUR
    >>> MicroroentgenPerHour(850).to(MILLIROENTGEN_PER_HOUR)
    0.85 mR/h

    """
    return ExposureRate(
        to_exact(value) * MICROROENTGEN_PER_HOUR.scale, MICROROENTGEN_PER_HOUR
    )


EXPOSURE_RATE_UNITS: Mapping[str, Callable[[Numeric], ExposureRate]] = unit_table(
    "EXPOSURE_RATE_UNITS",
    {
        AMPERE_PER_KILOGRAM: _ampere_per_kilogram,
        ROENTGEN_PER_SECOND: RoentgenPerSecond,
        ROENTGEN_PER_MINUTE: RoentgenPerMinute,
        ROENTGEN_PER_HOUR: RoentgenPerHour,
        MILLIROENTGEN_PER_HOUR: MilliroentgenPerHour,
        MICROROENTGEN_PER_HOUR: MicroroentgenPerHour,
    },
)

__all__ = [
    "EXPOSURE_RATE_UNITS",
    "MICROROENTGEN_PER_HOUR",
    "MILLIROENTGEN_PER_HOUR",
    "ROENTGEN_PER_HOUR",
    "ROENTGEN_PER_MINUTE",
    "ROENTGEN_PER_SECOND",
    "MicroroentgenPerHour",
    "MilliroentgenPerHour",
    "RoentgenPerHour",
    "RoentgenPerMinute",
    "RoentgenPerSecond",
]
