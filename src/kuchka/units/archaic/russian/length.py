"""Historical Russian units of length.

This module represents a selection of historical Russian length units in the
standardized imperial-era system.
Each unit is defined as an exact multiple of the English inch, so these historical
measurements participate in the same typed arithmetic as modern metric and customary
lengths.

The units span everything from the fine marks of a printmaker to the distances recorded
by a provincial courier:

===========  ==============  =====================
Unit         Translation     Size
===========  ==============  =====================
`Tochka`     point           1/100 inch
`Liniya`     line            1/10 inch
`Dyuym`      inch (perst)    1 inch
`Vershok`    tip             1 3/4 inches
`Ladon`      palm            3 inches
`Pyad`       span (quarter)  7 inches
`Fut`        foot            12 inches (1 ft)
`Lokot`      elbow, cubit    18 inches (1.5 ft)
`Shag`       step            28 inches (2 1/3 ft)
`Arshin`     yard            28 inches (2 1/3 ft)
`Sazhen`     fathom          84 inches (7 ft)
`Versta`     verst           500 sazhens (3500 ft)
===========  ==============  =====================

`Perst` is another name for `Dyuym`, and `Chetvert` for `Pyad`.
Both are aliases of the same objects.

`Shag` and `Arshin` have the same scale in this system but retain separate unit
definitions and names.
Although `Shag` translates as "step", it is a fixed historical length here, not a
measurement of an individual's actual gait.

A number of alternative units and values exist as well.
These historical variants have their own definitions and are not aliases of the
standardized road and surveying measures listed above.

==================  ========================  ========================
Unit                Translation               Size
==================  ========================  ========================
`MakhovayaSazhen`   swung sazhen              1.76 m
`KosayaSazhen`      skewed/oblique sazhen     3.5 arshins (98 inches)
`MezhevayaVersta`   double, or border verst   1000 sazhens (2.1336 km)
==================  =======================   ========================

- `MakhovayaSazhen` refers to the span between the fingertips with both arms
    stretched sideways.
- `KosayaSazhen` describes the diagonal reach from a raised arm to the opposite foot.
The expression "kosaya sazhen v plechakh" (косая сажень в плечах) survives in Russian
    as a figurative description of a broad-shouldered person.
- `MezhevayaVersta` is the older border-measure convention of 1000 sazhens.
    The standardized road `Versta` in this module is 500 sazhens, so one
    `MezhevayaVersta` equals exactly two `Versta` values.

Examples
--------
A travelling folk theatre is preparing a painted backdrop for a scene from the tale of
Baba Yaga.
The set designer lays out a panel twelve arshins wide and five arshins high.
Its area emerges directly from the two historical lengths:

>>> backdrop_width = Arshin(12)
>>> backdrop_height = Arshin(5)
>>> painted_area = backdrop_width * backdrop_height
>>> painted_area
30.3483264 m²

A fictional provincial travel notebook, in the spirit of Gogol's Russia, records
eight versts from the posting station to an estate.
The final approach winds through the grounds for another thirty-five sazhens,
followed by six arshins from the gate to the house:

>>> road = Versta(8)
>>> approach = Sazhen(35)
>>> entrance = Arshin(6)
>>> total_journey = road + approach + entrance
>>> total_journey.to(KILOMETRE)
8.6133432 km

The original measurements can coexist without manual conversion factors.
The total is still one `Length` quantity, regardless of the historical vocabulary used
to describe each leg.

A land-survey record specifies a boundary of three mezhevye versty.
The older boundary measure is twice the road verst represented by `Versta`:

>>> boundary = MezhevayaVersta(3)
>>> boundary == Versta(6)
True

Notes
-----
These are the standardized values represented by this module, not a claim that every
regional or earlier historical version of a Russian unit had the same size.

One arshin is exactly 28 English inches, and one sazhen is exactly three arshins.
One versta is 500 sazhens, giving exactly 1.0668 km.

`RUSSIAN_LENGTH_UNITS` maps each unit symbol, such as ``"arshin"`` or ``"versta"``,
to its constructor.
It is intended for boundary code that receives historical unit names from configuration
files, datasets, or transcribed measurements.

For historical records, the date and local measurement convention matter:
the standardized conversions here should not be applied blindly to every
pre-standardization source.

See Also
--------
~kuchka.quantities.Length
    Quantity type representing length.
~kuchka.units.length
    Modern metric and selected non-SI length constructors.

"""

from __future__ import annotations

from fractions import Fraction
from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import LENGTH
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Length
from kuchka.quantities import UnitDef
from kuchka.units.length import INCH

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

