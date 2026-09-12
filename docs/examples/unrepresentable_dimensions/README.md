# Working around an unrepresentable intermediate dimension

Some engineering formulas pass through a physical dimension that your application doesn't need as a first-class type.

For example, power dissipation

P = V² / R,

requires squaring a `Voltage`.
`Voltage * Voltage` is **not** `Power`, and unless your project defines that intermediate dimension, kuchka raises `UnrepresentableDimensionError`.

The same principle appears in resistor networks:
parallel resistance is most naturally computed through `Conductance`, because `1 / Resistance` is already representable.

| File                       | Purpose                                         |
| -------------------------- | ----------------------------------------------- |
| `resistor_network.py`      | `parallel()`, `series()`, `power_dissipation()` |
| `demo.py`                  | Example execution                               |
| `test_resistor_network.py` | Unit tests                                      |

## The pattern

Keep the public API fully typed.
Drop to `.magnitude` only for the single unrepresentable intermediate, then immediately reconstruct a typed quantity.

```python
def power_dissipation(voltage: Voltage, resistance: Resistance) -> Power:
    watts = voltage.magnitude * voltage.magnitude / resistance.magnitude
    return Watt(watts)
```

The function accepts `Voltage` and `Resistance`, returns `Power`, and exposes raw numbers only for the intermediate value that has no registered dimension.

## Parallel and series resistance

Parallel resistance stays entirely within typed arithmetic by converting resistances into conductances:

```python
def parallel(*resistors: Resistance) -> Resistance:
    total = 1 / resistors[0]
    for resistor in resistors[1:]:
        total = total + 1 / resistor
    return 1 / total
```

Because `1 / Resistance` produces a `Conductance`, no manual unit conversion is needed.

## Running it

```bash
cd docs/examples/unrepresentable_dimensions
python demo.py
pytest
```

## Takeaway

Use typed quantities everywhere they are representable.
When a formula genuinely requires an unregistered intermediate dimension, unwrap `.magnitude` for that step alone and immediately return to a typed quantity.
