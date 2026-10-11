"""Biblical and Talmudic length units, represented under three calibrations.

The Hebrew system of length is built on the etzba (אצבע, thumb-breadth).
The biblical and rabbinic vocabulary relates fingers, palms, spans, cubits, and longer
travel distances through a common set of ratios.

===========  ==============  =====================
Unit         Translation     Size
===========  ==============  =====================
`Etzba`      thumb-breadth   1 etzba
`Tefach`     hand-breadth    4 etzba'ot
`Zeret`      span            12 etzba'ot
`Amah`       cubit           24 etzba'ot
`Mil`        rabbinic mile   2000 amot
`Parsa`      parasang        4 milin
===========  ==============  =====================

The ratios are fixed in this model, but the absolute size of the etzba is disputed.
Each unit therefore comes in three calibrations:

* the unsuffixed constructors use a reference etzba of 2.2 cm, a rounded midpoint of
    the two halakhic estimates below;
* the `Naeh` suffix follows Rabbi Avraham Chaim Naeh, using an etzba of 2 cm;
* the `ChazonIsh` suffix follows the Chazon Ish, using an etzba of 2.38 cm.

The reference calibration is a convenient common scale, not a separate halakhic ruling.
The Naeh and Chazon Ish calibrations represent distinct interpretations of traditional
measurements.

All three calibrations construct ordinary `Length` quantities.
They therefore participate in the same arithmetic as modern metric units, and values
from different calibrations can be compared or combined.
The numerical result depends on the calibration chosen for each measurement.

Examples
--------
An educational exhibit about the *techum Shabbat* illustrates the traditional 2000-amah
boundary.
The exhibit lets visitors compare the three calibration conventions.
These calculations are illustrative, not a practical halakhic ruling:

>>> from kuchka.units.length import KILOMETRE, CENTIMETRE, METRE
>>> reference_boundary = Mil(1).to(KILOMETRE)
>>> reference_boundary
1.056 km

Under Rabbi Avraham Chaim Naeh's calibration, the same traditional distance is
represented by a shorter physical length:

>>> naeh_boundary = MilNaeh(1).to(KILOMETRE)
>>> naeh_boundary
0.96 km

Under the Chazon Ish calibration, it is longer:

>>> chazon_ish_boundary = MilChazonIsh(1).to(KILOMETRE)
>>> chazon_ish_boundary
1.1424 km

A museum preparing a model of ancient Israelite architecture uses a ten-by-five-amah
rectangular floor plan under the reference calibration.
The two dimensions produce an `Area` directly:

>>> room_width = Amah(10)
>>> room_depth = Amah(5)
>>> room_footprint = room_width * room_depth
>>> room_footprint
13.9392 m²

A separate display compares a ten-amah architectural span under the two halakhic
calibrations.
The difference is nearly a metre:

>>> (AmahChazonIsh(10) - AmahNaeh(10)).to(CENTIMETRE)
91.2 cm

Notes
-----
The base unit is the etzba. The relationships represented by this module are:

``1 tefach = 4 etzba'ot``
``1 zeret = 3 tefachim``
``1 amah = 2 zarot = 6 tefachim = 24 etzba'ot``
``1 mil = 2000 amot``
``1 parsa = 4 milin``

The selected calibration determines the absolute size of every unit.
In this module, the reference etzba is exactly 0.022 m, the Naeh etzba exactly 0.020 m,
and the Chazon Ish etzba exactly 0.0238 m.
These are exact decimal values in the computational model.
The historical and halakhic interpretations remain matters of scholarship and religious
tradition.

The names `Mil` and `Parsa` refer to historical travel distances, not to the modern
statute mile or a universally fixed real-world journey.
This module uses the stated relationships to provide deterministic arithmetic.

`HEBREW_LENGTH_UNITS` maps every symbol, such as ``"amah"`` or ``"amah (Naeh)"``, to
its constructor.
It is intended for boundary code that reads traditional measurement names from source
data, configuration files, or other external inputs.

See Also
--------
~kuchka.quantities.Length
    Quantity type representing length.
~kuchka.quantities.Area
    Area derived from multiplying two lengths.
~kuchka.units.length
    Modern metric and selected non-SI length constructors.
"""

