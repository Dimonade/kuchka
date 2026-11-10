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
The mole is the SI unit of amount of substance. Its definition fixes the
number of specified elementary entities in one mole exactly.

Metric submultiples are exact decimal fractions of the mole:

``1 mmol = 10⁻³ mol``
``1 umol = 10⁻⁶ mol``
``1 nmol = 10⁻⁹ mol``
``1 pmol = 10⁻¹² mol``
``1 fmol = 10⁻¹⁵ mol``

The kilomole is the corresponding large-scale engineering unit:

``1 kmol = 1000 mol```

Amount of substance is distinct from a simple count of objects.
A mole may refer to atoms, molecules, ions, electrons, or another specified set of
elementary entities, so the chemical identity belongs to the surrounding application
rather than to the `AmountOfSubstance` quantity itself.

`AMOUNT_OF_SUBSTANCE_UNITS` maps unit symbols such as ``"mol"``, ``"mmol"``,
``"umol"``, ``"nmol"``, ``"pmol"``, ``"fmol"``, and ``"kmol"`` to their
constructors. It is intended for boundary code that receives units from
configuration files, laboratory protocols, instrument data, or other external
sources.

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
    An analytical instrument reports 18 femtomoles of a trace compound in one sample
    and 27 femtomoles in another:

    >>> first_sample = Femtomole(18)
    >>> second_sample = Femtomole(27)
    >>> first_sample + second_sample
    45 fmol

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
    A trace analysis contains 250 picomoles of an analyte.
    A second fraction contributes another 0.3 nanomoles:

    >>> primary = Picomole(250)
    >>> additional = Nanomole(0.3)
    >>> primary + additional
    550 pmol

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
    A molecular biology protocol uses 120 nanomoles of primer.
    After transferring 35 nanomoles to a reaction, the stock contains:

    >>> stock = Nanomole(120)
    >>> transferred = Nanomole(35)
    >>> stock - transferred
    85 nmol

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
    A reaction requires 2.0 mmol of substrate and 500 micromol of catalyst:

    >>> substrate = Millimole(2)
    >>> catalyst = Micromole(500)
    >>> substrate + catalyst
    2.5 mmol

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
    A synthesis uses 2.0 mmol of one reagent and 750 micromol of another:

    >>> primary_reagent = Millimole(2)
    >>> secondary_reagent = Micromole(750)
    >>> total = primary_reagent + secondary_reagent
    >>> total
    2.75 mmol

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
    An industrial process receives 3.2 kmol of feedstock and consumes
    1.85 kmol during the first reaction stage:

    >>> feed = Kilomole(3.2)
    >>> consumed = Kilomole(1.85)
    >>> feed - consumed
    1.35 kmol

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

__all__ = [
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
