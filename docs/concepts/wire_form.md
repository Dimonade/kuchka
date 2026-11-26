# The wire form: a measurement as data

A configuration file, a JSON payload, a database column, and a command line carry a measurement as plain data, and the typed value comes back when the data enters the program.
`kuchka.wire` is the pair of functions for that crossing: `dump` writes a measurement as one string, and `load` reads what a boundary delivered into the quantity type a field holds.

## The form

The written form is the exact number, a space, and the unit's display symbol:

```python
from fractions import Fraction

from kuchka import Celsius
from kuchka import Millivolt
from kuchka import Voltage
from kuchka import Volt
from kuchka import wire

wire.dump(Millivolt(2800))  # '2800 mV'
wire.dump(Volt(4.2))  # '4.2 V'
wire.dump(Celsius(-40))  # '-40 °C'
wire.dump(Volt(Fraction(1, 3)))  # '1/3 V'
wire.load("1/3 V", Voltage) == Volt(Fraction(1, 3))  # True
```

The number is the magnitude in the unit the measurement displays in, so a value comes back in the unit it was written in, and every shape and every published unit works: temperatures, angles, levels, and the rest.
A magnitude that is a terminating decimal is written as a decimal, and any other is written as a fraction, so no digit is rounded away.
`str(Volt(Fraction(1, 3)))` rounds to 28 digits for reading, which is why display is not the wire form.

A string is the form because every format a boundary uses can carry one: TOML, YAML, JSON, environment variables, command lines, CSV cells.
The text is also what `parse` reads, so `parse(wire.dump(value), type(value))` is the value that was written.

## Reading

`load(value, quantity)` takes what the boundary delivered for a field of one quantity type:

| What arrives                                | What `load` does                       |
| ------------------------------------------- | -------------------------------------- |
| an instance of `quantity`                   | returns it unchanged                   |
| text, `"2800 mV"`                           | reads it as `parse` does               |
| a mapping, `{"value": "7/3", "unit": "mV"}` | reads the number and the unit spelling |
| a number, for a `Proportion`                | reads it as a ratio                    |

```python
from kuchka import Proportion

wire.load({"value": "2800", "unit": "millivolts"}, Voltage)  # 2800 mV
wire.load(0.25, Proportion)  # 0.25 1
wire.load("25 %", Proportion)  # 25 %
```

The mapping is read and never written, so a file written by hand in that shape loads, and the one written form stays a single string.
Its value is a number or the text of one, and a `float` is read by the digits it shows, the way the unit constructors read it, so `0.1` is one tenth.
The unit is read through the table of the type, so every spelling in [Unit spellings](unit_spellings.md) works.

Everything else is refused, and a number with no unit is refused for every quantity that needs one:

```python
from kuchka import Ampere

wire.load(2.8, Voltage)  # rejected: `ParseError`.
wire.load("150 mA", Voltage)  # rejected: `UnknownUnitError`.
wire.load(Ampere(1), Voltage)  # rejected: `ParseError`.
wire.load(True, Proportion)  # rejected: `ParseError`.
```

A bare `2.8` does not say whether it is volts, and a binary float from a file has already lost digits before the program sees it.
A proportion is the exception because it has no unit to leave out: its table names the ratio as the bare unit, so a number with no unit is a ratio.
That makes `25` a ratio of twenty-five, which is `2500 %`, and a percent is written `"25 %"`.

## As a mapping

A JSON document or a database row often wants the number and the unit as two fields, and `to_dict` writes the same exact data that way, with `from_dict` as its reader:

```python
from kuchka import Millivolt
from kuchka import Voltage

wire.to_dict(Millivolt(2800))  # {'value': '2800', 'unit': 'mV'}
wire.to_dict(Volt(1) / 3)  # {'value': '1/3', 'unit': 'V'}
wire.from_dict({"value": "1/3", "unit": "V"}, Voltage) == Volt(1) / 3  # True
wire.from_dict({"value": "5", "unit": "mA"}, Voltage)  # rejected: `UnknownUnitError`.
wire.from_dict({"value": True, "unit": "V"}, Voltage)  # rejected: `ParseError`.
wire.from_dict("5 V", Voltage)  # rejected: `ParseError`.
```

The value is the text that `dump` writes, a decimal when the magnitude terminates and a fraction when it does not, so no digit is rounded away and the unit is the one the measurement displays in.
A ratio keeps its symbol, `1`, so the mapping is always explicit, and `from_dict` needs both keys where `load` lets a proportion go without a unit.
The text of `dump` remains the canonical form, and `load` reads both.

`unit` writes the measurement in another unit of its quantity, given as a spelling or as a unit constant, and the conversion is exact:

```python
wire.to_dict(Millivolt(2800), unit="V")  # {'value': '2.8', 'unit': 'V'}
wire.to_dict(Celsius(20), unit="K")  # {'value': '293.15', 'unit': 'K'}
wire.to_dict(Volt(1), unit="mA")  # rejected: `UnknownUnitError`.
```

A consumer that accepts only JSON numbers gets `as_float=True`, which writes `value` as an `int` when the magnitude is whole and as a `float` otherwise:

```python
wire.to_dict(Volt(4.2), as_float=True)  # {'value': 4.2, 'unit': 'V'}
wire.to_dict(Millivolt(2800), as_float=True)  # {'value': 2800, 'unit': 'mV'}
```

A float is exact only where it reads back to the same decimal: `4.2` does, and a third of a volt does not, so the default is the one that round-trips.
A magnitude beyond the range of a `float`, or so small that a `float` would write it as zero, is refused with an `InvalidMeasurementError` and never written as a wrong number.

