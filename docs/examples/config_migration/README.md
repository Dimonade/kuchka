# Migrating a config from unit-suffixed keys to kuchka

An old `.ini` file where units live in the key name, migrated to a `.toml` file where units are data.
Then the data is parsed into typed dataclasses backed by kuchka quantities.

Files in this directory:

| File                    | What it is                                            |
| ----------------------- | ----------------------------------------------------- |
| `config_legacy.ini`     | The old format                                        |
| `config_modern.toml`    | The new format                                        |
| `device_config.py`      | The boundary layer: TOML in, typed dataclasses out    |
| `demo.py`               | Run this: loads the config, then breaks it three ways |
| `test_device_config.py` | Tests for `device_config.py`                          |

## The problem with the old format

```ini
[red_led]
accepted_voltage_min_mv = -1.000
accepted_voltage_max_mv = 1.000

[blue_led]
accepted_voltage_min_v = 0.000
accepted_voltage_max_v = 3.300
```

The unit is part of the key name, by convention. Nothing checks that convention.
An engineer can:

- write a millivolt value into a key ending `_v`
- copy a limit from `red_led` to `blue_led` without updating the suffix
- add a new field and forget the suffix entirely

The parser reading this file has no way to catch any of that.
It reads a number named `accepted_voltage_min_mv` and has to trust the name.

## The new format

```toml
[red_led.accepted_voltage]
min = "-1.000 mV"
max = "1.000 mV"

[blue_led.accepted_voltage]
min = "0.000 V"
max = "3.300 V"
```

The unit is now part of the value, not a naming convention, and `device_config.py` reads it through the quantity the field expects.
An engineer can still write the wrong unit -- but now something checks.

Each measurement is one quoted string.
TOML's bare numbers are binary floats with no unit, so a bare number is refused, and the digits inside the string are read exactly by `parse`, the same reason `kuchka` itself stores magnitudes as `Fraction`.

## The boundary layer

`device_config.py` is the only file in this example that ever reads a unit as text.
Its job, in three parts:

**1. Every field is closed to its own quantity by `parse`.**

```python
parse("-1.000 mV", Voltage)
```

`parse` reads the unit through the table of the type it is given.
Writing `"-1.000 mA"` for a voltage field isn't "the wrong prefix" -- `mA` simply isn't a unit of `Voltage`, so it fails the same way a typo would, with `UnknownUnitError`.
The code in this example builds no unit tables and splits no strings: `kuchka` is the one place that already knows every unit spelling.

**2. A value becomes a quantity, once.**

```python
def _read(section, path, quantity, *, field):
    ...
    return parse(node, quantity)
```

The rest of `_read` finds the field and turns a `ParseError` into a `ConfigError` that names it.
Everything past this function only ever sees a `Voltage`, a `Current`, a `Temperature`, a `Frequency`, or a `BaudRate`.
From this point on, it is never a bare number again, unless explicitly converted.

**3. Invalid configurations can't be constructed.**

```python
@dataclass(frozen=True)
class VoltageLimits:
    minimum: Voltage
    maximum: Voltage

    def __post_init__(self) -> None:
        if self.minimum > self.maximum:
            raise ConfigError(...)
```

A `VoltageLimits` where `minimum > maximum` doesn't exist.
There's no later code path that has to remember to check this, because the object that would represent it can't be built.

## Running it

```bash
cd docs/examples/config_migration
python demo.py
```

`demo.py` loads `config_modern.toml`, prints the parsed limits, then deliberately breaks the config three different ways and shows what `device_config.py` catches:

1. **A unit from the wrong quantity** -- `"-1.000 mA"` written into a voltage field.
2. **A value with no unit** -- a bare TOML number, `min = -1.0`.
3. **An inverted range** -- a copy-paste swap of `min` and `max`.

All three fail at load time, with a message that names the field and the reason, not three functions later as a `None` or a wrong comparison.

Run the tests the same way:

```bash
cd docs/examples/config_migration
pytest
```

## The payoff

`red_led`'s voltage limit is declared in millivolts.
`blue_led`'s is declared in volts.
Comparing them is still just Python:

```python
config.red_led.voltage.maximum < config.blue_led.voltage.maximum
```

The conversion to the same unit happens at the boundary.

## Frequency and BaudRate, the same way

The `comms` section in `config_modern.toml` exercises two more quantities the same way:

```toml
[comms]
uart_baud_rate = "9600 Bd"
sensor_poll_rate = "500 Hz"
```

`Frequency` and `BaudRate` share a physical dimension but are different concepts (see the main README's "Same dimension does not always mean the same concept").
Nothing about that distinction needed special handling here.
Adding a new quantity to this config format is "add one more dataclass field and one more `_read`", the same shape as every quantity before it.

## What this example is not

This is not a pitch for validating untrusted input.
The premise here is narrower and more specific:
a config file that engineers on the same team write and maintain, where the realistic failure mode is a mistyped unit or a copy-paste error, not an adversarial payload.

If the config format needs to defend against malicious input, that's a different problem with a different toolset -- this example is about catching honest mistakes as early and as clearly as possible, which is the problem `kuchka` is for.
