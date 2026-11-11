"""Historical Russian units of land area.

The modernized Russian system relates square units to a standardized sazhen of seven
English feet.
The principal land unit, the desyatina, had several historical definitions and must
therefore be qualified when precision matters.

+------------------------+--------------------------------+-------------------------------+-----------------------------------------+
| Unit                   | Russian name                   | Translation                   | Size                                    |
+------------------------+--------------------------------+-------------------------------+-----------------------------------------+
| `RussianSquareMile`    | квадратная миля                | Russian square mile           | 49 square verstas = 55.76504976 km²     |
| `SquareVersta`         | квадратная верста              | square verst                  | 250,000 square sazhens = 1.13806224 km² |
| `Desyatina`            | казённая десятина              | official / treasury desyatina | 2,400 square sazhens = 10,925.397504 m² |
| `VerstaDesyatina`      | десятина в одну десятую версты | early square desyatina        | 2,500 square sazhens = 11,380.6224 m²   |
| `ProprietorDesyatina`  | владельческая десятина         | proprietor's desyatina        | 3,200 square sazhens = 14,567.196672 m² |
| `KosayaDesyatina`      | хозяйственная косая десятина   | economic oblique desyatina    | 3,200 square sazhens = 14,567.196672 m² |
| `RoundDesyatina`       | хозяйственная круглая десятина | economic round desyatina      | 3,600 square sazhens = 16,388.096256 m² |
| `SotennayaDesyatina`   | сотенная десятина              | hundred-square desyatina      | 10,000 square sazhens = 45,522.4896 m²  |
| `BakhchevayaDesyatina` | бахчевая десятина              | melon-field desyatina         | 800 square sazhens = 3,641.799168 m²    |
| `Chet`                 | четь / четверть                | quarter (1,200 sq. sazhens)   | 1,200 square sazhens = 5,462.698752 m²  |
| `Chet1250`             | четь / четверть                | quarter (1,250 sq. sazhens)   | 1,250 square sazhens = 5,690.3112 m²    |
| `Chet1600`             | четь / четверть                | quarter (1,600 sq. sazhens)   | 1,600 square sazhens = 7,283.598336 m²  |
| `Osminnik`             | осьминник / осьмина            | eighth of a desyatina         | 300 square sazhens = 1,365.674688 m²    |
| `OsminnikSokha`        | осьминник (в статье о сохе)    | sokha-context osminnik        | 600 square sazhens = 2,731.349376 m²    |
| `SokhaQuarter`         | четверть для сохи              | sowing quarter (sokha)        | 600 square sazhens = 2,731.349376 m²    |
| `GovernmentSokha`      | служилая соха                  | service / government sokha    | 800 quarters = 2,185,079.5008 m²*       |
| `ChurchSokha`          | церковная соха                 | church sokha                  | 600 quarters = 1,638,809.6256 m²*       |
| `BlackSokha`           | чёрная соха                    | black / peasant sokha         | 400 quarters = 1,092,539.7504 m²*       |
| `SquareSazhen`         | квадратная сажень              | square sazhen                 | 9 square arshins = 49 square futs       |
| `SquareArshin`         | квадратный аршин               | square arshin                 | 256 square vershoks = 0.50580544 m²     |
| `SquareFut`            | квадратный фут                 | square foot (fut)             | 144 square dyuym = 0.09290304 m²        |
| `SquareVershok`        | квадратный вершок              | square vershok                | 3.0625 square dyuym = 19.758025 cm²     |
| `SquareDyuym`          | квадратный дюйм                | square inch (dyuym)           | 100 square liniya = 6.4516 cm²          |
| `SquareLiniya`         | квадратная линия               | square line (liniya)          | 1/100 square dyuym = 6.4516 mm²         |
+------------------------+--------------------------------+-------------------------------+-----------------------------------------+

The ordinary `Desyatina` constructor denotes the official desyatina of 2,400 square
sazhens, established by the 1753 land-survey instruction.
Other variants include:
- the early square desyatina of 2,500 square sazhens,
- the proprietor's / economic oblique desyatina (3,200),
- the economic round desyatina (3,600),
- the sotennaya desyatina (10,000),
- and the bakhchevaya desyatina (800 square sazhens).
The early square desyatina was defined as a square with sides one tenth of a versta.
`ProprietorDesyatina` and `KosayaDesyatina` intentionally remain separate named
definitions despite having the same scale.

The area unit `Chet` is one half of the official desyatina.
The sources also record chet variants of 1,250 square sazhens
(half of a 2,500-square-sazhendesyatina) and 1,600 square sazhens
(half of a 3,200-square-sazhen desyatina).
`Chetvert` is a parallel name for `Chet`.

`Osminnik` is the 300-square-sazhen unit in the Russian system's general area table.
`Osmina` is its parallel name.
The sokha account also uses an osminnik-sized term at 600 square sazhens.
This contextual variant is exposed as `OsminnikSokha` and stays separate from the
standard `Osminnik`.

A *sokha* was primarily a land-tax assessment unit, and its area varied.
For the three named categories, this module follows the sokha article's best-land
calibration: 800, 600, or 400 sowing quarters, each taken as 600 standardized
square sazhens (2,731.349376 m²).
This is deliberately represented by the separate `SokhaQuarter` definition.
The source also says that two such quarters equalled a desyatina, which conflicts with
the standardized official desyatina of 2,400 square sazhens.
Therefore these sokha definitions encode the selected area calibration only.
Historical usage varied across periods, and a tax assessment follows its own record.
Land quality and period could change the area represented by a sokha.

The metric values above are exact consequences of the standardized length scales;
historical surveys used scales of their own.
In particular, `SquareVersta` uses the 500-sazhen versta and `RussianSquareMile` uses
the Russian seven-versta mile.

Examples
--------
A Russian square mile is the square of a seven-versta Russian mile, which makes it far
larger than an English square mile:

>>> RussianSquareMile(1) == SquareVersta(49)
True
>>> SquareVersta(1) == SquareSazhen(250_000)
True

Three proprietor's desyatinas cover the same area as four official desyatinas:

>>> ProprietorDesyatina(3) == Desyatina(4)
True
>>> KosayaDesyatina(1) == ProprietorDesyatina(1)
True

A land register may use a round desyatina or the much larger sotennaya variant:

>>> RoundDesyatina(1) == SquareSazhen(3600)
True
>>> SotennayaDesyatina(1) == SquareSazhen(10_000)
True

An estate register can combine areas recorded in different units, each line kept as
written:

>>> estate = Desyatina(12) + Chet(6) + Osminnik(4)
>>> estate == SquareSazhen(37_200)
True

The named chet variants preserve the sizes associated with different calibrations of
the desyatina:

>>> Chet(1) == Desyatina(1) / 2
True
>>> Chet1600(1) == ProprietorDesyatina(1) / 2
True
>>> Chetvert(1) == Chet(1)
True

The standard osminnik is one eighth of an official desyatina.
The sokha article's sowing quarter has a different scale, so keep the two explicit:

>>> Osminnik(1) == Desyatina(1) / 8
True
>>> SokhaQuarter(2) == Chet(1)
True

A government sokha represents 800 of the selected sokha quarters.
This is a historical modelling convention, and land and tax assessments followed
their own records:

>>> GovernmentSokha(1) == SokhaQuarter(800)
True
>>> ChurchSokha(1) == SokhaQuarter(600)
True
>>> BlackSokha(1) == SokhaQuarter(400)
True

The square units are derived from the length definitions, so their exact ratios remain
consistent:

>>> SquareSazhen(1) == SquareArshin(9)
True
>>> SquareSazhen(1) == SquareFut(49)
True
>>> SquareArshin(1) == SquareVershok(256)
True
>>> SquareFut(1) == SquareDyuym(144)
True
>>> SquareDyuym(1) == SquareLiniya(100)
True

Notes
-----
`RUSSIAN_AREA_UNITS` is a read-only `UnitTable` that resolves each unit by its display
symbol, symbol aliases, and registered words.
The public constructor aliases provide familiar Python spellings for parallel
historical names.

References
----------
- https://ru.wikipedia.org/wiki/Русская_система_мер
- https://ru.wikipedia.org/wiki/Десятина_(мера_площади)
- https://ru.wikipedia.org/wiki/Четверть_(единица_площади)
- https://ru.wikipedia.org/wiki/Соха_(единица_измерения)

See Also
--------
~kuchka.quantities.Area
    The quantity every constructor in this module builds.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import AREA
from kuchka.internal import symbols
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Area
from kuchka.quantities import UnitDef
from kuchka.quantities.base.units import extend_units
from kuchka.units.archaic.russian.length import ARSHIN
from kuchka.units.archaic.russian.length import DYUYM
from kuchka.units.archaic.russian.length import FUT
from kuchka.units.archaic.russian.length import LINIYA
from kuchka.units.archaic.russian.length import SAZHEN
from kuchka.units.archaic.russian.length import VERSHOK
from kuchka.units.archaic.russian.length import VERSTA

if TYPE_CHECKING:
    from collections.abc import Callable

    from kuchka.internal.unit_table import SpelledUnit


_TWO = symbols.SUPERSCRIPT_TWO
_SQUARE_SAZHEN_SCALE = SAZHEN.scale**2


# Large square units. A Russian mile is seven verstas.
SQUARE_RUSSIAN_MILE = UnitDef(
    "square_russian_mile",
    f"rus. mi{_TWO}",
    49 * VERSTA.scale**2,
    AREA,
    aliases=("kv. milya", "кв. миля", "кв. мили"),
    words=(
        "square Russian mile",
        "square Russian miles",
        "kvadratnaya milya",
        "kvadratnaya milia",
        "квадратная миля",
    ),
)

SQUARE_VERSTA = UnitDef(
    "square_versta",
    f"versta{_TWO}",
    VERSTA.scale**2,
    AREA,
    aliases=("kv. versta", "кв. верста", "кв. вёрста"),
    words=(
        "square verst",
        "square versts",
        "kvadratnaya versta",
        "kvadratnaya vyorsta",
        "квадратная верста",
    ),
)


# Square subunits, composed directly from the corresponding Russian lengths.
SQUARE_SAZHEN = UnitDef(
    "square_sazhen",
    f"sazhen{_TWO}",
    SAZHEN.scale**2,
    AREA,
    aliases=("sq. sazhen", "sq. sazhens", "кв. сажень", "кв. саж."),
    words=(
        "square sazhen",
        "square sazhens",
        "square sazheni",
        "kvadratnaya sazhen",
        "квадратная сажень",
    ),
)

SQUARE_ARSHIN = UnitDef(
    "square_arshin",
    f"arshin{_TWO}",
    ARSHIN.scale**2,
    AREA,
    aliases=("sq. arshin", "кв. аршин", "кв. арш."),
    words=(
        "square arshin",
        "square arshins",
        "kvadratny arshin",
        "квадратный аршин",
    ),
)

SQUARE_FUT = UnitDef(
    "square_fut",
    f"fut{_TWO}",
    FUT.scale**2,
    AREA,
    aliases=("sq. fut", "кв. фут", "кв. фут."),
    words=(
        "square fut",
        "square foot (Russian standard)",
        "square feet (Russian standard)",
        "kvadratny fut",
        "квадратный фут",
    ),
)

SQUARE_VERSHOK = UnitDef(
    "square_vershok",
    f"vershok{_TWO}",
    VERSHOK.scale**2,
    AREA,
    aliases=("sq. vershok", "кв. вершок", "кв. верш."),
    words=(
        "square vershok",
        "square vershoks",
        "kvadratny vershok",
        "квадратный вершок",
    ),
)

SQUARE_DYUYM = UnitDef(
    "square_dyuym",
    f"dyuym{_TWO}",
    DYUYM.scale**2,
    AREA,
    aliases=("sq. dyuym", "кв. дюйм", "кв. дюйм."),
    words=(
        "square dyuym",
        "square inch (Russian standard)",
        "square inches (Russian standard)",
        "kvadratny dyuym",
        "квадратный дюйм",
    ),
)

SQUARE_LINIYA = UnitDef(
    "square_liniya",
    f"liniya{_TWO}",
    LINIYA.scale**2,
    AREA,
    aliases=("sq. liniya", "кв. линия", "кв. лин."),
    words=(
        "square liniya",
        "square liniyi",
        "square line (Russian measure)",
        "kvadratnaya liniya",
        "квадратная линия",
    ),
)


# Desyatina variants: all scales derive from the standardized square sazhen.


DESYATINA = UnitDef(
    "desyatina",
    "desyatina",
    2400 * _SQUARE_SAZHEN_SCALE,
    AREA,
    aliases=("des.", "дес."),
    words=(
        "desiatina",
        "dessiatin",
        "dessiatine",
        "official desyatina",
        "treasury desyatina",
        "kazyonnaya desyatina",
        "kazennaya desyatina",
        "казённая десятина",
        "казенная десятина",
    ),
)

VERSTA_DESYATINA = UnitDef(
    "versta_desyatina",
    "desyatina (1/10 versta square)",
    2500 * _SQUARE_SAZHEN_SCALE,
    AREA,
    aliases=("des. (versta square)",),
    words=(
        "versta desyatina",
        "old desyatina",
        "original desyatina",
        "square desyatina of 2500 square sazhens",
        "desyatina with sides of one tenth of a versta",
        "десятина в одну десятую версты",
        "десятина 2500 квадратных саженей",
    ),
)
"""The early Desyatina.

