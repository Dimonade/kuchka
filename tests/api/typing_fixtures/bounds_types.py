"""Not a pytest file directly-- run through mypy and pyright, like `should_fail.py`.

The static contract of `kuchka.bounds.Bounds`: the bounds are of one ordered quantity
type, and `check` takes and returns that type.
Bounds of two quantity types and a bound in an `attrs` validator for a field of another
type are refused when the program runs, since neither checker relates them.
"""

from kuchka import Ampere
from kuchka import Angle
from kuchka import Degree
from kuchka import Volt
from kuchka import Voltage
from kuchka.bounds import Bounds

supply = Bounds(gt=Volt(0), le=Volt(60))  # OK
bounded: Bounds[Voltage] = supply  # OK
checked: Voltage = supply.check(Volt(5))  # OK
contained: bool = Volt(5) in supply  # OK

# `check` takes the quantity type of the bounds.
_wrong_value = supply.check(Ampere(1))  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]

# A quantity with no ordering has no bounds.
_angle_bounds: Bounds[Angle] | None = None  # type: ignore[type-var]  # ty: ignore[invalid-type-arguments]
_angle_bound = Bounds[Voltage](ge=Degree(0))  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
