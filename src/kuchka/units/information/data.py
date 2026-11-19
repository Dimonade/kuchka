"""Data constructors: bits and bytes, in decimal and binary multiples.

    from kuchka import Gibibyte
    from kuchka import Megabyte

`Data` counts information, and its canonical unit is the bit.
A byte is 8 bits, and each of the two has multiples in two families:

* the SI prefixes count in thousands: a kilobyte (`kB`) is 1000 bytes, and the prefixes
  run through the petabyte (`PB`);
* the IEC binary prefixes count in powers of 1024: a kibibyte (`KiB`) is 1024 bytes,
  and the prefixes run through the pebibyte (`PiB`).

Examples
--------
A 4 MiB flash slot must hold the bootloader, application, calibration table, and
rollback image.
Calculate how much space remains after reserving each region:

>>> slot = Mebibyte(4)
>>> bootloader = Kibibyte(384)
>>> application = Mebibyte(11) / 4
>>> calibration = Kibibyte(16)
>>> rollback_image = Kibibyte(512)
>>> used = bootloader + application + calibration + rollback_image
>>> (slot - used).to(KIBIBYTE)
368 KiB

A device writes one 96-byte telemetry record every ten seconds.
Estimate its local storage requirement before deciding how often logs need to be
uploaded:

>>> record = Byte(96)
>>> records_per_day = 24 * 60 * 6
>>> daily_log = record * records_per_day
>>> daily_log.to(KIBIBYTE)
810 KiB
>>> (daily_log * 7).to(KIBIBYTE)
5670 KiB

A firmware update is sent in payload chunks of at most 1460 bytes.
The final chunk may be only partly filled, so calculate both the number of chunks and
the unused payload capacity in the last one:

>>> from math import ceil
>>> firmware = Mebibyte(3)
>>> payload = Byte(1460)
>>> chunks = ceil((firmware / payload).magnitude)
>>> chunks
2155
>>> (payload * chunks - firmware).to(BYTE)
572 B

A nominal 1 TB drive is marketed in decimal units, while the operating system may
report capacity in tebibytes.
Reserve 700 GiB for data, 64 GiB for the system, and 128 GiB for update staging, then
inspect what is left:

>>> drive = Terabyte(1)
>>> f"{drive.to(TEBIBYTE):.3f}"
'0.909 TiB'
>>> f"{(drive - Gibibyte(700) - Gibibyte(64) - Gibibyte(128)).to(GIBIBYTE):.1f}"
'39.3 GiB'

Notes
-----
`kB` is 1000 bytes and `KiB` is 1024 bytes. Symbols are case-sensitive: `KB` and `Kb`
are not accepted because uppercase `K` is not an SI prefix and the intended scale would
be ambiguous.
`MB` and `GB` denote megabytes and gigabytes; `Mb` denotes megabits, one eighth of a
megabyte at the same prefix.

The bit uses the symbol `bit` (or `b`), while the byte uses `B` (or the word `octet`).
These units count information; they do not represent transfer speed.
For information per unit time, use `DataRate`.

`DATA_UNITS` maps symbols such as ``"kB"``, ``"KiB"``, ``"Mbit"``, and ``"bit"`` to
their constructors.
It is intended for boundary code that reads sizes from configuration files, device
descriptors, protocol metadata, or other external sources.

See Also
--------
~kuchka.quantities.Data
    Quantity type representing an amount of information.
~kuchka.quantities.DataRate
    Data per unit of time.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import DATA
from kuchka.internal import prefixes
from kuchka.internal.prefixes import with_prefix
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Data
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

BIT = UnitDef("bit", "bit", 1, DATA, aliases=("b",))
BYTE = UnitDef("byte", "B", 8, DATA, words=("octet",))
KILOBIT = with_prefix(prefixes.KILO, BIT)
MEGABIT = with_prefix(prefixes.MEGA, BIT)
GIGABIT = with_prefix(prefixes.GIGA, BIT)
TERABIT = with_prefix(prefixes.TERA, BIT)
PETABIT = with_prefix(prefixes.PETA, BIT)
KIBIBIT = with_prefix(prefixes.KIBI, BIT)
MEBIBIT = with_prefix(prefixes.MEBI, BIT)
GIBIBIT = with_prefix(prefixes.GIBI, BIT)
TEBIBIT = with_prefix(prefixes.TEBI, BIT)
PEBIBIT = with_prefix(prefixes.PEBI, BIT)
KILOBYTE = with_prefix(prefixes.KILO, BYTE)
MEGABYTE = with_prefix(prefixes.MEGA, BYTE)
GIGABYTE = with_prefix(prefixes.GIGA, BYTE)
TERABYTE = with_prefix(prefixes.TERA, BYTE)
PETABYTE = with_prefix(prefixes.PETA, BYTE)
KIBIBYTE = with_prefix(prefixes.KIBI, BYTE)
MEBIBYTE = with_prefix(prefixes.MEBI, BYTE)
GIBIBYTE = with_prefix(prefixes.GIBI, BYTE)
TEBIBYTE = with_prefix(prefixes.TEBI, BYTE)
PEBIBYTE = with_prefix(prefixes.PEBI, BYTE)

Data._canonical_unit = BIT  # noqa: SLF001 -- this module owns Data's canonical unit


def Bit(value: Numeric) -> Data:
    """Construct a Data from a magnitude expressed in bits.

    Parameters
    ----------
    value : Numeric
        Amount of information in bits.

    Returns
    -------
    Data
        Amount of information represented in bits.

    Examples
    --------
    A 24-bit sensor field occupies exactly three bytes:

    >>> Bit(24).to(BYTE)
    3 B

    """
    return Data(to_exact(value) * BIT.scale, BIT)


def Kilobit(value: Numeric) -> Data:
    """Construct a Data from a magnitude expressed in kilobits.

    Parameters
    ----------
    value : Numeric
        Amount of information in kilobits.

    Returns
    -------
    Data
        Amount of information represented in kilobits.

    Examples
    --------
    A 12-kilobit buffer can hold 1500 bytes of payload:

    >>> Kilobit(12).to(BYTE)
    1500 B

    """
    return Data(to_exact(value) * KILOBIT.scale, KILOBIT)


def Megabit(value: Numeric) -> Data:
    """Construct a Data from a magnitude expressed in megabits.

    Parameters
    ----------
    value : Numeric
        Amount of information in megabits.

    Returns
    -------
    Data
        Amount of information represented in megabits.

    Examples
    --------
    A 24-megabit capture occupies three decimal megabytes:

    >>> Megabit(24).to(MEGABYTE)
    3 MB

    """
    return Data(to_exact(value) * MEGABIT.scale, MEGABIT)


def Gigabit(value: Numeric) -> Data:
    """Construct a Data from a magnitude expressed in gigabits.

    Parameters
    ----------
    value : Numeric
        Amount of information in gigabits.

    Returns
    -------
    Data
        Amount of information represented in gigabits.

    Examples
    --------
    Express an eight-gigabit export in the byte unit used by a storage API:

    >>> Gigabit(8).to(GIGABYTE)
    1 GB

    """
    return Data(to_exact(value) * GIGABIT.scale, GIGABIT)


def Terabit(value: Numeric) -> Data:
    """Construct a Data from a magnitude expressed in terabits.

    Parameters
    ----------
    value : Numeric
        Amount of information in terabits.

    Returns
    -------
    Data
        Amount of information represented in terabits.

    Examples
    --------
    A two-terabyte archive contains sixteen terabits of information:

    >>> Terabyte(2).to(TERABIT)
    16 Tbit

    """
    return Data(to_exact(value) * TERABIT.scale, TERABIT)


def Petabit(value: Numeric) -> Data:
    """Construct a Data from a magnitude expressed in petabits.

    Parameters
    ----------
    value : Numeric
        Amount of information in petabits.

    Returns
    -------
    Data
        Amount of information represented in petabits.

    Examples
    --------
    A petabyte-scale archive expressed in bits contains eight petabits:

    >>> Petabyte(1).to(PETABIT)
    8 Pbit

    """
    return Data(to_exact(value) * PETABIT.scale, PETABIT)


def Kibibit(value: Numeric) -> Data:
    """Construct a Data from a magnitude expressed in kibibits.

    Parameters
    ----------
    value : Numeric
        Amount of information in kibibits.

    Returns
    -------
    Data
        Amount of information represented in kibibits.

    Examples
    --------
    A 32-kibibit buffer holds four kibibytes:

    >>> Kibibit(32).to(KIBIBYTE)
    4 KiB

    """
    return Data(to_exact(value) * KIBIBIT.scale, KIBIBIT)


def Mebibit(value: Numeric) -> Data:
    """Construct a Data from a magnitude expressed in mebibits.

    Parameters
    ----------
    value : Numeric
        Amount of information in mebibits.

    Returns
    -------
    Data
        Amount of information represented in mebibits.

    Examples
    --------
    Eight mebibits make the one-mebibyte payload budget for a firmware component:

    >>> Mebibit(8).to(MEBIBYTE)
    1 MiB

    """
    return Data(to_exact(value) * MEBIBIT.scale, MEBIBIT)


def Gibibit(value: Numeric) -> Data:
    """Construct a Data from a magnitude expressed in gibibits.

    Parameters
    ----------
    value : Numeric
        Amount of information in gibibits.

    Returns
    -------
    Data
        Amount of information represented in gibibits.

    Examples
    --------
    Express a four-gibibyte image in gibibits for a bit-addressed interface:

    >>> Gibibyte(4).to(GIBIBIT)
    32 Gibit

    """
    return Data(to_exact(value) * GIBIBIT.scale, GIBIBIT)


def Tebibit(value: Numeric) -> Data:
    """Construct a Data from a magnitude expressed in tebibits.

    Parameters
    ----------
    value : Numeric
        Amount of information in tebibits.

    Returns
    -------
    Data
        Amount of information represented in tebibits.

    Examples
    --------
    Express a tebibyte of archived data in the units of a bit-counting interface:

    >>> Tebibyte(1).to(TEBIBIT)
    8 Tibit

    """
    return Data(to_exact(value) * TEBIBIT.scale, TEBIBIT)


def Pebibit(value: Numeric) -> Data:
    """Construct a Data from a magnitude expressed in pebibits.

    Parameters
    ----------
    value : Numeric
        Amount of information in pebibits.

    Returns
    -------
    Data
        Amount of information represented in pebibits.

    Examples
    --------
    Convert a pebibyte archive allocation to its bit-based capacity:

    >>> Pebibyte(1).to(PEBIBIT)
    8 Pibit

    """
    return Data(to_exact(value) * PEBIBIT.scale, PEBIBIT)


def Byte(value: Numeric) -> Data:
    """Construct a Data from a magnitude expressed in bytes.

    Parameters
    ----------
    value : Numeric
        Amount of information in bytes.

    Returns
    -------
    Data
        Amount of information represented in bytes.

    Examples
    --------
    A 1500-byte buffer has this many bits available to a bit-counting API:

    >>> Byte(1500).to(BIT)
    12000 bit

    """
    return Data(to_exact(value) * BYTE.scale, BYTE)


def Kilobyte(value: Numeric) -> Data:
    """Construct a Data from a magnitude expressed in kilobytes.

    Parameters
    ----------
    value : Numeric
        Amount of information in kilobytes.

    Returns
    -------
    Data
        Amount of information represented in kilobytes.

    Examples
    --------
    A 64 kB diagnostics buffer has 9 kB already occupied by headers.
    Find the remaining payload capacity in bytes:

    >>> (Kilobyte(64) - Kilobyte(9)).to(BYTE)
    55000 B

    """
    return Data(to_exact(value) * KILOBYTE.scale, KILOBYTE)


def Megabyte(value: Numeric) -> Data:
    """Construct a Data from a magnitude expressed in megabytes.

    Parameters
    ----------
    value : Numeric
        Amount of information in megabytes.

    Returns
    -------
    Data
        Amount of information represented in megabytes.

    Examples
    --------
    Split a 25 MB upload into five-megabyte transfer jobs:

    >>> int((Megabyte(25) / Megabyte(5)).magnitude)
    5

    """
    return Data(to_exact(value) * MEGABYTE.scale, MEGABYTE)


def Gigabyte(value: Numeric) -> Data:
    """Construct a Data from a magnitude expressed in gigabytes.

    Parameters
    ----------
    value : Numeric
        Amount of information in gigabytes.

    Returns
    -------
    Data
        Amount of information represented in gigabytes.

    Examples
    --------
    A 2 GB staging area contains a 750 MB package.
    Calculate the remaining space:

    >>> (Gigabyte(2) - Megabyte(750)).to(MEGABYTE)
    1250 MB

    """
    return Data(to_exact(value) * GIGABYTE.scale, GIGABYTE)


def Terabyte(value: Numeric) -> Data:
    """Construct a Data from a magnitude expressed in terabytes.

    Parameters
    ----------
    value : Numeric
        Amount of information in terabytes.

    Returns
    -------
    Data
        Amount of information represented in terabytes.

    Examples
    --------
    Split a 2 TB backup into 250 GB archive shards:

    >>> int((Terabyte(2) / Gigabyte(250)).magnitude)
    8

    """
    return Data(to_exact(value) * TERABYTE.scale, TERABYTE)


def Petabyte(value: Numeric) -> Data:
    """Construct a Data from a magnitude expressed in petabytes.

    Parameters
    ----------
    value : Numeric
        Amount of information in petabytes.

    Returns
    -------
    Data
        Amount of information represented in petabytes.

    Examples
    --------
    A 2 PB data lake partitioned into 250 TB archive tiers needs eight tiers:

    >>> int((Petabyte(2) / Terabyte(250)).magnitude)
    8

    """
    return Data(to_exact(value) * PETABYTE.scale, PETABYTE)


def Kibibyte(value: Numeric) -> Data:
    """Construct a Data from a magnitude expressed in kibibytes.

    Parameters
    ----------
    value : Numeric
        Amount of information in kibibytes.

    Returns
    -------
    Data
        Amount of information represented in kibibytes.

    Examples
    --------
    A 64 KiB buffer accommodates sixteen 4 KiB flash pages:

    >>> int((Kibibyte(64) / Kibibyte(4)).magnitude)
    16

    """
    return Data(to_exact(value) * KIBIBYTE.scale, KIBIBYTE)


def Mebibyte(value: Numeric) -> Data:
    """Construct a Data from a magnitude expressed in mebibytes.

    Parameters
    ----------
    value : Numeric
        Amount of information in mebibytes.

    Returns
    -------
    Data
        Amount of information represented in mebibytes.

    Examples
    --------
    A 128 MiB model bundle split into 8 MiB assets requires sixteen assets:

    >>> int((Mebibyte(128) / Mebibyte(8)).magnitude)
    16

    """
    return Data(to_exact(value) * MEBIBYTE.scale, MEBIBYTE)


def Gibibyte(value: Numeric) -> Data:
    """Construct a Data from a magnitude expressed in gibibytes.

    Parameters
    ----------
    value : Numeric
        Amount of information in gibibytes.

    Returns
    -------
    Data
        Amount of information represented in gibibytes.

    Examples
    --------
    A 6 GiB cache divided into 256 MiB slots has room for twenty-four slots:

    >>> int((Gibibyte(6) / Mebibyte(256)).magnitude)
    24

    """
    return Data(to_exact(value) * GIBIBYTE.scale, GIBIBYTE)


def Tebibyte(value: Numeric) -> Data:
    """Construct a Data from a magnitude expressed in tebibytes.

    Parameters
    ----------
    value : Numeric
        Amount of information in tebibytes.

    Returns
    -------
    Data
        Amount of information represented in tebibytes.

    Examples
    --------
    One TiB of storage can be split into four 256 GiB volumes:

    >>> int((Tebibyte(1) / Gibibyte(256)).magnitude)
    4

    """
    return Data(to_exact(value) * TEBIBYTE.scale, TEBIBYTE)


def Pebibyte(value: Numeric) -> Data:
    """Construct a Data from a magnitude expressed in pebibytes.

    Parameters
    ----------
    value : Numeric
        Amount of information in pebibytes.

    Returns
    -------
    Data
        Amount of information represented in pebibytes.

    Examples
    --------
    Split a 3 PiB archive into 24 TiB shards for independent processing:

    >>> int((Pebibyte(3) / Tebibyte(24)).magnitude)
    128

    """
    return Data(to_exact(value) * PEBIBYTE.scale, PEBIBYTE)


DATA_UNITS: Mapping[str, Callable[[Numeric], Data]] = unit_table(
    "DATA_UNITS",
    {
        BIT: Bit,
        KILOBIT: Kilobit,
        MEGABIT: Megabit,
        GIGABIT: Gigabit,
        TERABIT: Terabit,
        PETABIT: Petabit,
        KIBIBIT: Kibibit,
        MEBIBIT: Mebibit,
        GIBIBIT: Gibibit,
        TEBIBIT: Tebibit,
        PEBIBIT: Pebibit,
        BYTE: Byte,
        KILOBYTE: Kilobyte,
        MEGABYTE: Megabyte,
        GIGABYTE: Gigabyte,
        TERABYTE: Terabyte,
        PETABYTE: Petabyte,
        KIBIBYTE: Kibibyte,
        MEBIBYTE: Mebibyte,
        GIBIBYTE: Gibibyte,
        TEBIBYTE: Tebibyte,
        PEBIBYTE: Pebibyte,
    },
)

DATA_LADDERS: tuple[tuple[UnitDef, ...], ...] = (
    (
        BIT,
        KILOBIT,
        MEGABIT,
        GIGABIT,
        TERABIT,
        PETABIT,
    ),
    (
        BYTE,
        KILOBYTE,
        MEGABYTE,
        GIGABYTE,
        TERABYTE,
        PETABYTE,
    ),
    (
        KIBIBIT,
        MEBIBIT,
        GIBIBIT,
        TEBIBIT,
        PEBIBIT,
    ),
    (
        KIBIBYTE,
        MEBIBYTE,
        GIBIBYTE,
        TEBIBYTE,
        PEBIBYTE,
    ),
)
"""The runs of units `auto_scale` moves a data along.

There is one run for each family of prefixed units, smallest first.
"""

__all__ = [
    "BIT",
    "BYTE",
    "DATA_LADDERS",
    "DATA_UNITS",
    "GIBIBIT",
    "GIBIBYTE",
    "GIGABIT",
    "GIGABYTE",
    "KIBIBIT",
    "KIBIBYTE",
    "KILOBIT",
    "KILOBYTE",
    "MEBIBIT",
    "MEBIBYTE",
    "MEGABIT",
    "MEGABYTE",
    "PEBIBIT",
    "PEBIBYTE",
    "PETABIT",
    "PETABYTE",
    "TEBIBIT",
    "TEBIBYTE",
    "TERABIT",
    "TERABYTE",
    "Bit",
    "Byte",
    "Gibibit",
    "Gibibyte",
    "Gigabit",
    "Gigabyte",
    "Kibibit",
    "Kibibyte",
    "Kilobit",
    "Kilobyte",
    "Mebibit",
    "Mebibyte",
    "Megabit",
    "Megabyte",
    "Pebibit",
    "Pebibyte",
    "Petabit",
    "Petabyte",
    "Tebibit",
    "Tebibyte",
    "Terabit",
    "Terabyte",
]