A square one tenth of a versta on each side:
50 sazhens by 50 sazhens = 2,500 square sazhens.
"""


PROPRIETOR_DESYATINA = UnitDef(
    "proprietor_desyatina",
    "desyatina (proprietor)",
    3200 * _SQUARE_SAZHEN_SCALE,
    AREA,
    aliases=("des. (proprietor)",),
    words=(
        "proprietor's desyatina",
        "proprietors desyatina",
        "vladel'cheskaya desyatina",
        "vladelcheskaya desyatina",
        "vladel'cheskaya desiatina",
        "владельческая десятина",
    ),
)

# Same area as the proprietor's desyatina, retained as a separate named unit.
KOSAYA_DESYATINA = UnitDef(
    "kosaya_desyatina",
    "desyatina (kosaya)",
    3200 * _SQUARE_SAZHEN_SCALE,
    AREA,
    aliases=("des. (kosaya)", "хоз. косая дес."),
    words=(
        "kosaya desyatina",
        "economic oblique desyatina",
        "hozyaystvennaya kosaya desyatina",
        "khozyaystvennaya kosaya desyatina",
        "хозяйственная косая десятина",
    ),
)

ROUND_DESYATINA = UnitDef(
    "round_desyatina",
    "desyatina (round)",
    3600 * _SQUARE_SAZHEN_SCALE,
    AREA,
    aliases=("des. (round)", "хоз. круглая дес."),
    words=(
        "round desyatina",
        "circular desyatina",
        "hozyaystvennaya kruglaya desyatina",
        "khozyaystvennaya kruglaya desyatina",
        "хозяйственная круглая десятина",
    ),
)

SOTENNAYA_DESYATINA = UnitDef(
    "sotennaya_desyatina",
    "desyatina (sotennaya)",
    10_000 * _SQUARE_SAZHEN_SCALE,
    AREA,
    aliases=("des. (sotennaya)",),
    words=(
        "sotennaya desyatina",
        "hundred-square desyatina",
        "сотенная десятина",
    ),
)

BAKHCHEVAYA_DESYATINA = UnitDef(
    "bakhchevaya_desyatina",
    "desyatina (bakhchevaya)",
    800 * _SQUARE_SAZHEN_SCALE,
    AREA,
    aliases=("des. (bakhchevaya)",),
    words=(
        "bakhchevaya desyatina",
        "bakchevaya desyatina",
        "melon-field desyatina",
        "бахчевая десятина",
    ),
)


# Chet / chetvert has several documented calibrations.


CHET = UnitDef(
    "chet",
    "chet",
    1200 * _SQUARE_SAZHEN_SCALE,
    AREA,
    words=(
        "chetvert",
        "quarter",
        "чет",
        "четверть",
        "четь",
    ),
)

CHET_1250 = UnitDef(
    "chet_1250",
    "chet (1250 sazhen²)",
    1250 * _SQUARE_SAZHEN_SCALE,
    AREA,
    aliases=("чет (1250 кв. саж.)",),
    words=(
        "chet 1250",
        "chetvert 1250",
        "quarter of a 2500-square-sazhen desyatina",
        "четь 1250 квадратных саженей",
    ),
)

CHET_1600 = UnitDef(
    "chet_1600",
    "chet (1600 sazhen²)",
    1600 * _SQUARE_SAZHEN_SCALE,
    AREA,
    aliases=("чет (1600 кв. саж.)",),
    words=(
        "chet 1600",
        "chetvert 1600",
        "quarter of a 3200-square-sazhen desyatina",
        "четь 1600 квадратных саженей",
    ),
)


# The standardized area table gives an osminnik as 1/8 desyatina.
# A different 600-square-sazhen sowing quarter is kept separate for the sokha
# convention.
OSMINNIK = UnitDef(
    "osminnik",
    "osminnik",
    300 * _SQUARE_SAZHEN_SCALE,
    AREA,
    aliases=("осм.", "осьм."),
    words=(
        "osmina",
        "os'mina",
        "осьминник",
        "осьмина",
    ),
)

SOKHA_QUARTER = UnitDef(
    "sokha_quarter",
    "quarter (sokha)",
    600 * _SQUARE_SAZHEN_SCALE,
    AREA,
    aliases=("кв. сох.",),
    words=(
        "sokha quarter",
        "sokha sowing quarter",
        "sowing quarter in a sokha assessment",
        "quarter of sown land (sokha convention)",
        "четверть (соха)",
        "четверть пашенной земли в сохе",
    ),
)


OSMINNIK_SOKHA = UnitDef(
    "osminnik_sokha",
    "osminnik (sokha)",
    600 * _SQUARE_SAZHEN_SCALE,
    AREA,
    aliases=("осьм. (соха)",),
    words=(
        "osmina (sokha)",
        "osminnik in the sokha account",
        "osmina in the sokha account",
        "sokha-context osminnik",
        "осьминник (соха)",
        "осьминник в системе сохи",
        "осьмина в системе сохи",
    ),
)


# A sokha was an assessment class based on the amount and quality of land.
# These area values use the 600-square-sazhen SokhaQuarter calibration above.
GOVERNMENT_SOKHA = UnitDef(
    "government_sokha",
    "sokha (government)",
    800 * SOKHA_QUARTER.scale,
    AREA,
    aliases=("соха (служ.)",),
    words=(
        "government sokha",
        "service sokha",
        "sluzhilaya sokha",
        "sluzhilaya soha",
        "служилая соха",
    ),
)

CHURCH_SOKHA = UnitDef(
    "church_sokha",
    "sokha (church)",
    600 * SOKHA_QUARTER.scale,
    AREA,
    aliases=("соха (церк.)",),
    words=(
        "church sokha",
        "tserkovnaya sokha",
        "cerkovnaya sokha",
        "церковная соха",
    ),
)

BLACK_SOKHA = UnitDef(
    "black_sokha",
    "sokha (black)",
    400 * SOKHA_QUARTER.scale,
    AREA,
    aliases=("соха (чёрн.)",),
    words=(
        "black sokha",
        "peasant sokha",
        "chernaya sokha",
        "chornaya sokha",
        "чёрная соха",
        "черная соха",
    ),
)


def _construct(value: Numeric, unit: UnitDef) -> Area:
    """Build an Area using the exact scale defined by ``unit``."""
    return Area(to_exact(value) * unit.scale, unit)


def RussianSquareMile(value: Numeric) -> Area:
    """Construct area in Russian square miles (49 square verstas).

    Parameters
    ----------
    value : Numeric
        Area magnitude in Russian square miles.

    Returns
    -------
    Area
        Area represented in Russian square miles.

    Notes
    -----
    One Russian mile is seven verstas.
    Its square is therefore 49 square verstas, which makes it far larger than an English
    square mile.

    Examples
    --------
    A district map records a forest reserve of one Russian square mile and another
    seven square verstas of pasture:

    >>> district = RussianSquareMile(1) + SquareVersta(7)
    >>> district == SquareVersta(56)
    True

    """
    return _construct(value, SQUARE_RUSSIAN_MILE)


def SquareVersta(value: Numeric) -> Area:
    """Construct area in square verstas.

    Parameters
    ----------
    value : Numeric
        Area magnitude in square verstas.

    Returns
    -------
    Area
        Area represented in square verstas.

    Notes
    -----
    One standardized versta is 500 sazhens, making one square versta 250,000
    square sazhens.

    Examples
    --------
    A survey map groups six one-square-versta blocks into a single reserve:

    >>> reserve = SquareVersta(3 * 2)
    >>> reserve == SquareSazhen(1_500_000)
    True

    """
    return _construct(value, SQUARE_VERSTA)


def SquareSazhen(value: Numeric) -> Area:
    """Construct area in square sazhens.

    Parameters
    ----------
    value : Numeric
        Area magnitude in square sazhens.

    Returns
    -------
    Area
        Area represented in square sazhens.

    Notes
    -----
    One square sazhen is nine square arshins or 49 square futs.

    Examples
    --------
    A rye field measuring 40 by 30 sazhens was a traditional one-chet plot:

    >>> rye_field = SquareSazhen(40 * 30)
    >>> rye_field == Chet(1)
    True

    """
    return _construct(value, SQUARE_SAZHEN)


def SquareArshin(value: Numeric) -> Area:
    """Construct area in square arshins.

    Parameters
    ----------
    value : Numeric
        Area magnitude in square arshins.

    Returns
    -------
    Area
        Area represented in square arshins.

    Notes
    -----
    One arshin is 16 vershoks, or 28 inches, so one square arshin contains
    256 square vershoks.

    Examples
    --------
    A dyer's workshop floor is recorded as 18 by 12 arshins:

    >>> workshop_floor = SquareArshin(18 * 12)
    >>> workshop_floor == SquareSazhen(24)
    True

    """
    return _construct(value, SQUARE_ARSHIN)


def SquareFut(value: Numeric) -> Area:
    """Construct area in square futs (Russian-standardized square feet).

    Parameters
    ----------
    value : Numeric
        Area magnitude in square futs.

    Returns
    -------
    Area
        Area represented in square futs.

    Notes
    -----
    One sazhen is seven futs, so one square sazhen contains 49 square futs.

    Examples
    --------
    An old flooring account lists a hall measuring 14 by 7 futs:

    >>> hall_floor = SquareFut(14 * 7)
    >>> hall_floor == SquareSazhen(2)
    True

    """
    return _construct(value, SQUARE_FUT)


def SquareVershok(value: Numeric) -> Area:
    """Construct area in square vershoks.

    Parameters
    ----------
    value : Numeric
        Area magnitude in square vershoks.

    Returns
    -------
    Area
        Area represented in square vershoks.

    Notes
    -----
    One vershok is 1.75 inches, making one square vershok 3.0625 square dyuym.

    Examples
    --------
    A cabinetmaker cuts a square of decorative veneer 16 vershoks on each side:

    >>> veneer = SquareVershok(16 * 16)
    >>> veneer == SquareArshin(1)
    True

    """
    return _construct(value, SQUARE_VERSHOK)


def SquareDyuym(value: Numeric) -> Area:
    """Construct area in square dyuym (square inches).

    Parameters
    ----------
    value : Numeric
        Area magnitude in square dyuym.

    Returns
    -------
    Area
        Area represented in square dyuym.

    Notes
    -----
    One square dyuym contains 100 square liniya because one liniya is one tenth of a
    dyuym.

    Examples
    --------
    An engraver orders a metal plate measuring 12 by 6 dyuym:

    >>> plate = SquareDyuym(12 * 6)
    >>> plate == SquareFut(1) / 2
    True

    """
    return _construct(value, SQUARE_DYUYM)


def SquareLiniya(value: Numeric) -> Area:
    """Construct area in square liniya (square lines).

    Parameters
    ----------
    value : Numeric
        Area magnitude in square liniya.

    Returns
    -------
    Area
        Area represented in square liniya.

    Notes
    -----
    A liniya is one tenth of a dyuym; squaring the length ratio gives
    100 square liniya per square dyuym.

    Examples
    --------
    An instrument maker lays out a fine engraving 10 liniya wide and high:

    >>> engraving = SquareLiniya(10 * 10)
    >>> engraving == SquareDyuym(1)
    True

    """
    return _construct(value, SQUARE_LINIYA)


def Desyatina(value: Numeric) -> Area:
    """Construct area in official (treasury) desyatinas.

    Parameters
    ----------
    value : Numeric
        Area magnitude in official desyatinas.

    Returns
    -------
    Area
        Area represented in official desyatinas.

    Notes
    -----
    The 1753 land-survey instruction fixed the official desyatina at 2,400
    square sazhens.
    Other historical variants have separate constructors.

    Examples
    --------
    An estate register records 18 official desyatinas and two cheti:

    >>> registered_area = Desyatina(18) + Chet(2)
    >>> registered_area == Desyatina(19)
    True

    """
    return _construct(value, DESYATINA)


def VerstaDesyatina(value: Numeric) -> Area:
    """Construct area in the early square desyatina of 2,500 square sazhens.

    Parameters
    ----------
    value : Numeric
        Area magnitude in early square desyatinas.

    Returns
    -------
    Area
        Area represented in early square desyatinas.

    Notes
    -----
    This variant is described as a square with sides one tenth of a versta.
    With a standardized versta of 500 sazhens, each side is 50 sazhens.

    Examples
    --------
    A cadastral plan marks a plot one tenth of a versta on each side:

    >>> plot = VerstaDesyatina(1)
    >>> plot == SquareSazhen(50 * 50)
    True

    """
    return _construct(value, VERSTA_DESYATINA)


def ProprietorDesyatina(value: Numeric) -> Area:
    """Construct area in proprietor's desyatinas (3,200 square sazhens).

    Parameters
    ----------
    value : Numeric
        Area magnitude in proprietor's desyatinas.

    Returns
    -------
    Area
        Area represented in proprietor's desyatinas.

    Notes
    -----
    Three proprietor's desyatinas have the same area as four official desyatinas.

    Examples
    --------
    A deed records three proprietor's desyatinas plus one official desyatina:

    >>> deed_area = ProprietorDesyatina(3) + Desyatina(1)
    >>> deed_area == Desyatina(5)
    True

    """
    return _construct(value, PROPRIETOR_DESYATINA)


def KosayaDesyatina(value: Numeric) -> Area:
    """Construct area in economic oblique desyatinas (3,200 square sazhens).

    Parameters
    ----------
    value : Numeric
        Area magnitude in economic oblique desyatinas.

    Returns
    -------
    Area
        Area represented in economic oblique desyatinas.

    Notes
    -----
    The economic oblique desyatina is recorded as a plot 80 by 40 sazhens.
    It shares the proprietor's desyatina scale but retains its historical name.

    Examples
    --------
    A surveyor transcribes an oblique desyatina from an 80-by-40-sazhen plan:

    >>> field = KosayaDesyatina(1)
    >>> field == SquareSazhen(80 * 40)
    True

    """
    return _construct(value, KOSAYA_DESYATINA)


def RoundDesyatina(value: Numeric) -> Area:
    """Construct area in economic round desyatinas (3,600 square sazhens).

    Parameters
    ----------
    value : Numeric
        Area magnitude in economic round desyatinas.

    Returns
    -------
    Area
        Area represented in economic round desyatinas.

    Notes
    -----
    The recorded dimensions are 60 by 60 sazhens.
    The surveyed plot itself was a square, whatever its historical name suggests.

    Examples
    --------
    A land account identifies the 60-by-60-sazhen variant:

    >>> round_plot = RoundDesyatina(1)
    >>> round_plot == SquareSazhen(60 * 60)
    True

    """
    return _construct(value, ROUND_DESYATINA)


def SotennayaDesyatina(value: Numeric) -> Area:
    """Construct area in sotennaya desyatinas (10,000 square sazhens).

    Parameters
    ----------
    value : Numeric
        Area magnitude in sotennaya desyatinas.

    Returns
    -------
    Area
        Area represented in sotennaya desyatinas.

    Notes
    -----
    The name denotes a 100-by-100-sazhen plot.

    Examples
    --------
    A boundary plan reserves a square 100 sazhens on each side:

    >>> reserved_land = SotennayaDesyatina(1)
    >>> reserved_land == SquareSazhen(100 * 100)
    True

    """
    return _construct(value, SOTENNAYA_DESYATINA)


def BakhchevayaDesyatina(value: Numeric) -> Area:
    """Construct area in bakhchevaya (melon-field) desyatinas.

    Parameters
    ----------
    value : Numeric
        Area magnitude in bakhchevaya desyatinas.

    Returns
    -------
    Area
        Area represented in bakhchevaya desyatinas.

    Notes
    -----
    The cited definition is a plot 80 by 10 sazhens, or 800 square sazhens.

    Examples
    --------
    A market gardener's melon patch is entered in the ledger as 80 by 10 sazhens:

    >>> melon_patch = BakhchevayaDesyatina(1)
    >>> melon_patch == SquareSazhen(80 * 10)
    True

    """
    return _construct(value, BAKHCHEVAYA_DESYATINA)


def Chet(value: Numeric) -> Area:
    """Construct area in cheti using the 1,200-square-sazhen calibration.

    Parameters
    ----------
    value : Numeric
        Area magnitude in cheti.

    Returns
    -------
    Area
        Area represented in the 1,200-square-sazhen chet.

    Notes
    -----
    `Chetvert` is a parallel constructor name.
    Historical sources also record cheti of 1,250 or 1,600 square sazhens.
    Those have separate constructors.

    Examples
    --------
    A rye plot measuring 40 by 30 sazhens is one chet under this calibration:

    >>> rye_plot = Chet(1)
    >>> rye_plot == SquareSazhen(40 * 30)
    True

    """
    return _construct(value, CHET)


def Chet1250(value: Numeric) -> Area:
    """Construct area in the 1,250-square-sazhen chet calibration.

    Parameters
    ----------
    value : Numeric
        Area magnitude in cheti of 1,250 square sazhens.

    Returns
    -------
    Area
        Area represented in the 1,250-square-sazhen chet.

    Notes
    -----
    This chet is half of the early 2,500-square-sazhen desyatina.

    Examples
    --------
    An early cadastral entry records the 2,500-square-sazhen desyatina as two cheti
    under this calibration:

    >>> VerstaDesyatina(1) == Chet1250(2)
    True

    """
    return _construct(value, CHET_1250)


def Chet1600(value: Numeric) -> Area:
    """Construct area in the 1,600-square-sazhen chet calibration.

    Parameters
    ----------
    value : Numeric
        Area magnitude in cheti of 1,600 square sazhens.

    Returns
    -------
    Area
        Area represented in the 1,600-square-sazhen chet.

    Notes
    -----
    This chet is half of the 3,200-square-sazhen proprietor's / oblique desyatina.

    Examples
    --------
    A proprietor's holding is divided into two equal cheti:

    >>> ProprietorDesyatina(1) == Chet1600(2)
    True

    """
    return _construct(value, CHET_1600)


def Osminnik(value: Numeric) -> Area:
    """Construct area in osminniki of 300 square sazhens.

    Parameters
    ----------
    value : Numeric
        Area magnitude in standard osminniki.

    Returns
    -------
    Area
        Area represented in standard osminniki.

    Notes
    -----
    This is the one-eighth-desyatina size in the general Russian area table.
    The differently sized sokha-context term is represented by `OsminnikSokha`.

    Examples
    --------
    A steward divides an official desyatina into eight equal parcels:

    >>> parcels = Osminnik(8)
    >>> parcels == Desyatina(1)
    True

    """
    return _construct(value, OSMINNIK)


def SokhaQuarter(value: Numeric) -> Area:
    """Construct area in the 600-square-sazhen sokha sowing-quarter convention.

    Parameters
    ----------
    value : Numeric
        Area magnitude in sowing quarters under the selected sokha convention.

    Returns
    -------
    Area
        Area represented in sokha sowing quarters.

    Notes
    -----
    The source descriptions use *quarter* for several land-area and sowing measures.
    This named unit preserves the 600-square-sazhen calibration selected for the sokha
    account and stays apart from the 1,200-square-sazhen `Chet`.

    Examples
    --------
    An archival sowing ledger records two sokha quarters of rye land:

    >>> sowing_land = SokhaQuarter(2)
    >>> sowing_land == Chet(1)
    True

    """
    return _construct(value, SOKHA_QUARTER)


def OsminnikSokha(value: Numeric) -> Area:
    """Construct the 600-square-sazhen osminnik variant used in a sokha account.

    Parameters
    ----------
    value : Numeric
        Area magnitude in sokha-context osminniki.

    Returns
    -------
    Area
        Area represented in sokha-context osminniki.

    Notes
    -----
    This is distinct from the 300-square-sazhen osminnik in the general area table,
    despite the parallel historical name.

    Examples
    --------
    A historian transcribes a sokha-era record that calls a 600-square-sazhen patch an
    osminnik:

    >>> archival_plot = OsminnikSokha(1)
    >>> archival_plot == Osminnik(2)
    True

    """
    return _construct(value, OSMINNIK_SOKHA)


def GovernmentSokha(value: Numeric) -> Area:
    """Construct the area equivalent of service / government sokhas.

    Parameters
    ----------
    value : Numeric
        Number of government sokhas under the selected best-land calibration.

    Returns
    -------
    Area
        Area represented by government sokhas under that calibration.

    Notes
    -----
    The model uses 800 `SokhaQuarter` units per government sokha.
    A sokha was a land-tax assessment class, and its area varied.
    Period and land quality matter when interpreting a historical record.

    Examples
    --------
    An estate register lists three government sokhas under this model:

    >>> assessed_estate = GovernmentSokha(3)
    >>> assessed_estate == SokhaQuarter(2400)
    True

    """
    return _construct(value, GOVERNMENT_SOKHA)


def ChurchSokha(value: Numeric) -> Area:
    """Construct the area equivalent of church sokhas.

    Parameters
    ----------
    value : Numeric
        Number of church sokhas under the selected best-land calibration.

    Returns
    -------
    Area
        Area represented by church sokhas under that calibration.

    Notes
    -----
    The model uses 600 `SokhaQuarter` units per church sokha.
    This is one historical area convention among those of a tax sokha.

    Examples
    --------
    Under the selected convention, a government sokha exceeds a church sokha by
    200 sowing quarters:

    >>> GovernmentSokha(1) - ChurchSokha(1) == SokhaQuarter(200)
    True

    """
    return _construct(value, CHURCH_SOKHA)


def BlackSokha(value: Numeric) -> Area:
    """Construct the area equivalent of black / peasant sokhas.

    Parameters
    ----------
    value : Numeric
        Number of black sokhas under the selected best-land calibration.

    Returns
    -------
    Area
        Area represented by black sokhas under that calibration.

    Notes
    -----
    The model uses 400 `SokhaQuarter` units per black sokha.
    The category name and conversion belong to a particular historical classification.
    A land-tax rule of any period follows its own records.

    Examples
    --------
    In the selected best-land model, two black sokhas match one government sokha in
    area:

    >>> GovernmentSokha(1) == BlackSokha(2)
    True

    """
    return _construct(value, BLACK_SOKHA)


# Public parallel names and transliteration variants. These spellings denote
# exactly the same named unit and therefore reuse the same constructor object.
Chetvert = Chet
Osmina = Osminnik
OldDesyatina = VerstaDesyatina
KazyonnayaDesyatina = Desyatina
KazennayaDesyatina = Desyatina
VladelcheskayaDesyatina = ProprietorDesyatina
ServiceSokha = GovernmentSokha
SluzhilayaSokha = GovernmentSokha
OsminaSokha = OsminnikSokha
TserkovnayaSokha = ChurchSokha
ChernayaSokha = BlackSokha
ChornayaSokha = BlackSokha


_UNIT_CONSTRUCTORS: dict[SpelledUnit, Callable[[Numeric], Area]] = {
    SQUARE_RUSSIAN_MILE: RussianSquareMile,
    SQUARE_VERSTA: SquareVersta,
    SQUARE_SAZHEN: SquareSazhen,
    SQUARE_ARSHIN: SquareArshin,
    SQUARE_FUT: SquareFut,
    SQUARE_VERSHOK: SquareVershok,
    SQUARE_DYUYM: SquareDyuym,
    SQUARE_LINIYA: SquareLiniya,
    DESYATINA: Desyatina,
    VERSTA_DESYATINA: VerstaDesyatina,
    PROPRIETOR_DESYATINA: ProprietorDesyatina,
    KOSAYA_DESYATINA: KosayaDesyatina,
    ROUND_DESYATINA: RoundDesyatina,
    SOTENNAYA_DESYATINA: SotennayaDesyatina,
    BAKHCHEVAYA_DESYATINA: BakhchevayaDesyatina,
    CHET: Chet,
    CHET_1250: Chet1250,
    CHET_1600: Chet1600,
    OSMINNIK: Osminnik,
    SOKHA_QUARTER: SokhaQuarter,
    OSMINNIK_SOKHA: OsminnikSokha,
    GOVERNMENT_SOKHA: GovernmentSokha,
    CHURCH_SOKHA: ChurchSokha,
    BLACK_SOKHA: BlackSokha,
}

RUSSIAN_AREA_UNITS = unit_table("RUSSIAN_AREA_UNITS", _UNIT_CONSTRUCTORS)
"""Constructors by symbol, alias, or registered word for boundary code."""

# Importing this module makes Area display in the units of its table.
extend_units(Area, RUSSIAN_AREA_UNITS)


__all__ = [
    "BAKHCHEVAYA_DESYATINA",
    "BLACK_SOKHA",
    "CHET",
    "CHET_1250",
    "CHET_1600",
    "CHURCH_SOKHA",
    "DESYATINA",
    "GOVERNMENT_SOKHA",
    "KOSAYA_DESYATINA",
    "OSMINNIK",
    "OSMINNIK_SOKHA",
    "PROPRIETOR_DESYATINA",
    "ROUND_DESYATINA",
    "RUSSIAN_AREA_UNITS",
    "SOKHA_QUARTER",
    "SOTENNAYA_DESYATINA",
    "SQUARE_ARSHIN",
    "SQUARE_DYUYM",
    "SQUARE_FUT",
    "SQUARE_LINIYA",
    "SQUARE_RUSSIAN_MILE",
    "SQUARE_SAZHEN",
    "SQUARE_VERSHOK",
    "SQUARE_VERSTA",
    "VERSTA_DESYATINA",
    "BakhchevayaDesyatina",
    "BlackSokha",
    "ChernayaSokha",
    "Chet",
    "Chet1250",
    "Chet1600",
    "Chetvert",
    "ChornayaSokha",
    "ChurchSokha",
    "Desyatina",
    "GovernmentSokha",
    "KazennayaDesyatina",
    "KazyonnayaDesyatina",
    "KosayaDesyatina",
    "OldDesyatina",
    "Osmina",
    "OsminaSokha",
    "Osminnik",
    "OsminnikSokha",
    "ProprietorDesyatina",
    "RoundDesyatina",
    "RussianSquareMile",
    "ServiceSokha",
    "SluzhilayaSokha",
    "SokhaQuarter",
    "SotennayaDesyatina",
    "SquareArshin",
    "SquareDyuym",
    "SquareFut",
    "SquareLiniya",
    "SquareSazhen",
    "SquareVershok",
    "SquareVersta",
    "TserkovnayaSokha",
    "VerstaDesyatina",
    "VladelcheskayaDesyatina",
]
