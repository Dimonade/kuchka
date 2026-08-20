---
title: kuchka
sub_title: a small pile of physically-typed units for Python
author: dimonade
---

## Hi! My name is `kuchka`

<!-- new_lines: 8 -->

_A small pile of units._

_Deliberately small._

<!-- pause -->

<!-- new_lines: 2 -->

Voltage, Current, Power, Resistance, Temperature.

<!-- new_lines: 2 -->

Nothing else, on purpose.
Yet.

<!-- pause -->

<!-- new_lines: 2 -->

Everything on the following slides actually runs.
No screenshots.
No "trust me."

<!-- end_slide -->

## The problem

The year 1999. NASA loses a $125M spacecraft.

<!-- pause -->

Not an explosion.
Not aliens.
One team's software spoke `pound-force-seconds`.
The other assumed `newton-seconds`.
Nobody in between noticed.

<!-- pause -->

<!-- new_lines: 2 -->

You'd think 28 years later we've learned more.

<!-- pause -->

<!-- new_lines: 2 -->

> [!caution]
>
> Our reports aren't going to Mars.
> 
> But the failure mode is identical, just smaller and slower:
> a number quietly loses track of what it means, somewhere between acquisition and the printed page.

<!-- end_slide -->

## The Python problem specifically

```python
v_tot = voltage_v + mv / 1000  # this time the units are correct, trust me,  I prefixed them, I checked 4 times!
```

<!-- pause -->

Python will happily let you add Volts and Millivolts as well as subtract an Ampere from a Volt.

It will compute an answer.

It will just be **wrong**, quietly, at 2am, in a report nobody proofreads.

<!-- pause -->

<!-- new_lines: 2 -->

> _[Voice in my head]_
>
> "Rust wouldn't let this near a compiler..."

<!-- pause -->

<!-- new_lines: 2 -->

> _[The other voice in my head]_
>
> We don't have Rust here. We have Python, and a manager who wants reports to go brrr.

<!-- end_slide -->

## We already tried sticks

Linter rules.
Style guides nobody reads.
"Please use volts here" in a PR comment.

<!-- pause -->

It holds -- right up until whoever's enforcing it gets pulled onto something else, and everyone, little by little, drifts back to `measurement_mv`.

<!-- pause -->

<!-- new_lines: 2 -->

> _[Voice in my head]_
>
> Is `mv` "milli" or "micro"-Volts, though? They must be using `u` for "micro", right? Right?_

<!-- pause -->

<!-- new_lines: 2 -->

> [!caution]
>
> A rule you have to _remember_ is a rule you will, eventually, forget.
> Three months later it's a bug in a report, and a manager asking why "we had a rule about this" wasn't enough.

<!-- end_slide -->

## An experiment: the chip nobody wants to own

<!-- new_lines: 2 -->

Enough of the thought experiment.

Let's get our hands dirty.

<!-- pause -->

<!-- new_lines: 2 -->

The diode driver we're actually stuck with.

Sourced from a supplier in Shenzhen.
Python bindings written by a contractor in Shanghai.

<!-- pause -->

<!-- new_lines: 2 -->

Contract ended two years ago.
The contractor does not work there anymore.

<!-- end_slide -->

## The documentation, such as it is

<!-- pause -->

_... crickets ..._

<!-- pause -->

<!-- new_lines: 2 -->

Well, it is non-existent.

<!-- pause -->

<!-- new_lines: 2 -->

```python
def read_status():
    ...
```

<!-- end_slide -->

## The actual task

<!-- new_lines: 2 -->

```text {1|3-5|7-8|10-16|all}
Quick task: diode pre-flight check.

We're prototyping a pre-flight safety check for the new diode
driver before it goes into the acquisition pipeline.
Nothing fancy - just a first pass.

Time box: 10 minutes.
Don't overthink it, don't go looking things up, just write what you'd normally write.

What you're given
------------------
1. `read_status()` which returns the `status` of the diode.
2. From the datasheet, section 4.2 (Absolute Maximum Ratings):
    MAX_CURRENT_MA = 250
    MAX_CASE_TEMP_C = 45
    MAX_POWER_MW = 500
```

<!-- end_slide -->

## What `read_status()` actually returns

<!-- new_lines: 2 -->

```python
status = {
    "i_meas": 187500,
    "v_meas": 2350,
    "t_case": 314.85,
}
```

<!-- pause -->

<!-- new_lines: 2 -->

That's the whole interface.

No units in the field names.

No units in the docstring either -- go check, they aren't there.

<!-- new_lines: 1 -->

Ten minutes. No hints. Go.

<!-- end_slide -->

## Participants - handful of AI models, handful of humans

The task was given to a number of AI models, as well as to a number of humans.

<!-- end_slide -->

## Two models read it carefully

```python +line_numbers
current_ma = status["i_meas"] / 1000
voltage_v = status["v_meas"] / 1000
temp_c = status["t_case"] - 273.15
power_mw = current_ma * voltage_v
```

