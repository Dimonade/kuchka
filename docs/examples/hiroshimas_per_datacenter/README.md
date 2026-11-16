# Hiroshimas per datacenter

An interesting post on Reddit claimed that the planned off-grid **Stratos Project** data center in Utah, spanning 40,000 acres (the size of 2,000 Walmart Supercenters) and drawing 9 GW of power, will "generate the heat equivalent of 23 atom bombs detonating every single day."

A Reddit math breakdown checked the claim and found two interesting things:

1. **The tweet's math is actually right.**
2. **The comparison is misleading**, because normal sunlight hitting that same patch of desert delivers more than twice as much heat.

This example models that entire back-of-the-envelope calculation in `kuchka`.
Every figure from the thread is represented as a typed physical quantity (`Power`, `Energy`, `Area`, `Fluence`, `Proportion`) without manual conversion factors.

Credits go to u/NovaTaima for the original question, u/tx_queer for the physics breakdown, and u/EarthTrash for inventing the unit "Hiroshimas per Walmart Supercenter".

## Files

| File                  | Purpose                                                                                          |
| :-------------------- | :----------------------------------------------------------------------------------------------- |
| `site_spec.toml`      | Input numbers from the thread stored as unit-bearing strings (`"9 GW"`, `"40000 ac"`, `"53 %"`). |
| `heat_budget.py`      | Boundary parser and typed thermodynamic calculations.                                            |
| `demo.py`             | Runs the scenario and prints the full comparison.                                                |
| `test_heat_budget.py` | Verifies exact rational equivalence across different calculation paths.                          |

## Checking the "23 bombs a day" claim

The math works out because the data center is planned to be off-grid:

- The servers draw **9 GW** of electricity, and virtually all of it ends up as heat.
- Generating 9 GW on-site with natural gas turbines at roughly **53% efficiency** produces another **7.98 GW** of waste heat.
- Total continuous heat output is **16.98 GW** (`1,467 TJ` over 24 hours).

In `kuchka`, efficiency is a `Proportion` (`Percent(53)`), so dividing `Power` by `Proportion` returns `Power` directly:

```python
from kuchka import Gigawatt
from kuchka import Hour
from kuchka import Percent

electrical_output = Gigawatt(9)
efficiency = Percent(53)

thermal_input = electrical_output / efficiency  # Power: 16.98 GW
waste_heat = thermal_input - electrical_output  # Power: 7.98 GW
daily_heat = thermal_input * Hour(24)  # Energy: 1,467 TJ
```

A standard Hiroshima bomb (`15 kt` of TNT) releases **62.76 TJ** of energy.
Dividing two `Energy` quantities yields a dimensionless `Proportion`:

```python
from kuchka import KilotonneOfTNT

HIROSHIMA = KilotonneOfTNT(15)  # Energy: 62.76 TJ
bombs_per_day = daily_heat / HIROSHIMA  # Proportion: 23.4
time_per_bomb = HIROSHIMA / thermal_input  # Time: 61.6 min
```

## Slow heat vs. fast heat (Energy vs. Power)

The tweet treats **total energy** as if it were the same thing as **rate of release**:

- A nuclear weapon dumps `62.76 TJ` in roughly **1 millisecond** (`62.76 PW`).
- The data center bleeds that same `62.76 TJ` slowly over **61.6 minutes** (`16.98 GW`).

```python
from kuchka import Millisecond

blast_power = HIROSHIMA / Millisecond(1)  # Power: 62.76 PW
intensity_ratio = blast_power / thermal_input  # Proportion: 3,695,867
```

Both involve the same `Energy`, but dividing by `Time` produces a `Power` and shows a 3.7-million-fold difference in intensity.

## Sunlight and nuclear plants

Spreading energy over land gives energy per unit area, which is a `Fluence` (`Energy / Area`):

- **The data center** spreads `1,467 TJ/day` across `40,000 acres`, or **9.1 MJ/m²** (`2.5 kWh/m²`).
- **Normal Utah sunlight** hitting that same 40,000-acre plot delivers **3,200 TJ/day** (**51 Hiroshimas a day**), or **19.8 MJ/m²** (`5.5 kWh/m²`).
- **A 3.3 GW nuclear power plant** (at 33% efficiency) vents **9.2 Hiroshimas a day** into the atmosphere as water vapor.

## Hiroshimas per Walmart Supercenter

At the end of the thread, a commenter mentioned a non-metric unit for the site, which rightfully belongs in "anything-but-metric".
Given 2,000 Supercenters covering 40,000 acres (`20 acres` per store and parking lot), one Hiroshima spread over one Supercenter is a reference `Fluence`:

```python
from kuchka import Acre

HIROSHIMA_PER_SUPERCENTER = HIROSHIMA / Acre(20)
site_fluence = daily_heat / Acre(40_000)

ratio = site_fluence / HIROSHIMA_PER_SUPERCENTER  # Proportion: 0.0117
```

Because `kuchka` uses exact `Fraction` arithmetic under the hood, `site_fluence / HIROSHIMA_PER_SUPERCENTER` produces the exact same rational value as `(daily_heat / HIROSHIMA) / 2000`.

## Why typed units matter here

Every input in `site_spec.toml` is parsed at the boundary with `parse(raw_value, ExpectedQuantity)`:

- Passing `"9 A"` instead of `"9 GW"` fails immediately with `UnknownUnitError`.
- Passing a bare `9` without a unit fails with `TypeError`.
- Mixing up `Energy` (total heat) with `Power` (blast intensity) or `Fluence` (heat per acre) is caught statically by `mypy` and `pyright`, as well as at runtime.

## Running the example

```bash
cd docs/examples/hiroshimas_per_datacenter
python demo.py
pytest
```

`demo.py` prints:

```text
A Hiroshima is 15 ktTNT = 62.76 TJ

The site, as the post describes it:

  servers draw                   9 GW
  gas plant efficiency           53 %
  waste heat of the plant        7.98 GW
  all heat the site releases     16.98 GW
  per day                        1467 TJ
  in Hiroshimas per day          23.4
  one Hiroshima of heat every    61.6 min
  per Walmart Supercenter        0.0117 Hiroshimas per day (20 ac each)

Against what else the ground and the sky deliver:

  sunlight per m2 and day        19.8 MJ/m², 5.5 kWh/m²
  site heat per m2 and day       9.1 MJ/m², 2.5 kWh/m²
  nuclear plant, 3.3 GW          9.2 Hiroshimas a day vented

Why the comparison misleads:

  one Hiroshima in 1 ms          62.76 PW
  against the site's heat        3,695,867 times as fast

What the efficiency of the gas plant changes:

  efficiency 50 %   24.8 Hiroshimas a day
  efficiency 53 %   23.4 Hiroshimas a day
  efficiency 55 %   22.5 Hiroshimas a day
```
