"""Rung 2, attrs: the same file, one converter and one validator per field.

`attrs` builds classes, and `parse_field` turns each field into a quantity: whatever the
file holds is read into the quantity type the field names, and `Bounds` checks it
against what the hardware can do.
`attrs` does not walk nested tables by itself, so `_nested` is the three lines that turn
a table into its class; and it stops at the first mistake, and says less about where it
is: a converter's error carries no attribute name, and none carries the path in the
file.
That is the price of a lighter tool.

Needs `attrs`, and nothing else from kuchka: `kuchka.attrs` imports nothing from it.
"""

from __future__ import annotations

import tomllib
from typing import TYPE_CHECKING
from typing import Any
from typing import TypeVar

import attrs
from fixture import MAX_CURRENT
from fixture import MAX_TEMPERATURE
from fixture import MAX_VOLTAGE
from fixture import MIN_TEMPERATURE

from kuchka import BaudRate
from kuchka import Current
from kuchka import Frequency
from kuchka import Milliampere
from kuchka import Temperature
from kuchka import Voltage
from kuchka.attrs import Bounds
from kuchka.attrs import parse_field

if TYPE_CHECKING:
    from collections.abc import Callable

_T = TypeVar("_T")

SAFE_VOLTAGE = Bounds(ge=-MAX_VOLTAGE, le=MAX_VOLTAGE)
SAFE_CURRENT = Bounds(ge=Milliampere(0), le=MAX_CURRENT)
SAFE_TEMPERATURE = Bounds(ge=MIN_TEMPERATURE, le=MAX_TEMPERATURE)


def _nested(cls: type[_T]) -> Callable[[Any], _T]:
    """Return a converter that builds `cls` from a table, and keeps an instance."""
    return lambda raw: raw if isinstance(raw, cls) else cls(**raw)


@attrs.define(frozen=True)
class VoltageWindow:
    """The accepted voltage range of one LED."""

    minimum: Voltage = attrs.field(
        converter=parse_field(Voltage), validator=SAFE_VOLTAGE
    )
    maximum: Voltage = attrs.field(
        converter=parse_field(Voltage), validator=SAFE_VOLTAGE
    )

    def __attrs_post_init__(self) -> None:
        Bounds(ge=self.minimum, le=self.maximum)  # raises ValueError when inverted


@attrs.define(frozen=True)
class CurrentWindow:
    """The accepted current range of one LED."""

    minimum: Current = attrs.field(
        converter=parse_field(Current), validator=SAFE_CURRENT
    )
    maximum: Current = attrs.field(
        converter=parse_field(Current), validator=SAFE_CURRENT
    )

    def __attrs_post_init__(self) -> None:
        Bounds(ge=self.minimum, le=self.maximum)  # raises ValueError when inverted


@attrs.define(frozen=True)
class TemperatureWindow:
    """The accepted case-temperature range of one LED."""

    minimum: Temperature = attrs.field(
        converter=parse_field(Temperature), validator=SAFE_TEMPERATURE
    )
    maximum: Temperature = attrs.field(
        converter=parse_field(Temperature), validator=SAFE_TEMPERATURE
    )

    def __attrs_post_init__(self) -> None:
        Bounds(ge=self.minimum, le=self.maximum)  # raises ValueError when inverted


@attrs.define(frozen=True)
class LedLimits:
    """Everything a measured LED has to stay within."""

    accepted_voltage: VoltageWindow = attrs.field(converter=_nested(VoltageWindow))
    accepted_current: CurrentWindow = attrs.field(converter=_nested(CurrentWindow))
    accepted_temperature: TemperatureWindow = attrs.field(
        converter=_nested(TemperatureWindow)
    )


@attrs.define(frozen=True)
class CommsSettings:
    """How fast the board talks, and how often the fixture polls it."""

    uart_baud_rate: BaudRate = attrs.field(converter=parse_field(BaudRate))
    sensor_poll_rate: Frequency = attrs.field(converter=parse_field(Frequency))


@attrs.define(frozen=True)
class DeviceConfig:
    """The typed configuration the rest of the application sees."""

    red_led: LedLimits = attrs.field(converter=_nested(LedLimits))
    blue_led: LedLimits = attrs.field(converter=_nested(LedLimits))
    comms: CommsSettings = attrs.field(converter=_nested(CommsSettings))


def loads(text: str) -> DeviceConfig:
    """Read a limits file from its TOML text; raises `ValueError` or `TypeError`."""
    return DeviceConfig(**tomllib.loads(text))