from __future__ import annotations

from decimal import Decimal
from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import LENGTH
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Length
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

_ETZBA_MID = Decimal("0.022")
_ETZBA_NAEH = Decimal("0.02")
_ETZBA_CHAZON_ISH = Decimal("0.0238")

# Plain calibration, etzba of 2.2 cm.
ETZBA = UnitDef("etzba", "etzba", _ETZBA_MID, LENGTH)
TEFACH = UnitDef("tefach", "tefach", 4 * _ETZBA_MID, LENGTH)
ZERET = UnitDef("zeret", "zeret", 12 * _ETZBA_MID, LENGTH)
AMAH = UnitDef("amah", "amah", 24 * _ETZBA_MID, LENGTH)
MIL = UnitDef("mil", "mil", 48000 * _ETZBA_MID, LENGTH)
PARSA = UnitDef("parsa", "parsa", 192000 * _ETZBA_MID, LENGTH)

# Naeh calibration, etzba of 2 cm.
ETZBA_NAEH = UnitDef("etzba_naeh", "etzba (Naeh)", _ETZBA_NAEH, LENGTH)
TEFACH_NAEH = UnitDef("tefach_naeh", "tefach (Naeh)", 4 * _ETZBA_NAEH, LENGTH)
ZERET_NAEH = UnitDef("zeret_naeh", "zeret (Naeh)", 12 * _ETZBA_NAEH, LENGTH)
AMAH_NAEH = UnitDef("amah_naeh", "amah (Naeh)", 24 * _ETZBA_NAEH, LENGTH)
MIL_NAEH = UnitDef("mil_naeh", "mil (Naeh)", 48000 * _ETZBA_NAEH, LENGTH)
PARSA_NAEH = UnitDef("parsa_naeh", "parsa (Naeh)", 192000 * _ETZBA_NAEH, LENGTH)

# Chazon ish calibration, etzba of 2.38 cm.
ETZBA_CHAZON_ISH = UnitDef(
    "etzba_chazon_ish", "etzba (Chazon Ish)", _ETZBA_CHAZON_ISH, LENGTH
)
TEFACH_CHAZON_ISH = UnitDef(
    "tefach_chazon_ish", "tefach (Chazon Ish)", 4 * _ETZBA_CHAZON_ISH, LENGTH
)
ZERET_CHAZON_ISH = UnitDef(
    "zeret_chazon_ish", "zeret (Chazon Ish)", 12 * _ETZBA_CHAZON_ISH, LENGTH
)
AMAH_CHAZON_ISH = UnitDef(
    "amah_chazon_ish", "amah (Chazon Ish)", 24 * _ETZBA_CHAZON_ISH, LENGTH
)
MIL_CHAZON_ISH = UnitDef(
    "mil_chazon_ish", "mil (Chazon Ish)", 48000 * _ETZBA_CHAZON_ISH, LENGTH
)
PARSA_CHAZON_ISH = UnitDef(
    "parsa_chazon_ish", "parsa (Chazon Ish)", 192000 * _ETZBA_CHAZON_ISH, LENGTH
)


