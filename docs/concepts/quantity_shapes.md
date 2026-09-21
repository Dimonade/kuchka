# Quantity shapes and semantics

`kuchka` does not treat every physical quantity as an ordinary number.
Each quantity belongs to an arithmetic shape that defines which operations are meaningful and what those operations return.

## Linear

Linear quantities have units related by a scale factor.
Addition, subtraction, scalar multiplication, and ordering follow ordinary numeric behavior.

Examples include `Voltage`, `Current`, `Length`, `Mass`, and `Time`.

```python
Volt(1) + Millivolt(200) == Volt(1.2)
```

## Affine

Affine quantities represent readings on a scale whose units differ by both a scale and an offset.
A reading is a point, not a vector.

`Temperature` is the current example.
Subtracting two readings produces a linear temperature delta; adding a delta to a reading produces another reading.
Adding two readings is rejected.

```python
Celsius(25) - Celsius(20) == DeltaCelsius(5)
Celsius(20) + DeltaCelsius(5) == Celsius(25)
Celsius(20) + Celsius(5)  # rejected
Celsius(20) * 2  # rejected: no `__mul__` implemented at all.
```

Absolute zero is enforced for temperature readings.

`AffineQuantity` is generic so that a future point-in-time type can reuse the same semantics without making `Temperature` special.

## Modular

Modular quantities wrap around after a fixed period.
`Angle` is the current example.

```python
Degree(350) + Degree(20) == Degree(10)
Degree(300).difference(Degree(350)) == Degree(-50)
Degree(10) < Degree(20)  # rejected
```

`+` and `-` are ordinary wraparound group arithmetic over `[0, period)`. `difference()` is a separate shortest-signed-path operation over `(-period/2, +period/2]`. Scalar multiplication and division wrap their result the same way.

Construction does **not** normalize: `Degree(370)` is stored as-is and stays distinct from `Degree(10)` until it's compared (equality normalizes both sides) or explicitly wrapped with `.normalize()`.

There is deliberately no total order for modular quantities: a cyclic value has no universal `greater than` relationship without choosing a direction of travel.
