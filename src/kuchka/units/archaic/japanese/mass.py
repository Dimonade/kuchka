"""Japanese shakkan-hō units of mass.

The shakkan-hō (尺貫法) is the traditional Japanese system of measurement.
Its mass scale is based on the kan (貫), which was fixed by statute in 1891
at exactly 3.75 kilograms.

The units in this module use exact decimal scales. They construct ordinary
`Mass` quantities, allowing traditional Japanese mass measurements to take
part in the same arithmetic as grams and kilograms.

Mass
----

=============  ===========  ============  =================  =========
Unit           Romanised    Kanji         Relationship       SI value
=============  ===========  ============  =================  =========
`Mo`           Mō           毛, 毫         1/1,000,000 kan    3.75 mg
`Rin`          Rin          厘             1/100,000 kan      37.5 mg
`Fun`          Fun          分             1/10,000 kan       375 mg
`Monme`        Monme        匁             1/1,000 kan        3.75 g
`Hyakume`      Hyakume      百目           1/10 kan           375 g
`Kin`          Kin          斤             4/25 kan           600 g
`Kan`          Kan(me)      貫, 貫目       1 kan              3.75 kg
`Maru`         Maru         丸             8 kan              30 kg
`Tan`          Tan          担, 擔         16 kan             60 kg
=============  ===========  ============  =================  =========

Monme is familiar from traditional weighing practices, including the
Japanese pearl trade. Kin and kan provide larger scales for weighing
goods and materials.

Examples
--------
A pearl-trading workshop near Toba prepares a consignment weighing
80 monme. The pearls are divided evenly among four trays for sorting:

>>> from kuchka.units.mass import GRAM
>>> consignment = Monme(80)
>>> tray_mass = (consignment / 4).to(GRAM)
>>> tray_mass
75 g

A Kyoto confectionery workshop prepares five kin of azuki beans for
a seasonal batch of anko. The stock is divided into six equal portions:

>>> bean_stock = Kin(5)
>>> batch_mass = (bean_stock / 6).to(GRAM)
>>> batch_mass
500 g

A foundry preparing bronze fittings for a temple restoration records
its available metal in kan. Eight kan divided among four casting batches
gives each batch a mass of:

>>> bronze_stock = Kan(8)
>>> casting_mass = (bronze_stock / 4).to(KILOGRAM)
>>> casting_mass
7.5 kg

Notes
-----
The principal standardized definitions are:

``1 monme = 3.75 g``
``1 kin = 160 monme = 600 g``
``1 kan = 1000 monme = 3.75 kg``

These definitions represent the selected standardized system, not every
historical or regional convention. In particular, the modern metric
equivalences should not be applied uncritically to records made before
standardization.

`JAPANESE_MASS_UNITS` maps each unit symbol, such as ``"monme"`` or
``"kan"``, to its constructor. It is intended for boundary code that reads
measurements from configuration files, inventories, catalogues, or other
external sources.

For historical background, see:
https://en.wikipedia.org/wiki/Japanese_units_of_measurement

See Also
--------
~kuchka.quantities.Mass
    Quantity type representing mass.
~kuchka.quantities.Density
    Mass per unit volume.
~kuchka.units.mass
    Modern metric and selected non-SI mass constructors.
"""

from __future__ import annotations

from decimal import Decimal
from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import MASS
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Mass
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping


MO = UnitDef(
    "mo",
    "mo",
    KAN.scale / Decimal(1_000_000),
    MASS,
    aliases=("毛", "毫", "mō"),
)
RIN = UnitDef(
    "rin",
    "rin",
    KAN.scale / Decimal(100_000),
    MASS,
    aliases=("厘",),
)
FUN = UnitDef(
    "fun",
    "fun",
    KAN.scale / Decimal(10_000),
    MASS,
    aliases=("分",),
)
MONME = UnitDef(
    "monme",
    "monme",
    Decimal("0.00375"),
    MASS,
    aliases=("匁", "momme"),
)
HYAKUME = UnitDef(
    "hyakume",
    "hyakume",
    KAN.scale / Decimal(10),
    MASS,
    aliases=("百目",),
)
KIN = UnitDef("kin", "kin", 160 * MONME.scale, MASS, aliases=("斤",))
KAN = UnitDef(
    "kan",
    "kan",
    1000 * MONME.scale,
    MASS,
    aliases=("貫", "貫目", "kanme"),
)
MARU = UnitDef("maru", "maru", 8 * KAN.scale, MASS, aliases=("丸",))
TAN = UnitDef("tan", "tan", 16 * KAN.scale, MASS, aliases=("担", "擔"))

