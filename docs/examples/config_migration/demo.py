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

    _show_failure(
        "1. A unit that belongs to the wrong quantity "
        '(milliamps written into a voltage field, "-1.000 mA")',
        old='min = "-1.000 mV"',
        new='min = "-1.000 mA"',
    )
    _show_failure(
        "2. A value with no unit at all (a bare TOML number, which is a float)",
        old='min = "-1.000 mV"',
        new="min = -1.0",
    )
    _show_failure(
        "3. A minimum that is actually larger than the maximum (a copy-paste swap)",
        old='min = "-1.000 mV"\nmax = "1.000 mV"',
        new='min = "1.000 mV"\nmax = "-1.000 mV"',
    )


def _show_failure(description: str, *, old: str, new: str) -> None:
    """Break the shipped config by replacing `old` with `new`, and show the failure."""
    from device_config import _parse_led_limits  # noqa: PLC0415 -- demo-only.

    print(f"  {description}")
    text = (Path(__file__).parent / "config_modern.toml").read_text(encoding="utf-8")
    raw = tomllib.loads(text.replace(old, new, 1))
    try:
        _parse_led_limits(raw["red_led"], led_name="red_led")
    except ConfigError as error:
        print(f"     -> ConfigError: {error}\n")
    else:
        print("     -> unexpectedly succeeded\n")


if __name__ == "__main__":
    main()
