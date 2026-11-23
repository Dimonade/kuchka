# A limits file, read four ways

Line 3's end-of-line tester decides whether an LED board passes by comparing its measurements with acceptance limits, and the limits live in a TOML file that engineers edit by hand.
This example reads that one file four ways, from the way that does the most for you to the way that shows how it all works, and then follows the file back to the legacy format it was migrated from.

Every rung reads the same `config_modern.toml` into the same typed limits, refuses the same mistakes, and checks the same thing the file can never be allowed to say: that it asks for more than the fixture's hardware can do.

```bash
pip install "kuchka[pydantic]" attrs
cd docs/examples/config_migration
python demo.py
```

| File                   | What it is                                                         |
| ---------------------- | ------------------------------------------------------------------ |
| `config_modern.toml`   | The limits file: one string per measurement, a number and its unit |
| `config_legacy.ini`    | The old format it was migrated from                                |
| `fixture.py`           | What the fixture's hardware can do                                 |
| `mistakes.py`          | Ways to break the file on purpose, for the demo and the tests      |
| `settings_pydantic.py` | Rung 1: annotate the fields                                        |
| `settings_attrs.py`    | Rung 2: a converter and a validator per field                      |
| `settings_parse.py`    | Rung 3: no framework, `parse` and ordinary Python                  |
| `migrate.py`           | Rung 4: the `*_UNITS` tables, and writing the file back            |
| `demo.py`              | Run this: walks the four rungs and breaks the file on purpose      |
| `test_*.py`            | Tests for each rung, and one that holds the rungs to each other    |

## The file

```toml
[red_led.accepted_voltage]
minimum = "-1 mV"
maximum = "1 mV"

[blue_led.accepted_voltage]
minimum = "0 V"
maximum = "3.3 V"

[red_led.accepted_temperature]
minimum = "15 °C"
maximum = "45 °C"

[blue_led.accepted_temperature]
minimum = "288.15 K"
maximum = "318.15 K"
```

The red LED's voltage window is in millivolts and the blue one's in volts; the temperatures are in degrees Celsius and in kelvin.
Each team wrote its limits in the unit its datasheet uses, and nothing converts them: the unit is part of the value, and a quantity compares in whatever unit either side was written.

Each measurement is one quoted string.
TOML's bare numbers are binary floats with no unit, so a bare number is refused, and the digits inside a string are read exactly, the way `kuchka` itself keeps magnitudes.

## Rung 1: Pydantic

`settings_pydantic.py` is the shortest way to a typed configuration, and the one most projects will take.
The annotations carry everything: which quantity each field is, and how far the hardware lets it go.

```python
SafeVoltage = Annotated[Voltage, Quantity, Bounds(ge=-MAX_VOLTAGE, le=MAX_VOLTAGE)]
```

```python
def loads(text: str) -> DeviceConfig:
    """Read a limits file from its TOML text; raises `pydantic.ValidationError`."""
    return DeviceConfig.model_validate(tomllib.loads(text))
```

That is the whole loader: Pydantic walks the nested tables, `Quantity` reads each string as the quantity the field names, and `Bounds` refuses what the fixture cannot do.
When the file has mistakes, Pydantic reports all of them at once, each with its path:

```text
red_led.accepted_voltage.minimum: 'mA' is not a unit of Voltage (see VOLTAGE_UNITS).
comms.uart_baud_rate: 'V' is not a unit of BaudRate (see BAUD_RATE_UNITS).
```

A minimum above its maximum is the one mistake no annotation can see, because it is about two fields.
Constructing a `Bounds` refuses an inverted range, so the window checks itself with one line:

```python
    @model_validator(mode="after")
    def _ordered(self) -> Self:
        Bounds(ge=self.minimum, le=self.maximum)  # raises ValueError when inverted
        return self
```

## Rung 2: attrs

`settings_attrs.py` is the same file with `attrs` classes: `parse_field` is the converter of a field, and `Bounds` is its validator.

```python
@attrs.define(frozen=True)
class VoltageWindow:
    """The accepted voltage range of one LED."""

    minimum: Voltage = attrs.field(
        converter=parse_field(Voltage),
        validator=SAFE_VOLTAGE,
    )
    maximum: Voltage = attrs.field(
        converter=parse_field(Voltage),
        validator=SAFE_VOLTAGE,
    )

    def __attrs_post_init__(self) -> None:
        Bounds(ge=self.minimum, le=self.maximum)  # raises ValueError when inverted
```

`attrs` does not walk nested tables, so `_nested`, three lines, turns a table into its class.
It also stops at the first mistake and says less about where it is: the error of a converter carries no attribute name, and none carries the path in the file.
That is the price of a lighter tool, and it is why the rung exists next to the first: a project that already uses `attrs` everywhere gets the same strictness without a new dependency.

