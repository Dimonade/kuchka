"""Data-rate unit constructors: bits and bytes per second.

    from kuchka import GigabitPerSecond, MebibytePerSecond

`DataRate` measures how quickly information moves, with bit per second as its canonical
unit.
It has its own dimension, so link speed is not interchangeable with `Frequency`,
`SampleRate`, or `BaudRate`.
The module provides SI decimal multiples and IEC binary multiples for both bits and
bytes per second.

Examples
--------
A 750 MB firmware bundle must be delivered during a maintenance window over a
250 Mbit/s link.
Estimate the ideal transfer time before allowing for protocol overhead and
device-side validation:

>>> from kuchka import Megabyte
>>> duration = Megabyte(750) / MegabitPerSecond(250)
>>> f"{duration:.1f}"
'24.0 s'

A fleet of 50 sensors sends a 96-byte report every ten seconds.
Calculate the aggregate uplink requirement to size a shared telemetry channel:

>>> from kuchka import Byte, Second
>>> per_sensor = Byte(96) / Second(10)
>>> fleet_rate = per_sensor * 50
>>> f"{fleet_rate.to(KILOBIT_PER_SECOND):.2f}"
'3.84 kbit/s'

A nominally faster link does not change how much data fits into a fixed transfer
window.
At 800 Mbit/s, the expected payload budget for a 90-second window is:

>>> from kuchka.units.data import GIGABYTE
>>> (MegabitPerSecond(800) * Second(90)).to(GIGABYTE)
9 GB

A storage benchmark reports 300 MiB/s, while a network capacity plan is written in
decimal megabits per second.
Convert the measured throughput before comparing it with the network budget:

>>> f"{MebibytePerSecond(300).to(MEGABIT_PER_SECOND):.1f}"
'2516.6 Mbit/s'

Notes
-----
Network interfaces and link contracts are commonly expressed in bits per second
(`Mbit/s`, `Gbit/s`); storage tools usually report bytes per second (`MB/s`,
`MiB/s`).
The lowercase `b` denotes bits and uppercase `B` denotes bytes.
SI prefixes use powers of 1000, while IEC prefixes use powers of 1024.

These calculations describe nominal or configured throughput.
Real transfer rates can be lower because of framing, acknowledgements, congestion,
storage latency, retransmissions, and application processing.
A baud rate counts symbols per second, not bits per second, and remains a separate
`BaudRate` quantity.

`DATA_RATE_UNITS` maps symbols such as ``"Mbit/s"``, ``"MB/s"``, ``"MiB/s"``,
and ``"bps"`` to their constructors.
It is intended for boundary code that reads throughput values from configuration files,
network diagnostics, benchmarks, or external device descriptors.

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
    A 12-byte status packet sent five times per second consumes this bit rate on the
    telemetry link:

    >>> from kuchka import Byte, Second
    >>> packet_rate = (Byte(12) * 5) / Second(1)
    >>> packet_rate.to(BIT_PER_SECOND)
    480 bit/s

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
    A 24 KiB diagnostic log sent over a 9.6 kbit/s maintenance link needs this much
    transfer time:

    >>> from kuchka import Kibibyte
    >>> duration = Kibibyte(24) / KilobitPerSecond(9.6)
    >>> f"{duration:.2f}"
    '20.48 s'

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
    A 12 Mbit/s recording stream running for 45 minutes produces this amount of data
    before container and filesystem overhead:

    >>> from kuchka import Second
    >>> from kuchka.units.data import GIGABYTE
    >>> recording = MegabitPerSecond(12) * Second(45 * 60)
    >>> recording.to(GIGABYTE)
    4.05 GB

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
    A 250 GB backup sent over a dedicated 10 Gbit/s link has this expected transfer
    time:

    >>> from kuchka import Gigabyte
    >>> duration = Gigabyte(250) / GigabitPerSecond(10)
    >>> f"{duration:.0f}"
    '200 s'

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
    An aggregate 2 Tbit/s datacenter fabric moves this much payload in a 30-second
    measurement window:

    >>> from kuchka import Second
    >>> from kuchka.units.data import TERABYTE
    >>> moved = TerabitPerSecond(2) * Second(30)
    >>> moved.to(TERABYTE)
    7.5 TB

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
    At an aggregate rate of 1 Pbit/s, an eight-second data movement window carries one
    decimal petabyte:

    >>> from kuchka import Second
    >>> from kuchka.units.data import PETABYTE
    >>> (PetabitPerSecond(1) * Second(8)).to(PETABYTE)
    1 PB

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
    A 64 Kibit/s service channel can deliver this much data during a 15-second
    diagnostic session:

    >>> from kuchka import Second
    >>> from kuchka.units.data import KIBIBYTE
    >>> (KibibitPerSecond(64) * Second(15)).to(KIBIBYTE)
    120 KiB

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
    A 384 MiB capture transferred at 96 Mibit/s takes this long on a perfect channel:

    >>> from kuchka import Mebibyte
    >>> duration = Mebibyte(384) / MebibitPerSecond(96)
    >>> f"{duration:.0f}"
    '32 s'

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
    A 2 Gibit/s channel carries this much data in a five-second burst:

    >>> from kuchka import Second
    >>> from kuchka.units.data import GIBIBYTE
    >>> (GibibitPerSecond(2) * Second(5)).to(GIBIBYTE)
    1.25 GiB

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
    A 32 TiB checkpoint crossing a 4 Tibit/s aggregate fabric has this expected
    transfer time:

    >>> from kuchka import Tebibyte
    >>> duration = Tebibyte(32) / TebibitPerSecond(4)
    >>> f"{duration:.0f}"
    '64 s'

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
    Moving a 16 PiB dataset over an aggregate 8 Pibit/s data path takes this long in
    the case that everything is perfect:

    >>> from kuchka import Pebibyte
    >>> duration = Pebibyte(16) / PebibitPerSecond(8)
    >>> f"{duration:.0f}"
    '16 s'

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
    A logger writes a 24-byte status record 20 times each second.
    Its payload rate is:

    >>> from kuchka import Byte, Second
    >>> log_rate = (Byte(24) * 20) / Second(1)
    >>> log_rate.to(BYTE_PER_SECOND)
    480 B/s

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
    A 480 kB diagnostic archive copied at 12 kB/s requires this much transfer time:

    >>> from kuchka import Kilobyte
    >>> duration = Kilobyte(480) / KilobytePerSecond(12)
    >>> f"{duration:.0f}"
    '40 s'

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
    A video-ingest service sustaining 150 MB/s accepts this much footage in a ten
    minute capture window:

    >>> from kuchka import Second
    >>> from kuchka.units.data import GIGABYTE
    >>> captured = MegabytePerSecond(150) * Second(10 * 60)
    >>> captured.to(GIGABYTE)
    90 GB

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
    A 800 GB working set flushed at 5 GB/s takes this long under nominal conditions:

    >>> from kuchka import Gigabyte
    >>> duration = Gigabyte(800) / GigabytePerSecond(5)
    >>> f"{duration:.0f}"
    '160 s'

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
    An in-memory cluster shuffle moving 8 TB across an aggregate 2 TB/s pipeline has
    the following expected completion time:

    >>> from kuchka import Terabyte
    >>> duration = Terabyte(8) / TerabytePerSecond(2)
    >>> f"{duration:.0f}"
    '4 s'

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
    A 3 PB simulation checkpoint drained through a sustained 0.5 PB/s aggregate
    pipeline requires this much time in the idealized model:

    >>> from kuchka import Petabyte
    >>> duration = Petabyte(3) / PetabytePerSecond(0.5)
    >>> f"{duration:.0f}"
    '6 s'

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
    A 384 KiB device configuration sent at 64 KiB/s takes this long over a maintenance
    channel:

    >>> from kuchka import Kibibyte
    >>> duration = Kibibyte(384) / KibibytePerSecond(64)
    >>> f"{duration:.0f}"
    '6 s'

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
    Four capture workers each writing at 250 MiB/s create a combined storage load of
    1000 MiB/s.
    Express it in GiB/s for comparison with the host bus:

    >>> aggregate = MebibytePerSecond(250) * 4
    >>> f"{aggregate.to(GIBIBYTE_PER_SECOND):.3f}"
    '0.977 GiB/s'

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
    A checkpoint pipeline sustaining 8 GiB/s writes this much data in two seconds:

    >>> from kuchka import Second
    >>> from kuchka.units.data import GIBIBYTE
    >>> (GibibytePerSecond(8) * Second(2)).to(GIBIBYTE)
    16 GiB

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
    An array sustaining 4 TiB/s can stream this much data during a six-second
    benchmark interval:

    >>> from kuchka import Second
    >>> from kuchka.units.data import TEBIBYTE
    >>> (TebibytePerSecond(4) * Second(6)).to(TEBIBYTE)
    24 TiB

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
    At an aggregate 1 PiB/s, a 5 PiB distributed archive takes the following amount of
    time to pass through the pipeline:

    >>> from kuchka import Pebibyte
    >>> duration = Pebibyte(5) / PebibytePerSecond(1)
    >>> f"{duration:.0f}"
    '5 s'

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
