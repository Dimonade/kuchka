"""Run this file directly: `python demo.py` from this directory.

The story: line 3's end-of-line tester decides whether an LED board passes by comparing
its measurements with acceptance limits, and the limits live in a TOML file that
engineers edit by hand.
The same file is read here four ways, from the one that does the most for you to the one
that shows how it all works:

    1. Pydantic        annotate the fields and the whole file validates
    2. attrs           one converter and one validator per field
    3. parse           no framework: one function reads a measurement
    4. the UNITS tables  how the file was made from the legacy one

Needs `pip install "kuchka[pydantic]" attrs`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import migrate
import settings_attrs
import settings_parse
import settings_pydantic
from pydantic import ValidationError

from kuchka import BoundsError
from kuchka import parse
from kuchka import wire
from kuchka.bounds import Bounds

HERE = Path(__file__).parent
MODERN = (HERE / "config_modern.toml").read_text(encoding="utf-8")
LEGACY = (HERE / "config_legacy.ini").read_text(encoding="utf-8")


def heading(title: str) -> None:
    """Print a section heading."""
    print(f"\n{'=' * 72}\n{title}\n{'=' * 72}\n")


def limits(config: Any) -> dict[str, str]:  # noqa: ANN401 -- any rung's configuration
    """Write every limit of a configuration as text, whichever rung built it.

    The three rungs share the names of the fields, so one function reads them all.
    """
    written = {}
    for led in ("red_led", "blue_led"):
        for field in ("accepted_voltage", "accepted_current", "accepted_temperature"):
            window = getattr(getattr(config, led), field)
            written[f"{led}.{field}"] = (
                f"{wire.dump(window.minimum)} .. {wire.dump(window.maximum)}"
            )
    written["comms.uart_baud_rate"] = wire.dump(config.comms.uart_baud_rate)
    written["comms.sensor_poll_rate"] = wire.dump(config.comms.sensor_poll_rate)
    return written


def show(config: Any) -> None:  # noqa: ANN401 -- any rung's configuration
    """Print the limits of a configuration."""
    for name, value in limits(config).items():
        print(f"  {name:<32}{value}")


# Three honest mistakes, and the two that engineers make while copy-pasting.
MISTAKES = {
    "a current's unit in a voltage field": ('minimum = "-1 mV"', 'minimum = "-1 mA"'),
    "a number with no unit (TOML reads it as a float)": (
        'minimum = "-1 mV"',
        "minimum = -1.0",
    ),
    "a limit the fixture's hardware cannot reach": (
        'maximum = "20 mA"',
        'maximum = "0.5 A"',
    ),
    "a minimum and a maximum swapped": (
        'minimum = "15 °C"\nmaximum = "45 °C"',
        'minimum = "45 °C"\nmaximum = "15 °C"',
    ),
}


def broken(old: str, new: str) -> str:
    """Return the shipped file with `old` replaced by `new`, once."""
    assert old in MODERN, old  # noqa: S101 -- a typo in this demo would hide the point
    return MODERN.replace(old, new, 1)


def rung_pydantic() -> None:
    """Rung 1: the whole file validates, and every mistake is reported at once."""
    heading("Rung 1 -- Pydantic: annotate the fields")
    config = settings_pydantic.loads(MODERN)
    print("config_modern.toml, read with one call, `DeviceConfig.model_validate`:\n")
    show(config)

    print("\nNow the mistakes. Pydantic names where each one is:\n")
    for what, (old, new) in MISTAKES.items():
        print(f"  {what}")
        try:
            settings_pydantic.loads(broken(old, new))
        except ValidationError as error:
            for problem in error.errors():
                where = ".".join(str(part) for part in problem["loc"])
                message = problem["msg"].removeprefix("Value error, ")
                print(f"     {where}: {message}")
        print()

    print("  Two mistakes in one file are both reported, in one go:")
    both = broken('minimum = "-1 mV"', 'minimum = "-1 mA"')
    both = both.replace('uart_baud_rate = "9600 Bd"', 'uart_baud_rate = "9600 V"')
    try:
        settings_pydantic.loads(both)
    except ValidationError as error:
        for problem in error.errors():
            where = ".".join(str(part) for part in problem["loc"])
            print(f"     {where}")


def rung_attrs() -> None:
    """Rung 2: the same file with attrs, which stops at the first mistake."""
    heading("Rung 2 -- attrs: one converter and one validator per field")
    config = settings_attrs.loads(MODERN)
    print("The same file, the same limits:\n")
    show(config)

    print("\nThe same mistakes. attrs stops at the first, and says less about where:\n")
    for what, (old, new) in MISTAKES.items():
        print(f"  {what}")
        try:
            settings_attrs.loads(broken(old, new))
        except (ValueError, TypeError) as error:
            print(f"     {type(error).__name__}: {error}")
        print()


def rung_parse() -> None:
    """Rung 3: the same file by hand, with messages written for this application."""
    heading("Rung 3 -- parse: no framework")
    config = settings_parse.loads(MODERN)
    print("The same file; the code around `parse` is what rungs 1 and 2 do for you:\n")
    show(config)

    print("\nThe same mistakes, in the application's own ConfigError:\n")
    for what, (old, new) in MISTAKES.items():
        print(f"  {what}")
        try:
            settings_parse.loads(broken(old, new))
        except settings_parse.ConfigError as error:
            print(f"     ConfigError: {error}")
        print()


def agree() -> None:
    """Show that the three rungs read the same file into the same limits."""
    heading("The three rungs agree")
    pydantic = limits(settings_pydantic.loads(MODERN))
    attrs = limits(settings_attrs.loads(MODERN))
    by_hand = limits(settings_parse.loads(MODERN))
    print(f"  Pydantic == attrs == parse:  {pydantic == attrs == by_hand}")
    print(
        "\n  red_led's voltage limit is written in millivolts, blue_led's in volts, and"
    )
    print("  the temperatures in degrees Celsius and kelvin: nothing was converted.")


def on_the_line() -> None:
    """Use the limits: measurements in whatever unit the instruments speak."""
    heading("On the line -- board 1042 against the limits")
    config = settings_pydantic.loads(MODERN)
    measured = [
        ("red_led", "accepted_voltage", "0.0004 V"),
        ("red_led", "accepted_current", "21.5 mA"),
        ("blue_led", "accepted_voltage", "3.31 V"),
        ("blue_led", "accepted_temperature", "30 °C"),
    ]
    for led, field, text in measured:
        window = getattr(getattr(config, led), field)
        accepted = Bounds(ge=window.minimum, le=window.maximum)
        name = f"{led}.{field.removeprefix('accepted_')}"
        try:
            accepted.check(parse(text, type(window.minimum)))
        except BoundsError as error:
            print(f"  {name:<24}FAIL  {error}")
        else:
            print(f"  {name:<24}pass  {text}")
    print("\n  The voltage is in volts against a window in millivolts, and the")
    print(
        "  temperature in Celsius against a window in kelvin: the comparison is exact."
    )


def excerpt(text: str, section: str, count: int) -> list[str]:
    """Return the header of `section` and its first `count` entries."""
    lines = text.splitlines()
    start = lines.index(f"[{section}]")
    return lines[start : start + 1 + count]


def rung_tables() -> None:
    """Rung 4: how the modern file was made, from a legacy file with units in names."""
    heading("Rung 4 -- the UNITS tables: how the file was made")
    print("The legacy file keeps units in the key names:\n")
    for section in ("red_led", "blue_led"):
        for line in excerpt(LEGACY, section, 2):
            print(f"  {line}")
    print("\nThe number and the unit arrive apart. A table turns the spelling into the")
    print("quantity, VOLTAGE_UNITS['mV'] is Millivolt, and the digits stay as typed.\n")
    modern = migrate.migrate(LEGACY)
    print("migrate.py writes what every rung above reads, one exact string a value:\n")
    for line in excerpt(modern, "red_led.accepted_voltage", 2):
        print(f"  {line}")
    print(f"\n  identical to the shipped config_modern.toml: {modern == MODERN}")

    print(
        "\nThe convention was never checked. A voltage key with a current's suffix:\n"
    )
    legacy = LEGACY.replace("accepted_voltage_min_mv", "accepted_voltage_min_ma", 1)
    try:
        migrate.migrate(legacy)
    except migrate.MigrationError as error:
        print(f"  MigrationError: {error}")
        print("  The old parser read it as a voltage. The voltage table has no 'mA'.")


def main() -> None:
    """Walk the ladder, from the framework that does the most to the tables."""
    print("Line 3's tester reads its acceptance limits from config_modern.toml.")
    print("Four ways to read it, from the most used to the one that explains it all.")
    rung_pydantic()
    rung_attrs()
    rung_parse()
    agree()
    on_the_line()
    rung_tables()


if __name__ == "__main__":
    main()
