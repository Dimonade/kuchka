"""Run this file directly: `python demo.py` from this directory.

Loads config_modern.toml successfully, then deliberately breaks it three
different ways to show what the boundary layer catches, and how.
"""

from __future__ import annotations

import tomllib
from pathlib import Path

from device_config import ConfigError
from device_config import load_device_config


def main() -> None:
    """Load the shipped config, then break it three different ways."""
    config_path = Path(__file__).parent / "config_modern.toml"
    config = load_device_config(config_path)

    print("Loaded config_modern.toml successfully:\n")
    print(f"  red_led voltage limits:  {config.red_led.voltage}")
    print(f"  blue_led voltage limits: {config.blue_led.voltage}")
    print(f"  red_led current limits:  {config.red_led.current}")
    print(f"  blue_led current limits: {config.blue_led.current}")
    print(f"  red_led temp limits:     {config.red_led.temperature}")
    print(f"  blue_led temp limits:    {config.blue_led.temperature}")
    print(f"  comms settings:          {config.comms}")

    # The point of the exercise: red_led's voltage limit was written in millivolts,
    # blue_led's in volts, and this comparison is still just ordinary Python --
    # no manual unit alignment required to ask a meaningful question across the two.
    print(
        "\n  red_led max voltage < blue_led max voltage: "
        f"{config.red_led.voltage.maximum < config.blue_led.voltage.maximum}",
    )

    print("\nNow, three ways a config file can go wrong:\n")

    wrong_dimension_toml = """
    [red_led.accepted_voltage]
    min = { value = "-1.000", unit = "mA" }
    max = { value = "1.000", unit = "mV" }
    [red_led.accepted_current]
    min = { value = "0.000", unit = "mA" }
    max = { value = "20.000", unit = "mA" }
    [red_led.accepted_temperature]
    min = { value = "15.0", unit = "C" }
    max = { value = "45.0", unit = "C" }
    """
    _show_failure(
        "1. A unit that belongs to the wrong dimension "
        '(milliamps written into a voltage field, unit = "mA")',
        wrong_dimension_toml,
        section="red_led",
    )

    unknown_unit_toml = """
    [red_led.accepted_voltage]
    min = { value = "-1.000", unit = "dBm" }
    max = { value = "1.000", unit = "mV" }
    [red_led.accepted_current]
    min = { value = "0.000", unit = "mA" }
    max = { value = "20.000", unit = "mA" }
    [red_led.accepted_temperature]
    min = { value = "15.0", unit = "C" }
    max = { value = "45.0", unit = "C" }
    """
    _show_failure(
        '2. A unit nothing recognises at all (unit = "dBm")',
        unknown_unit_toml,
        section="red_led",
    )

    inverted_range_toml = """
    [red_led.accepted_voltage]
    min = { value = "1.000", unit = "mV" }
    max = { value = "-1.000", unit = "mV" }
    [red_led.accepted_current]
    min = { value = "0.000", unit = "mA" }
    max = { value = "20.000", unit = "mA" }
    [red_led.accepted_temperature]
    min = { value = "15.0", unit = "C" }
    max = { value = "45.0", unit = "C" }
    """
    _show_failure(
        "3. A minimum that is actually larger than the maximum (a copy-paste swap)",
        inverted_range_toml,
        section="red_led",
    )


def _show_failure(description: str, broken_toml: str, *, section: str) -> None:
    from device_config import _parse_led_limits  # noqa: PLC0415, I001 -- demo-only, internal helper.

    print(f"  {description}")
    raw = tomllib.loads(broken_toml)
    try:
        _parse_led_limits(raw[section], led_name=section)
    except ConfigError as error:
        print(f"     -> ConfigError: {error}\n")
    else:
        print("     -> unexpectedly succeeded\n")


if __name__ == "__main__":
    main()
