"""Ways to break the limits file on purpose, shared by the demo and the tests.

Each mistake is a function from the text of the file to the text of a broken one.
They edit by table and key and not by searching for text, so they work whatever the
line endings of the file are, and whatever blank lines or comments a formatter left in
it.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


def _span(lines: list[str], table: str) -> tuple[int, int]:
    """Return the first line of `table` and the line where the next table starts."""
    header = f"[{table}]"
    start = next(i for i, line in enumerate(lines) if line.strip() == header)
    end = next(
        (i for i in range(start + 1, len(lines)) if lines[i].lstrip().startswith("[")),
        len(lines),
    )
    return start, end


def _line_of(lines: list[str], table: str, key: str) -> int:
    """Return the index of the line that sets `key` in `table`."""
    start, end = _span(lines, table)
    return next(
        i for i in range(start + 1, end) if lines[i].split("=")[0].strip() == key
    )


def _text(lines: list[str]) -> str:
    return "\n".join(lines) + "\n"


def set_value(text: str, table: str, key: str, value: str) -> str:
    """Set `key` of `table` to `value`, written as TOML: quoted for a string."""
    lines = text.splitlines()
    lines[_line_of(lines, table, key)] = f"{key} = {value}"
    return _text(lines)


def remove_key(text: str, table: str, key: str) -> str:
    """Remove `key` from `table`."""
    lines = text.splitlines()
    del lines[_line_of(lines, table, key)]
    return _text(lines)


def add_key(text: str, table: str, line: str) -> str:
    """Add the line `line` to `table`, right under its header."""
    lines = text.splitlines()
    lines.insert(_span(lines, table)[0] + 1, line)
    return _text(lines)


def swap_values(text: str, table: str, first: str, second: str) -> str:
    """Swap the values of the keys `first` and `second` of `table`."""
    lines = text.splitlines()
    one, two = _line_of(lines, table, first), _line_of(lines, table, second)
    value_one = lines[one].split("=", 1)[1].strip()
    value_two = lines[two].split("=", 1)[1].strip()
    lines[one] = f"{first} = {value_two}"
    lines[two] = f"{second} = {value_one}"
    return _text(lines)


VOLTAGE = "red_led.accepted_voltage"
CURRENT = "red_led.accepted_current"
TEMPERATURE = "red_led.accepted_temperature"

# The honest mistakes: a mistyped unit, a copy-paste error, a limit nobody checked.
MISTAKES: dict[str, Callable[[str], str]] = {
    "a current's unit in a voltage field": lambda text: set_value(
        text, VOLTAGE, "minimum", '"-1 mA"'
    ),
    "a number with no unit (TOML reads it as a float)": lambda text: set_value(
        text, VOLTAGE, "minimum", "-1.0"
    ),
    "text with no number": lambda text: set_value(text, VOLTAGE, "minimum", '"mV"'),
    "a current the fixture cannot source": lambda text: set_value(
        text, CURRENT, "maximum", '"0.5 A"'
    ),
    "a voltage the fixture cannot drive": lambda text: set_value(
        text, VOLTAGE, "maximum", '"6 V"'
    ),
    "a minimum and a maximum swapped": lambda text: swap_values(
        text, TEMPERATURE, "minimum", "maximum"
    ),
    "a frequency written as a baud rate": lambda text: set_value(
        text, "comms", "uart_baud_rate", '"500 Hz"'
    ),
    "a missing key": lambda text: remove_key(text, CURRENT, "maximum"),
    "an unknown key": lambda text: add_key(text, "comms", 'parity = "none"'),
}