def Etzba(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in thumb-breadths (etzba'ot).

    Parameters
    ----------
    value : Numeric
        Length magnitude in thumb-breadths (etzba'ot).

    Returns
    -------
    Length
        Length represented in thumb-breadths (etzba'ot).

    Notes
    -----
    One etzba is the base unit of the Hebrew length system.

    Uses the plain calibration: an etzba of 2.2 cm.

    Examples
    --------
    A conservator preparing a modern Judaica mosaic lays out a rectangular decorative
    panel twelve thumb-breadths wide and eight high:

    >>> panel_width = Etzba(12)
    >>> panel_height = Etzba(8)
    >>> panel_width * panel_height
    0.046464 m²

    """
    return Length(to_exact(value) * ETZBA.scale, ETZBA)


def Tefach(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in hand-breadths (tefachim).

    Parameters
    ----------
    value : Numeric
        Length magnitude in hand-breadths (tefachim).

    Returns
    -------
    Length
        Length represented in hand-breadths (tefachim).

    Notes
    -----
    One tefach is 4 etzba'ot.

    Uses the plain calibration: an etzba of 2.2 cm.

    Examples
    --------
    A Jerusalem heritage workshop prepares a hand-sized ceramic panel for an
    educational display.
    Its layout is five tefachim by four:

    >>> panel_width = Tefach(5)
    >>> panel_height = Tefach(4)
    >>> panel_width * panel_height
    0.15488 m²

    """
    return Length(to_exact(value) * TEFACH.scale, TEFACH)


def Zeret(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in spans (zarot).

    Parameters
    ----------
    value : Numeric
        Length magnitude in spans (zarot).

    Returns
    -------
    Length
        Length represented in spans (zarot).

    Notes
    -----
    One zeret is 3 tefachim, or 12 etzba'ot.

    Uses the plain calibration: an etzba of 2.2 cm.

    Examples
    --------
    A textile artist preparing a panel for a modern Israeli folk-dance performance
    measures the fabric in spans.
    A panel three zarot long and two zarot wide has this area under the reference
    calibration:

    >>> panel_length = Zeret(3)
    >>> panel_width = Zeret(2)
    >>> panel_length * panel_width
    0.418176 m²

    """
    return Length(to_exact(value) * ZERET.scale, ZERET)


def Amah(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in cubits (amot).

    Parameters
    ----------
    value : Numeric
        Length magnitude in cubits (amot).

    Returns
    -------
    Length
        Length represented in cubits (amot).

    Notes
    -----
    One amah is 2 zarot, 6 tefachim, or 24 etzba'ot.

    Uses the plain calibration: an etzba of 2.2 cm.

    Examples
    --------
    A museum reconstruction of an ancient Jerusalem doorway uses a four-amah opening
    height under the reference calibration:

    >>> from kuchka.units.length import METRE
    >>> doorway_height = Amah(4)
    >>> doorway_height.to(METRE)
    2.112 m

    """
    return Length(to_exact(value) * AMAH.scale, AMAH)


def Mil(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in miles (milin).

    Parameters
    ----------
    value : Numeric
        Length magnitude in miles (milin).

    Returns
    -------
    Length
        Length represented in miles (milin).

    Notes
    -----
    One mil is 2000 amot.

    Uses the plain calibration: an etzba of 2.2 cm.

    Examples
    --------
    A study group annotating an ancient travel narrative records a route of two milin.
    The reference calibration gives the route a definite computational length:

    >>> from kuchka.units.length import KILOMETRE
    >>> route = Mil(2)
    >>> route.to(KILOMETRE)
    2.112 km

    """
    return Length(to_exact(value) * MIL.scale, MIL)


def Parsa(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in parasangs (parsa'ot).

    Parameters
    ----------
    value : Numeric
        Length magnitude in parasangs (parsa'ot).

    Returns
    -------
    Length
        Length represented in parasangs (parsa'ot).

    Notes
    -----
    One parsa is 4 milin, or 8000 amot.

    Uses the plain calibration: an etzba of 2.2 cm.

    Examples
    --------
    A historical map for a lesson on rabbinic travel narratives marks a journey of
    three parasangs.
    Under this module's reference calibration, the journey is represented as:

    >>> from kuchka.units.length import KILOMETRE
    >>> journey = Parsa(3)
    >>> journey.to(KILOMETRE)
    12.672 km

    """
    return Length(to_exact(value) * PARSA.scale, PARSA)


def EtzbaNaeh(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in thumb-breadths (etzba'ot).

    Parameters
    ----------
    value : Numeric
        Length magnitude in thumb-breadths (etzba'ot).

    Returns
    -------
    Length
        Length represented in thumb-breadths (etzba'ot).

    Notes
    -----
    One etzba is the base unit of the Hebrew length system.

    Uses Rabbi Avraham Chaim Naeh's calibration: an etzba of 2 cm.

    Examples
    --------
    A calligraphy exhibition in modern Israel includes a decorative line eleven
    thumb-breadths long.
    Using the Naeh calibration gives a twenty-two-centimetre line:

    >>> from kuchka.units.length import CENTIMETRE
    >>> decorative_line = EtzbaNaeh(11)
    >>> decorative_line.to(CENTIMETRE)
    22 cm

    """
    return Length(to_exact(value) * ETZBA_NAEH.scale, ETZBA_NAEH)


def TefachNaeh(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in hand-breadths (tefachim).

    Parameters
    ----------
    value : Numeric
        Length magnitude in hand-breadths (tefachim).

    Returns
    -------
    Length
        Length represented in hand-breadths (tefachim).

    Notes
    -----
    One tefach is 4 etzba'ot.

    Uses Rabbi Avraham Chaim Naeh's calibration: an etzba of 2 cm.

    Examples
    Examples
    --------
    A workshop designing a patterned tile for a Jerusalem courtyard display specifies a
    five-by-three-tefach rectangle using the Naeh calibration:

    >>> tile_width = TefachNaeh(5)
    >>> tile_height = TefachNaeh(3)
    >>> tile_width * tile_height
    0.096 m²

    """
    return Length(to_exact(value) * TEFACH_NAEH.scale, TEFACH_NAEH)


def ZeretNaeh(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in spans (zarot).

    Parameters
    ----------
    value : Numeric
        Length magnitude in spans (zarot).

    Returns
    -------
    Length
        Length represented in spans (zarot).

    Notes
    -----
    One zeret is 3 tefachim, or 12 etzba'ot.

    Uses Rabbi Avraham Chaim Naeh's calibration: an etzba of 2 cm.

    Examples
    --------
    A costume maker preparing a fabric strip for a modern Israeli folk performance
    measures its length as two and a half spans.
    Under the Naeh calibration, the strip is sixty centimetres long:

    >>> from kuchka.units.length import CENTIMETRE
    >>> fabric_strip = ZeretNaeh(2.5)
    >>> fabric_strip.to(CENTIMETRE)
    60 cm

    """
    return Length(to_exact(value) * ZERET_NAEH.scale, ZERET_NAEH)


def AmahNaeh(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in cubits (amot).

    Parameters
    ----------
    value : Numeric
        Length magnitude in cubits (amot).

    Returns
    -------
    Length
        Length represented in cubits (amot).

    Notes
    -----
    One amah is 2 zarot, 6 tefachim, or 24 etzba'ot.

    Uses Rabbi Avraham Chaim Naeh's calibration: an etzba of 2 cm.

    Examples
    --------
    A heritage-centre workshop creates a rectangular floor panel for a teaching model,
    measuring four by three amot under the Naeh calibration.
    Its area follows directly from the two lengths:

    >>> panel_width = AmahNaeh(4)
    >>> panel_depth = AmahNaeh(3)
    >>> panel_width * panel_depth
    2.7648 m²

    """
    return Length(to_exact(value) * AMAH_NAEH.scale, AMAH_NAEH)


def MilNaeh(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in miles (milin).

    Parameters
    ----------
    value : Numeric
        Length magnitude in miles (milin).

    Returns
    -------
    Length
        Length represented in miles (milin).

    Notes
    -----
    One mil is 2000 amot.

    Uses Rabbi Avraham Chaim Naeh's calibration: an etzba of 2 cm.

    Examples
    --------
    A walking route in an educational reconstruction of a rabbinic travel account is
    recorded as two milin.
    Under the Naeh calibration, the represented distance is:

    >>> from kuchka.units.length import KILOMETRE
    >>> route = MilNaeh(2)
    >>> route.to(KILOMETRE)
    1.92 km

    """
    return Length(to_exact(value) * MIL_NAEH.scale, MIL_NAEH)


def ParsaNaeh(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in parasangs (parsa'ot).

    Parameters
    ----------
    value : Numeric
        Length magnitude in parasangs (parsa'ot).

    Returns
    -------
    Length
        Length represented in parasangs (parsa'ot).

    Notes
    -----
    One parsa is 4 milin, or 8000 amot.

    Uses Rabbi Avraham Chaim Naeh's calibration: an etzba of 2 cm.

    Examples
    --------
    A lesson on traditional travel terminology maps a three-parsa journey using
    Rabbi Avraham Chaim Naeh's calibration:

    >>> from kuchka.units.length import KILOMETRE
    >>> journey = ParsaNaeh(3)
    >>> journey.to(KILOMETRE)
    11.52 km

    """
    return Length(to_exact(value) * PARSA_NAEH.scale, PARSA_NAEH)


def EtzbaChazonIsh(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in thumb-breadths (etzba'ot).

    Parameters
    ----------
    value : Numeric
        Length magnitude in thumb-breadths (etzba'ot).

    Returns
    -------
    Length
        Length represented in thumb-breadths (etzba'ot).

    Notes
    -----
    One etzba is the base unit of the Hebrew length system.

    Uses the Chazon Ish's calibration: an etzba of 2.38 cm.

    Examples
    --------
    An educational exhibit compares the three traditional calibrations.
    Under the Chazon Ish calibration, ten thumb-breadths make a
    twenty-three-point-eight-centimetre reference segment:

    >>> from kuchka.units.length import CENTIMETRE
    >>> reference_segment = EtzbaChazonIsh(10)
    >>> reference_segment.to(CENTIMETRE)
    23.8 cm

    """
    return Length(to_exact(value) * ETZBA_CHAZON_ISH.scale, ETZBA_CHAZON_ISH)


def TefachChazonIsh(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in hand-breadths (tefachim).

    Parameters
    ----------
    value : Numeric
        Length magnitude in hand-breadths (tefachim).

    Returns
    -------
    Length
        Length represented in hand-breadths (tefachim).

    Notes
    -----
    One tefach is 4 etzba'ot.

    Uses the Chazon Ish's calibration: an etzba of 2.38 cm.

    Examples
    --------
    A curator designs a rectangular exhibit tile whose edges are seven and
    three hand-breadths under the Chazon Ish calibration:

    >>> tile_width = TefachChazonIsh(7)
    >>> tile_height = TefachChazonIsh(3)
    >>> tile_width * tile_height
    0.19032384 m²

    """
    return Length(to_exact(value) * TEFACH_CHAZON_ISH.scale, TEFACH_CHAZON_ISH)


def ZeretChazonIsh(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in spans (zarot).

    Parameters
    ----------
    value : Numeric
        Length magnitude in spans (zarot).

    Returns
    -------
    Length
        Length represented in spans (zarot).

    Notes
    -----
    One zeret is 3 tefachim, or 12 etzba'ot.

    Uses the Chazon Ish's calibration: an etzba of 2.38 cm.

    Examples
    --------
    A reconstruction model uses two and a half spans for a reference dimension in its
    display.
    Under the Chazon Ish calibration, this is:

    >>> from kuchka.units.length import METRE
    >>> reference_span = ZeretChazonIsh(2.5)
    >>> reference_span.to(METRE)
    0.714 m

    """
    return Length(to_exact(value) * ZERET_CHAZON_ISH.scale, ZERET_CHAZON_ISH)


def AmahChazonIsh(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in cubits (amot).

    Parameters
    ----------
    value : Numeric
        Length magnitude in cubits (amot).

    Returns
    -------
    Length
        Length represented in cubits (amot).

    Notes
    -----
    One amah is 2 zarot, 6 tefachim, or 24 etzba'ot.

    Uses the Chazon Ish's calibration: an etzba of 2.38 cm.

    Examples
    --------
    A museum's architectural model includes a three-amah span, measured using the
    Chazon Ish calibration:

    >>> from kuchka.units.length import METRE
    >>> architectural_span = AmahChazonIsh(3)
    >>> architectural_span.to(METRE)
    1.7136 m

    """
    return Length(to_exact(value) * AMAH_CHAZON_ISH.scale, AMAH_CHAZON_ISH)


def MilChazonIsh(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in miles (milin).

    Parameters
    ----------
    value : Numeric
        Length magnitude in miles (milin).

    Returns
    -------
    Length
        Length represented in miles (milin).

    Notes
    -----
    One mil is 2000 amot.

    Uses the Chazon Ish's calibration: an etzba of 2.38 cm.

    Examples
    --------
    An educational map represents a route of one and a half milin under the Chazon Ish
    calibration:

    >>> from kuchka.units.length import KILOMETRE
    >>> route = MilChazonIsh(1.5)
    >>> route.to(KILOMETRE)
    1.7136 km

    """
    return Length(to_exact(value) * MIL_CHAZON_ISH.scale, MIL_CHAZON_ISH)


def ParsaChazonIsh(value: Numeric) -> Length:
    """Construct length from a magnitude expressed in parasangs (parsa'ot).

    Parameters
    ----------
    value : Numeric
        Length magnitude in parasangs (parsa'ot).

    Returns
    -------
    Length
        Length represented in parasangs (parsa'ot).

    Notes
    -----
    One parsa is 4 milin, or 8000 amot.

    Uses the Chazon Ish's calibration: an etzba of 2.38 cm.

    Examples
    --------
    A study group maps a two-parsa journey described in a traditional travel account.
    Under the Chazon Ish calibration, the modeled distance is:

    >>> from kuchka.units.length import KILOMETRE
    >>> journey = ParsaChazonIsh(2)
    >>> journey.to(KILOMETRE)
    9.1392 km

    """
    return Length(to_exact(value) * PARSA_CHAZON_ISH.scale, PARSA_CHAZON_ISH)


HEBREW_LENGTH_UNITS: Mapping[str, Callable[[Numeric], Length]] = MappingProxyType(
    {
        ETZBA.symbol: Etzba,
        TEFACH.symbol: Tefach,
        ZERET.symbol: Zeret,
        AMAH.symbol: Amah,
        MIL.symbol: Mil,
        PARSA.symbol: Parsa,
        ETZBA_NAEH.symbol: EtzbaNaeh,
        TEFACH_NAEH.symbol: TefachNaeh,
        ZERET_NAEH.symbol: ZeretNaeh,
        AMAH_NAEH.symbol: AmahNaeh,
        MIL_NAEH.symbol: MilNaeh,
        PARSA_NAEH.symbol: ParsaNaeh,
        ETZBA_CHAZON_ISH.symbol: EtzbaChazonIsh,
        TEFACH_CHAZON_ISH.symbol: TefachChazonIsh,
        ZERET_CHAZON_ISH.symbol: ZeretChazonIsh,
        AMAH_CHAZON_ISH.symbol: AmahChazonIsh,
        MIL_CHAZON_ISH.symbol: MilChazonIsh,
        PARSA_CHAZON_ISH.symbol: ParsaChazonIsh,
    }
)
"""Constructors by symbol, for configuration files and external interfaces."""


__all__ = [
    "AMAH",
    "AMAH_CHAZON_ISH",
    "AMAH_NAEH",
    "ETZBA",
    "ETZBA_CHAZON_ISH",
    "ETZBA_NAEH",
    "HEBREW_LENGTH_UNITS",
    "MIL",
    "MIL_CHAZON_ISH",
    "MIL_NAEH",
    "PARSA",
    "PARSA_CHAZON_ISH",
    "PARSA_NAEH",
    "TEFACH",
    "TEFACH_CHAZON_ISH",
    "TEFACH_NAEH",
    "ZERET",
    "ZERET_CHAZON_ISH",
    "ZERET_NAEH",
    "Amah",
    "AmahChazonIsh",
    "AmahNaeh",
    "Etzba",
    "EtzbaChazonIsh",
    "EtzbaNaeh",
    "Mil",
    "MilChazonIsh",
    "MilNaeh",
    "Parsa",
    "ParsaChazonIsh",
    "ParsaNaeh",
    "Tefach",
    "TefachChazonIsh",
    "TefachNaeh",
    "Zeret",
    "ZeretChazonIsh",
    "ZeretNaeh",
]