```
Current: 187.50 mA (Max: 250 mA) -> PASS
Case Temp: 41.70 C (Max: 45 C) -> PASS
Power: 440.63 mW (Max: 500 mW) -> PASS
```

<!-- pause -->

<!-- new_lines: 2 -->

Both flagged the ambiguity themselves, unprompted:

<!-- new_lines: 1 -->

- "The units aren't explicitly stated in the code... "
- "... that is inferred rather than specified."

<!-- pause -->

<!-- new_lines: 2 -->

The two most careful readers in the room, telling us the interface is the problem.

<!-- end_slide -->

## One model read it wrong -- and didn't even notice

```python
t_case_c = status["t_case"] / 1000
```

```
Case temperature: 0.31 °C   PASS
```

<!-- pause -->

<!-- new_lines: 2 -->

Nothing crashed. Nothing looked out of range to the model.

<!-- new_lines: 2 -->

A diode, supposedly under load, reported a third of a degree above freezing -- colder than your fridge.

The only thing anyone would see is a clean "PASS."

<!-- end_slide -->

## Then a human tried it

```python
temp_check = "PASS" if status["t_case"] <= MAX_CASE_TEMP_C else "FAIL"
```

```
temperature, 314.85, FAIL
```

<!-- pause -->

<!-- new_lines: 2 -->

Kelvin, compared straight against a Celsius limit.

The diode is actually fine -- 41.7°C, well under spec.
The report says confidently otherwise.

<!-- end_slide -->

## The same submission, one line up

```python
power_check = "PASS" if power_in_w / 1000 > MAX_POWER_MW else "FAIL"
print(f"power, {power_in_w * 1000}, {power_check}")
```

```
power, 440.62500000000006, FAIL
```

<!-- pause -->

<!-- new_lines: 2 -->

> [!caution]
>
> Read that line again.
>
> The *number* is exactly right -- 440.6 mW, well under the 500 mW limit.
> The *verdict* next to it came from a different, wrongly-scaled expression.
>
> Not a units mix-up.
> Two numbers that were supposed to be the same value, are drifting apart.

<!-- pause -->

<!-- new_lines: 2 -->

> [!caution]
>
> Also, take a note of that ugly `.0000000006`. We will deal with that later.

<!-- end_slide -->

## None of this is a skill gap

<!-- pause -->

Two frontier models, reading closely: right twice, and said so out loud.

<!-- new_lines: 1 -->

Another frontier model, reading just as closely: silently wrong, no error, no hesitation.

<!-- new_lines: 1 -->

A competent engineer, on a real clock: right on the hard part, wrong on the easy part, for a reason nobody wrote down.

<!-- pause -->

<!-- new_lines: 2 -->

Different people. Different mistakes. Same root cause:

a `float` doesn't know what it means, and nothing forces the number you check against the number you print to be the same number.

<!-- end_slide -->

## So: carrots

Not a better stick.
Not a bot or an agent.
No PR police patrol.

<!-- pause -->

Give engineers something more attractive to reach for than a raw `float` -- every time, not just when someone's watching -- and there's nothing left to be disciplined about.

<!-- pause -->

<!-- new_lines: 2 -->

```python
Volt(5) + Millivolt(200)   # -> Volt(5.2).
Volt(5) * Ampere(2)        # -> Power, computed, not asserted in a comment.
```

<!-- pause -->

The correctness isn't sitting _next to_ the nice interface, waiting to be bypassed.

It's load-bearing -- `mypy`, `ty`, and runtime all agree, because there was never a separate rule to begin with.

<!-- pause -->

<!-- new_lines: 2 -->

That's the pitch.

Now let's see if it survives contact with an actual undocumented part.

<!-- end_slide -->

## Same three fields, through `kuchka`

<!-- new_lines: 2 -->

We've seen what a plain `dict` does to three careful readers.

Let's watch the same three demos land on the thing that broke.

<!-- end_slide -->

## Demo: Decimal, not float

`0.1 + 0.2` should never surprise anyone.

SI prefixes are powers of ten -- exact in `Decimal`, not exact in binary `float`.

<!-- pause -->

```python {1-2|4|6|all} +exec +line_numbers
voltage_a_v = 0.1
voltage_b_mv = 200

voltage_sum = voltage_a_v + voltage_b_mv / 1000  # "obviously" 0.3 V

print(voltage_sum)
```
<!-- pause -->

`kuchka` doesn't surprise you:

```python {1|3-4|all} +exec +line_numbers
from kuchka import Volt, Millivolt

print(Volt(1) + Millivolt(200))
print(Volt(1) + Millivolt(200) == Volt(1.2))
```

<!-- end_slide -->

## Demo: derived dimensions

Multiplication and division understand physics, not just numbers.

```python +exec +line_numbers
from kuchka import Volt, Ampere

power = Volt(5) * Ampere(2)
print(power)
print(type(power).__name__)
```

<!-- pause -->

That's a real `Power` instance.
Not a `float`.
Not a `Quantity` wearing a trench coat.

