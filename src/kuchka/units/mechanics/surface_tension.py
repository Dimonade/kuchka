"""Surface tension constructors: N/m, mN/m, kN/m, and dyn/cm.

`SurfaceTension` is a force along a line, `Force / Length`, which is also an energy on a
surface, `Energy / Area`.
Its canonical unit is the newton per metre (`N/m`), which is one joule per square metre.
The module provides `NewtonPerMetre`, its prefixes `MillinewtonPerMetre` and
`KilonewtonPerMetre`, and `DynePerCentimetre`, the CGS unit.

A water surface that pulls on a contact line with 72 mN/m and a coil spring that
pushes back with 25 kN/m share a dimension, and one type reads both:

>>> from kuchka import KilonewtonPerMetre
>>> from kuchka import MillinewtonPerMetre
>>> water = MillinewtonPerMetre(72)
>>> spring = KilonewtonPerMetre(25)
>>> water
72 mN/m

The units cover the interfaces of liquids and the stiffness of structures:

* millinewtons per metre (mN/m) and dynes per centimetre (dyn/cm) describe the surface
  tension of liquids, from ethanol at about 22 mN/m through water at about 72 mN/m to
  mercury at about 485 mN/m, in tensiometry, coatings, inkjet printing, and
  microfluidics;
* newtons per metre (N/m) are the spring constants of laboratory springs, balances, and
  the cantilevers of atomic force microscopes, which run from 0.01 N/m to tens of N/m;
* kilonewtons per metre (kN/m) are the stiffness of a vehicle's coil springs, and the
  line loads that walls and tracks put on beams.

Examples
--------
A Wilhelmy plate hangs from a balance and dips into a liquid, which pulls it down along
its whole wetted perimeter.
A plate with a 40 mm perimeter in water is pulled with a force of 2.88 mN, assuming the
liquid wets it completely:

>>> from kuchka import Millimetre
>>> from kuchka.units import MILLINEWTON
>>> (water * Millimetre(40)).to(MILLINEWTON)
2.88 mN

The same quantity is the energy it costs to make a surface.
Opening one square metre of fresh water surface takes 0.072 J:

>>> from kuchka import SquareMetre
>>> water * SquareMetre(1)
0.072 J

A curved interface adds a pressure.
The Laplace pressure inside a water droplet of 1 µm radius is twice the surface
tension over the radius:

>>> from kuchka import Micrometre
>>> from kuchka.units import KILOPASCAL
>>> (2 * water / Micrometre(1)).to(KILOPASCAL)
144 kPa

A spring of 250 N/m, compressed by 4 cm, pushes back with 10 N and stores 0.2 J,
where `E = k x² / 2`:

>>> from kuchka import Centimetre
>>> from kuchka import NewtonPerMetre
>>> stiffness = NewtonPerMetre(250)
>>> compression = Centimetre(4)
>>> stiffness * compression
10 N
>>> stiffness * compression * compression / 2
0.2 J

The CGS unit is exactly a millinewton per metre, so tensiometer readings from older
literature carry over without a factor:

>>> DynePerCentimetre(72) == MillinewtonPerMetre(72)
True

A force along a line is a force per length, and a force alone is a different quantity:

>>> from kuchka import Newton
>>> water + Newton(1)  # doctest: +ELLIPSIS
Traceback (most recent call last):
...
kuchka.errors.IncompatibleDimensionError: ...

Notes
-----
One newton per metre is one joule per square metre and one kilogram per second squared:

`1 N/m = 1 J/m² = 1 kg/s²`.

A surface tension is a measured property of a pair of materials at a stated
temperature, and 72 mN/m is the value of water against air near room temperature.

The dyne is exactly `1e-5` N and the centimetre `1e-2` m, so one dyne per centimetre is
exactly one millinewton per metre.
The erg per square centimetre, which older literature uses for the same quantity, is
one dyne per centimetre too, and the library reads it as that unit.

A stiffness, a line load, an interfacial tension, and an energy release rate have this
dimension and read as a `SurfaceTension`.
`SurfaceTension` and `Fluence` are two kinds of one dimension, and
`Fluence.from_surface_tension` is the explicit move between them.

`SURFACE_TENSION_UNITS` maps symbols such as ``"mN/m"``, ``"dyn/cm"``, and
``"erg/cm2"`` to their constructors, for boundary code that reads a unit as a string
from outside the application.

References
----------
NIST, Special Publication 811, Guide for the Use of the International System of Units,
on the CGS units dyne and erg:
https://www.nist.gov/pml/special-publication-811

BIPM, The International System of Units (SI Brochure), on the coherent derived units:
https://www.bipm.org/en/publications/si-brochure

See Also
--------
~kuchka.quantities.Force
    The force along a line, per length of that line.
~kuchka.quantities.Energy
    The energy of a surface, per area of that surface.
~kuchka.quantities.Pressure
    The Laplace pressure of a curved interface.
~kuchka.quantities.Fluence
    The radiometric kind of the same dimension.
~kuchka.units.mechanics.force
    Force units, including the dyne.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import SURFACE_TENSION
from kuchka.internal import prefixes
from kuchka.internal.prefixes import with_prefix
from kuchka.internal.spelling import powered
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import to_exact
from kuchka.quantities import SurfaceTension
from kuchka.quantities import UnitDef
from kuchka.units.length import CENTIMETRE
from kuchka.units.mechanics.force import DYNE

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.numeric import Numeric

NEWTON_PER_METRE = UnitDef(
    "newton_per_metre",
    "N/m",
    1,
    SURFACE_TENSION,
    words=("newtons per metre", "newtons per meter"),
)
MILLINEWTON_PER_METRE = with_prefix(prefixes.MILLI, NEWTON_PER_METRE)
KILONEWTON_PER_METRE = with_prefix(prefixes.KILO, NEWTON_PER_METRE)
DYNE_PER_CENTIMETRE = UnitDef(
    "dyne_per_centimetre",
    "dyn/cm",
    DYNE.scale / CENTIMETRE.scale,
    SURFACE_TENSION,
    aliases=("erg/cm2", *powered("erg/cm", 2)),
    words=(
        "dynes per centimetre",
        "dynes per centimeter",
        "ergs per square centimetre",
        "ergs per square centimeter",
    ),
)
"""The CGS unit of surface tension, exactly one millinewton per metre."""

SurfaceTension._canonical_unit = NEWTON_PER_METRE  # noqa: SLF001 -- this module owns SurfaceTension's canonical unit


def NewtonPerMetre(value: Numeric) -> SurfaceTension:
    """Construct a SurfaceTension from newtons per metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in newtons per metre.

    Returns
    -------
    SurfaceTension
        SurfaceTension represented in newtons per metre.

    Notes
    -----
    One newton per metre is one joule per square metre.

    Examples
    --------
    The cantilever of an atomic force microscope bends like a spring of 0.2 N/m:

    >>> cantilever = NewtonPerMetre(0.2)
    >>> cantilever
    0.2 N/m

    Bent by 5 µm, it pushes back with 1 µN:

    >>> from kuchka import Micrometre
    >>> from kuchka.units import MICRONEWTON
    >>> (cantilever * Micrometre(5)).to(MICRONEWTON)
    1 µN

    A newton per metre is a joule per square metre, so a 3 N/m film tension stores 3 J
    over each square metre of film:

    >>> from kuchka import SquareMetre
    >>> NewtonPerMetre(3) * SquareMetre(1)
    3 J

    """
    return SurfaceTension(to_exact(value) * NEWTON_PER_METRE.scale, NEWTON_PER_METRE)


def MillinewtonPerMetre(value: Numeric) -> SurfaceTension:
    """Construct a SurfaceTension from millinewtons per metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in millinewtons per metre.

    Returns
    -------
    SurfaceTension
        SurfaceTension represented in millinewtons per metre.

    Examples
    --------
    Ethanol has a surface tension of about 22 mN/m at room temperature, a third of the
    value of water:

    >>> ethanol = MillinewtonPerMetre(22)
    >>> ethanol
    22 mN/m

    A surfactant brings water down to about 30 mN/m, so a measured 72 mN/m falls by
    exactly 42 mN/m:

    >>> MillinewtonPerMetre(72) - MillinewtonPerMetre(30)
    42 mN/m

    """
    return SurfaceTension(
        to_exact(value) * MILLINEWTON_PER_METRE.scale, MILLINEWTON_PER_METRE
    )


def KilonewtonPerMetre(value: Numeric) -> SurfaceTension:
    """Construct a SurfaceTension from kilonewtons per metre.

    Parameters
    ----------
    value : Numeric
        Magnitude in kilonewtons per metre.

    Returns
    -------
    SurfaceTension
        SurfaceTension represented in kilonewtons per metre.

    Examples
    --------
    A wall that stands on a beam puts a line load of 12 kN/m on it:

    >>> wall = KilonewtonPerMetre(12)
    >>> wall
    12 kN/m

    Over a span of 5 m the beam carries 60 kN:

    >>> from kuchka import Metre
    >>> from kuchka.units import KILONEWTON
    >>> (wall * Metre(5)).to(KILONEWTON)
    60 kN

    """
    return SurfaceTension(
        to_exact(value) * KILONEWTON_PER_METRE.scale, KILONEWTON_PER_METRE
    )


def DynePerCentimetre(value: Numeric) -> SurfaceTension:
    """Construct a SurfaceTension from dynes per centimetre.

    Parameters
    ----------
    value : Numeric
        Magnitude in dynes per centimetre.

    Returns
    -------
    SurfaceTension
        SurfaceTension represented in dynes per centimetre.

    Notes
    -----
    One dyne per centimetre is exactly one millinewton per metre, and equals one erg
    per square centimetre.

    Examples
    --------
    Older tensiometers and the literature that follows them report mercury at about
    485 dyn/cm:

    >>> mercury = DynePerCentimetre(485)
    >>> mercury
    485 dyn/cm

    The value in SI units is exactly 0.485 N/m:

    >>> from kuchka.units import NEWTON_PER_METRE
    >>> mercury.to(NEWTON_PER_METRE)
    0.485 N/m

    A reading written as text with the older spelling for the same unit enters the
    library through the unit table:

    >>> SURFACE_TENSION_UNITS["erg/cm2"](485) == mercury
    True

    """
    return SurfaceTension(
        to_exact(value) * DYNE_PER_CENTIMETRE.scale, DYNE_PER_CENTIMETRE
    )


SURFACE_TENSION_UNITS: Mapping[str, Callable[[Numeric], SurfaceTension]] = unit_table(
    "SURFACE_TENSION_UNITS",
    {
        NEWTON_PER_METRE: NewtonPerMetre,
        MILLINEWTON_PER_METRE: MillinewtonPerMetre,
        KILONEWTON_PER_METRE: KilonewtonPerMetre,
        DYNE_PER_CENTIMETRE: DynePerCentimetre,
    },
)

__all__ = [
    "DYNE_PER_CENTIMETRE",
    "KILONEWTON_PER_METRE",
    "MILLINEWTON_PER_METRE",
    "NEWTON_PER_METRE",
    "SURFACE_TENSION_UNITS",
    "DynePerCentimetre",
    "KilonewtonPerMetre",
    "MillinewtonPerMetre",
    "NewtonPerMetre",
]
