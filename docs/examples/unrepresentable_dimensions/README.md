# Working past an unrepresentable intermediate dimension

Power dissipation, P = V^2 / R, needs a `Voltage` squared partway through.
A voltage times a voltage isn't a `Power`, and kuchka has no type for that dimension
(yet), so `Voltage * Voltage` raises `UnrepresentableDimensionError`.

Total resistance of resistors in parallel may require multiplying N resistors, which
is not representable.
Thus, the pathway is to go through `Conductance` instead.

| File                        | What it is                                    |
| ---------------------------- | ----------------------------------------------- |
| `resistor_network.py`        | `parallel()`, `series()`, `power_dissipation()` |
| `demo.py`                    | Run this                                        |
| `test_resistor_network.py`   | Tests for `resistor_network.py`                 |

## The pattern

Similarly to Rust's `unsafe`, only within this function does the information within
the types get exposed through the `.magnitute`.

```python
def power_dissipation(voltage: Voltage, resistance: Resistance) -> Power:
    watts = voltage.magnitude * voltage.magnitude / resistance.magnitude
    return Watt(watts)
```

Real `Voltage` and `Resistance` go in, a real `Power` comes out.
Only the one intermediate step with no type to hold it drops to `.magnitude`;
everything else stays typed.

## parallel() and series()

`parallel()` and `series()` combine resistors using ordinary typed arithmetic --
`1 / Resistance` is a `Conductance`, so summing reciprocals needs no unit handling of
its own:

```python
def parallel(*resistors: Resistance) -> Resistance:
    total_conductance = 1 / resistors[0]
    for resistor in resistors[1:]:
        total_conductance = total_conductance + 1 / resistor
    return 1 / total_conductance
```

## Running it

```bash
cd docs/examples/unrepresentable_dimensions
python demo.py
pytest
```

## The general shape

Stay in typed quantities up to the point a formula genuinely needs an unregistered
dimension, drop to `.magnitude` for exactly that step, and reconstruct a real
quantity the moment the result is representable again.