TOCHKA = UnitDef("tochka", "tochka", INCH.scale / 100, LENGTH)
LINIYA = UnitDef("liniya", "liniya", INCH.scale / 10, LENGTH)
DYUYM = UnitDef("dyuym", "dyuym", INCH.scale, LENGTH)
VERSHOK = UnitDef("vershok", "vershok", Fraction(7, 4) * INCH.scale, LENGTH)
LADON = UnitDef("ladon", "ladon", 3 * INCH.scale, LENGTH)
PYAD = UnitDef("pyad", "pyad", 7 * INCH.scale, LENGTH)
FUT = UnitDef("fut", "fut", 12 * INCH.scale, LENGTH)
LOKOT = UnitDef("lokot", "lokot", 18 * INCH.scale, LENGTH)
SHAG = UnitDef("shag", "shag", 28 * INCH.scale, LENGTH)
ARSHIN = UnitDef("arshin", "arshin", 28 * INCH.scale, LENGTH)
SAZHEN = UnitDef("sazhen", "sazhen", 84 * INCH.scale, LENGTH)
VERSTA = UnitDef("versta", "versta", 500 * SAZHEN.scale, LENGTH)

PERST = DYUYM
CHETVERT = PYAD


def Tochka(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in points (tochki).

    Parameters
    ----------
    value : Numeric
        Length magnitude in points (tochki).

    Returns
    -------
    Length
        Length represented in points (tochki).

    Notes
    -----
    One tochka is 1/100 inch, or exactly 0.254 mm.

    Examples
    --------
    A lubok printmaker lays out the fine details of a traditional popular woodblock
    illustration.
    A line measuring twenty-four tochki is just over six millimetres long:

    >>> detail = Tochka(24)
    >>> detail.to(MILLIMETRE)
    6.096 mm

    """
    return Length(to_exact(value) * TOCHKA.scale, TOCHKA)


def Liniya(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in lines (linii).

    Parameters
    ----------
    value : Numeric
        Length magnitude in lines (linii).

    Returns
    -------
    Length
        Length represented in lines (linii).

    Notes
    -----
    One liniya is 1/10 inch, or exactly 2.54 mm.

    Examples
    --------
    A bookbinder preparing an illustrated volume reserves a six-liniya strip for the
    spine decoration:

    >>> spine_decoration = Liniya(6)
    >>> spine_decoration.to(MILLIMETRE)
    15.24 mm

    """
    return Length(to_exact(value) * LINIYA.scale, LINIYA)


def Dyuym(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in inches (dyuymy).

    Parameters
    ----------
    value : Numeric
        Length magnitude in inches (dyuymy).

    Returns
    -------
    Length
        Length represented in inches (dyuymy).

    Notes
    -----
    One dyuym, also called a perst, is exactly 2.54 cm.

    Examples
    --------
    A tinsmith in Tula fits a brass collar around a samovar's chimney.
    The collar is specified as three dyuymy across:

    >>> chimney_collar = Dyuym(3)
    >>> chimney_collar.to(CENTIMETRE)
    7.62 cm

    """
    return Length(to_exact(value) * DYUYM.scale, DYUYM)


def Vershok(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in vershoks.

    Parameters
    ----------
    value : Numeric
        Length magnitude in vershoks.

    Returns
    -------
    Length
        Length represented in vershoks.

    Notes
    -----
    One vershok is 1 3/4 inches, or exactly 4.445 cm.

    Examples
    --------
    A traditional horse-height record gives two arshins and five vershoks at the
    withers.
    The standardized measurements represented here yield:

    >>> height = Arshin(2) + Vershok(5)
    >>> height.to(CENTIMETRE)
    164.465 cm

    """
    return Length(to_exact(value) * VERSHOK.scale, VERSHOK)


def Ladon(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in palms (ladoni).

    Parameters
    ----------
    value : Numeric
        Length magnitude in palms (ladoni).

    Returns
    -------
    Length
        Length represented in palms (ladoni).

    Notes
    -----
    One ladon is 3 inches, or exactly 7.62 cm.

    Examples
    --------
    A woodcarver designing an ornate frame for a painted icon marks out a
    two-ladoni-wide wooden support:

    >>> support_width = Ladon(2)
    >>> support_width.to(CENTIMETRE)
    15.24 cm

    """
    return Length(to_exact(value) * LADON.scale, LADON)


def Pyad(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in spans (pyadi).

    Parameters
    ----------
    value : Numeric
        Length magnitude in spans (pyadi).

    Returns
    -------
    Length
        Length represented in spans (pyadi).

    Notes
    -----
    One pyad, also called a chetvert, is 7 inches: a quarter of an arshin.

    Examples
    --------
    A carpenter preparing carved timber for a northern Russian izba lays out an opening
    three pyadi wide:

    >>> opening = Pyad(3)
    >>> opening.to(CENTIMETRE)
    53.34 cm

    """
    return Length(to_exact(value) * PYAD.scale, PYAD)


def Fut(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in feet (futy).

    Parameters
    ----------
    value : Numeric
        Length magnitude in feet (futy).

    Returns
    -------
    Length
        Length represented in feet (futy).

    Notes
    -----
    One fut is 12 inches, equal to the English foot.

    Examples
    --------
    A museum workshop reconstructing a traditional folk-theatre prop needs a nine-fut
    timber beam for its supporting frame:

    >>> support_beam = Fut(9)
    >>> support_beam.to(METRE)
    2.7432 m

    """
    return Length(to_exact(value) * FUT.scale, FUT)


def Lokot(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in elbows (lokti).

    Parameters
    ----------
    value : Numeric
        Length magnitude in elbows (lokti).

    Returns
    -------
    Length
        Length represented in elbows (lokti).

    Notes
    -----
    One lokot is 18 inches, or exactly 45.72 cm, in this standardized system.

    Examples
    --------
    A museum tailor reconstructing a traditional market costume records a piece of
    linen as three lokti long:

    >>> linen = Lokot(3)
    >>> linen.to(CENTIMETRE)
    137.16 cm

    """
    return Length(to_exact(value) * LOKOT.scale, LOKOT)


def Shag(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in steps (shagi).

    Parameters
    ----------
    value : Numeric
        Length magnitude in steps (shagi).

    Returns
    -------
    Length
        Length represented in steps (shagi).

    Notes
    -----
    One shag is 28 inches, or exactly 71.12 cm.
    It shares the scale of `Arshin`, but retains its own unit definition.

    Despite its translation as "step", this constructor represents a fixed historical
    length, not the variable length of an actual walking step.

    Examples
    --------
    A stage designer plans the blocking for a folktale performance:
    the distance from the izba door to the well is eight standardized shagi.

    >>> doorway_to_well = Shag(8)
    >>> doorway_to_well.to(METRE)
    5.6896 m

    """
    return Length(to_exact(value) * SHAG.scale, SHAG)


def Arshin(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in arshins.

    Parameters
    ----------
    value : Numeric
        Length magnitude in arshins.

    Returns
    -------
    Length
        Length represented in arshins.

    Notes
    -----
    One arshin is 28 inches, or exactly 71.12 cm.
    Sixteen vershoks make one arshin in this standardized system.

    Examples
    --------
    A set designer paints a backdrop depicting a Russian fairy-tale forest.
    The panel is twelve arshins wide and five arshins high.
    Because `Length` participates in geometric arithmetic, its dimensions produce an
    `Area`:

    >>> backdrop_width = Arshin(12)
    >>> backdrop_height = Arshin(5)
    >>> backdrop_width * backdrop_height
    30.3483264 m²

    """
    return Length(to_exact(value) * ARSHIN.scale, ARSHIN)


def Sazhen(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in fathoms (sazheni).

    Parameters
    ----------
    value : Numeric
        Length magnitude in fathoms (sazheni).

    Returns
    -------
    Length
        Length represented in fathoms (sazheni).

    Notes
    -----
    One sazhen is 84 inches, or exactly seven English feet.

    Examples
    --------
    A Volga river pilot lowers a sounding line to check the depth of a navigable
    channel.
    The recorded depth is four sazhens:

    >>> channel_depth = Sazhen(4)
    >>> channel_depth.to(METRE)
    8.5344 m

    """
    return Length(to_exact(value) * SAZHEN.scale, SAZHEN)


def Versta(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in versts (versty).

    Parameters
    ----------
    value : Numeric
        Length magnitude in versts (versty).

    Returns
    -------
    Length
        Length represented in versts (versty).

    Notes
    -----
    One versta is 500 sazhens, or exactly 1.0668 km.

    Examples
    --------
    A fictional provincial courier's itinerary records twelve versts to a market town,
    then another seven versts to the next posting station:

    >>> first_stage = Versta(12)
    >>> second_stage = Versta(7)
    >>> total_route = first_stage + second_stage
    >>> total_route.to(KILOMETRE)
    20.2692 km

    """
    return Length(to_exact(value) * VERSTA.scale, VERSTA)


Perst = Dyuym
Chetvert = Pyad

# Alternative units.

MAKHOVAYA_SAZHEN = UnitDef(
    "makhovaya_sazhen",
    "makhovaya sazhen",
    Fraction(8800, 127) * INCH.scale,  # The reported 1.76 m convention.
    LENGTH,
)

KOSAYA_SAZHEN = UnitDef(
    "kosaya_sazhen",
    "kosaya sazhen",
    Fraction(98) * INCH.scale,
    LENGTH,
)

MEZHEVAYA_VERSTA = UnitDef(
    "mezhevaya_versta",
    "mezhevaya versta",
    1000 * SAZHEN.scale,
    LENGTH,
)


def MakhovayaSazhen(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in swung sazhens.

    Parameters
    ----------
    value : Numeric
        Length magnitude in swung sazhens.

    Returns
    -------
    Length
        Length represented in swung sazhens.

    Notes
    -----
    This module adopts the reported 1.76 m convention, represented as an exact
    scale relative to the English inch. Historical sources differ on the
    precise definition of similarly named measuring sazhens.

    Examples
    --------
    A reconstruction of a traditional Russian workshop uses the extended
    arm span as a reference length. Under this convention, one swung sazhen
    is shorter than the standardized seven-foot sazhen:

    >>> span = MakhovayaSazhen(1)
    >>> span.to(METRE)
    1.76 m
    >>> span < Sazhen(1)
    True

    """
    return Length(to_exact(value) * MAKHOVAYA_SAZHEN.scale, MAKHOVAYA_SAZHEN)


def KosayaSazhen(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in skewed sazhens.

    Parameters
    ----------
    value : Numeric
        Length magnitude in skewed sazhens.

    Returns
    -------
    Length
        Length represented in skewed sazhens.

    Notes
    -----
    One kosaya sazhen is 3.5 arshins, or exactly 98 English inches.

    Examples
    --------
    A stage reconstruction of a Russian folk-tale bogatyr uses the diagonal
    reach from a raised hand to the opposite foot as its reference measure:

    >>> diagonal_reach = KosayaSazhen(1)
    >>> diagonal_reach.to(METRE)
    2.4892 m

    The historical relationship to the arshin remains exact:

    >>> diagonal_reach == Arshin(Fraction(7, 2))
    True

    """
    return Length(to_exact(value) * KOSAYA_SAZHEN.scale, KOSAYA_SAZHEN)


def MezhevayaVersta(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in border versts.

    Parameters
    ----------
    value : Numeric
        Length magnitude in border versts (mezhevye versty).

    Returns
    -------
    Length
        Length represented in border versts.

    Notes
    -----
    One border verst is 1000 sazhens, or exactly 2.1336 km under the
    standardized sazhen used in this module. This historical measure was
    used for land surveying and distances between settlements.

    Examples
    --------
    A provincial landowner's estate inventory, worthy of Gogol's *Dead Souls*,
    describes a rectangular meadow by its surveyed dimensions:
    one and a half border versts along the road and 240 sazhens across. The dimensions
    produce an area directly, without manually converting either measurement:

    >>> meadow_length = MezhevayaVersta(Fraction(3, 2))
    >>> meadow_width = Sazhen(240)
    >>> meadow_area = meadow_length * meadow_width
    >>> meadow_area
    1638809.6256 m²

    The resulting area is about 164 hectares of meadowland:

    >>> meadow_area.to(HECTARE)
    163.88096256 ha

    """
    return Length(to_exact(value) * MEZHEVAYA_VERSTA.scale, MEZHEVAYA_VERSTA)


RUSSIAN_LENGTH_UNITS: Mapping[str, Callable[[Numeric], Length]] = MappingProxyType(
    {
        TOCHKA.symbol: Tochka,
        LINIYA.symbol: Liniya,
        DYUYM.symbol: Dyuym,
        VERSHOK.symbol: Vershok,
        LADON.symbol: Ladon,
        PYAD.symbol: Pyad,
        FUT.symbol: Fut,
        LOKOT.symbol: Lokot,
        SHAG.symbol: Shag,
        ARSHIN.symbol: Arshin,
        SAZHEN.symbol: Sazhen,
        VERSTA.symbol: Versta,
        MAKHOVAYA_SAZHEN.symbol: MakhovayaSazhen,
        KOSAYA_SAZHEN.symbol: KosayaSazhen,
        MEZHEVAYA_VERSTA.symbol: MezhevayaVersta,
    }
)
"""Constructors by symbol, for configuration files and external interfaces."""


__all__ = [
    "ARSHIN",
    "CHETVERT",
    "DYUYM",
    "FUT",
    "KOSAYA_SAZHEN",
    "LADON",
    "LINIYA",
    "LOKOT",
    "MAKHOVAYA_SAZHEN",
    "MEZHEVAYA_VERSTA",
    "PERST",
    "PYAD",
    "RUSSIAN_LENGTH_UNITS",
    "SAZHEN",
    "SHAG",
    "TOCHKA",
    "VERSHOK",
    "VERSTA",
    "Arshin",
    "Chetvert",
    "Dyuym",
    "Fut",
    "KosayaSazhen",
    "Ladon",
    "Liniya",
    "Lokot",
    "MakhovayaSazhen",
    "MezhevayaVersta",
    "Perst",
    "Pyad",
    "Sazhen",
    "Shag",
    "Tochka",
    "Vershok",
    "Versta",
]
