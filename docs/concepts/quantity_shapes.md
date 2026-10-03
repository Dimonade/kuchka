# Quantity shapes and semantics

`kuchka` does not treat every physical quantity as an ordinary number.
Each quantity belongs to an arithmetic shape that defines which operations are meaningful and what those operations return.

## Linear

Linear quantities have units related by a scale factor.
Addition, subtraction, scalar multiplication, and ordering follow ordinary numeric behavior.

Examples include `Voltage`, `Current`, `Length`, `Mass`, and `Time`.

```python
from kuchka import Gram, Kilogram

Kilogram(2) + Gram(500) == Kilogram(2.5)
Kilogram(10) * 3 == Kilogram(30)
Kilogram(2) < Kilogram(3)
```

## Affine

Affine quantities represent readings on a scale whose units differ by both a scale and an offset.
A reading is a point, not a vector.

`Temperature` is the current example.
Subtracting two readings produces a linear temperature delta; adding a delta to a reading produces another reading.
Adding two readings is rejected.

```python
from kuchka import DeltaKelvin, Kelvin

setpoint = Kelvin(350)
reading = Kelvin(352)
tolerance = DeltaKelvin(5)

abs(reading - setpoint) <= tolerance
# True

Kelvin(20) * 2  # rejected: no __mul__ on an affine quantity.
```

Kelvin, Celsius, and Fahrenheit readings are all `Temperature`.
Their units differ by a scale and an offset, and kuchka keeps both exact: a Fahrenheit degree is exactly 5/9 of a kelvin, and 0 °F sits at exactly 459.67 x 5/9 K.

```python
from kuchka import Celsius, DeltaCelsius, DeltaFahrenheit, Fahrenheit, Kelvin

Fahrenheit(32) == Celsius(0)
# True

Fahrenheit(-459.67) == Kelvin(0)
# True

Fahrenheit(77) - Fahrenheit(68) == DeltaFahrenheit(9)
# True

DeltaFahrenheit(9) == DeltaCelsius(5)
# True
```

A temperature difference is a size, not a position, so `DeltaFahrenheit` and `DeltaCelsius` differ by scale only (9 °F of difference is 5 °C of difference).

Absolute zero is enforced for temperature readings.

`AffineQuantity` is generic so that a future point-in-time type can reuse the same semantics without making `Temperature` special.

## Modular

Modular quantities wrap around after a fixed period.
`Angle` is the current example.

```python
from kuchka import Degree

commanded = Degree(370)  # construction never wraps.
commanded == Degree(10)
# True -- equality already compares wrapped magnitude.
commanded.magnitude == Degree(10).magnitude
# False -- the raw stored value is still 370 degrees worth.
commanded.normalize().magnitude == Degree(10).magnitude
# True.
```

`+` and `-` are ordinary wraparound group arithmetic over `[0, period)`. `difference()` is a separate shortest-signed-path operation over `(-period/2, +period/2]`. Scalar multiplication and division wrap their result the same way.

Construction does **not** normalize: `Degree(370)` is stored as-is and stays distinct from `Degree(10)` until it's compared (equality normalizes both sides) or explicitly wrapped with `.normalize()`.

There is deliberately no total order for modular quantities: a cyclic value has no universal `greater than` relationship without choosing a direction of travel.

`is_close(other, tolerance=...)` asks whether two readings are within a stated tolerance of each other, measured the short way round the circle.
It exists on every shape; see [Comparing with a tolerance](exactness.md#comparing-with-a-tolerance).

## Logarithmic

Logarithmic quantities are the logarithm of a ratio.
`LogarithmicRatio` is the current example, expressed in decibels or bels.

The level is stored exactly.
Multiplying two ratios adds their levels, so `+` and `-` combine stages in series and are exact:

```python
from kuchka import Bel, Decibel

amplifier = Decibel(20)
cable = Decibel(-3.5)
amplifier + cable  # 16.5 dB
amplifier - cable  # 23.5 dB
-cable  # 3.5 dB, the reciprocal ratio.
Bel(1) == Decibel(10)  # True
```

Scaling by a plain number scales the level: `Decibel(-0.2) * 30 == Decibel(-6)`.
Dividing a level by a level gives a plain `Fraction`: `Decibel(6) / Decibel(3) == 2`.
Levels have a total order, since a larger ratio is a larger level.
`abs()` gives the size of a deviation, which is what a gain tolerance check compares.

Level times level, level plus a naked number, and level plus a linear `Proportion` are rejected.

### Converting to and from a linear ratio

The same number of decibels describes a different linear ratio depending on the kind of quantity.
`as_power_ratio()` uses `10 ** (level / 10)` for power, energy, and intensity.
`as_field_ratio()` uses `10 ** (level / 20)` for voltage, current, and pressure.
Both return a `Proportion`.
`LogarithmicRatio.from_power_ratio()` and `LogarithmicRatio.from_field_ratio()` go the other way and require a positive ratio.

```python
from kuchka import Decibel, LogarithmicRatio, Ratio

Decibel(30).as_power_ratio() == Ratio(1000)
Decibel(40).as_field_ratio() == Ratio(100)
Decibel(6).as_field_ratio() == Decibel(3).as_power_ratio()
LogarithmicRatio.from_field_ratio(Ratio(10)) == Decibel(20)
```

A logarithm of a general ratio is irrational, so this is the one place a logarithmic quantity leaves exact arithmetic.
The conversion is evaluated in `Decimal` at the active context precision, and the result is stored as the exact `Fraction` of that `Decimal`.
Whole multiples of 10 dB (power) or 20 dB (field) yield exact powers of ten and stay exact.
"The 3 dB point is a factor of two" is a close approximation: `Decibel(3).as_power_ratio()` is `1.99526...`.

### Reference levels

`LogarithmicRatio` is the ratio of two quantities of the same kind.
A level relative to a fixed reference, such as dBm (1 mW), dBW, dBV, dBu, or dBFS, is a separate family with its own semantics, planned for when a use case calls for it.
