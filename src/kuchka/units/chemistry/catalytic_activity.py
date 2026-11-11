"""Catalytic activity constructors: the katal, its prefixes, and the enzyme unit.

    from kuchka import EnzymeUnit
    from kuchka import Katal
    from kuchka import Microkatal
    from kuchka import Millikatal
    from kuchka import Nanokatal
    from kuchka import parse
    from kuchka.quantities import CatalyticActivity

    assay = EnzymeUnit(180)
    pilot_reactor = Millikatal(2.5)

`Katal` is the canonical, SI-coherent unit.
One katal (kat) represents a catalytic activity of one mole converted per second.

The practical scale of catalytic activity spans several areas of enzymology and
bioprocess engineering:

* nanokatals (nkat) describe small enzyme preparations, analytical assays, and highly
    sensitive biochemical measurements;
* microkatals (µkat) are useful for laboratory enzyme preparations and routine
    biochemical assays;
* millikatals (mkat) cover larger enzyme preparations and process-scale biocatalysis;
* katals (kat) are the SI-coherent unit, particularly useful as a reference for large
    catalytic rates;
* enzyme units (U) remain common in laboratory reports and enzyme specifications,
    despite being a non-SI unit.

Examples
--------
A laboratory assay reports an enzyme preparation with an activity of 180 U under its
specified assay conditions.
Express the result in microkatals and as a molar flow rate:

>>> assay = EnzymeUnit(180)
>>> assay == Microkatal(3)
True
>>> assay.to_molar_flow_rate()
0.000003 mol/s

A microfluidic enzyme assay reports a catalytic activity of 120 nkat.
The corresponding reaction rate is 120 nmol/s:

>>> microfluidic_assay = Nanokatal(120)
>>> microfluidic_assay.to_molar_flow_rate()
0.00000012 mol/s

Laboratory reports may represent the same activity using different units.
`parse` reads the complete measurement and constructs the appropriate quantity:

>>> from kuchka import parse
>>> from kuchka import CatalyticActivity
>>> parse("180 U", CatalyticActivity) == parse("3 µkat", CatalyticActivity)
True

Notes
-----
Catalytic activity describes the rate of conversion of a specified chemical reaction in
an assay system.
Its SI-coherent unit is the katal:

``1 kat = 1 mol/s``

The enzyme unit (U) is an older, non-SI unit defined as one micromole converted per
minute under specified assay conditions:

``1 U = 1 µmol/min = 1/60 µkat = 50/3 nkat``

Consequently, one katal corresponds to exactly 60 million enzyme units.

Enzyme activity depends on the reaction and measurement procedure.
When reporting an experimental result, identify the assay procedure and indicator
reaction, as well as relevant experimental conditions.

The symbol `IU` is deliberately not accepted as an alias for `U`.
International units are also used to express the biological activity of substances such
as vitamins and hormones, and do not have one universal conversion factor.
`EnzymeUnit` represents the specific enzyme-activity convention defined above.

`CatalyticActivity` has the same physical dimension as `MolarFlowRate`, but the
quantities have distinct meanings.
Catalytic activity describes chemical conversion in a reaction system; molar flow rate
describes the transport of an amount of substance per unit time.
Use `CatalyticActivity.to_molar_flow_rate()` for the explicit conversion.

These constructors represent total catalytic activity, not catalytic activity
concentration.
Measurements such as ``U/L`` and ``kat/L`` include a volume denominator and describe a
different quantity.

`parse` reads complete measurements such as ``"180 U"`` or ``"3 µkat"``, including
registered alternative unit spellings.

`CATALYTIC_ACTIVITY_UNITS` maps supported unit symbols to their constructors.
It is useful when an application receives a unit symbol separately from its numeric
value and needs to select a constructor programmatically.

The katal was adopted by the 21st CGPM in Resolution 12 (1999):
https://www.bipm.org/en/-/resolution-cgpm-21-12

See Also
--------
~kuchka.quantities.CatalyticActivity
    Quantity type representing catalytic activity.

~kuchka.quantities.MolarFlowRate
    Molar flow rate, which shares the physical dimension of catalytic activity
    but represents a distinct quantity.

~kuchka.units.chemistry.molar_flow_rate
    Constructors for molar flow rate.

"""

from __future__ import annotations

from fractions import Fraction
from typing import TYPE_CHECKING

from kuchka.dimensions import MOLAR_FLOW_RATE
from kuchka.internal import prefixes
from kuchka.internal.prefixes import prefixed_unit
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import CatalyticActivity
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

KATAL_NAME = "katal"
KATAL_SYMBOL = "kat"

