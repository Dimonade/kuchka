# Bounds: the range a field accepts

A value that reads as a voltage can still be a voltage the device must not be given: a supply is above zero and at most 60 V, a duty is between 0 and 1, an operating temperature is between -40 °C and 85 °C.
`kuchka.bounds.Bounds` holds such a limit, as measurements of one quantity type; the [limits-file example](../examples/config_migration/README.md) uses it to refuse a configuration that asks for more than the hardware can do:

```python
from kuchka import Millivolt
from kuchka import Volt
from kuchka.bounds import Bounds

supply = Bounds(gt=Volt(0), le=Volt(60))

supply.check(Millivolt(12000))  # 12000 mV
Volt(61) in supply  # False
supply.check(Volt(61))  # rejected: `BoundsError`.
```

`gt` and `lt` exclude their edge, `ge` and `le` include it, and at least one is given.
`check(value)` returns the value or raises `BoundsError`, so it fits a chain of conversions, and `value in bounds` answers with a `bool`.
The message writes the value and the bound with their units, in the [wire form](wire_form.md): `61 V is above 60 V, the most allowed.`

## What a bound compares

A bound compares exactly, in whatever unit either side was written, and the comparison is the ordering of the quantity type:

```python
from kuchka import Celsius
from kuchka import Fahrenheit
from kuchka import Percent
from kuchka import Ratio

operating = Bounds(ge=Celsius(-40), le=Celsius(85))
Fahrenheit(-40) in operating  # True
Celsius(85.01) in operating  # False

duty = Bounds(ge=Ratio(0), le=Ratio(1))
Percent(25) in duty  # True
Ratio(25) in duty  # False
```

A quantity with no ordering has no bounds: an `Angle` is a point on a circle, so `Bounds(ge=Degree(0))` raises `TypeError`, and both type checkers report it.
The bounds are checked where they are written: no bound, `gt` with `ge` or `lt` with `le`, bounds of different quantity types, and a range that no value is in each raise when the `Bounds` is made, so a mistake in the program shows at the line that wrote it.

The proportion is the quantity where a limit matters most.
A number with no unit is a ratio, so a duty written `25` for twenty-five percent is a ratio of twenty-five, which is `2500 %`, and the bounds of a ratio between 0 and 1 refuse it with `25 is above 1, the most allowed.`

## The error

`BoundsError` is a `ValueError`, so a validation framework reports it, and an `InvalidMeasurementError`, so one `except InvalidMeasurementError` handles it together with a `ParseError` from reading the value.
It is not a `ParseError`, which stands for text that is no measurement: the value was read, and it lies outside the range.

## In a Pydantic model

`kuchka.pydantic.Bounds` is an `Annotated` marker beside `Quantity`:

```python
from typing import Annotated

from pydantic import BaseModel

from kuchka import Proportion
from kuchka import Voltage
from kuchka.pydantic import Bounds as FieldBounds
from kuchka.pydantic import Quantity


class PowerSupplyConfig(BaseModel):
    max_voltage: Annotated[Voltage, Quantity, FieldBounds(gt=Volt(0), le=Volt(60))]
    duty: Annotated[Proportion, Quantity, FieldBounds(ge=Ratio(0), le=Ratio(1))]


PowerSupplyConfig.model_validate({"max_voltage": "12 V", "duty": "25 %"}).duty  # 25 %
PowerSupplyConfig.model_validate(
    {"max_voltage": "61 V", "duty": 0.5}
)  # rejected: `ValueError`.
PowerSupplyConfig.model_validate(
    {"max_voltage": "12 V", "duty": 25}
)  # rejected: `ValueError`.
```

A value outside the range is a validation error at the path of the field, with the message above, and the JSON Schema description of the field says the range: `A Voltage, written as a number and a unit, such as "5 V". It is above 0 V and at most 60 V.`
The marker may be written before or after `Quantity`, several markers may be given, and each is checked.
Bounds of another quantity type than the field, and a marker with no `Quantity`, are reported when the class is defined.

Only a validated value is checked: an instance passed in is checked, and a default is checked when the field asks for its defaults to be validated (`Field(default="12 V", validate_default=True)`).

## In an attrs class

`kuchka.attrs.Bounds` is the validator of the field, which `attrs` runs after the converter:

```python
import attrs

from kuchka.attrs import Bounds as ValidatorBounds
from kuchka.attrs import parse_field


@attrs.define(frozen=True)
class SensorSpec:
    threshold: Voltage = attrs.field(
        converter=parse_field(Voltage),
        validator=ValidatorBounds(gt=Volt(0), le=Volt(60)),
    )


SensorSpec("12 V").threshold  # 12 V
SensorSpec("61 V")  # rejected: `BoundsError`.
```

The error names the attribute: `threshold: 61 V is above 60 V, the most allowed.`
Bounds of another quantity type than the field are reported, with the attribute, when the instance is made, since `attrs` validators carry no type that a checker relates to the field.

## In a msgspec struct

`msgspec` has no constraint for a type it does not know, and a struct checks the range in `__post_init__`, where a `ValueError` is reported as `msgspec.ValidationError`:

```python
import msgspec

from kuchka.msgspec import kuchka_dec_hook


class Payload(msgspec.Struct):
    v: Voltage

    def __post_init__(self) -> None:
        supply.check(self.v)


msgspec.json.decode(b'{"v": "12 V"}', type=Payload, dec_hook=kuchka_dec_hook).v  # 12 V
msgspec.json.decode(
    b'{"v": "61 V"}', type=Payload, dec_hook=kuchka_dec_hook
)  # rejected: `ValueError`.
```

`msgspec` reports an error raised in `__post_init__` without the path of the field, so the message is the whole of what says which value was refused.