## Errors

Every refusal of data is a `ParseError`, and a `ParseError` is a `ValueError`: text that is no measurement of the type, an unknown unit, a number with no unit, a measurement of another quantity type, and a value the quantity cannot hold, such as `-300 °C`.
A framework that reports the `ValueError` of a validator as a validation error needs nothing else, and one `except ParseError` around the loading of a file catches every bad value in it.
A `TypeError` marks a mistake in the program, such as a quantity that is no quantity type with units.

## In an attrs class

`kuchka.attrs.parse_field(Voltage)` is `load` for one quantity type, as the converter of an `attrs` field:

```python
from collections.abc import Mapping

import attrs

from kuchka import Voltage
from kuchka.attrs import parse_field


@attrs.define(frozen=True)
class SensorSpec:
    threshold: Voltage = attrs.field(converter=parse_field(Voltage))


SensorSpec("2800 mV").threshold  # 2800 mV
SensorSpec(3.3)  # rejected: `ParseError`.
```

The attribute is a `Voltage` whatever arrived, and a value that is no voltage fails when the instance is made, with a `ValueError` that says why.
The converter is a plain function, so `kuchka.attrs` imports nothing from `attrs`.

`pyright` reads the converter in full, so `SensorSpec(3.3)` is a static error there.
`mypy` types the attribute as `Voltage` and reports a converter that is a call as unsupported, because its `attrs` plugin reads only named functions, types, and lambdas.
A named function gives `mypy` the same `__init__`:

```python
from kuchka import wire


def to_voltage(value: Voltage | str | Mapping[str, object]) -> Voltage:
    return wire.load(value, Voltage)


@attrs.define(frozen=True)
class Probe:
    limit: Voltage = attrs.field(converter=to_voltage)


Probe("1 V").limit  # 1 V
```

## In a Pydantic model

`kuchka.pydantic.Quantity` is `load` and `dump` as a Pydantic v2 field; it needs the extra, `pip install kuchka[pydantic]`:

```python
from typing import Annotated

from pydantic import BaseModel

from kuchka.pydantic import Quantity


class PowerSupplyConfig(BaseModel):
    max_voltage: Annotated[Voltage, Quantity]


config = PowerSupplyConfig.model_validate({"max_voltage": "2800 mV"})
config.max_voltage  # 2800 mV
config.model_dump_json()  # '{"max_voltage":"2800 mV"}'
PowerSupplyConfig.model_validate_json(config.model_dump_json()) == config  # True
PowerSupplyConfig.model_validate({"max_voltage": 3.3})  # rejected: `ValueError`.
```

The refusals of `load` are `ValueError`s, so Pydantic reports them as its `ValidationError`, which is a `ValueError` too, and the message says what to write.
`model_dump()` keeps the `Voltage`, and `model_dump(mode="json")` writes the text, which validation reads back exactly, in the unit it was written in.
The JSON Schema of the field is a string whose description names the quantity (a `Proportion` also allows a number).
A field may be optional, in a list, or in a dict, and `Quantity(allow_archaic=True)` reads archaic units.

Both type checkers type the attribute as `Voltage`.
The constructor of a model takes the annotated type, so `PowerSupplyConfig(max_voltage="2800 mV")` is reported by `mypy` and `pyright` and works at runtime; data from a file or a payload enters through `model_validate` and `model_validate_json`, which take any data.

## In a msgspec struct

`kuchka.msgspec` has the hooks that `msgspec` calls for a type it does not know; it needs the extra, `pip install kuchka[msgspec]`:

```python
import msgspec

from kuchka.msgspec import kuchka_dec_hook
from kuchka.msgspec import kuchka_enc_hook


class Payload(msgspec.Struct):
    v: Voltage


payload = msgspec.json.decode(b'{"v": "4.2 V"}', type=Payload, dec_hook=kuchka_dec_hook)
payload.v  # 4.2 V
msgspec.json.encode(payload, enc_hook=kuchka_enc_hook)  # b'{"v":"4.2 V"}'
msgspec.json.decode(
    b'{"v": 3.3}', type=Payload, dec_hook=kuchka_dec_hook
)  # rejected: `ValueError`.
```

The decoding hook is `load` and the encoding hook is `dump`.
A refusal is a `ParseError`, a `ValueError`, so `msgspec` reports it as its `ValidationError` with the path of the field, such as `` at `$.v` ``.
Both hooks raise `NotImplementedError` for what is not a quantity, the protocol `msgspec` defines, so an application chains them with its own hooks.
`msgspec.json.schema` refuses a type it does not know, and `kuchka_schema_hook` describes the quantity types to it: `msgspec.json.schema(Payload, schema_hook=kuchka_schema_hook)`.
`make_dec_hook(allow_archaic=True)` makes a decoding hook that reads archaic units.
The same text works in every `msgspec` format and in `msgspec.convert` and `msgspec.to_builtins`.

A field may also limit its range, with `Bounds` from the same bridge; see [Bounds](bounds.md).

## Archaic units

An archaic unit is written like any other.
`load` reads it back only when asked, with the same `allow_archaic` argument that `parse` takes, so a file that holds one needs the same opt-in on the way in.

## Limits

The numbers that `parse` reads are held to the numeric limits of the library, a fraction included, so a payload cannot make the program build a number of a million digits.
A magnitude whose decimal form would pass the limits is written as a fraction, and a round trip is exact for every magnitude the limits admit.
