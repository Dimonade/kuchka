"""Boundary layer for device-limits configuration: TOML in, typed settings out.

This is the only place in an application that should ever see a unit as a string.
Everything below `load_device_config` returns typed `kuchka` quantities;
nothing downstream of it ever sees a bare number again.

Three rules, matching `kuchka`'s own design:

1. Unit resolution is closed per physical dimension.
    A voltage field only ever looks a unit symbol up in `VOLTAGE_UNITS`;
    writing `unit = "mA"` for a voltage field is not "the wrong prefix",
    it is a symbol that simply is not in that table, and fails the same way a typo
    would.
2. A value is parsed through `Decimal(str)`, never `float(str)`, for the same reason
    `kuchka` itself stores magnitudes as `Decimal`:
    the digits an engineer typed should survive parsing exactly.
3. Unknown keys are treated the same as missing ones.
    A typo'd section or field name fails loudly at load time, not silently three
    functions later when something expected is `None`.
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from decimal import Decimal
from decimal import InvalidOperation
from typing import Any
from typing import TYPE_CHECKING

from kuchka import Ampere
from kuchka import Baud
from kuchka import BaudRate
from kuchka import Celsius
from kuchka import Current
from kuchka import Frequency
from kuchka import Hertz
from kuchka import Kelvin
from kuchka import Kiloampere
from kuchka import Kilobaud
from kuchka import Kilohertz
from kuchka import Kilovolt
from kuchka import Megahertz
from kuchka import Microampere
from kuchka import Microvolt
from kuchka import Milliampere
from kuchka import Millivolt
from kuchka import Temperature
from kuchka import Volt
from kuchka import Voltage

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping
    from pathlib import Path

    from kuchka.numeric import Numeric


class ConfigError(Exception):
    """A device-limits config file could not be parsed into typed settings."""


# Unit resolution tables: one per physical dimension, deliberately closed.
# A field for one dimension can never accidentally accept a unit that
# belongs to a different one, because it is never even looked up in that
# dimension's table.
VOLTAGE_UNITS: Mapping[str, Callable[[Numeric], Voltage]] = {
    "uV": Microvolt,
    "mV": Millivolt,
    "V": Volt,
    "kV": Kilovolt,
}
CURRENT_UNITS: Mapping[str, Callable[[Numeric], Current]] = {
    "uA": Microampere,
    "mA": Milliampere,
    "A": Ampere,
    "kA": Kiloampere,
}
TEMPERATURE_UNITS: Mapping[str, Callable[[Numeric], Temperature]] = {
    "C": Celsius,
    "K": Kelvin,
}
FREQUENCY_UNITS: Mapping[str, Callable[[Numeric], Frequency]] = {
    "Hz": Hertz,
    "kHz": Kilohertz,
    "MHz": Megahertz,
}
BAUD_RATE_UNITS: Mapping[str, Callable[[Numeric], BaudRate]] = {
    "Bd": Baud,
    "kBd": Kilobaud,
}


def _build_quantity[Q](
    raw: Mapping[str, Any],
    units: Mapping[str, Callable[[Numeric], Q]],
    *,
    field: str,
) -> Q:
    """Turn a {value, unit} table into a typed quantity, or fail with why."""
    try:
        raw_value = raw["value"]
        unit_symbol = raw["unit"]
    except KeyError as exc:
        msg = f"{field}: expected a table with 'value' and 'unit', got {raw!r}"
        raise ConfigError(msg) from exc

    try:
        magnitude = Decimal(raw_value)
    except InvalidOperation as exc:
        msg = f"{field}: {raw_value!r} is not a valid decimal number"
        raise ConfigError(msg) from exc

    try:
        constructor = units[unit_symbol]
    except KeyError as exc:
        allowed = ", ".join(sorted(units))
        msg = (
            f"{field}: unit {unit_symbol!r} is not recognised for this "
            f"field's physical dimension. Expected one of: {allowed}."
        )
        raise ConfigError(msg) from exc

    return constructor(magnitude)


@dataclass(frozen=True)
class VoltageLimits:
    """The accepted voltage range for one device, min and max inclusive."""

    minimum: Voltage
    maximum: Voltage

    def __post_init__(self) -> None:
        if self.minimum > self.maximum:
            msg = f"minimum voltage {self.minimum!r} exceeds maximum {self.maximum!r}"
            raise ConfigError(msg)


@dataclass(frozen=True)
class CurrentLimits:
    """The accepted current range for one device, min and max inclusive."""

    minimum: Current
    maximum: Current

    def __post_init__(self) -> None:
        if self.minimum > self.maximum:
            msg = f"minimum current {self.minimum!r} exceeds maximum {self.maximum!r}"
            raise ConfigError(msg)


@dataclass(frozen=True)
class TemperatureLimits:
    """The accepted case-temperature range for one device, min and max inclusive."""

    minimum: Temperature
    maximum: Temperature

    def __post_init__(self) -> None:
        if self.minimum > self.maximum:
            msg = (
                f"minimum temperature {self.minimum!r} exceeds maximum {self.maximum!r}"
            )
            raise ConfigError(msg)


@dataclass(frozen=True)
class LedLimits:
    """The full set of accepted operating limits for one LED."""

    voltage: VoltageLimits
    current: CurrentLimits
    temperature: TemperatureLimits


@dataclass(frozen=True)
class CommsSettings:
    """Communication settings shared across the device: how fast, how often."""

    uart_baud_rate: BaudRate
    sensor_poll_rate: Frequency


@dataclass(frozen=True)
class DeviceConfig:
    """The fully typed device configuration: what the rest of the application sees."""

    red_led: LedLimits
    blue_led: LedLimits
    comms: CommsSettings


def _parse_led_limits(raw: Mapping[str, Any], *, led_name: str) -> LedLimits:
    return LedLimits(
        voltage=VoltageLimits(
            minimum=_build_quantity(
                raw["accepted_voltage"]["min"],
                VOLTAGE_UNITS,
                field=f"{led_name}.accepted_voltage.min",
            ),
            maximum=_build_quantity(
                raw["accepted_voltage"]["max"],
                VOLTAGE_UNITS,
                field=f"{led_name}.accepted_voltage.max",
            ),
        ),
        current=CurrentLimits(
            minimum=_build_quantity(
                raw["accepted_current"]["min"],
                CURRENT_UNITS,
                field=f"{led_name}.accepted_current.min",
            ),
            maximum=_build_quantity(
                raw["accepted_current"]["max"],
                CURRENT_UNITS,
                field=f"{led_name}.accepted_current.max",
            ),
        ),
        temperature=TemperatureLimits(
            minimum=_build_quantity(
                raw["accepted_temperature"]["min"],
                TEMPERATURE_UNITS,
                field=f"{led_name}.accepted_temperature.min",
            ),
            maximum=_build_quantity(
                raw["accepted_temperature"]["max"],
                TEMPERATURE_UNITS,
                field=f"{led_name}.accepted_temperature.max",
            ),
        ),
    )


def _parse_comms(raw: Mapping[str, Any]) -> CommsSettings:
    return CommsSettings(
        uart_baud_rate=_build_quantity(
            raw["uart_baud_rate"],
            BAUD_RATE_UNITS,
            field="comms.uart_baud_rate",
        ),
        sensor_poll_rate=_build_quantity(
            raw["sensor_poll_rate"],
            FREQUENCY_UNITS,
            field="comms.sensor_poll_rate",
        ),
    )


_KNOWN_TOP_LEVEL_SECTIONS = frozenset({"red_led", "blue_led", "comms"})


def load_device_config(path: Path) -> DeviceConfig:
    """Load and fully validate a device-limits TOML file into a `DeviceConfig`.

    Raises `ConfigError` for anything wrong with the file: an unknown
    section, a missing field, an unparsable number, or a unit that does
    not belong to the field it was written for.
    """
    with path.open("rb") as handle:
        raw = tomllib.load(handle)

    unknown_sections = set(raw) - _KNOWN_TOP_LEVEL_SECTIONS
    if unknown_sections:
        msg = f"unknown top-level section(s): {', '.join(sorted(unknown_sections))}"
        raise ConfigError(msg)

    missing_sections = _KNOWN_TOP_LEVEL_SECTIONS - set(raw)
    if missing_sections:
        msg = f"missing top-level section(s): {', '.join(sorted(missing_sections))}"
        raise ConfigError(msg)

    return DeviceConfig(
        red_led=_parse_led_limits(raw["red_led"], led_name="red_led"),
        blue_led=_parse_led_limits(raw["blue_led"], led_name="blue_led"),
        comms=_parse_comms(raw["comms"]),
    )
