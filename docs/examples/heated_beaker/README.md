# A heated beaker on a stepper-driven lever

A beaker of liquid sits on a lever.
A stepper motor with an encoder swings the lever toward and away from a heat source, and a temperature sensor in the liquid reports how it responds.
The liquid has to stay inside a temperature window.

The inputs are two text files that people and instruments write, a TOML spec of limits and a CSV log of one run.
Every cell is a number with its unit, and the log mixes them the way real instruments do.
The example reads both through `parse`, then answers questions about the run with ordinary typed arithmetic.

| File                | What it is                                                         |
| ------------------- | ------------------------------------------------------------------ |
| `bench_spec.toml`   | Lever, liquid, and motor limits                                    |
| `run_log.csv`       | One run: time, lever angle, motor voltage and current, temperature |
| `bench_log.py`      | The boundary layer and the analysis                                |
| `demo.py`           | Run this: reports on the run, then breaks the inputs three ways    |
| `test_bench_log.py` | Tests for `bench_log.py`                                           |

## What the log looks like

```csv
time,lever_angle,motor_voltage,motor_current,temperature
40 s,9 deg,11.9 V,315 mA,57.6 °C
50 s,12 deg,11700 mV,0.3 A,61.8 °C
70 s,12.2 deg,0 V,0 mA,143.8 °F
```

The driver reports `11700 mV` and `0.3 A` on one row and `11.9 V` and `315 mA` on the others, and a second sensor reports `°F`.
None of that reaches the analysis: `parse` turns each cell into a `Voltage`, a `Current`, or a `Temperature`, and the quantities compare and combine exactly whatever unit they were written in.

## What the types do here

**Angle versus travel.**
The encoder reports an `Angle`, which wraps at 360°, and the spec puts home at `350 deg`, just below the wrap.
The lever swings through 0° on its way to the heater, so a plain subtraction wraps around too, and ordering two angles is refused.
`Angle.difference` is the shortest signed path, and `to_angular_displacement()` turns it into an `AngularDisplacement`, a linear quantity that orders, so `abs(...)` and `max(...)` measure the travel and compare it to `max_travel`:

```python
swing = (s.angle.difference(spec.home).to_angular_displacement() for s in samples)
travel = max(abs(d) for d in swing)  # 22.2 °
```

**A temperature and a temperature difference.**
`Temperature` is an affine reading and `TemperatureDelta` is a linear difference.
The tolerance on the setpoint is a `0.5 ΔK`, and `"0.5 K"` is refused, because a tolerance is a difference and `K` is the unit of a reading.
`Temperature.is_close(setpoint, tolerance=...)` takes the delta type and nothing else.

**Rate of change.**
The liquid must not heat too fast, so the spec limits the rate: `max_heating_rate = "1 K/s"`.
`(b.temperature - a.temperature) / (b.time - a.time)` is a `TemperatureDelta` over a `Time`, which is a `HeatingRate`, and `max(...)` finds the peak, `0.88 K/s`, to compare with the limit.
The reading in `°F` and the readings in `°C` subtract without a conversion, because a difference of readings is a `TemperatureDelta` whatever scale they were written in.

**Time from instants.**
The `time` column is read as an `Instant`, so `settled.time - first.time` is a `Time`, while adding two instants is refused.

**Electrical power into energy.**
`voltage * current` is a `Power`, times a `Time` is an `Energy`, and the sum starts from `Joule(0)` so it has the right type even for an empty run.
The motor spent 296.81 J, which `.to(MILLIWATT_HOUR)` shows as `82.4 mWh`.
The sum is exact, so the test compares it with `==`: the cell written as `11700 mV` times the cell written as `0.3 A` adds up with the others to exactly `296.81 J`.

**A tolerance on position.**
`returned_home` asks whether the final encoder angle is close to home with a `0.5 deg` tolerance, measured the short way round, so `350.2 deg` is close to `350 deg` and `359.9 deg` is close to `0.1 deg`.

## Running it

```bash
cd docs/examples/heated_beaker
python demo.py
pytest
```

`demo.py` prints the report and then breaks the inputs three ways:

1. **A current written in volts** -- the error names the file, the line, and the column.
2. **A setpoint with no unit** -- a bare TOML number is refused before it can become a float in the control path.
3. **A tolerance written as a temperature** -- `0.5 K` is not a temperature difference.

## What kuchka does not do here

The lever geometry, the distance of the beaker from the heater as a function of the angle, needs trigonometry that `kuchka` does not provide, and so does the heat transfer.
`kuchka` types the readings and the limits, and leaves the physics model to the code around it.
