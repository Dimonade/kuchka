"""Data-rate unit constructors: bits and bytes per second.

    from kuchka import GigabitPerSecond, MebibytePerSecond

`DataRate` measures how fast information moves, and its canonical unit is the bit per
second.
It has its own dimension, so a link speed is never mistaken for a `Frequency`, a
`SampleRate`, or a `BaudRate`.
The module offers the bit per second and the byte per second with the same two
families of multiples as `kuchka.units.data`: the SI prefixes through the petabit and
petabyte per second, and the IEC binary prefixes through the pebibit and pebibyte per
second.

Examples
--------
A gigabit link moves 125 MB every second:

>>> from kuchka import Second
>>> from kuchka.units.data import MEGABYTE
>>> (GigabitPerSecond(1) * Second(1)).to(MEGABYTE)
125 MB

Copying a 4 GiB image over a 100 MB/s link takes about 43 seconds:

>>> from kuchka import Gibibyte
>>> duration = Gibibyte(4) / MegabytePerSecond(100)
>>> f"{duration:.1f}"
'42.9 s'

A file system benchmark reports 250 MiB/s, which a network tool would call:

>>> f"{MebibytePerSecond(250).to(MEGABIT_PER_SECOND):.1f}"
'2097.2 Mbit/s'

Notes
-----
Link speeds are quoted in bits per second with SI prefixes (`Mbit/s`, `Gbit/s`), and
file transfers in bytes per second, so both are here.
A baud rate counts symbols and not bits, and it stays a `BaudRate`.

`DATA_RATE_UNITS` maps symbols such as ``"Mbit/s"``, ``"MB/s"``, ``"MiB/s"``, and
``"bps"`` to their constructors.

See Also
--------
~kuchka.quantities.DataRate
    Quantity type representing data per unit of time.
~kuchka.quantities.Data
    An amount of information.
~kuchka.quantities.BaudRate
    Symbol rate, which is not a bit rate.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import DATA_RATE
from kuchka.internal import prefixes
from kuchka.internal.prefixes import with_prefix
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import DataRate
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

BIT_PER_SECOND = UnitDef(
    "bit_per_second",
    "bit/s",
    1,
    DATA_RATE,
    aliases=("b/s", "bps"),
    words=("bit per second", "bits per second", "bit/sec"),
)
BYTE_PER_SECOND = UnitDef(
    "byte_per_second",
    "B/s",
    8,
    DATA_RATE,
    aliases=("Bps",),
    words=("byte per second", "bytes per second", "byte/sec", "octet per second"),
)
KILOBIT_PER_SECOND = with_prefix(prefixes.KILO, BIT_PER_SECOND)
MEGABIT_PER_SECOND = with_prefix(prefixes.MEGA, BIT_PER_SECOND)
GIGABIT_PER_SECOND = with_prefix(prefixes.GIGA, BIT_PER_SECOND)
TERABIT_PER_SECOND = with_prefix(prefixes.TERA, BIT_PER_SECOND)
PETABIT_PER_SECOND = with_prefix(prefixes.PETA, BIT_PER_SECOND)
KIBIBIT_PER_SECOND = with_prefix(prefixes.KIBI, BIT_PER_SECOND)
MEBIBIT_PER_SECOND = with_prefix(prefixes.MEBI, BIT_PER_SECOND)
GIBIBIT_PER_SECOND = with_prefix(prefixes.GIBI, BIT_PER_SECOND)
TEBIBIT_PER_SECOND = with_prefix(prefixes.TEBI, BIT_PER_SECOND)
PEBIBIT_PER_SECOND = with_prefix(prefixes.PEBI, BIT_PER_SECOND)
KILOBYTE_PER_SECOND = with_prefix(prefixes.KILO, BYTE_PER_SECOND)
MEGABYTE_PER_SECOND = with_prefix(prefixes.MEGA, BYTE_PER_SECOND)
GIGABYTE_PER_SECOND = with_prefix(prefixes.GIGA, BYTE_PER_SECOND)
TERABYTE_PER_SECOND = with_prefix(prefixes.TERA, BYTE_PER_SECOND)
PETABYTE_PER_SECOND = with_prefix(prefixes.PETA, BYTE_PER_SECOND)
KIBIBYTE_PER_SECOND = with_prefix(prefixes.KIBI, BYTE_PER_SECOND)
MEBIBYTE_PER_SECOND = with_prefix(prefixes.MEBI, BYTE_PER_SECOND)
GIBIBYTE_PER_SECOND = with_prefix(prefixes.GIBI, BYTE_PER_SECOND)
TEBIBYTE_PER_SECOND = with_prefix(prefixes.TEBI, BYTE_PER_SECOND)
PEBIBYTE_PER_SECOND = with_prefix(prefixes.PEBI, BYTE_PER_SECOND)

DataRate._canonical_unit = BIT_PER_SECOND  # noqa: SLF001 -- this module owns DataRate's canonical unit


def BitPerSecond(value: Numeric) -> DataRate:
    """Construct a DataRate from a magnitude expressed in bits per second.

    Parameters
    ----------
    value : Numeric
        Data rate in bits per second.

    Returns
    -------
    DataRate
        Data rate represented in bits per second.

    Examples
    --------
    >>> BitPerSecond(8).to(BYTE_PER_SECOND)
    1 B/s

    """
    return DataRate(to_exact(value) * BIT_PER_SECOND.scale, BIT_PER_SECOND)


def KilobitPerSecond(value: Numeric) -> DataRate:
    """Construct a DataRate from a magnitude expressed in kilobits per second.

    Parameters
    ----------
    value : Numeric
        Data rate in kilobits per second.

    Returns
    -------
    DataRate
        Data rate represented in kilobits per second.

    Examples
    --------
    >>> KilobitPerSecond(1).to(BIT_PER_SECOND)
    1000 bit/s

    """
    return DataRate(to_exact(value) * KILOBIT_PER_SECOND.scale, KILOBIT_PER_SECOND)


def MegabitPerSecond(value: Numeric) -> DataRate:
    """Construct a DataRate from a magnitude expressed in megabits per second.

    Parameters
    ----------
    value : Numeric
        Data rate in megabits per second.

    Returns
    -------
    DataRate
        Data rate represented in megabits per second.

    Examples
    --------
    >>> MegabitPerSecond(1).to(BIT_PER_SECOND)
    1000000 bit/s

    """
    return DataRate(to_exact(value) * MEGABIT_PER_SECOND.scale, MEGABIT_PER_SECOND)


def GigabitPerSecond(value: Numeric) -> DataRate:
    """Construct a DataRate from a magnitude expressed in gigabits per second.

    Parameters
    ----------
    value : Numeric
        Data rate in gigabits per second.

    Returns
    -------
    DataRate
        Data rate represented in gigabits per second.

    Examples
    --------
    >>> GigabitPerSecond(1).to(BIT_PER_SECOND)
    1000000000 bit/s

    """
    return DataRate(to_exact(value) * GIGABIT_PER_SECOND.scale, GIGABIT_PER_SECOND)


def TerabitPerSecond(value: Numeric) -> DataRate:
    """Construct a DataRate from a magnitude expressed in terabits per second.

    Parameters
    ----------
    value : Numeric
        Data rate in terabits per second.

    Returns
    -------
    DataRate
        Data rate represented in terabits per second.

    Examples
    --------
    >>> TerabitPerSecond(1).to(BIT_PER_SECOND)
    1000000000000 bit/s

    """
    return DataRate(to_exact(value) * TERABIT_PER_SECOND.scale, TERABIT_PER_SECOND)


def PetabitPerSecond(value: Numeric) -> DataRate:
    """Construct a DataRate from a magnitude expressed in petabits per second.

    Parameters
    ----------
    value : Numeric
        Data rate in petabits per second.

    Returns
    -------
    DataRate
        Data rate represented in petabits per second.

    Examples
    --------
    >>> PetabitPerSecond(1).to(BIT_PER_SECOND)
    1000000000000000 bit/s

    """
    return DataRate(to_exact(value) * PETABIT_PER_SECOND.scale, PETABIT_PER_SECOND)


def KibibitPerSecond(value: Numeric) -> DataRate:
    """Construct a DataRate from a magnitude expressed in kibibits per second.

    Parameters
    ----------
    value : Numeric
        Data rate in kibibits per second.

    Returns
    -------
    DataRate
        Data rate represented in kibibits per second.

    Examples
    --------
    >>> KibibitPerSecond(1).to(BIT_PER_SECOND)
    1024 bit/s

    """
    return DataRate(to_exact(value) * KIBIBIT_PER_SECOND.scale, KIBIBIT_PER_SECOND)


def MebibitPerSecond(value: Numeric) -> DataRate:
    """Construct a DataRate from a magnitude expressed in mebibits per second.

    Parameters
    ----------
    value : Numeric
        Data rate in mebibits per second.

    Returns
    -------
    DataRate
        Data rate represented in mebibits per second.

    Examples
    --------
    >>> MebibitPerSecond(1).to(BIT_PER_SECOND)
    1048576 bit/s

    """
    return DataRate(to_exact(value) * MEBIBIT_PER_SECOND.scale, MEBIBIT_PER_SECOND)


def GibibitPerSecond(value: Numeric) -> DataRate:
    """Construct a DataRate from a magnitude expressed in gibibits per second.

    Parameters
    ----------
    value : Numeric
        Data rate in gibibits per second.

    Returns
    -------
    DataRate
        Data rate represented in gibibits per second.

    Examples
    --------
    >>> GibibitPerSecond(1).to(BIT_PER_SECOND)
    1073741824 bit/s

    """
    return DataRate(to_exact(value) * GIBIBIT_PER_SECOND.scale, GIBIBIT_PER_SECOND)


def TebibitPerSecond(value: Numeric) -> DataRate:
    """Construct a DataRate from a magnitude expressed in tebibits per second.

    Parameters
    ----------
    value : Numeric
        Data rate in tebibits per second.

    Returns
    -------
    DataRate
        Data rate represented in tebibits per second.

    Examples
    --------
    >>> TebibitPerSecond(1).to(BIT_PER_SECOND)
    1099511627776 bit/s

    """
    return DataRate(to_exact(value) * TEBIBIT_PER_SECOND.scale, TEBIBIT_PER_SECOND)


def PebibitPerSecond(value: Numeric) -> DataRate:
    """Construct a DataRate from a magnitude expressed in pebibits per second.

    Parameters
    ----------
    value : Numeric
        Data rate in pebibits per second.

    Returns
    -------
    DataRate
        Data rate represented in pebibits per second.

    Examples
    --------
    >>> PebibitPerSecond(1).to(BIT_PER_SECOND)
    1125899906842624 bit/s

    """
    return DataRate(to_exact(value) * PEBIBIT_PER_SECOND.scale, PEBIBIT_PER_SECOND)


def BytePerSecond(value: Numeric) -> DataRate:
    """Construct a DataRate from a magnitude expressed in bytes per second.

    Parameters
    ----------
    value : Numeric
        Data rate in bytes per second.

    Returns
    -------
    DataRate
        Data rate represented in bytes per second.

    Examples
    --------
    >>> BytePerSecond(1).to(BIT_PER_SECOND)
    8 bit/s

    """
    return DataRate(to_exact(value) * BYTE_PER_SECOND.scale, BYTE_PER_SECOND)


def KilobytePerSecond(value: Numeric) -> DataRate:
    """Construct a DataRate from a magnitude expressed in kilobytes per second.

    Parameters
    ----------
    value : Numeric
        Data rate in kilobytes per second.

    Returns
    -------
    DataRate
        Data rate represented in kilobytes per second.

    Examples
    --------
    >>> KilobytePerSecond(1).to(BYTE_PER_SECOND)
    1000 B/s

    """
    return DataRate(to_exact(value) * KILOBYTE_PER_SECOND.scale, KILOBYTE_PER_SECOND)


def MegabytePerSecond(value: Numeric) -> DataRate:
    """Construct a DataRate from a magnitude expressed in megabytes per second.

    Parameters
    ----------
    value : Numeric
        Data rate in megabytes per second.

    Returns
    -------
    DataRate
        Data rate represented in megabytes per second.

    Examples
    --------
    >>> MegabytePerSecond(1).to(BYTE_PER_SECOND)
    1000000 B/s

    """
    return DataRate(to_exact(value) * MEGABYTE_PER_SECOND.scale, MEGABYTE_PER_SECOND)


def GigabytePerSecond(value: Numeric) -> DataRate:
    """Construct a DataRate from a magnitude expressed in gigabytes per second.

    Parameters
    ----------
    value : Numeric
        Data rate in gigabytes per second.

    Returns
    -------
    DataRate
        Data rate represented in gigabytes per second.

    Examples
    --------
    >>> GigabytePerSecond(1).to(BYTE_PER_SECOND)
    1000000000 B/s

    """
    return DataRate(to_exact(value) * GIGABYTE_PER_SECOND.scale, GIGABYTE_PER_SECOND)


def TerabytePerSecond(value: Numeric) -> DataRate:
    """Construct a DataRate from a magnitude expressed in terabytes per second.

    Parameters
    ----------
    value : Numeric
        Data rate in terabytes per second.

    Returns
    -------
    DataRate
        Data rate represented in terabytes per second.

    Examples
    --------
    >>> TerabytePerSecond(1).to(BYTE_PER_SECOND)
    1000000000000 B/s

    """
    return DataRate(to_exact(value) * TERABYTE_PER_SECOND.scale, TERABYTE_PER_SECOND)


def PetabytePerSecond(value: Numeric) -> DataRate:
    """Construct a DataRate from a magnitude expressed in petabytes per second.

    Parameters
    ----------
    value : Numeric
        Data rate in petabytes per second.

    Returns
    -------
    DataRate
        Data rate represented in petabytes per second.

    Examples
    --------
    >>> PetabytePerSecond(1).to(BYTE_PER_SECOND)
    1000000000000000 B/s

    """
    return DataRate(to_exact(value) * PETABYTE_PER_SECOND.scale, PETABYTE_PER_SECOND)


def KibibytePerSecond(value: Numeric) -> DataRate:
    """Construct a DataRate from a magnitude expressed in kibibytes per second.

    Parameters
    ----------
    value : Numeric
        Data rate in kibibytes per second.

    Returns
    -------
    DataRate
        Data rate represented in kibibytes per second.

    Examples
    --------
    >>> KibibytePerSecond(1).to(BYTE_PER_SECOND)
    1024 B/s

    """
    return DataRate(to_exact(value) * KIBIBYTE_PER_SECOND.scale, KIBIBYTE_PER_SECOND)


def MebibytePerSecond(value: Numeric) -> DataRate:
    """Construct a DataRate from a magnitude expressed in mebibytes per second.

    Parameters
    ----------
    value : Numeric
        Data rate in mebibytes per second.

    Returns
    -------
    DataRate
        Data rate represented in mebibytes per second.

    Examples
    --------
    >>> MebibytePerSecond(1).to(BYTE_PER_SECOND)
    1048576 B/s

    """
    return DataRate(to_exact(value) * MEBIBYTE_PER_SECOND.scale, MEBIBYTE_PER_SECOND)


def GibibytePerSecond(value: Numeric) -> DataRate:
    """Construct a DataRate from a magnitude expressed in gibibytes per second.

    Parameters
    ----------
    value : Numeric
        Data rate in gibibytes per second.

    Returns
    -------
    DataRate
        Data rate represented in gibibytes per second.

    Examples
    --------
    >>> GibibytePerSecond(1).to(BYTE_PER_SECOND)
    1073741824 B/s

    """
    return DataRate(to_exact(value) * GIBIBYTE_PER_SECOND.scale, GIBIBYTE_PER_SECOND)


def TebibytePerSecond(value: Numeric) -> DataRate:
    """Construct a DataRate from a magnitude expressed in tebibytes per second.

    Parameters
    ----------
    value : Numeric
        Data rate in tebibytes per second.

    Returns
    -------
    DataRate
        Data rate represented in tebibytes per second.

    Examples
    --------
    >>> TebibytePerSecond(1).to(BYTE_PER_SECOND)
    1099511627776 B/s

    """
    return DataRate(to_exact(value) * TEBIBYTE_PER_SECOND.scale, TEBIBYTE_PER_SECOND)


def PebibytePerSecond(value: Numeric) -> DataRate:
    """Construct a DataRate from a magnitude expressed in pebibytes per second.

    Parameters
    ----------
    value : Numeric
        Data rate in pebibytes per second.

    Returns
    -------
    DataRate
        Data rate represented in pebibytes per second.

    Examples
    --------
    >>> PebibytePerSecond(1).to(BYTE_PER_SECOND)
    1125899906842624 B/s

    """
    return DataRate(to_exact(value) * PEBIBYTE_PER_SECOND.scale, PEBIBYTE_PER_SECOND)


DATA_RATE_UNITS: Mapping[str, Callable[[Numeric], DataRate]] = unit_table(
    "DATA_RATE_UNITS",
    {
        BIT_PER_SECOND: BitPerSecond,
        KILOBIT_PER_SECOND: KilobitPerSecond,
        MEGABIT_PER_SECOND: MegabitPerSecond,
        GIGABIT_PER_SECOND: GigabitPerSecond,
        TERABIT_PER_SECOND: TerabitPerSecond,
        PETABIT_PER_SECOND: PetabitPerSecond,
        KIBIBIT_PER_SECOND: KibibitPerSecond,
        MEBIBIT_PER_SECOND: MebibitPerSecond,
        GIBIBIT_PER_SECOND: GibibitPerSecond,
        TEBIBIT_PER_SECOND: TebibitPerSecond,
        PEBIBIT_PER_SECOND: PebibitPerSecond,
        BYTE_PER_SECOND: BytePerSecond,
        KILOBYTE_PER_SECOND: KilobytePerSecond,
        MEGABYTE_PER_SECOND: MegabytePerSecond,
        GIGABYTE_PER_SECOND: GigabytePerSecond,
        TERABYTE_PER_SECOND: TerabytePerSecond,
        PETABYTE_PER_SECOND: PetabytePerSecond,
        KIBIBYTE_PER_SECOND: KibibytePerSecond,
        MEBIBYTE_PER_SECOND: MebibytePerSecond,
        GIBIBYTE_PER_SECOND: GibibytePerSecond,
        TEBIBYTE_PER_SECOND: TebibytePerSecond,
        PEBIBYTE_PER_SECOND: PebibytePerSecond,
    },
)

__all__ = [
    "BIT_PER_SECOND",
    "BYTE_PER_SECOND",
    "DATA_RATE_UNITS",
    "GIBIBIT_PER_SECOND",
    "GIBIBYTE_PER_SECOND",
    "GIGABIT_PER_SECOND",
    "GIGABYTE_PER_SECOND",
    "KIBIBIT_PER_SECOND",
    "KIBIBYTE_PER_SECOND",
    "KILOBIT_PER_SECOND",
    "KILOBYTE_PER_SECOND",
    "MEBIBIT_PER_SECOND",
    "MEBIBYTE_PER_SECOND",
    "MEGABIT_PER_SECOND",
    "MEGABYTE_PER_SECOND",
    "PEBIBIT_PER_SECOND",
    "PEBIBYTE_PER_SECOND",
    "PETABIT_PER_SECOND",
    "PETABYTE_PER_SECOND",
    "TEBIBIT_PER_SECOND",
    "TEBIBYTE_PER_SECOND",
    "TERABIT_PER_SECOND",
    "TERABYTE_PER_SECOND",
    "BitPerSecond",
    "BytePerSecond",
    "GibibitPerSecond",
    "GibibytePerSecond",
    "GigabitPerSecond",
    "GigabytePerSecond",
    "KibibitPerSecond",
    "KibibytePerSecond",
    "KilobitPerSecond",
    "KilobytePerSecond",
    "MebibitPerSecond",
    "MebibytePerSecond",
    "MegabitPerSecond",
    "MegabytePerSecond",
    "PebibitPerSecond",
    "PebibytePerSecond",
    "PetabitPerSecond",
    "PetabytePerSecond",
    "TebibitPerSecond",
    "TebibytePerSecond",
    "TerabitPerSecond",
    "TerabytePerSecond",
]