One honest limit: `mypy` reads only named functions as converters, so `mypy --strict` reports `converter=parse_field(Voltage)` as unsupported, and types the constructor parameter as `Any`.
`pyright` reads it in full, so `VoltageWindow("-1 mV", "1 mV")` is accepted, `VoltageWindow(3.3, "1 mV")` is a static error there, and the attribute is a `Voltage` under both checkers.
See [the wire form](../../concepts/wire_form.md#in-an-attrs-class) for the named-function form that gives `mypy` the same constructor.

## Rung 3: parse

`settings_parse.py` is what the first two rungs do for you, written out.
`parse(text, Voltage)` reads one measurement and refuses what is no voltage; everything else is ordinary Python around it.

```python
    with _at(here):
        value = parse(text, quantity)
        return value if within is None else within.check(value)
```

`_at` names the key in any `ValueError` raised inside, which covers an unknown unit, unreadable text, a bound, and a swapped window alike.
Take this rung when the file is read by a program that already has its own configuration classes, or when the messages have to be written by hand:

```text
ConfigError: red_led.accepted_current.maximum: 0.5 A is above 100 mA, the most allowed.
```

A bare TOML number is refused because `parse` takes text, not because anything checks for it: `parse(2.8, Voltage)` is a `TypeError`, and the loader turns it into a message.

## Rung 4: the unit tables

`migrate.py` reads the legacy file, where the unit is in the name of the key:

```ini
[red_led]
accepted_voltage_min_mv = -1.000
accepted_voltage_max_mv = 1.000
```

The number and the unit reach a program as two separate pieces of text, so there is nothing for `parse` to read.
This is what the `*_UNITS` tables are for: a table maps the spelling of a unit to the constructor of the quantity.

```python
    label, table = TABLES[stem]
    spelling = SUFFIXES.get(suffix)
    constructor = None if spelling is None else table.get(spelling)
```

`VOLTAGE_UNITS["mV"]` is `Millivolt`, and `Millivolt(Decimal("-1.000"))` keeps the digits as they were typed.
`wire.dump` writes each quantity back as the one exact string every rung above reads, and `config_modern.toml` is the output of this rung, and a test holds the shipped file to the data the migration writes.

The old convention never checked that a suffix belonged to its key:

```ini
accepted_voltage_min_ma = -1.000
```

The old parser read that as a voltage.
Here the voltage table has no `mA`, and the migration says so instead of copying the mistake into the new file:

```text
MigrationError: red_led.accepted_voltage_min_ma: 'ma' is not a unit of voltage
```

## What each rung does for you

|                                     | Pydantic          | attrs                   | parse                                       |
| ----------------------------------- | ----------------- | ----------------------- | ------------------------------------------- |
| Walks nested tables                 | yes               | `_nested`, three lines  | by hand                                     |
| Refuses a unit of another quantity  | yes               | yes                     | yes                                         |
| Refuses a bare number               | yes               | yes                     | yes, as a `TypeError` turned into a message |
| Refuses what the hardware cannot do | `Bounds`          | `Bounds`                | `Bounds.check`                              |
| Refuses a swapped window            | one validator     | `__attrs_post_init__`   | `__post_init__`                             |
| Reports every mistake               | all at once       | the first               | the first                                   |
| Says where the mistake is           | the full path     | sometimes the attribute | the full path, written by hand              |
| Writes a value back as text         | `model_dump_json` | `wire.dump`             | `wire.dump`                                 |

`test_ladder.py` holds the three rungs to each other: the same file reads into the same limits, every mistake in `mistakes.py`, a list of nine, is refused by all three, and the file reads the same whatever its line endings.

## On the line

The point of a typed limit is what the application does with it.
A window is a range of measurements, and a measurement is checked against it in whatever unit the instrument speaks:

```python
        accepted = Bounds(ge=window.minimum, le=window.maximum)
        name = f"{led}.{field.removeprefix('accepted_')}"
        try:
            accepted.check(parse(text, type(window.minimum)))
```

Board 1042 comes off the line, and the instruments answer in their own units:

```text
red_led.voltage         pass  0.0004 V
red_led.current         FAIL  21.5 mA is above 20 mA, the most allowed.
blue_led.voltage        FAIL  3.31 V is above 3.3 V, the most allowed.
blue_led.temperature    pass  30 °C
```

The voltage is in volts against a window in millivolts, and the temperature in degrees Celsius against a window in kelvin.
Nothing was converted by hand, and the check is exact.

## Frequency and BaudRate, the same way

The `comms` table reads two more quantities the same way:

```toml
[comms]
uart_baud_rate = "9600 Bd"
sensor_poll_rate = "500 Hz"
```

`Frequency` and `BaudRate` share a physical dimension and are different concepts (see "Same dimension does not always mean the same concept" in the main README), so `"500 Hz"` in the baud rate field is refused by every rung, and a test says so.

## What this example is not

This is not a pitch for validating untrusted input.
The premise is narrower: a configuration that engineers on the same team write and maintain, where the realistic failure modes are a mistyped unit, a copy-paste error, and a limit nobody checked against the hardware, and not an adversarial payload.
If the format has to defend against malicious input, that is a different problem with a different toolset.
This example is about catching honest mistakes as early and as clearly as possible, which is the problem `kuchka` is for.

Run the tests the same way:

```bash
pytest docs/examples/config_migration
```