# TODO: MONME can be aliased to MOMME?
# TODO: KAN and KANME?


def Mo(value: Numeric) -> Mass:
    """Construct mass from a magnitude expressed in mō.

    Parameters
    ----------
    value : Numeric
        Mass magnitude in mō.

    Returns
    -------
    Mass
        Mass represented in mō.

    Notes
    -----
    One mō is 1/1,000,000 kan, or exactly 3.75 milligrams.

    Examples
    --------
    A Kyoto metalworker preparing fine gold details for a lacquer repair weighs an
    amount of gold foil equivalent to 800 mō:

    >>> from kuchka.units.mass import GRAM
    >>> gold_foil = Mo(800)
    >>> gold_foil.to(GRAM)
    3 g
    """
    return Mass(to_exact(value) * MO.scale, MO)


def Rin(value: Numeric) -> Mass:
    """Construct mass from a magnitude expressed in rin.

    Parameters
    ----------
    value : Numeric
        Mass magnitude in rin.

    Returns
    -------
    Mass
        Mass represented in rin.

    Notes
    -----
    One rin is 1/100,000 kan, or exactly 37.5 milligrams.

    Examples
    --------
    A small ingredient sample prepared by a traditional Japanese apothecary weighs
    eight rin:

    >>> from kuchka.units.mass import GRAM
    >>> sample = Rin(8)
    >>> sample.to(GRAM)
    0.3 g
    """
    return Mass(to_exact(value) * RIN.scale, RIN)


def Fun(value: Numeric) -> Mass:
    """Construct mass from a magnitude expressed in fun.

    Parameters
    ----------
    value : Numeric
        Mass magnitude in fun.

    Returns
    -------
    Mass
        Mass represented in fun.

    Notes
    -----
    One fun is 1/10,000 kan, or exactly 375 milligrams.

    Examples
    --------
    A medicine prepared in a Meiji-era Japanese pharmacy is weighed out as eight fun,
    giving a three-gram quantity:

    >>> from kuchka.units.mass import GRAM
    >>> preparation = Fun(8)
    >>> preparation.to(GRAM)
    3 g
    """
    return Mass(to_exact(value) * FUN.scale, FUN)


def Monme(value: Numeric) -> Mass:
    """Construct mass from a magnitude expressed in monme.

    Parameters
    ----------
    value : Numeric
        Mass magnitude in monme.

    Returns
    -------
    Mass
        Mass represented in monme.

    Notes
    -----
    One monme is exactly 3.75 g under the standardized definition.

    Examples
    --------
    A pearl-trading workshop prepares an 80-monme consignment for sorting.
    Dividing it into four equal trays gives each tray a mass of 75 g:

    >>> from kuchka.units.mass import GRAM
    >>> consignment = Monme(80)
    >>> (consignment / 4).to(GRAM)
    75 g
    """
    return Mass(to_exact(value) * MONME.scale, MONME)


def Hyakume(value: Numeric) -> Mass:
    """Construct mass from a magnitude expressed in hyakume.

    Parameters
    ----------
    value : Numeric
        Mass magnitude in hyakume.

    Returns
    -------
    Mass
        Mass represented in hyakume.

    Notes
    -----
    One hyakume is 1/10 kan, or exactly 375 grams.

    Examples
    --------
    A merchant preparing a shipment of traditional Japanese goods divides one hyakume
    of material equally between three packages:

    >>> from kuchka.units.mass import GRAM
    >>> shipment = Hyakume(1)
    >>> package_mass = (shipment / 3).to(GRAM)
    >>> package_mass
    125 g
    """
    return Mass(to_exact(value) * HYAKUME.scale, HYAKUME)


