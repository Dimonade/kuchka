"""Not a pytest file directly-- run through mypy and pyright, like `should_fail.py`.

The static contract of `kuchka.pydantic.Quantity` in a model: the attribute is the exact
quantity type under both checkers, the validating entry points take data, and the
constructor takes the annotated type, so a string there is reported by both.
"""

from typing import Annotated

from pydantic import BaseModel

from kuchka import Ampere
from kuchka import Current
from kuchka import Length
from kuchka import Volt
from kuchka import Voltage
from kuchka.pydantic import Bounds
from kuchka.pydantic import Quantity


class PowerSupplyConfig(BaseModel):
    """A supply limit and a length of cable that may be archaic."""

    max_voltage: Annotated[Voltage, Quantity, Bounds(gt=Volt(0), le=Volt(60))]
    cable: Annotated[Length, Quantity(allow_archaic=True)]


# Data enters through the validating entry points.
config = PowerSupplyConfig.model_validate(
    {"max_voltage": "2800 mV", "cable": "2 m"}
)  # OK
from_json = PowerSupplyConfig.model_validate_json('{"max_voltage": "1 V"}')  # OK

# The attribute is the exact type.
max_voltage: Voltage = config.max_voltage  # OK
cable: Length = config.cable  # OK
wrong_attribute: Current = config.max_voltage  # type: ignore[assignment]  # ty: ignore[invalid-assignment]

# The constructor takes the annotated type.
from_instances = PowerSupplyConfig(max_voltage=Volt(3.3), cable=config.cable)  # OK
_string_constructor = PowerSupplyConfig(max_voltage="2800 mV", cable=config.cable)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
_wrong_instance = PowerSupplyConfig(max_voltage=Ampere(1), cable=config.cable)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