NANOKATAL = prefixed_unit(prefixes.NANO, KATAL_NAME, KATAL_SYMBOL, MOLAR_FLOW_RATE)
MICROKATAL = prefixed_unit(prefixes.MICRO, KATAL_NAME, KATAL_SYMBOL, MOLAR_FLOW_RATE)
MILLIKATAL = prefixed_unit(prefixes.MILLI, KATAL_NAME, KATAL_SYMBOL, MOLAR_FLOW_RATE)
KATAL = prefixed_unit(prefixes.UNIT, KATAL_NAME, KATAL_SYMBOL, MOLAR_FLOW_RATE)
ENZYME_UNIT = UnitDef(
    "enzyme_unit",
    "U",
    Fraction(1, 60_000_000),
    MOLAR_FLOW_RATE,
    words=("enzyme unit",),
)

CatalyticActivity._canonical_unit = KATAL  # noqa: SLF001 -- this module owns CatalyticActivity's canonical unit


def Nanokatal(value: Numeric) -> CatalyticActivity:
    """Construct a catalytic activity from a magnitude in nanokatals.

    Parameters
    ----------
    value : Numeric
        Catalytic activity magnitude in nkat.

    Returns
    -------
    CatalyticActivity
        Catalytic activity represented in nanokatals.

    Examples
    --------
    A microfluidic enzyme assay measures a substrate conversion rate of 120 nmol/s:

    >>> activity = Nanokatal(120)
    >>> activity.to_molar_flow_rate()
    0.00000012 mol/s

    """
    return CatalyticActivity(to_exact(value) * NANOKATAL.scale, NANOKATAL)


def Microkatal(value: Numeric) -> CatalyticActivity:
    """Construct a catalytic activity from a magnitude in microkatals.

    Parameters
    ----------
    value : Numeric
        Catalytic activity magnitude in µkat.

    Returns
    -------
    CatalyticActivity
        Catalytic activity represented in microkatals.

    Examples
    --------
    A purified enzyme preparation converts 0.5 µmol of substrate per second under its
    specified assay conditions:

    >>> activity = Microkatal(0.5)
    >>> activity.to_molar_flow_rate()
    0.0000005 mol/s

    """
    return CatalyticActivity(to_exact(value) * MICROKATAL.scale, MICROKATAL)


def Millikatal(value: Numeric) -> CatalyticActivity:
    """Construct a catalytic activity from a magnitude in millikatals.

    Parameters
    ----------
    value : Numeric
        Catalytic activity magnitude in mkat.

    Returns
    -------
    CatalyticActivity
        Catalytic activity represented in millikatals.

    Examples
    --------
    A process-scale bioreactor is designed to convert 2.5 mmol of substrate per second
    through an immobilized-enzyme bed:

    >>> activity = Millikatal(2.5)
    >>> activity.to_molar_flow_rate()
    0.0025 mol/s

    """
    return CatalyticActivity(to_exact(value) * MILLIKATAL.scale, MILLIKATAL)


def Katal(value: Numeric) -> CatalyticActivity:
    """Construct a catalytic activity from a magnitude in katals.

    Parameters
    ----------
    value : Numeric
        Catalytic activity magnitude in kat.

    Returns
    -------
    CatalyticActivity
        Catalytic activity represented in katals.

    Examples
    --------
    One katal represents a catalytic activity corresponding to the conversion of one
    mole of substrate per second in an assay system:

    >>> activity = Katal(1)
    >>> activity.to_molar_flow_rate()
    1 mol/s

    """
    return CatalyticActivity(to_exact(value) * KATAL.scale, KATAL)


def EnzymeUnit(value: Numeric) -> CatalyticActivity:
    """Construct a catalytic activity from a magnitude in enzyme units.

    Parameters
    ----------
    value : Numeric
        Catalytic activity magnitude in U.

    Returns
    -------
    CatalyticActivity
        Catalytic activity represented in enzyme units.

    Notes
    -----
    One enzyme unit corresponds to the conversion of one micromole of substrate per
    minute under specified assay conditions.

    Examples
    --------
    An enzyme preparation is reported to have an activity of 60 U.
    Express the same catalytic activity in the SI-prefixed unit microkatal:

    >>> EnzymeUnit(60) == Microkatal(1)
    True

    The corresponding molar flow rate is:

    >>> EnzymeUnit(60).to_molar_flow_rate()
    0.000001 mol/s

    """
    return CatalyticActivity(to_exact(value) * ENZYME_UNIT.scale, ENZYME_UNIT)


CATALYTIC_ACTIVITY_UNITS: Mapping[str, Callable[[Numeric], CatalyticActivity]] = (
    unit_table(
        "CATALYTIC_ACTIVITY_UNITS",
        {
            NANOKATAL: Nanokatal,
            MICROKATAL: Microkatal,
            MILLIKATAL: Millikatal,
            KATAL: Katal,
            ENZYME_UNIT: EnzymeUnit,
        },
    )
)

__all__ = [
    "CATALYTIC_ACTIVITY_UNITS",
    "ENZYME_UNIT",
    "KATAL",
    "MICROKATAL",
    "MILLIKATAL",
    "NANOKATAL",
    "EnzymeUnit",
    "Katal",
    "Microkatal",
    "Millikatal",
    "Nanokatal",
]
