"""Japanese shakkan-hō units of volume.

These units belong to the shakkan-hō (尺貫法), the traditional Japanese measurement
system.
The standardized capacity scale is organized around the *shō* (升):
- ten *gō* (合) make one shō,
- ten shō make one *to* (斗),
- and ten to make one *koku* (石).

The smaller *shaku* (勺) and *sai* (才) are one hundredth and one thousandth of a shō,
respectively.

The gō is familiar as a measure of rice and sake.
A large sake bottle called an *isshōbin* (一升瓶) is named for its nominal one-shō
capacity.
The koku is historically important in agricultural and fiscal records, where rice
yields and stipends were expressed in koku.

Volume
------

======= ========== ====== =============== =======================
Unit    Romanised  Kanji  Relative to shō Exact volume
======= ========== ====== =============== =======================
Sai     Sai        才     1/1000          2401/1,331,000 L
Shaku   Shaku      勺     1/100           2401/133,100 L
Go      Gō         合     1/10            2401/13,310 L
Sho     Shō        升     1               2401/1,331 L
To      To         斗     10              24,010/1,331 L
Koku    Koku       石     100             240,100/1,331 L
======= ========== ====== =============== =======================

The metric values are exact fractions.
In particular, one shō is exactly 2401/1331 litres under the standardized capacity
definition, which is slightly more than 1.8 litres.

Examples
--------
A brewery prepares eighteen shō for three inns.
The tasting counter reserves fifteen gō, and the remainder is split evenly among the
inns.
Expressing each shipment in both gō and shō makes the order easy to check against the
two notations used by the brewery and its customers:

>>> batch = Sho(18)
>>> tasting_reserve = Go(15)
>>> shipment_per_inn = (batch - tasting_reserve) / 3
>>> shipment_per_inn.to(GO)
55 go
>>> shipment_per_inn.to(SHO)
5.5 sho

A rice district's ledger records seventeen koku after the harvest.
Three koku remain in the district granary, while the balance is divided among seven
storehouses:

>>> harvest = Koku(17)
>>> central_reserve = Koku(3)
>>> storehouse_share = ((harvest - central_reserve) / 7).to(KOKU)
>>> storehouse_share
2 koku

Notes
-----
The exact standardized relationships are::

    1 shō = 10 gō = 100 shaku = 1000 sai
    1 to  = 10 shō
    1 koku = 10 to = 100 shō
    1 shō = 2401/1331 L

``Shaku`` here denotes the volume unit 勺.
Japanese measurement systems also use the romanization *shaku* for other units,
including the length unit 尺; the kanji and dimension distinguish them.
The constructor is deliberately named ``Shaku`` without adding a dimension suffix:
callers can choose import aliases when two domain-specific names collide in their
local namespace.

``Koku`` models the standardized capacity unit 石 equal to 100 shō.
Historical trade also used commodity-specific measures called shipping koku, timber
koku, and fish koku.
Those conventions denoted volumes of their own, which this constructor leaves to a
future definition.
These definitions follow the selected standardized system.

``JAPANESE_VOLUME_UNITS`` maps unit symbols such as ``"gō"``, ``"sho"``, and ``"石"`` to
their constructors.
It is intended for boundary code that reads measurements from records, configuration
files, catalogues, or other external sources.

For historical background, see:
https://en.wikipedia.org/wiki/Japanese_units_of_measurement

See Also
--------
~kuchka.quantities.Volume
    Quantity type representing volume.
~kuchka.quantities.Density
    Mass per unit volume.
~kuchka.units.volume
    Metric and other volume constructors, including litres and cubic metres.
~kuchka.units.japanese.mass
    Japanese mass units, including the kan used in historical weight records.

"""

from __future__ import annotations

from fractions import Fraction
from typing import TYPE_CHECKING

from kuchka.dimensions import VOLUME
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import UnitDef
from kuchka.quantities import Volume
from kuchka.quantities.base.units import extend_units

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping


SHO = UnitDef(
    "sho",
    "sho",
    Fraction(2401, 1_331_000),
    VOLUME,
    aliases=("升", "shō"),
)
SAI = UnitDef(
    "sai",
    "sai",
    SHO.scale / 1000,
    VOLUME,
    aliases=("才",),
)
SHAKU = UnitDef(
    "shaku",
    "shaku",
    SHO.scale / 100,
    VOLUME,
    aliases=("勺",),
)
GO = UnitDef(
    "go",
    "go",
    SHO.scale / 10,
    VOLUME,
    aliases=("合", "gō"),
)
TO = UnitDef(
    "to",
    "to",
    10 * SHO.scale,
    VOLUME,
    aliases=("斗", "tō"),
)
KOKU = UnitDef(
    "koku",
    "koku",
    100 * SHO.scale,
    VOLUME,
    aliases=("石",),
)


def Sai(value: Numeric) -> Volume:
    """Construct volume from a magnitude expressed in sai (才).

    Parameters
    ----------
    value : Numeric
        Volume magnitude in sai.

    Returns
    -------
    Volume
        Volume represented in sai.

    Notes
    -----
    One sai is 1/1000 shō, or exactly 2401/1,331,000 litres.

    Examples
    --------
    A reconstructed batch sheet contains two small measurements.
    After combining them, five shaku are set aside as a reference sample:

    >>> measured = Sai(640) + Sai(360)
    >>> usable = (measured - Shaku(5)).to(GO)
    >>> usable
    9.5 go

    """
    return Volume(to_exact(value) * SAI.scale, SAI)


