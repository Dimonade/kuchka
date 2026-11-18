"""Activity constructors: the becquerel, the curie, and their prefixes.

    from kuchka import Becquerel
    from kuchka import Curie
    from kuchka import Megabecquerel
    from kuchka import Millicurie

`Activity` counts nuclear transformations per second.
Its SI unit is the becquerel (`Bq`), exactly one transformation per second.
The curie (`Ci`) is the older unit, defined exactly as 37,000,000,000 becquerels.

The module provides the becquerel from milli- through tera- multiples, and the curie in
milli-, micro-, nano-, and pico-multiples.
These are units of total activity:
they are not units of activity concentration, absorbed dose, or biological risk.

Examples
--------
Potassium-40 occurs naturally in the human body.
A commonly cited estimate for a 70 kg adult is about 4,000 Bq of potassium-40 activity:

>>> body_potassium = Becquerel(4000)
>>> body_potassium.to(KILOBECQUEREL)
4 kBq

The U.S. Government Accountability Office's review of the Three Mile Island accident
reported estimates of 2.4 to 13 million curies of noble gases released to the
atmosphere, mainly xenon-133.
Convert the lower end of that historical estimate to the largest SI multiple defined
here:

>>> tmi_noble_gases = Curie(2_400_000)
>>> tmi_noble_gases.to(TERABECQUEREL)
88800 TBq

The same report gives about 15 Ci of iodine-131.
This is a separate radionuclide release estimate, not a dose to a person:

>>> Curie(15).to(GIGABECQUEREL)
555 GBq

For contrast, the Austrian adult diagnostic reference table lists 650 MBq for skeletal
scintigraphy using technetium-99m bisphosphonates.
A reference value is not an individual prescription:

>>> skeletal_scan_reference = Megabecquerel(650)
>>> skeletal_scan_reference.to(GIGABECQUEREL)
0.65 GBq

A science-fiction example for an activity on a scale more often associated with large
industrial or reactor inventories: the fictional survey ship *Alfredo the Reddo* logs
2.4 TBq in a captured sample of reactor-activation products.
This is an invented setting and value, not a claim about a real reactor or release:

>>> captured_sample = Terabecquerel(2.4)
>>> captured_sample.to(GIGABECQUEREL)
2400 GBq

Historical context
------------------
Published source-term estimates for the Chernobyl accident include about 1,760 PBq of
iodine-131 and 85 PBq of caesium-137 released.
For Fukushima Daiichi, the UNSCEAR 2013 review found published estimates around
100-500 PBq for iodine-131 and 6-20 PBq for caesium-137.
Those Fukushima estimates were not strictly comparable: studies differed in their
methods and in what periods or fractions of the releases they counted.
These are isotope-specific estimates of activity released during the accidents, not
present-day activities at the sites, personal doses, or direct measures of health
effects.

Notes
-----
Activity is distinct from absorbed dose and effective dose.
The radionuclide, its radiation emissions, exposure pathway, distance, shielding,
biological uptake, and time all matter when estimating dose or health effects.
Do not infer a person's exposure from a release activity alone.

`Activity` has the same physical dimension as frequency, but it remains a distinct
quantity type.
To request an explicit conversion to ordinary frequency, use `Activity.to_frequency()`.

`ACTIVITY_UNITS` maps symbols such as ``"Bq"``, ``"kBq"``, ``"MBq"``, ``"Ci"``,
``"mCi"``, ``"uCi"``, and ``"pCi"`` to their constructors for boundary code that
reads unit labels from external data.

References
----------
* U.S. Government Accountability Office, *Three Mile Island: The Most Studied Nuclear
  Accident in History* (1980), pp. 5-6:
  https://www.gao.gov/assets/emd-80-109.pdf
* OECD Nuclear Energy Agency, *Chernobyl: Assessment of Radiological and Health
  Impact*, chapter II:
  https://www.oecd-nea.org/rp/chernobyl/c02
* UNSCEAR, *2013 Report*, Fukushima release estimates, paragraphs 43 onward:
  https://www.env.go.jp/content/900411726.pdf
* U.S. Department of Health and Human Services / ATSDR, potassium-40 activity
  in the body, as reproduced in PubChem:
  https://pubchem.ncbi.nlm.nih.gov/compound/Potassium_-radioactive
* Austrian *Medizinische Strahlenschutzverordnung*, Anlage 1, diagnostic
  reference values for nuclear-medicine procedures:
  https://ris.bka.gv.at/NormDokument.wxe?Abfrage=Bundesnormen&Anlage=1&Artikel=&FassungVom=2026-04-19&Gesetzesnummer=20010088&Paragraf=&Uebergangsrecht=

See Also
--------
~kuchka.quantities.Activity
    Quantity type representing radioactive activity.
~kuchka.quantities.Frequency
    Quantity type representing frequency.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import FREQUENCY
from kuchka.internal import prefixes
from kuchka.internal.prefixes import with_prefix
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import Activity
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

BECQUEREL = UnitDef("becquerel", "Bq", 1, FREQUENCY)
CURIE = UnitDef("curie", "Ci", 37_000_000_000, FREQUENCY)
MILLIBECQUEREL = with_prefix(prefixes.MILLI, BECQUEREL)
KILOBECQUEREL = with_prefix(prefixes.KILO, BECQUEREL)
MEGABECQUEREL = with_prefix(prefixes.MEGA, BECQUEREL)
GIGABECQUEREL = with_prefix(prefixes.GIGA, BECQUEREL)
TERABECQUEREL = with_prefix(prefixes.TERA, BECQUEREL)
MILLICURIE = with_prefix(prefixes.MILLI, CURIE)
MICROCURIE = with_prefix(prefixes.MICRO, CURIE)
NANOCURIE = with_prefix(prefixes.NANO, CURIE)
PICOCURIE = with_prefix(prefixes.PICO, CURIE)

Activity._canonical_unit = BECQUEREL  # noqa: SLF001 -- this module owns Activity's canonical unit


def Becquerel(value: Numeric) -> Activity:
    """Construct an Activity from a magnitude expressed in becquerels.

    Parameters
    ----------
    value : Numeric
        Activity in becquerels.

    Returns
    -------
    Activity
        Activity represented in becquerels.

    Examples
    --------
    A commonly cited estimate for potassium-40 in a 70 kg adult is about 4,000 Bq.
    Express that total activity in kilobecquerels:

    >>> body_potassium = Becquerel(4000)
    >>> body_potassium.to(KILOBECQUEREL)
    4 kBq

    """
    return Activity(to_exact(value) * BECQUEREL.scale, BECQUEREL)


def Millibecquerel(value: Numeric) -> Activity:
    """Construct an Activity from a magnitude expressed in millibecquerels.

    Parameters
    ----------
    value : Numeric
        Activity in millibecquerels.

    Returns
    -------
    Activity
        Activity represented in millibecquerels.

    Examples
    --------
    A hypothetical low-background lab reports 25 mBq of total activity in a sample
    blank.
    Convert it to the canonical unit before storing the result:

    >>> sample_blank = Millibecquerel(25)
    >>> sample_blank.to(BECQUEREL)
    0.025 Bq

    """
    return Activity(to_exact(value) * MILLIBECQUEREL.scale, MILLIBECQUEREL)


def Kilobecquerel(value: Numeric) -> Activity:
    """Construct an Activity from a magnitude expressed in kilobecquerels.

    Parameters
    ----------
    value : Numeric
        Activity in kilobecquerels.

    Returns
    -------
    Activity
        Activity represented in kilobecquerels.

    Examples
    --------
    A lab assays two portions from the same batch at 12 kBq and 8 kBq.
    If the portions are combined, their total activity is the sum of both measurements:

    >>> filter_activity = Kilobecquerel(12)
    >>> dust_activity = Kilobecquerel(8)
    >>> (filter_activity + dust_activity).to(KILOBECQUEREL)
    20 kBq

    """
    return Activity(to_exact(value) * KILOBECQUEREL.scale, KILOBECQUEREL)


def Megabecquerel(value: Numeric) -> Activity:
    """Construct an Activity from a magnitude expressed in megabecquerels.

    Parameters
    ----------
    value : Numeric
        Activity in megabecquerels.

    Returns
    -------
    Activity
        Activity represented in megabecquerels.

    Examples
    --------
    Austria's adult diagnostic reference table lists 650 MBq for skeletal scintigraphy
    using technetium-99m bisphosphonates.
    The reference value is for standardized diagnostic practice, not a prescription
    for every patient:

    >>> skeletal_scan_reference = Megabecquerel(650)
    >>> skeletal_scan_reference.to(GIGABECQUEREL)
    0.65 GBq

    """
    return Activity(to_exact(value) * MEGABECQUEREL.scale, MEGABECQUEREL)


def Gigabecquerel(value: Numeric) -> Activity:
    """Construct an Activity from a magnitude expressed in gigabecquerels.

    Parameters
    ----------
    value : Numeric
        Activity in gigabecquerels.

    Returns
    -------
    Activity
        Activity represented in gigabecquerels.

    Examples
    --------
    A historical U.S. Government Accountability Office review reported about 15 Ci of
    iodine-131 released during the Three Mile Island accident.
    That estimate corresponds to 555 GBq:

    >>> iodine_release = Gigabecquerel(555)
    >>> iodine_release.to(CURIE)
    15 Ci

    """
    return Activity(to_exact(value) * GIGABECQUEREL.scale, GIGABECQUEREL)


def Terabecquerel(value: Numeric) -> Activity:
    """Construct an Activity from a magnitude expressed in terabecquerels.

    Parameters
    ----------
    value : Numeric
        Activity in terabecquerels.

    Returns
    -------
    Activity
        Activity represented in terabecquerels.

    Examples
    --------
    In a clearly fictional science-fiction scenario, the survey ship
    *Alfredo the Reddo* logs 2.4 TBq of activity in a captured sample of
    reactor-activation products.
    This is an invented setting and value, not a real-world source estimate:

    >>> captured_sample = Terabecquerel(2.4)
    >>> captured_sample.to(GIGABECQUEREL)
    2400 GBq

    """
    return Activity(to_exact(value) * TERABECQUEREL.scale, TERABECQUEREL)


def Curie(value: Numeric) -> Activity:
    """Construct an Activity from a magnitude expressed in curies.

    Parameters
    ----------
    value : Numeric
        Activity in curies.

    Returns
    -------
    Activity
        Activity represented in curies.

    Examples
    --------
    The 1980 U.S. Government Accountability Office review reported a range of 2.4 to
    13 million Ci for noble gases released during the Three Mile Island accident.
    Converting the lower-end estimate gives:

    >>> lower_estimate = Curie(2_400_000)
    >>> lower_estimate.to(TERABECQUEREL)
    88800 TBq

    """
    return Activity(to_exact(value) * CURIE.scale, CURIE)


def Millicurie(value: Numeric) -> Activity:
    """Construct an Activity from a magnitude expressed in millicuries.

    Parameters
    ----------
    value : Numeric
        Activity in millicuries.

    Returns
    -------
    Activity
        Activity represented in millicuries.

    Examples
    --------
    A radiation-instrument calibration certificate lists a source as 1 mCi.
    Convert the label to the SI activity unit commonly used in lab records:

    >>> calibration_source = Millicurie(1)
    >>> calibration_source.to(MEGABECQUEREL)
    37 MBq

    """
    return Activity(to_exact(value) * MILLICURIE.scale, MILLICURIE)


def Microcurie(value: Numeric) -> Activity:
    """Construct an Activity from a magnitude expressed in microcuries.

    Parameters
    ----------
    value : Numeric
        Activity in microcuries.

    Returns
    -------
    Activity
        Activity represented in microcuries.

    Examples
    --------
    The natural potassium-40 activity often estimated for a 70 kg adult is about
    4,000 Bq, or roughly 0.108 microcurie.
    Format the converted value to three decimal places for a comparison with an older
    instrument log:

    >>> f"{Becquerel(4000).to(MICROCURIE):.3f}"
    '0.108 µCi'

    """
    return Activity(to_exact(value) * MICROCURIE.scale, MICROCURIE)


def Nanocurie(value: Numeric) -> Activity:
    """Construct an Activity from a magnitude expressed in nanocuries.

    Parameters
    ----------
    value : Numeric
        Activity in nanocuries.

    Returns
    -------
    Activity
        Activity represented in nanocuries.

    Examples
    --------
    Check sources for counting equipment are sold in nanocurie and microcurie
    strengths.
    A 5 nCi source decays 185 times a second:

    >>> check_source = Nanocurie(5)
    >>> check_source.to(BECQUEREL)
    185 Bq

    A thousand nanocuries are a microcurie:

    >>> Nanocurie(1000) == Microcurie(1)
    True

    """
    return Activity(to_exact(value) * NANOCURIE.scale, NANOCURIE)


def Picocurie(value: Numeric) -> Activity:
    """Construct an Activity from a magnitude expressed in picocuries.

    Parameters
    ----------
    value : Numeric
        Activity in picocuries.

    Returns
    -------
    Activity
        Activity represented in picocuries.

    Examples
    --------
    A measurement record can express a tiny total activity as 4 pCi:

    >>> sample_activity = Picocurie(4)
    >>> sample_activity.to(BECQUEREL)
    0.148 Bq

    Note that a radon reading in pCi/L is an activity concentration, not a total
    activity.
    This constructor represents pCi only; it cannot by itself represent the volume
    denominator in pCi/L.

    """
    return Activity(to_exact(value) * PICOCURIE.scale, PICOCURIE)


ACTIVITY_UNITS: Mapping[str, Callable[[Numeric], Activity]] = unit_table(
    "ACTIVITY_UNITS",
    {
        BECQUEREL: Becquerel,
        MILLIBECQUEREL: Millibecquerel,
        KILOBECQUEREL: Kilobecquerel,
        MEGABECQUEREL: Megabecquerel,
        GIGABECQUEREL: Gigabecquerel,
        TERABECQUEREL: Terabecquerel,
        CURIE: Curie,
        MILLICURIE: Millicurie,
        MICROCURIE: Microcurie,
        NANOCURIE: Nanocurie,
        PICOCURIE: Picocurie,
    },
)

__all__ = [
    "ACTIVITY_UNITS",
    "BECQUEREL",
    "CURIE",
    "GIGABECQUEREL",
    "KILOBECQUEREL",
    "MEGABECQUEREL",
    "MICROCURIE",
    "MILLIBECQUEREL",
    "MILLICURIE",
    "NANOCURIE",
    "PICOCURIE",
    "TERABECQUEREL",
    "Becquerel",
    "Curie",
    "Gigabecquerel",
    "Kilobecquerel",
    "Megabecquerel",
    "Microcurie",
    "Millibecquerel",
    "Millicurie",
    "Nanocurie",
    "Picocurie",
    "Terabecquerel",
]
