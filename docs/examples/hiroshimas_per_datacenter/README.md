# Hiroshimas per datacenter

A post went around about a planned off-grid data center that will "generate the heat equivalent of 23 atom bombs detonating every single day".
A reply on Reddit ran the numbers and found that the tweet is accurate and that the heat still matters little, a thread that ends with a unit for everything that is not metric: Hiroshimas per Walmart Supercenter.
That thread has the whole toolbox of a unit library in it: gigawatts, an efficiency, TNT equivalents, gigajoules and terajoules, a plot measured in acres, and a count of bombs.

Credits go to u/NovaTaima for the post, u/tx_queer for the math breakout, and u/EarthTrash for the fake unit.

The figures are the post's own, rounded the way the post rounds them, and they serve as story material here.
The names and numbers can change to any scenario, a fictional Project Alfredo included, and the arithmetic stays the same.

| File                  | What it is                                                     |
| --------------------- | -------------------------------------------------------------- |
| `site_spec.toml`      | The figures of the site and of a nuclear plant to compare with |
| `heat_budget.py`      | The boundary layer and the heat arithmetic                     |
| `demo.py`             | Run this: counts the heat in Hiroshimas, then varies the plant |
| `test_heat_budget.py` | Tests for `heat_budget.py`                                     |

## The math of the thread, as types

The servers draw 9 GW, and nearly all of it ends as heat.
A gas plant of about 53 percent efficiency feeds them, so the plant burns `9 GW / 53 %` of fuel heat, and everything it does not turn into electricity leaves as waste heat:

```python
thermal_input = electrical_output / efficiency  # 16.98 GW
waste_heat = thermal_input - electrical_output  # 7.98 GW
```

The thread's "9 GW plus 8 GW makes about 17 GW" is the same sum, and `Site.total_heat` adds it the same way.
The efficiency is a `Proportion`, so `Power / Proportion` is a `Power`, and `53 %` reads as `Percent(53)` with no conversion to a fraction by hand.

A day of that heat is `Power * Time`, an `Energy`, and the thread's "1,468 TJ" comes from `.to(TERAJOULE)`.

## A Hiroshima is a reference quantity

The bomb is 15 kilotonnes of TNT, and the library knows that unit:

```python
HIROSHIMA = KilotonneOfTNT(15)  # 62.76 TJ
```

Counting in Hiroshimas is dividing by it.
`Energy / Energy` is a `Proportion`, so `hiroshimas(energy)` returns the count of bombs as an exact typed number, and `23.4` is the result of a division.
The same division works for sunlight, 3,200 TJ a day, which is 51 Hiroshimas, and for a 3.3 GW nuclear plant of 33 percent efficiency, which vents 9.2.

`Energy / Power` is a `Time`, so `time_per_hiroshima(heat)` answers the question the thread leaves open: the site releases one Hiroshima of heat about every 61.6 minutes.

## The fake unit

Hiroshimas per Walmart Supercenter needs a Walmart Supercenter, and the post supplies one: 2,000 of them cover 40,000 acres, so a supercenter is 20 acres, the store and its parking lot.
A Hiroshima spread over an area is energy per area, a `Fluence`:

```python
def one_hiroshima_per_supercenter(site: Site) -> Fluence:
    return HIROSHIMA / site.supercenter
```

A fake unit is a reference quantity, and measuring in it is a division by that quantity.
`hiroshimas_per_supercenter` divides the heat the site releases per area and day by it and gets `0.0117` as a `Proportion`, next to the thread's `0.0115` Hiroshimas per Walmart Supercenter.
The test checks the second route too: the daily count divided by the 2,000 supercenters is exactly the same value, because every step is exact.

## Slow heat and fast heat

The reply points out that one bomb releases its 62.76 TJ at once and the site releases its heat slowly.
`blast_power(Millisecond(1))` is `Energy / Time`, 62.76 PW, and the demo divides it by the site's heat output: a millisecond-long bomb is 3.7 million times the power of the site.
Both are the same `Energy` per Hiroshima, and the types keep the difference as a `Power`.

## What the library says differently

- The thread rounds the bomb to 63 TJ and gets 23.3 bombs a day.
  The library's TNT is the thermochemical 4.184 GJ per tonne, so a Hiroshima is 62.76 TJ and the count is 23.4.
- The efficiency of the plant is an input, so the demo shows 24.8, 23.4, and 22.5 bombs a day for 50, 53, and 55 percent.
- Daily sunlight on the plot is a `Fluence` like the site's own heat, 19.8 MJ/m² or 5.5 kWh/m² against 9.1 MJ/m² or 2.5 kWh/m², and `Energy / Area` and `HeatFlux * Time` both produce one.

## The boundary

`site_spec.toml` holds every figure as one string, a number and its unit, and `load_scenario` reads each with `parse`.
A figure in the wrong unit, such as `"9 A"` for a power, raises `UnknownUnitError`, and a bare `9` is refused before it becomes a float in the arithmetic.
The count of supercenters is a plain integer, because a count has no unit.

## Running it

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
