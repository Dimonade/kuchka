"""Absorbed dose constructors: the gray, its prefixes, and the rad.

    from kuchka import Centigray, Gray, Kilogray, Rad
    from kuchka.units import CENTIGRAY, GRAY

    prescription = Gray(2)
    process_dose = Kilogray(25)
    legacy_record = Rad(350)

`Gray` is the canonical, SI-coherent unit.
Absorbed dose describes the mean energy imparted by ionizing radiation to a material,
divided by its mass.
One gray (Gy) is exactly one joule per kilogram.

The rad (rad) is the older CGS unit of absorbed dose, defined as one hundredth of a
gray:

``1 Gy = 1 J/kg = 100 rad``

The module provides gray from nano- through mega- multiples, as well as the rad and
millirad.

The practical scales cover several fields of radiation dosimetry:

* nanograys (nGy) and micrograys (µGy) describe small absorbed doses in low-dose
    irradiation studies, detector characterization, and material dosimetry;
* milligrays (mGy) are used in diagnostic imaging dosimetry, reference phantoms, and
    experimental irradiation;
* centigrays (cGy) are common in radiotherapy treatment prescriptions and treatment
    records;
* grays (Gy) are used throughout radiotherapy, radiobiology, and experimental radiation
    physics;
* kilograys (kGy) describe radiation processing, including medical-device
    sterilization, food irradiation, and polymer modification;
* megagrays (MGy) appear in high-dose materials irradiation research;
* rads and millirads (rad, mrad) remain useful when interpreting historical dosimetry
    records and older radiation-effects measurements.

Examples
--------
A radiotherapy treatment course consists of 30 fractions, each prescribing 200 cGy at
the reference point.
Calculate the accumulated absorbed dose:

>>> fraction = Centigray(200)
>>> course = fraction * 30
>>> course.to(GRAY)
60 Gy

A medical-device radiation-processing specification lists an absorbed dose of 25 kGy.
Express it in the SI unit:

>>> Kilogray(25).to(GRAY)
25000 Gy

The symbol ``rad`` has two meanings in the library: it represents both the
absorbed-dose unit and the radian, the unit of plane angle.
`parse` resolves the spelling using the requested quantity type:

>>> from kuchka import AbsorbedDose, Angle, Centigray, Radian, parse
>>> parse("1 rad", AbsorbedDose) == Centigray(1)
True
>>> parse("1 rad", Angle) == Radian(1)
True

Notes
-----
Absorbed dose, denoted by D, is the quotient of the mean energy imparted by ionizing
radiation and the mass of the irradiated material:

``D = dε̄/dm``

Its SI unit is the gray:

``1 Gy = 1 J/kg``

The rad is related to the gray by an exact conversion:

``1 rad = 0.01 Gy = 100 erg/g``

The material is part of the specification of an absorbed-dose measurement.
A dose may refer to water, soft tissue, air, silicon, or another material.
The spatial region or mass over which the dose is averaged is also part of the
measurement context.

Absorbed dose is a physical quantity of energy imparted per unit mass.
It does not incorporate radiation weighting.
Equivalent dose applies radiation weighting factors to absorbed dose averaged over a
specified organ or tissue:

``H_T = Σ_R w_R D_T,R``

Consequently, equal absorbed doses from different radiation types can correspond to
different equivalent doses.
The explicit conversion is provided by `EquivalentDose.from_absorbed_dose()`.

Absorbed dose is distinct from exposure.
Exposure describes ionization charge produced per unit mass of air by X-rays and gamma
radiation.
The gray and roentgen therefore represent different physical quantities, despite both
appearing in radiation measurement records.

The symbol ``rad`` is also the symbol for the radian.
The two units belong to different quantity types and separate unit tables.
`parse` uses its explicit quantity argument to resolve the intended meaning.

`parse` reads complete measurements such as ``"2 Gy"``, ``"200 cGy"``, ``"25 kGy"``,
and ``"350 rad"``.
The quantity type determines which unit table is consulted.

`ABSORBED_DOSE_UNITS` maps symbols such as ``"nGy"``, ``"µGy"``, ``"mGy"``, ``"cGy"``,
``"Gy"``, ``"kGy"``, ``"MGy"``, ``"rad"``, and ``"mrad"`` to their constructors.
It is intended for boundary code that receives a numeric magnitude and a separate unit
symbol from an external source.

The gray was adopted as the SI unit of absorbed dose by the
15th CGPM in Resolution 9 (1975):
https://www.bipm.org/en/-/resolution-cgpm-15-9

For the definition and use of absorbed dose and equivalent dose, see
ICRP Publication 144:
https://doi.org/10.1177/0146645320906277

See Also
--------
~kuchka.quantities.AbsorbedDose
    Quantity type representing absorbed dose.

~kuchka.quantities.AbsorbedDoseRate
    Absorbed dose delivered per unit time.

~kuchka.quantities.EquivalentDose
    Radiation-weighted absorbed dose.

~kuchka.quantities.EquivalentDoseRate
    Equivalent dose delivered per unit time.

~kuchka.quantities.Exposure
    Ionization charge produced per unit mass of air.

~kuchka.quantities.Angle
    Plane angle, whose radian unit shares the symbol ``rad``.

~kuchka.units.radiation.absorbed_dose_rate
    Constructors for absorbed dose rate.

~kuchka.units.radiation.equivalent_dose
    Constructors for equivalent dose.

"""