def Shaku(value: Numeric) -> Volume:
    """Construct volume from a magnitude expressed in shaku (勺).

    Parameters
    ----------
    value : Numeric
        Volume magnitude in shaku (勺).

    Returns
    -------
    Volume
        Volume represented in shaku.

    Notes
    -----
    One shaku is 1/100 shō, or exactly 2401/133,100 litres.
    This is the volume unit 勺; the length unit 尺 has its own constructor in the length
    module.

    Examples
    --------
    A small trial blend records twelve shaku of concentrate and eight shaku of rinse,
    then adds three gō of carrier liquid:

    >>> trial_blend = Shaku(12) + Shaku(8) + Go(3)
    >>> trial_blend.to(GO)
    5 go

    """
    return Volume(to_exact(value) * SHAKU.scale, SHAKU)


def Go(value: Numeric) -> Volume:
    """Construct volume from a magnitude expressed in gō (合).

    Parameters
    ----------
    value : Numeric
        Volume magnitude in gō.

    Returns
    -------
    Volume
        Volume represented in gō.

    Notes
    -----
    One gō is 1/10 shō, or exactly 2401/13,310 litres.
    A gō is a familiar traditional measure for rice and sake.

    Examples
    --------
    A sake house prepares six shō for a tasting event and withholds twelve gō for
    quality checks.
    The remaining volume is expressed as gō-sized measures:

    >>> saleable = Sho(6) - Go(12)
    >>> saleable.to(GO)
    48 go

    """
    return Volume(to_exact(value) * GO.scale, GO)


def Sho(value: Numeric) -> Volume:
    """Construct volume from a magnitude expressed in shō (升).

    Parameters
    ----------
    value : Numeric
        Volume magnitude in shō.

    Returns
    -------
    Volume
        Volume represented in shō.

    Notes
    -----
    One shō is exactly 2401/1331 litres.
    The isshōbin (一升瓶), a familiar large sake bottle, takes its name from its nominal
    one-shō capacity.

    Examples
    --------
    A cooperative allocates fifteen shō to a bottling run.
    Three shō remain in its own cellar, and the remainder is divided between six
    receiving casks:

    >>> saleable = Sho(15) - Sho(3)
    >>> cask_fill = (saleable / 6).to(SHO)
    >>> cask_fill
    2 sho

    """
    return Volume(to_exact(value) * SHO.scale, SHO)


def To(value: Numeric) -> Volume:
    """Construct volume from a magnitude expressed in to (斗).

    Parameters
    ----------
    value : Numeric
        Volume magnitude in to.

    Returns
    -------
    Volume
        Volume represented in to.

    Notes
    -----
    One to is ten shō, or exactly 24,010/1331 litres.

    Examples
    --------
    A delivery contains four to.
    After five shō are diverted to a starter batch, the remainder is divided evenly
    among seven vats:

    >>> remainder = To(4) - Sho(5)
    >>> each_vat = (remainder / 7).to(SHO)
    >>> each_vat
    5 sho

    """
    return Volume(to_exact(value) * TO.scale, TO)


def Koku(value: Numeric) -> Volume:
    """Construct volume from a magnitude expressed in koku (石).

    Parameters
    ----------
    value : Numeric
        Volume magnitude in koku.

    Returns
    -------
    Volume
        Volume represented in koku.

    Notes
    -----
    One koku is one hundred shō, or exactly 240,100/1331 litres.
    The koku was prominent in rice-yield and stipend records.
    The familiar comparison with a person's yearly rice needs is a historical rule of
    thumb, which suits a story and serves no accounting definition.

    Examples
    --------
    A district ledger records seventeen koku after harvest.
    Three koku are kept in the central granary, and the balance is divided among seven
    storehouses:

    >>> harvest = Koku(17)
    >>> central_reserve = Koku(3)
    >>> storehouse_share = ((harvest - central_reserve) / 7).to(KOKU)
    >>> storehouse_share
    2 koku

    """
    return Volume(to_exact(value) * KOKU.scale, KOKU)


JAPANESE_VOLUME_UNITS: Mapping[str, Callable[[Numeric], Volume]] = unit_table(
    "JAPANESE_VOLUME_UNITS",
    {
        SAI: Sai,
        SHAKU: Shaku,
        GO: Go,
        SHO: Sho,
        TO: To,
        KOKU: Koku,
    },
)
"""Volume constructors by symbol, for configuration files and external interfaces."""


# Importing this module makes Volume display in the units of its table.
extend_units(Volume, JAPANESE_VOLUME_UNITS)


__all__ = [
    "GO",
    "JAPANESE_VOLUME_UNITS",
    "KOKU",
    "SAI",
    "SHAKU",
    "SHO",
    "TO",
    "Go",
    "Koku",
    "Sai",
    "Shaku",
    "Sho",
    "To",
]
