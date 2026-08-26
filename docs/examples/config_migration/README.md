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
min = { value = "-1.000", unit = "mV" }
max = { value = "1.000", unit = "mV" }

[blue_led.accepted_voltage]
min = { value = "0.000", unit = "V" }
max = { value = "3.300", unit = "V" }
```

The unit is now a field, not a naming convention.
`device_config.py` reads it and checks it against the physical dimension the field expects.
An engineer can still write the wrong unit -- but now something checks.

One deliberate detail: `value` is a quoted string, not a bare TOML number.
TOML's bare numbers are binary floats.
Quoting the value means `device_config.py` parses the digits through `Decimal(str)`, the same reason `kuchka` itself stores magnitudes as `Decimal` rather than `float`.

## The boundary layer

`device_config.py` is the only file in this example that ever sees a unit as a string.
Its job, in three parts:

**1. Unit resolution is closed per dimension, using tables kuchka already maintains.**

```python
from kuchka.units import VOLTAGE_UNITS, CURRENT_UNITS
```

`kuchka.units` ships a `Mapping[str, Callable[[Numeric], Q]]` for every
dimension it knows about -- `VOLTAGE_UNITS`, `CURRENT_UNITS`,
`TEMPERATURE_UNITS`, `FREQUENCY_UNITS`, `BAUD_RATE_UNITS`, and so on --
each one closed to that dimension's own constructors and immutable
(`MappingProxyType`, not a plain `dict`). A voltage field only ever
looks its unit up in `VOLTAGE_UNITS`. Writing `unit = "mA"` for a
voltage field isn't "the wrong prefix" -- `"mA"` simply isn't in that
table, so it fails the same way a typo would. Nothing in this example
hand-builds these tables; every application doing config-boundary work
would otherwise be maintaining the same mapping independently, and
kuchka is the one place that already knows every constructor it exports.

**2. A value becomes a quantity, once.**

```python
def _build_quantity(raw, units, *, field):
    magnitude = Decimal(raw["value"])
    constructor = units[raw["unit"]]
    return constructor(magnitude)
```

Everything past this function only ever sees a `Voltage`, a `Current`, a `Temperature`, a `Frequency`, or a `BaudRate`.
Never a bare number again.

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

1. **A unit from the wrong dimension** -- `unit = "mA"` written into a voltage field.
2. **A unit nothing recognises** -- `unit = "dBm"`.
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

No manual "convert both to the same unit first" step.
That step already happened, once, at the boundary.

## Frequency and BaudRate, the same way

The `comms` section in `config_modern.toml` exercises two more dimensions the same way:

```toml
[comms]
uart_baud_rate = { value = "9600", unit = "Bd" }
sensor_poll_rate = { value = "500", unit = "Hz" }
```

```python
from kuchka.units import FREQUENCY_UNITS, BAUD_RATE_UNITS
```

`Frequency` and `BaudRate` share a physical dimension but are different concepts (see the main README's "Same dimension, different concepts").
Nothing about that distinction needed special handling here -- adding a new dimension to this config format is "import one more table, add one more dataclass field", the same shape as every dimension before it.

## What this example is not

This is not a pitch for validating untrusted input.
The premise here is narrower and more specific:
a config file that engineers on the same team write and maintain, where the realistic failure mode is a mistyped unit or a copy-paste error, not an adversarial payload.
If the config format needs to defend against malicious input, that's a different problem with a different toolset -- this example is about catching honest mistakes as early and as clearly as possible, which is the problem `kuchka` is for.
