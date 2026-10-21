"""Data unit constructors: bits and bytes, in decimal and binary multiples.

    from kuchka import Gibibyte, Megabyte

`Data` counts information, and its canonical unit is the bit.
A byte is 8 bits, and each of the two has multiples in two families:

* the SI prefixes count in thousands: a kilobyte (`kB`) is 1000 bytes, and the
  prefixes run through the petabyte (`PB`);
* the IEC binary prefixes count in powers of 1024: a kibibyte (`KiB`) is 1024 bytes,
  and the prefixes run through the pebibyte (`PiB`).

Examples
--------
A firmware image of 3 MiB is written to flash in pages of 4 KiB:

>>> image = Mebibyte(3)
>>> page = Kibibyte(4)
>>> int((image / page).magnitude)
768

A drive sold as 1 TB holds fewer bytes than a tebibyte, which is what an operating
system reporting in binary multiples shows:

>>> Terabyte(1) < Tebibyte(1)
True
>>> f"{Terabyte(1).to(TEBIBYTE):.3f}"
'0.909 TiB'

Bits and bytes convert exactly, so a count of bits does not drift:

>>> Kilobyte(1).to(BIT)
8000 bit
>>> Kibibit(1) == Bit(1024)
True

Notes
-----
`kB` is 1000 bytes and `KiB` is 1024 bytes, and the two are never mixed up: symbols
are case-sensitive, so `KB` and `Kb` are refused, since a capital K names no SI prefix
and the number it was written to mean is a choice between the two families.
`MB` and `GB` read as the SI megabyte and gigabyte, and `Mb` is the megabit, which is
an eighth of that size.

The bit is `bit` (or `b`) and the byte is `B` (or the word `octet`).

`DATA_UNITS` maps symbols such as ``"kB"``, ``"KiB"``, ``"Mbit"``, and ``"bit"`` to
their constructors.
It is intended for boundary code that reads a size from configuration files, device
descriptors, or other external sources.

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
    >>> Bit(8).to(BYTE)
    1 B

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
    >>> Kilobit(1).to(BIT)
    1000 bit

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
    >>> Megabit(1).to(BIT)
    1000000 bit

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
    >>> Gigabit(1).to(BIT)
    1000000000 bit

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
    >>> Terabit(1).to(BIT)
    1000000000000 bit

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
    >>> Petabit(1).to(BIT)
    1000000000000000 bit

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
    >>> Kibibit(1).to(BIT)
    1024 bit

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
    >>> Mebibit(1).to(BIT)
    1048576 bit

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
    >>> Gibibit(1).to(BIT)
    1073741824 bit

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
    >>> Tebibit(1).to(BIT)
    1099511627776 bit

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
    >>> Pebibit(1).to(BIT)
    1125899906842624 bit

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
    >>> Byte(1).to(BIT)
    8 bit

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
    >>> Kilobyte(1).to(BYTE)
    1000 B

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
    >>> Megabyte(1).to(BYTE)
    1000000 B

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
    >>> Gigabyte(1).to(BYTE)
    1000000000 B

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
    >>> Terabyte(1).to(BYTE)
    1000000000000 B

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
    >>> Petabyte(1).to(BYTE)
    1000000000000000 B

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
    >>> Kibibyte(1).to(BYTE)
    1024 B

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
    >>> Mebibyte(1).to(BYTE)
    1048576 B

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
    >>> Gibibyte(1).to(BYTE)
    1073741824 B

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
    >>> Tebibyte(1).to(BYTE)
    1099511627776 B

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
    >>> Pebibyte(1).to(BYTE)
    1125899906842624 B

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

__all__ = [
    "BIT",
    "BYTE",
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
