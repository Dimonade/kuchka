"""Amount-of-substance constructors: the mole, from femtomoles to kilomoles.

`AmountOfSubstance` represents the amount of a chemical substance.
The module provides the mole as the canonical SI unit, with metric submultiples for
laboratory and analytical chemistry and the kilomole for large-scale chemical
engineering.

The different scales suit very different physical contexts:

* femtomoles and picomoles describe trace quantities in analytical chemistry;
* nanomoles are common for biomolecules, assay samples, and molecular biology;
* micromoles and millimoles are everyday laboratory scales for reagents and reaction
    stoichiometry;
* moles are the natural scale for ordinary chemical calculations;
* kilomoles are useful for industrial process streams and reaction engineering.

Examples
--------
Amount-of-substance values carry their chemical meaning through arithmetic.

A synthesis requires 2.0 mmol of one reagent and 750 micromol of another.
The measured additions can be combined directly even though they use different
laboratory scales:

>>> primary_reagent = Millimole(2)
>>> secondary_reagent = Micromole(750)
>>> total = primary_reagent + secondary_reagent
>>> total
2.75 mmol

Stoichiometric calculations often depend on simple whole-number ratios.
A reaction consumes three moles of reagent B for every two moles of reagent A:

>>> reagent_a = Mole(4)
>>> reagent_b = reagent_a * 3 / 2
>>> reagent_b
6 mol

Trace analysis operates many orders of magnitude below the mole.
A detector identifies 250 picomoles of an analyte in one sample and 0.3 nanomoles in
another:

>>> sample_a = Picomole(250)
>>> sample_b = Nanomole(0.3)
>>> combined = sample_a + sample_b
>>> combined
550 pmol

Large chemical processes reach the kilomole scale.
A process vessel receives 3.2 kmol of one feedstock and consumes 1.85 kmol during the
first reaction stage:

>>> feed = Kilomole(3.2)
>>> consumed = Kilomole(1.85)
>>> remaining = feed - consumed
>>> remaining
1.35 kmol

Notes
-----
The mole is the SI unit of amount of substance. Its definition fixes the Avogadro
constant at exactly 6.02214076E+23 elementary entities per mole.

Metric submultiples are exact decimal fractions of the mole:

``1 mmol = 10⁻³ mol``
``1 umol = 10⁻⁶ mol``
``1 nmol = 10⁻⁹ mol``
``1 pmol = 10⁻¹² mol``
``1 fmol = 10⁻¹⁵ mol``

The kilomole is the corresponding large-scale engineering unit:

``1 kmol = 1000 mol``

A mole may refer to atoms, molecules, ions, electrons, or another specified set of
elementary entities, and the chemical identity belongs to the surrounding application.
Multiplying an amount by the Avogadro constant gives the exact number of entities.

`AMOUNT_OF_SUBSTANCE_UNITS` maps unit symbols such as ``"mol"``, ``"mmol"``,
``"umol"``, ``"nmol"``, ``"pmol"``, ``"fmol"``, and ``"kmol"`` to their
constructors. It is intended for boundary code that receives units from
configuration files, laboratory protocols, instrument data, or other external
sources.

References
----------
BIPM, The International System of Units (SI Brochure), on the mole:
https://www.bipm.org/en/publications/si-brochure

See Also
--------
~kuchka.quantities.AmountOfSubstance
    Quantity type representing amount of substance.
~kuchka.quantities.Mass
    Mass of a sample or reagent.
~kuchka.quantities.Volume
    Volume in which a given amount of substance is dissolved or contained.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import AMOUNT_OF_SUBSTANCE
from kuchka.internal import prefixes
from kuchka.internal.prefixes import prefixed_unit
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import AmountOfSubstance

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.quantities import UnitDef
MOLE_NAME = "mole"
MOLE_SYMBOL = "mol"

FEMTOMOLE = prefixed_unit(prefixes.FEMTO, MOLE_NAME, MOLE_SYMBOL, AMOUNT_OF_SUBSTANCE)
PICOMOLE = prefixed_unit(prefixes.PICO, MOLE_NAME, MOLE_SYMBOL, AMOUNT_OF_SUBSTANCE)
NANOMOLE = prefixed_unit(prefixes.NANO, MOLE_NAME, MOLE_SYMBOL, AMOUNT_OF_SUBSTANCE)
MICROMOLE = prefixed_unit(prefixes.MICRO, MOLE_NAME, MOLE_SYMBOL, AMOUNT_OF_SUBSTANCE)
MILLIMOLE = prefixed_unit(prefixes.MILLI, MOLE_NAME, MOLE_SYMBOL, AMOUNT_OF_SUBSTANCE)
MOLE = prefixed_unit(prefixes.UNIT, MOLE_NAME, MOLE_SYMBOL, AMOUNT_OF_SUBSTANCE)
KILOMOLE = prefixed_unit(prefixes.KILO, MOLE_NAME, MOLE_SYMBOL, AMOUNT_OF_SUBSTANCE)


AmountOfSubstance._canonical_unit = MOLE  # noqa: SLF001 -- this module owns AmountOfSubstance's canonical unit


def Femtomole(value: Numeric) -> AmountOfSubstance:
    """Construct an AmountOfSubstance from a magnitude expressed in femtomoles.

    Parameters
    ----------
    value : Numeric
        Amount of substance in femtomoles.

    Returns
    -------
    AmountOfSubstance
        Amount represented in femtomoles.

    Examples
    --------
    An analytical instrument reports 18 femtomoles of a trace compound in a sample:

    >>> first_sample = Femtomole(18)
    >>> first_sample
    18 fmol

    A second sample holds 27 femtomoles, and the two together hold:

    >>> second_sample = Femtomole(27)
    >>> first_sample + second_sample
    45 fmol

    One femtomole is exactly 602 214 076 entities, from the exact Avogadro constant:

    >>> from kuchka.constants.codata_2022 import AVOGADRO_CONSTANT
    >>> Femtomole(1) * AVOGADRO_CONSTANT
    Fraction(602214076, 1)

    """
    return AmountOfSubstance(to_exact(value) * FEMTOMOLE.scale, FEMTOMOLE)


def Picomole(value: Numeric) -> AmountOfSubstance:
    """Construct an AmountOfSubstance from a magnitude expressed in picomoles.

    Parameters
    ----------
    value : Numeric
        Amount of substance in picomoles.

    Returns
    -------
    AmountOfSubstance
        Amount represented in picomoles.

    Examples
    --------
    A trace analysis finds 250 picomoles of an analyte:

    >>> primary = Picomole(250)
    >>> primary
    250 pmol

    A second fraction contributes another 0.3 nanomoles:

    >>> from kuchka import Nanomole
    >>> additional = Nanomole(0.3)
    >>> primary + additional
    550 pmol

    Dissolved in 50 microlitres, the analyte reaches a concentration of 5 µmol/L:

    >>> from kuchka import Microlitre
    >>> from kuchka.units import MICROMOLE_PER_LITRE
    >>> (primary / Microlitre(50)).to(MICROMOLE_PER_LITRE)
    5 µmol/L

    """
    return AmountOfSubstance(to_exact(value) * PICOMOLE.scale, PICOMOLE)


def Nanomole(value: Numeric) -> AmountOfSubstance:
    """Construct an AmountOfSubstance from a magnitude expressed in nanomoles.

    Parameters
    ----------
    value : Numeric
        Amount of substance in nanomoles.

    Returns
    -------
    AmountOfSubstance
        Amount represented in nanomoles.

    Examples
    --------
    A molecular biology protocol uses 120 nanomoles of primer:

    >>> stock = Nanomole(120)
    >>> stock
    120 nmol

    After transferring 35 nanomoles to a reaction, the stock contains:

    >>> transferred = Nanomole(35)
    >>> stock - transferred
    85 nmol

    A 20-base primer has a molar mass of about 6000 g/mol, so the stock weighs 720 µg:

    >>> from kuchka import GramPerMole
    >>> from kuchka.units import MICROGRAM
    >>> (stock * GramPerMole(6000)).to(MICROGRAM)
    720 µg

    """
    return AmountOfSubstance(to_exact(value) * NANOMOLE.scale, NANOMOLE)


def Micromole(value: Numeric) -> AmountOfSubstance:
    """Construct an AmountOfSubstance from a magnitude expressed in micromoles.

    Parameters
    ----------
    value : Numeric
        Amount of substance in micromoles.

    Returns
    -------
    AmountOfSubstance
        Amount represented in micromoles.

    Examples
    --------
    A reaction requires 500 micromoles of catalyst:

    >>> catalyst = Micromole(500)
    >>> catalyst
    500 µmol

    Added to 2.0 mmol of substrate, the reaction mixture holds:

    >>> from kuchka import Millimole
    >>> substrate = Millimole(2)
    >>> substrate + catalyst
    2.5 mmol

    If the catalyst were glucose, with a molar mass of 180.156 g/mol, 500 µmol would
    weigh 90.08 mg:

    >>> from decimal import Decimal
    >>> from kuchka import GramPerMole
    >>> from kuchka.units import MILLIGRAM
    >>> f"{(catalyst * GramPerMole(Decimal('180.156'))).to(MILLIGRAM):.2f}"
    '90.08 mg'

    """
    return AmountOfSubstance(to_exact(value) * MICROMOLE.scale, MICROMOLE)


def Millimole(value: Numeric) -> AmountOfSubstance:
    """Construct an AmountOfSubstance from a magnitude expressed in millimoles.

    Parameters
    ----------
    value : Numeric
        Amount of substance in millimoles.

    Returns
    -------
    AmountOfSubstance
        Amount represented in millimoles.

    Examples
    --------
    A synthesis uses 2 mmol of one reagent:

    >>> primary_reagent = Millimole(2)
    >>> primary_reagent
    2 mmol

    With 750 micromoles of another reagent, the total is:

    >>> from kuchka import Micromole
    >>> secondary_reagent = Micromole(750)
    >>> primary_reagent + secondary_reagent
    2.75 mmol

    Fasting blood glucose of 5 mmol per litre is the amount in one litre of blood:

    >>> from kuchka import Litre
    >>> from kuchka.units import MILLIMOLE_PER_LITRE
    >>> (Millimole(5) / Litre(1)).to(MILLIMOLE_PER_LITRE)
    5 mmol/L

    """
    return AmountOfSubstance(to_exact(value) * MILLIMOLE.scale, MILLIMOLE)


def Mole(value: Numeric) -> AmountOfSubstance:
    """Construct an AmountOfSubstance from a magnitude expressed in moles.

    Parameters
    ----------
    value : Numeric
        Amount of substance in moles.

    Returns
    -------
    AmountOfSubstance
        Amount represented in moles.

    Examples
    --------
    A reaction consumes three moles of reagent B for every two moles of reagent A.
    Starting with 4 mol of A therefore requires 6 mol of B:

    >>> reagent_a = Mole(4)
    >>> reagent_b = reagent_a * 3 / 2
    >>> reagent_b
    6 mol

    Eighteen grams of water, with a molar mass of 18 g/mol, are one mole:

    >>> from kuchka import Gram
    >>> from kuchka import GramPerMole
    >>> Gram(18) / GramPerMole(18)
    1 mol

    A mole holds the Avogadro number of entities:

    >>> from kuchka.constants.codata_2022 import AVOGADRO_CONSTANT
    >>> float(Mole(1) * AVOGADRO_CONSTANT)
    6.02214076e+23

    """
    return AmountOfSubstance(to_exact(value) * MOLE.scale, MOLE)


def Kilomole(value: Numeric) -> AmountOfSubstance:
    """Construct an AmountOfSubstance from a magnitude expressed in kilomoles.

    Parameters
    ----------
    value : Numeric
        Amount of substance in kilomoles.

    Returns
    -------
    AmountOfSubstance
        Amount represented in kilomoles.

    Examples
    --------
    An industrial process receives 3.2 kmol of feedstock and consumes 1.85 kmol
    during the first reaction stage:

    >>> feed = Kilomole(3.2)
    >>> consumed = Kilomole(1.85)
    >>> feed - consumed
    1.35 kmol

    Fed over one hour, the 3.2 kmol make a molar flow of about 0.89 mol/s:

    >>> from kuchka import Hour
    >>> from kuchka.units import MOLE_PER_SECOND
    >>> f"{(feed / Hour(1)).to(MOLE_PER_SECOND):.2f}"
    '0.89 mol/s'

    """
    return AmountOfSubstance(to_exact(value) * KILOMOLE.scale, KILOMOLE)


AMOUNT_OF_SUBSTANCE_UNITS: Mapping[str, Callable[[Numeric], AmountOfSubstance]] = (
    unit_table(
        "AMOUNT_OF_SUBSTANCE_UNITS",
        {
            FEMTOMOLE: Femtomole,
            PICOMOLE: Picomole,
            NANOMOLE: Nanomole,
            MICROMOLE: Micromole,
            MILLIMOLE: Millimole,
            MOLE: Mole,
            KILOMOLE: Kilomole,
        },
    )
)

AMOUNT_OF_SUBSTANCE_LADDERS: tuple[tuple[UnitDef, ...], ...] = (
    (
        FEMTOMOLE,
        PICOMOLE,
        NANOMOLE,
        MICROMOLE,
        MILLIMOLE,
        MOLE,
        KILOMOLE,
    ),
)
"""The units `auto_scale` moves an amount of substance along, smallest first."""

__all__ = [
    "AMOUNT_OF_SUBSTANCE_LADDERS",
    "AMOUNT_OF_SUBSTANCE_UNITS",
    "FEMTOMOLE",
    "KILOMOLE",
    "MICROMOLE",
    "MILLIMOLE",
    "MOLE",
    "NANOMOLE",
    "PICOMOLE",
    "Femtomole",
    "Kilomole",
    "Micromole",
    "Millimole",
    "Mole",
    "Nanomole",
    "Picomole",
]