from __future__ import annotations

from fractions import Fraction
from typing import TYPE_CHECKING

from kuchka.dimensions import SPECIFIC_ENERGY
from kuchka.internal import prefixes
from kuchka.internal.prefixes import with_prefix
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import AbsorbedDose
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

GRAY = UnitDef("gray", "Gy", 1, SPECIFIC_ENERGY)
NANOGRAY = with_prefix(prefixes.NANO, GRAY)
MICROGRAY = with_prefix(prefixes.MICRO, GRAY)
MILLIGRAY = with_prefix(prefixes.MILLI, GRAY)
CENTIGRAY = with_prefix(prefixes.CENTI, GRAY)
KILOGRAY = with_prefix(prefixes.KILO, GRAY)
MEGAGRAY = with_prefix(prefixes.MEGA, GRAY)
RAD = UnitDef("rad", "rad", Fraction(1, 100), SPECIFIC_ENERGY)
MILLIRAD = with_prefix(prefixes.MILLI, RAD)

AbsorbedDose._canonical_unit = GRAY  # noqa: SLF001 -- this module owns AbsorbedDose's canonical unit


def Gray(value: Numeric) -> AbsorbedDose:
    """Construct an AbsorbedDose from a magnitude in grays.

    Parameters
    ----------
    value : Numeric
        Magnitude in Gy.

    Returns
    -------
    AbsorbedDose
        AbsorbedDose represented in grays.

    Examples
    --------
    A radiotherapy plan specifies an absorbed dose of 2 Gy at a reference point:

    >>> prescription = Gray(2)
    >>> prescription
    2 Gy

    Two radiation beams contribute 1.2 Gy and 0.8 Gy to the same point in a treatment
    volume.
    Calculate their combined dose:

    >>> first_beam = Gray(1.2)
    >>> second_beam = Gray(0.8)
    >>> (first_beam + second_beam).to(GRAY)
    2 Gy

    """
    return AbsorbedDose(to_exact(value) * GRAY.scale, GRAY)


def Nanogray(value: Numeric) -> AbsorbedDose:
    """Construct an AbsorbedDose from a magnitude in nanograys.

    Parameters
    ----------
    value : Numeric
        Magnitude in nGy.

    Returns
    -------
    AbsorbedDose
        AbsorbedDose represented in nanograys.

    Examples
    --------
    A silicon test coupon in a low-dose irradiation experiment records an absorbed dose
    increment of 750 nGy:

    >>> reading = Nanogray(750)
    >>> reading
    750 nGy

    A dosimetry instrument exports the same measurement as text.
    Read the complete measurement:

    >>> from kuchka import AbsorbedDose, parse
    >>> parse("750 nGy", AbsorbedDose) == reading
    True

    """
    return AbsorbedDose(to_exact(value) * NANOGRAY.scale, NANOGRAY)


def Microgray(value: Numeric) -> AbsorbedDose:
    """Construct an AbsorbedDose from a magnitude in micrograys.

    Parameters
    ----------
    value : Numeric
        Magnitude in µGy.

    Returns
    -------
    AbsorbedDose
        AbsorbedDose represented in micrograys.

    Examples
    --------
    A low-dose photon irradiation study records an absorbed dose of 12 µGy in a
    reference specimen:

    >>> reading = Microgray(12)
    >>> reading
    12 µGy

    Express the same measurement in nanograys:

    >>> reading.to(NANOGRAY)
    12000 nGy

    """
    return AbsorbedDose(to_exact(value) * MICROGRAY.scale, MICROGRAY)


def Milligray(value: Numeric) -> AbsorbedDose:
    """Construct an AbsorbedDose from a magnitude in milligrays.

    Parameters
    ----------
    value : Numeric
        Magnitude in mGy.

    Returns
    -------
    AbsorbedDose
        AbsorbedDose represented in milligrays.

    Examples
    --------
    A tissue-equivalent phantom records an absorbed dose of 0.45 mGy at a reference
    point during an imaging acquisition:

    >>> reading = Milligray(Fraction(45, 100))
    >>> reading
    0.45 mGy

    Two acquisitions contribute 0.35 mGy and 0.45 mGy at the same reference point.
    Calculate the accumulated absorbed dose:

    >>> first = Milligray(Fraction(7, 20))
    >>> second = Milligray(Fraction(9, 20))
    >>> (first + second).to(MILLIGRAY)
    0.8 mGy

    """
    return AbsorbedDose(to_exact(value) * MILLIGRAY.scale, MILLIGRAY)


