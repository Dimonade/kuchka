---
title: kuchka
sub_title: a personal tool for safer quantity and unit data operations -- manager summary
author: dimonade
---

## What this is

<!-- pause -->

A personal open-source Python library for safe quantity and unit operations.

<!-- pause -->

I'd like to publish it to PyPI, and make it available -- entirely optionally -- for our own test tooling if anyone finds it useful.

<!-- end_slide -->

## Where our data actually lives today

<!-- pause -->

```text
expected_current_ma = 620
reader_supply_mv    = 12.0
supply_min_v        = 10.5
cycle_time_ms       = 180
```

<!-- pause -->

Every `_ma` / `_v` / `_mv` / `_ms` suffix is a promise about what that number means.

<!-- pause -->

Nothing enforces it.
It's a naming convention, not a check.

<!-- end_slide -->

## A bug that already looks familiar

<!-- pause -->

```python +exec +line_numbers
measured_current_a = 0.52       # from the current-meter driver -- always amps
MAX_ALLOWED_CURRENT_MA = 500    # straight off the datasheet, in mA
 
naive_check = "PASS" if measured_current_a <= MAX_ALLOWED_CURRENT_MA else "FAIL"
print(naive_check)
```

<!-- pause -->

520 mA is over the 500 mA limit. The check says PASS.

<!-- pause -->

Nobody chose to get this wrong.
The meter driver just always reports amps; the datasheet just always writes mA.
Two numbers, two unrelated sources, compared directly by an honest mistake.

<!-- pause -->

<!-- new_lines: 2 -->

> [!caution]
>
> This check passes for any current up to 500 A -- a device in this class could never draw that much.
> This is just to prove a point.


<!-- end_slide -->

## The fix

<!-- pause -->

```python +exec +line_numbers
from kuchka import Ampere, Milliampere

measured_current = Ampere(0.52)
MAX_ALLOWED_CURRENT = Milliampere(500)

correct_check = "PASS" if measured_current <= MAX_ALLOWED_CURRENT else "FAIL"
print(correct_check)
```

<!-- pause -->

No conversion step to remember, on either side.
Nothing to get backwards.

`measured_current` is a Current -- amps or milliamps, `kuchka` already knows they're the same kind of thing.

<!-- end_slide -->

## And it's not just a naming discipline -- it's enforced

<!-- pause -->

```python +exec +line_numbers
from kuchka import Volt, Ampere

try:
    Volt(12) - Ampere(2)
except Exception as e:
    print(type(e).__name__, "-\n\n", e)
```

<!-- pause -->

Not a lint warning.
A runtime guarantee: a `Current` and a `Voltage` are different Python types.

No code path -- not a config value, not a sensor reading, not a number some other function handed back -- can accidentally treat one as the other, ever.

<!-- end_slide -->

## A couple more mistakes that never make it into a report

<!-- pause -->

```python +exec +line_numbers
from kuchka import Volt

try:
    Volt(5) + 4.2
except Exception as e:
    print(type(e).__name__, "-\n\n", e)
```

<!-- pause -->

Combining a measurement with a plain number -- the "forgot to wrap it" mistake -- is rejected too, with a message that says exactly what to do about it.

<!-- pause -->

```python +exec +line_numbers
from kuchka import Volt, Ampere

try:
    Volt(Ampere(5))
except Exception as e:
    print(type(e).__name__, "-\n\n", e)
```

<!-- pause -->

Passing the wrong kind of measurement into the wrong constructor fails at the moment it's written, not the moment it's used.

<!-- end_slide -->

## Config files: units as data, not a naming convention

<!-- pause -->

```python +exec +line_numbers
reading = {"value": 620, "unit": "mA"}

from kuchka.units import CURRENT_UNITS
current = CURRENT_UNITS[reading["unit"]](reading["value"])
print(current)
```

<!-- pause -->

Whatever a config, a device, or a colleague hands us -- `{"value": 42, "unit": "mV"}`, `"V"`, `"A"`, whatever the sensor speaks -- gets validated against a closed table for that physical quantity at load time.

<!-- pause -->

An unrecognised unit, or one from the wrong quantity entirely (a voltage field written as `"mA"`), fails loudly at startup, naming the field and the reason.
Not three functions later, as a silently wrong report.

<!-- end_slide -->

## Stress testing: the numbers that matter, computed automatically

<!-- pause -->

```python +exec +line_numbers
from kuchka import Milliampere, Second, Coulomb

charge_per_cycle = Milliampere(620) * Second(0.15)
total_charge = charge_per_cycle * 50_000

print(f"charge per actuation:  {charge_per_cycle}")
print(f"charge over campaign:  {total_charge.to(Coulomb(1).unit)}")
```

<!-- pause -->

Current times time is charge -- derived automatically, the same way voltage times current gives power.
No formula copy-pasted into every analysis script that needs cumulative numbers.

<!-- pause -->

Directly useful for battery life estimation on wireless locks and readers, with zero risk of a scaling mistake in the math.

<!-- end_slide -->

## What this actually buys us

<!-- pause -->

- Whole classes of bugs stop being possible -- not just harder to write.
- Mistakes surface at the line that made them, in the editor, not in a report someone already trusted.
- Zero dependencies. Adopted one field at a time, not a rewrite.
- Same guarantee end to end: acquisition, log parsing, analysis, reporting -- one boundary crossing, then it's typed everywhere.

<!-- end_slide -->

## No IP conflict

<!-- pause -->

- Personal project, personal time.
- A Python revival of a personal Rust project of mine, itself inspired by an existing open-source Rust library -- the design predates this job.
- No company code, no company data, no product-specific logic. It's a general physical-units library; it has no idea what a lock or a reader is.
- Open source, permissively licensed (Apache-2.0), hosted publicly.

<!-- end_slide -->

## What's next, if there's appetite for it

<!-- pause -->

- A small set of physical constants (speed of light and similar), so common reference values don't get re-typed as bare floats either.
- A few more physical quantities as real engineering needs come up -- the same pattern each time, no architecture change required.
- Longer-term, possible NumPy/pandas integration for higher-rate acquisition -- not needed yet, not blocking anything today.

<!-- pause -->

None of this is required for what's being asked for today.
It's context for where the tool goes if it turns out to be useful.

<!-- end_slide -->

## The ask

<!-- pause -->

1. Okay to publish this to PyPI under my own name.
2. No company resources, no company endorsement required.
3. If anyone on the team ever wants to use it, that's optional -- always.

<!-- end_slide -->

<!-- jump_to_middle -->

## Questions?