def Kin(value: Numeric) -> Mass:
    """Construct mass from a magnitude expressed in kin.

    Parameters
    ----------
    value : Numeric
        Mass magnitude in kin.

    Returns
    -------
    Mass
        Mass represented in kin.

    Notes
    -----
    One kin is 160 monme, or exactly 600 g.

    Examples
    --------
    A Kyoto confectionery workshop prepares five kin of azuki beans for a seasonal
    batch of anko, then portions the stock into six equal batches:

    >>> from kuchka.units.mass import GRAM
    >>> bean_stock = Kin(5)
    >>> batch_mass = (bean_stock / 6).to(GRAM)
    >>> batch_mass
    500 g
    """
    return Mass(to_exact(value) * KIN.scale, KIN)


def Kan(value: Numeric) -> Mass:
    """Construct mass from a magnitude expressed in kan.

    Parameters
    ----------
    value : Numeric
        Mass magnitude in kan.

    Returns
    -------
    Mass
        Mass represented in kan.

    Notes
    -----
    One kan is 1000 monme, or exactly 3.75 kg.

    Examples
    --------
    A foundry preparing bronze fittings for a temple restoration records eight kan of
    metal.
    Dividing the stock between four casting batches gives each batch a mass of 7.5 kg:

    >>> from kuchka.units.mass import KILOGRAM
    >>> bronze_stock = Kan(8)
    >>> casting_mass = (bronze_stock / 4).to(KILOGRAM)
    >>> casting_mass
    7.5 kg
    """
    return Mass(to_exact(value) * KAN.scale, KAN)


def Maru(value: Numeric) -> Mass:
    """Construct mass from a magnitude expressed in maru.

    Parameters
    ----------
    value : Numeric
        Mass magnitude in maru.

    Returns
    -------
    Mass
        Mass represented in maru.

    Notes
    -----
    One maru is eight kan, or exactly 30 kilograms.

    Examples
    --------
    A traditional goods depot records three maru of material, divided evenly between
    six storage loads:

    >>> from kuchka.units.mass import KILOGRAM
    >>> inventory = Maru(3)
    >>> load_mass = (inventory / 6).to(KILOGRAM)
    >>> load_mass
    15 kg
    """
    return Mass(to_exact(value) * MARU.scale, MARU)


def Tan(value: Numeric) -> Mass:
    """Construct mass from a magnitude expressed in tan.

    Parameters
    ----------
    value : Numeric
        Mass magnitude in tan.

    Returns
    -------
    Mass
        Mass represented in tan.

    Notes
    -----
    One tan is sixteen kan, or exactly 60 kilograms.

    Examples
    --------
    A rice cooperative records a five-tan grain delivery and divides it evenly among
    ten storage lots:

    >>> from kuchka.units.mass import KILOGRAM
    >>> delivery = Tan(5)
    >>> lot_mass = (delivery / 10).to(KILOGRAM)
    >>> lot_mass
    30 kg
    """
    return Mass(to_exact(value) * TAN.scale, TAN)


JAPANESE_MASS_UNITS: Mapping[str, Callable[[Numeric], Mass]] = unit_table(
    "JAPANESE_MASS_UNITS",
    {
        MO: Mo,
        RIN: Rin,
        FUN: Fun,
        MONME: Monme,
        HYAKUME: Hyakume,
        KIN: Kin,
        KAN: Kan,
        MARU: Maru,
        TAN: Tan,
    },
)
"""Mass constructors by symbol, for configuration files and external interfaces."""


__all__ = [
    "JAPANESE_MASS_UNITS",
    "KAN",
    "KIN",
    "MONME",
    "Kan",
    "Kin",
    "Monme",
    "FUN",
    "HYAKUME",
    "MARU",
    "MO",
    "RIN",
    "TAN",
    "Fun",
    "Hyakume",
    "Maru",
    "Mo",
    "Rin",
    "Tan",
]