<!-- end_slide -->

## Demo: incompatible dimensions

```python +exec +line_numbers
from kuchka import Volt, Ampere, IncompatibleDimensionError

try:
    Volt(5) + Ampere(2)
except IncompatibleDimensionError as e:
    print(e)
```

<!-- pause -->

The error tells you what you did wrong in engineering terms, not `TypeError: unsupported operand type(s) for +`.

<!-- end_slide -->

## Demo: temperature is not a float either

```python +exec +line_numbers
from kuchka import Celsius, MeasurementError

print(Celsius(0).kelvin)               # exact -- 273.15, no rounding
print(Celsius(20) - Celsius(15))       # a real TemperatureDelta

try:
    Celsius(20) + Celsius(5)
except MeasurementError as e:
    print(e)
```

<!-- pause -->

"Hot + hot" isn't a number. The library agrees with you.

<!-- end_slide -->

## Demo: some things just don't exist

```python +exec +line_numbers
from kuchka import Celsius

try:
    Celsius(20) * 2
except TypeError as e:
    print(e)
```

<!-- pause -->

No code was written to "ban" this.

`Temperature` simply has no `__mul__`.

Python raises the error on its own -- and so does the type checker, for the same reason.

<!-- end_slide -->

## Demo: mypy agrees with all of this, statically

```bash +exec +line_numbers
cat > /tmp/kuchka_demo.py <<'EOF'
from kuchka import Ampere, Millivolt, Volt, Voltage


def analyse(voltage: Voltage) -> None: ...


analyse(4.2)             # naked float
analyse(Ampere(4.2))     # wrong dimension
analyse(Volt(4.2))       # should pass
analyse(Millivolt(4.2))  # should pass
EOF
mypy --strict /tmp/kuchka_demo.py
```

<!-- pause -->

Two errors, exactly where we want them.
Before anyone runs the code, not after.

<!-- end_slide -->

## The overload table, if anyone asks

Runtime arithmetic is fully general -- exponent algebra, works for any future quantity.

Static typing isn't; mypy can't infer "Voltage × Current = Power" on its own.

```python +line_numbers
# What mypy sees is an explicit, hand-written pair:

@overload
def __mul__(self, other: Current) -> Power: ...
@overload
def __mul__(self, other: Numeric) -> Voltage: ...
def __mul__(self, other):
    return super().__mul__(other)   # runtime logic unchanged
```

<!-- pause -->

Six pairs for v0.1 (Ohm's law + the power triangle).
Autogenerate this later, once it outgrows six.

<!-- end_slide -->

## How would kuchka solve this?

<!-- new_lines: 2 -->

The same driver. The same three fields. This time typed at
the boundary, once:

```python {1-2|6-9|11-14|all} +exec +line_numbers
from kuchka import Microampere, Millivolt, Kelvin, Milliampere, Celsius, Milliwatt
from kuchka.units import MILLIAMPERE, MILLIWATT

current = Microampere(187500)
voltage = Millivolt(2350)
temp = Kelvin(314.85)
power = current * voltage

MAX_CURRENT = Milliampere(250)
MAX_TEMP = Celsius(45)
MAX_POWER = Milliwatt(500)

print("current:", current.to(MILLIAMPERE), "PASS" if current <= MAX_CURRENT else "FAIL")
print("temp:   ", temp.to(MAX_TEMP.unit), "PASS" if temp <= MAX_TEMP else "FAIL")
print("power:  ", power.to(MILLIWATT), "PASS" if power <= MAX_POWER else "FAIL")
```

<!-- end_slide -->

## The line that can't be written

<!-- new_lines: 2 -->

The exact comparison that broke two separate submissions:

```python
temp <= 45
```

<!-- pause -->

<!-- new_lines: 2 -->

```bash +exec
cat > /tmp/bare_compare.py <<'EOF'
from kuchka import Kelvin
temp = Kelvin(314.85)
result = temp <= 45
EOF
mypy --strict /tmp/bare_compare.py
```

<!-- pause -->

<!-- new_lines: 2 -->

Not "wrong answer."
Not even "runtime crash."
The comparison doesn't type-check, so it never ships.

<!-- new_lines: 1 -->

Not because we banned it.
Because a `Temperature` and an `int` were never the same kind of thing to begin with.

<!-- end_slide -->

## Scope, on purpose

| In v0.1                     | Not yet, and that's fine     |
| --------------------------- | ----------------------------- |
| Voltage, Current            | Length, Mass, Time           |
| Power, Resistance           | NumPy / Pandas integration   |
| Temperature (Celsius, K)    | JSON / DB persistence        |
| Immutable, `Decimal`-backed | Autogenerated prefix classes |

<!-- pause -->

> [!note]
>
> Narrow scope isn't a limitation here -- it's what makes the whole thing tractable.
>
> It's also why nobody else has shipped exactly this.

<!-- end_slide -->

<!-- jump_to_middle -->

## Let's build the rest of the pile.