def Centigray(value: Numeric) -> AbsorbedDose:
    """Construct an AbsorbedDose from a magnitude in centigrays.

    Parameters
    ----------
    value : Numeric
        Magnitude in cGy.

    Returns
    -------
    AbsorbedDose
        AbsorbedDose represented in centigrays.

    Examples
    --------
    A radiotherapy treatment plan specifies 200 cGy per fraction:

    >>> fraction = Centigray(200)
    >>> fraction
    200 cGy

    The prescribed course contains 30 identical fractions.
    Calculate the total absorbed dose at the reference point:

    >>> course = fraction * 30
    >>> course.to(GRAY)
    60 Gy

    """
    return AbsorbedDose(to_exact(value) * CENTIGRAY.scale, CENTIGRAY)


def Kilogray(value: Numeric) -> AbsorbedDose:
    """Construct an AbsorbedDose from a magnitude in kilograys.

    Parameters
    ----------
    value : Numeric
        Magnitude in kGy.

    Returns
    -------
    AbsorbedDose
        AbsorbedDose represented in kilograys.

    Examples
    --------
    A medical-device radiation-sterilization specification lists an absorbed dose of
    25 kGy:

    >>> process_dose = Kilogray(25)
    >>> process_dose
    25 kGy

    Express the process dose in grays:

    >>> process_dose.to(GRAY)
    25000 Gy

    """
    return AbsorbedDose(to_exact(value) * KILOGRAY.scale, KILOGRAY)


def Megagray(value: Numeric) -> AbsorbedDose:
    """Construct an AbsorbedDose from a magnitude in megagrays.

    Parameters
    ----------
    value : Numeric
        Magnitude in MGy.

    Returns
    -------
    AbsorbedDose
        AbsorbedDose represented in megagrays.

    Examples
    --------
    A high-dose materials-irradiation study reports a cumulative absorbed dose of 1 MGy
    for a polymer specimen:

    >>> specimen_dose = Megagray(1)
    >>> specimen_dose
    1 MGy

    Express the accumulated dose in kilograys:

    >>> specimen_dose.to(KILOGRAY)
    1000 kGy

    """
    return AbsorbedDose(to_exact(value) * MEGAGRAY.scale, MEGAGRAY)


def Rad(value: Numeric) -> AbsorbedDose:
    """Construct an AbsorbedDose from a magnitude in rads.

    Parameters
    ----------
    value : Numeric
        Magnitude in rad.

    Returns
    -------
    AbsorbedDose
        AbsorbedDose represented in rads.

    Examples
    --------
    A historical radiation-effects report records an absorbed dose of 350 rad in a
    silicon device:

    >>> reading = Rad(350)
    >>> reading
    350 rad

    The same symbol is also used for radians.
    The parser resolves the meaning from the requested quantity type:

    >>> from kuchka import AbsorbedDose, Angle, Radian, parse
    >>> parse("1 rad", AbsorbedDose) == Rad(1)
    True
    >>> parse("1 rad", Angle) == Radian(1)
    True

    """
    return AbsorbedDose(to_exact(value) * RAD.scale, RAD)


def Millirad(value: Numeric) -> AbsorbedDose:
    """Construct an AbsorbedDose from a magnitude in millirads.

    Parameters
    ----------
    value : Numeric
        Magnitude in mrad.

    Returns
    -------
    AbsorbedDose
        AbsorbedDose represented in millirads.

    Examples
    --------
    A legacy semiconductor irradiation record lists an absorbed dose of 250 mrad for
    one exposure stage:

    >>> reading = Millirad(250)
    >>> reading
    250 mrad

    A subsequent irradiation stage contributes another 750 mrad.
    Calculate the accumulated dose in rads:

    >>> accumulated = reading + Millirad(750)
    >>> accumulated.to(RAD)
    1 rad

    """
    return AbsorbedDose(to_exact(value) * MILLIRAD.scale, MILLIRAD)


ABSORBED_DOSE_UNITS: Mapping[str, Callable[[Numeric], AbsorbedDose]] = unit_table(
    "ABSORBED_DOSE_UNITS",
    {
        GRAY: Gray,
        NANOGRAY: Nanogray,
        MICROGRAY: Microgray,
        MILLIGRAY: Milligray,
        CENTIGRAY: Centigray,
        KILOGRAY: Kilogray,
        MEGAGRAY: Megagray,
        RAD: Rad,
        MILLIRAD: Millirad,
    },
)

__all__ = [
    "ABSORBED_DOSE_UNITS",
    "CENTIGRAY",
    "GRAY",
    "KILOGRAY",
    "MEGAGRAY",
    "MICROGRAY",
    "MILLIGRAY",
    "MILLIRAD",
    "NANOGRAY",
    "RAD",
    "Centigray",
    "Gray",
    "Kilogray",
    "Megagray",
    "Microgray",
    "Milligray",
    "Millirad",
    "Nanogray",
    "Rad",
]
