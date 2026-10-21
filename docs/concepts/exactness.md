# Exactness, angles, and tolerance

Every magnitude in `kuchka` is stored as an exact `Fraction`.

`int` and `Decimal` values can therefore enter the system without rounding.
`float` input is parsed through its string representation first, so `Volt(4.2)` keeps the digits written by the programmer instead of the binary floating-point representation.

```python
from fractions import Fraction
from kuchka import Litre
from kuchka.units import LITRE

q = Litre(Fraction(5, 18))
q.magnitude
# Fraction(1, 3600) -- Volume's canonical unit is `CubicMetre`, not `Litre`.
q.value_in(LITRE)
# Fraction(5, 18) -- exact, recovered in the unit it was constructed with.
```

`.magnitude` reads out in the canonical unit.
`.value_in(unit)` reads out in any compatible unit.
Both stay exact regardless of which one is summoned.
The scale factor between litres and cubic metres (`1/1000`) is itself an exact `Fraction`, so nothing is lost converting between them.

`Decimal` is materialized for display:

```python
repr(q)
# 0.2777777777777777777777777778 L
```

## Angles and pi

`Turn` is the canonical angle unit.
`Degree`, `Gradian`, `ArcMinute`, and `ArcSecond` are plain rational fractions of a turn (a degree is 1/360 of one), so conversions and comparisons among them and `Turn` are exact and pi appears nowhere in them.

`Radian` is the one unit tied to a turn by an irrational number, because a turn is two pi radians.
A `Fraction` cannot hold pi, so kuchka holds it as an exact rational to 100 decimal places (`kuchka.internal.constants.PI`) and uses it for the radian scale alone.
That has three consequences:

- A conversion to or from radians is off by less than one part in 10¹⁰⁰, so every digit that is displayed is correct.
- A value built in radians reads back exactly what was given, and converting degrees to radians and back returns the original.
- A radian value built from `PI` itself is exactly a half turn.

```python
from fractions import Fraction

from kuchka import Degree
from kuchka import Radian
from kuchka.units import RADIAN

Radian(Fraction(2, 7)).value_in(RADIAN)
# Fraction(2, 7) -- exact.
repr(Radian(1).to(Degree(1).unit))
# '57.29577951308232087679815481 °' -- every digit shown is correct.
```

### Why `Radian(math.pi) == Degree(180)` is `False`

Equality compares the exact numbers that two values denote, and a `float` is read by its shortest decimal string.
The rule is the same everywhere in kuchka: `Volt(0.1) + Volt(0.2) == Volt(0.3)` holds because the digits were typed, and `Volt(0.1 + 0.2) == Volt(0.3)` does not, because the float sum denotes `0.30000000000000004`.

`math.pi` denotes `3.141592653589793`, which is about 2.4e-16 short of pi, so `Radian(math.pi)` is that decimal number in radians, or `179.99999999999998634 °`.
No finite number is pi, which makes any rule that equates a float with 180 degrees a tolerance in disguise.
A tolerance does not belong inside `==`:

- Equality is used for hashing and set membership, and a tolerance breaks both: a can be close to b, and b to c, while a is not close to c.
- The right tolerance is a property of the application (a sensor's resolution, a servo's deadband, a specification limit), and `==` has nowhere to take it from.
- Equality would be the one operation in the library that is approximate.

So the two questions are two operations.
`==` asks whether two values are the same number, and `is_close` asks whether they are near enough for a purpose.

What this means in practice:

- Angles from configuration or a specification, in degrees, turns, gradians, or arcseconds, compare with `==`.
- Radians from a sensor or from `math` compare with `is_close`.
- `float(Degree(180).value_in(RADIAN)) == math.pi`, so an exact angle passes to `math` functions without loss.

## Comparing with a tolerance

Every quantity shape has `is_close(other, *, tolerance)`.
The tolerance is a quantity, required, with no default and no positional form, so what counts as close is always written down by the caller and a bare number such as `1e-9` is rejected for having no unit.

| Shape                             | `tolerance` is                                                     |
| --------------------------------- | ------------------------------------------------------------------ |
| Linear (`Voltage`, `Length`, ...) | the same type                                                      |
| Affine (`Temperature`, `Instant`) | the delta type: `TemperatureDelta`, `Time`                         |
| Logarithmic (`LogarithmicRatio`)  | the same type                                                      |
| Modular (`Angle`)                 | the same type; distance is measured the short way round the circle |

The test is `|a - b| <= tolerance`, evaluated exactly and inclusive, so a value sitting on the boundary is close.
A negative tolerance, a tolerance of another type, and an `other` of another type raise.
`is_close` is symmetric and is not transitive.

```python
import math

from kuchka import Degree
from kuchka import Millivolt
from kuchka import Radian
from kuchka import Volt

Volt(0.1 + 0.2) == Volt(0.3)
# False
Volt(0.1 + 0.2).is_close(Volt(0.3), tolerance=Millivolt(1))
# True

Radian(math.pi / 2).is_close(Degree(90), tolerance=Radian(1e-12))
# True
Degree(359.9999).is_close(Degree(0.0001), tolerance=Degree(0.001))
# True -- the short way round the circle.
```

## Truth value

A quantity has no truth value, because zero is a measurement and not an absence.
`if not reading:` could not tell a missing reading from `Volt(0)`, and a zero depends on the shape: `Celsius(0)` is not `Kelvin(0)`, `Degree(360)` is `Degree(0)`, and `Decibel(0)` is a ratio of one.
`bool()` raises `TypeError`, so `if reading:`, `reading or default`, and `any(readings)` fail where they are written.
A missing value is `is None`, and zero is an equality:

```python
from kuchka import Volt

reading = Volt(0)
reading is not None
reading == Volt(0)
bool(reading)  # rejected: `TypeError`.
```

## Summing

`sum()` starts from the plain number `0`, which a quantity refuses to add, so give it a start of the same type:

```python
from kuchka import Volt

sum([Volt(1), Volt(2)])  # rejected: `InvalidMeasurementError`.
sum([Volt(1), Volt(2)], start=Volt(0)) == Volt(3)
```

## Logarithmic conversions

Levels (`LogarithmicRatio`) store an exact `Fraction` and every combination of levels is exact.
Converting a level to or from a linear ratio evaluates a logarithm, which is irrational for a general ratio.
That conversion runs in `Decimal` at the active context precision and stores the exact `Fraction` of the resulting `Decimal`.
Whole multiples of 10 dB (power) or 20 dB (field) convert to exact powers of ten.
