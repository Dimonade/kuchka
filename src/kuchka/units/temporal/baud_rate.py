"""Unit constructors for BaudRate: a symbol rate used by digital communications.

    from kuchka import Baud, Kilobaud

    uart_rate = Baud(115200)
    telemetry_rate = Kilobaud(250)

`BaudRate` measures symbols per second.
It is dimensionally identical to `Frequency` and `SampleRate`, but those quantities
describe different things:
- a hertz counts cycles,
- a sample rate counts samples,
- and a baud rate counts symbols.

The distinction matters even when the numerical values happen to be identical.
A 10 kBd communication channel and a 10 kHz oscillator do not describe the same
physical quantity and cannot be combined accidentally.

The available scales cover the rates commonly encountered in digital interfaces and
communication systems:

* baud describes low-speed serial links and instrument interfaces;
* kilobaud covers UARTs, control links, and moderate-rate telemetry;
* megabaud covers high-speed digital links and radio modems;
* gigabaud reaches high-throughput optical and spacecraft communication systems.

Examples
--------
BaudRate keeps symbol rate distinct from other quantities that share its physical
dimension.

A spacecraft telemetry link is configured for 250 kBd.
A separate reference oscillator happens to run at 250 kHz, but those numbers describe
different physical concepts:

>>> telemetry = Kilobaud(250)
>>> reference = Hertz(250_000)
>>> telemetry != reference
True

The distinction remains even when arithmetic would otherwise make the values look
interchangeable.

A serial instrument is upgraded from 9.6 kBd to 115.2 kBd:

>>> old_link = Kilobaud(9.6)
>>> new_link = Kilobaud(115.2)
>>> new_link - old_link
105.6 kBd

>>> new_link / old_link
100

A communication system can also express the same configured symbol rate at a different
engineering scale:

>>> link = Megabaud(2.5)
>>> link.to(KILOBAUD)
2500 kBd

For a fictional deep-space optical link, a 12.5 GBd symbol stream is combined with a
2.5 GBd secondary channel in the system configuration.
The aggregate configured symbol throughput is therefore 15 GBd:

>>> primary = Gigabaud(12.5)
>>> secondary = Gigabaud(2.5)
>>> primary + secondary
15 GBd

Notes
-----
A baud is one symbol per second:

``1 Bd = 1 symbol/s``

A symbol is not necessarily one bit.
A modulation scheme may encode multiple bits in one symbol, so a baud rate must not be
treated as a bit rate without knowing the signaling scheme.

For example, the numerical relationship

``2 MBd -> 8 Mbit/s``

would only follow from a modulation scheme carrying four bits per symbol.
`BaudRate` deliberately represents only the symbol rate.
The encoding belongs to the communication protocol.

`BaudRate` has the same physical dimension as `Frequency`, but `kuchka` keeps the
concepts separate.
A frequency counts periodic cycles, while a baud rate counts communication symbols.
Likewise, a sample rate counts acquired samples.
Equal dimensions do not make those concepts interchangeable.

`BAUD_RATE_UNITS` maps symbols such as ``"Bd"``, ``"kBd"``, ``"MBd"``, and ``"GBd"`` to
their constructors.
It is intended for boundary code that reads a symbol rate from configuration files,
device descriptors, protocol definitions, or other external sources.

See Also
--------
~kuchka.quantities.BaudRate
    Quantity type representing symbol rate.
~kuchka.quantities.Frequency
    Frequency of a periodic phenomenon.
~kuchka.quantities.SampleRate
    Rate at which samples are acquired.

"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from kuchka.dimensions import FREQUENCY
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import BaudRate
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

BAUD = UnitDef("baud", "Bd", Decimal(1), FREQUENCY)
KILOBAUD = UnitDef("kilobaud", "kBd", Decimal(1000), FREQUENCY)
MEGABAUD = UnitDef("megabaud", "MBd", Decimal(1_000_000), FREQUENCY)
GIGABAUD = UnitDef("gigabaud", "GBd", Decimal(1_000_000_000), FREQUENCY)

BaudRate._canonical_unit = BAUD  # noqa: SLF001 -- this module owns BaudRate's canonical unit


def Baud(value: Numeric) -> BaudRate:
    """Construct a BaudRate from a magnitude expressed in baud.

    Parameters
    ----------
    value : Numeric
        Symbol rate in baud.

    Returns
    -------
    BaudRate
        Symbol rate represented in baud.

    Examples
    --------
    A laboratory instrument communicates over a serial control link at
    115200 symbols per second:

    >>> link = Baud(115200)
    >>> link
    115200 Bd

    """
    return BaudRate(to_exact(value) * BAUD.scale, BAUD)


def Kilobaud(value: Numeric) -> BaudRate:
    """Construct a BaudRate from a magnitude expressed in kilobaud.

    Parameters
    ----------
    value : Numeric
        Symbol rate in kilobaud.

    Returns
    -------
    BaudRate
        Symbol rate represented in kilobaud.

    Examples
    --------
    A spacecraft telemetry channel is configured for 250 kBd.
    A later software revision raises the configured symbol rate to 400 kBd:

    >>> old_rate = Kilobaud(250)
    >>> new_rate = Kilobaud(400)
    >>> new_rate - old_rate
    150 kBd

    >>> new_rate / old_rate
    100

    """
    return BaudRate(to_exact(value) * KILOBAUD.scale, KILOBAUD)


def Megabaud(value: Numeric) -> BaudRate:
    """Construct a BaudRate from a magnitude expressed in megabaud.

    Parameters
    ----------
    value : Numeric
        Symbol rate in megabaud.

    Returns
    -------
    BaudRate
        Symbol rate represented in megabaud.

    Examples
    --------
    A radio modem is configured for a 2.5 MBd symbol stream:

    >>> modem = Megabaud(2.5)
    >>> modem.to(KILOBAUD)
    2500 kBd

    """
    return BaudRate(to_exact(value) * MEGABAUD.scale, MEGABAUD)


def Gigabaud(value: Numeric) -> BaudRate:
    """Construct a BaudRate from a magnitude expressed in gigabaud.

    Parameters
    ----------
    value : Numeric
        Symbol rate in gigabaud.

    Returns
    -------
    BaudRate
        Symbol rate represented in gigabaud.

    Examples
    --------
    A deep-space optical communications link uses a 12.5 GBd primary channel and a
    2.5 GBd secondary channel:

    >>> primary = Gigabaud(12.5)
    >>> secondary = Gigabaud(2.5)
    >>> primary + secondary
    15 GBd

    """
    return BaudRate(to_exact(value) * GIGABAUD.scale, GIGABAUD)


BAUD_RATE_UNITS: Mapping[str, Callable[[Numeric], BaudRate]] = unit_table(
    "BAUD_RATE_UNITS",
    {
        BAUD: Baud,
        KILOBAUD: Kilobaud,
        MEGABAUD: Megabaud,
        GIGABAUD: Gigabaud,
    },
)

__all__ = [
    "BAUD",
    "BAUD_RATE_UNITS",
    "GIGABAUD",
    "KILOBAUD",
    "MEGABAUD",
    "Baud",
    "Gigabaud",
    "Kilobaud",
    "Megabaud",
]
