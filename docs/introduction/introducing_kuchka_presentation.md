---
title: kuchka
sub_title: a small pile of physically-typed units for Python
author: dimonade
---

## Hi! My name is `kuchka`

<!-- pause -->

_A small pile of units._

_Deliberately small._

<!-- pause -->

Voltage, Current, Power, Resistance, Temperature.

Nothing else, on purpose.

<!-- pause -->

Everything on the following slides actually runs.

<!-- end_slide -->

## The problem

<!-- pause -->

The year 1999. NASA loses a $125M spacecraft.

<!-- pause -->

Not an explosion.
Not aliens.

One team's software spoke `pound-force-seconds`.
The other assumed `newton-seconds`.

Nobody in between noticed.

<!-- pause -->

You'd think nearly 27 years later we've learned more.

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

<!-- pause -->

```python
v_tot = voltage_v + mv / 1000
```

<!-- pause -->

The comment usually says:

<!-- pause -->

```text
# this time the units are correct, trust me
```

<!-- pause -->

Python will happily let you add Volts and Millivolts.

It will also happily subtract an Ampere from a Volt.

It will compute an answer.

It will just occasionally be the wrong answer, quietly, at 2am, in a report nobody proofreads.

<!-- pause -->

<!-- new_lines: 2 -->

> _Voice in my head_
>
> "Rust wouldn't let this near a compiler..."

<!-- pause -->

<!-- new_lines: 2 -->

> _The other voice in my head_
>
> "We don't have Rust here. We have Python."

<!-- end_slide -->

## We already tried sticks

<!-- pause -->

Linter rules.
Style guides nobody reads.
"Please use volts here" in a PR comment.

<!-- pause -->

It holds -- right up until whoever's enforcing it gets pulled onto something else.

Then everyone drifts back to:

```python
measurement_mv
time_ms
t_c
```

<!-- pause -->

<!-- new_lines: 2 -->

> [!caution]
>
> A rule you have to _remember_ is a rule you will, eventually, forget.
>
> The toolchain should carry the stick for us.

<!-- end_slide -->

## So let's use a real interface

<!-- pause -->

Enough of the thought experiment.

I took the shape of a real engineering problem: a vendor diode driver feeding Python, followed by a safety check before acquisition.

The point is not the diode.

The point is the boundary between:

```text
hardware -> vendor driver -> read_status() -> safety check -> acquisition pipeline
```

That boundary is where raw numbers are supposed to become engineering quantities.

<!-- end_slide -->

## The documentation, such as it is

<!-- pause -->

The driver is inherited.
The documentation is stale.
The interface is small.

<!-- pause -->

And the function that actually matters looks like this:

<!-- pause -->

```python
def read_status(): ...
```

<!-- pause -->

That's it.

<!-- pause -->

No units in the field names.

No units in the docstring.

No typed return value.

<!-- end_slide -->

## The interface I handed to people

<!-- pause -->

I gave the same interface to several AI models and several humans.

The participant-facing task was deliberately ordinary:

<!-- pause -->

> Implement the pre-flight check.
>
> You have ten minutes.
>
> Don't look anything up.
>
> Write what you would normally write.

<!-- pause -->

The important part was **not** whether someone could write ten lines of Python.

The important part was whether the interface gave them enough information to know what those ten lines should mean.

<!-- end_slide -->

## What `read_status()` actually returns

<!-- pause -->

```python +line_numbers
status = {
    "i_meas": 187500,
    "v_meas": 2350,
    "t_case": 314.85,
}
```

<!-- pause -->

And the safety limits were:

```text
250 mA
45 °C
500 mW
```

<!-- pause -->

That's the whole interface.

No units attached to the measurements.

<!-- pause -->

What would you assume?

<!-- end_slide -->

## The first thing that happened

<!-- pause -->

Two models did the careful thing.

They inferred the intended units from the values and the specification:

```python +line_numbers
current_ma = status["i_meas"] / 1000
voltage_v = status["v_meas"] / 1000
temp_c = status["t_case"] - 273.15
power_mw = current_ma * voltage_v
```

<!-- pause -->

And they got:

```text
Current:   187.50 mA   PASS
Case Temp:  41.70 °C   PASS
Power:     440.63 mW   PASS
```

<!-- pause -->

More interestingly, both stopped and said essentially the same thing:

> The units aren't explicitly stated in the interface.

<!-- end_slide -->

## That is useful feedback

<!-- pause -->

They solved the calculation.

But they also found a defect in the interface.

That is the result I care about more.

The correct implementation depends on knowledge that exists somewhere outside the value itself.

<!-- pause -->

A human engineer can compensate.

A careful model can compensate.

A future engineer who has never seen the hardware has to rediscover it.

<!-- end_slide -->

## Another model made a different assumption

<!-- pause -->

It treated the temperature as if the value were milli-Celsius:

```python
t_case_c = status["t_case"] / 1000
```

<!-- pause -->

Result:

```text
Case temperature: 0.31 °C   PASS
```

<!-- pause -->

Nothing crashed.

Nothing was out of numerical range.

The answer looked plausible enough to continue.

<!-- pause -->

The diode was supposedly colder than your refrigerator while operating under load.

The interface had no mechanism for objecting.

<!-- end_slide -->

## Then a human tried it

<!-- pause -->

The current calculation was correct.

<!-- pause -->

The temperature check was:

```python
temp_check = "PASS" if status["t_case"] <= MAX_CASE_TEMP_C else "FAIL"
```

<!-- pause -->

Which gives:

```text
temperature, 314.85, FAIL
```

<!-- pause -->

But `314.85 K` is `41.70 °C`.

The diode is fine.

The report is wrong.

<!-- end_slide -->

## And the power check was worse

<!-- pause -->

The same submission contained:

```python +line_numbers
power_check = "PASS" if power_in_w / 1000 > MAX_POWER_MW else "FAIL"
print(f"power, {power_in_w * 1000}, {power_check}")
```

<!-- pause -->

Result:

```text
power, 440.625..., FAIL
```

<!-- pause -->

The number being printed is correct.

The verdict next to it was computed from a different expression.

<!-- pause -->

> Not one unit conversion error.
>
> Two pieces of code that were supposed to describe the same value quietly stopped agreeing.

<!-- end_slide -->

## What did the exercise actually show?

<!-- pause -->

Not:

> "AI is better than engineers."

<!-- pause -->

Not:

> "Engineers can't code anymore."

<!-- pause -->

Something much simpler:

> **The interface creates failure opportunities even for competent readers.**

<!-- pause -->

Different participants made different mistakes.

The interface made all of those mistakes easy to express.

<!-- pause -->

A `float` does not remember whether it is:

```text
187500 µA
187.5 mA
0.1875 A
```

The program sees three numbers.

<!-- end_slide -->

## This is where the sticks come back

<!-- pause -->

We can tell people:

```text
Use milliamps here.
Convert Kelvin here.
Don't repeat the power calculation.
Check the units before review.
```

Those are sticks.

<!-- pause -->

Let's then move the sticks into the toolchain.

Let's make the carrot the natural interface.

<!-- end_slide -->

## What if the values remembered?

<!-- pause -->

```python +exec +line_numbers
/// from kuchka import Microampere, Millivolt, Kelvin
current = Microampere(187500)
voltage = Millivolt(2350)
temp = Kelvin(314.85)

power = current * voltage
/// print(f"{current = }     | ({type(current).__name__})")
/// print(f"{voltage = }       | ({type(voltage).__name__})")
/// print(f"{temp = }         | ({type(temp).__name__})")
/// print(f"{power = }   | ({type(power).__name__})")
```

Now these are not three anonymous numbers.

They are measurements.

<!-- pause -->

```python +line_numbers
MAX_CURRENT = Milliampere(250)
MAX_TEMP = Celsius(45)
MAX_POWER = Milliwatt(500)
```

And the comparisons happen between physical values, not between conventions encoded in variable names.

<!-- end_slide -->

## The diode check again

<!-- pause -->

```python {1-3|5|7-9|all} +line_numbers
current = Microampere(187500)
voltage = Millivolt(2350)
temp = Kelvin(314.85)

power = current * voltage

MAX_CURRENT = Milliampere(250)
MAX_TEMP = Celsius(45)
MAX_POWER = Milliwatt(500)
```

<!-- pause -->

Then:

```python +line_numbers
current <= MAX_CURRENT
temp <= MAX_TEMP
power <= MAX_POWER
```

<!-- pause -->

```text
current: 187.500 mA   PASS
temp:     41.70 °C    PASS
power:   440.625 mW   PASS
```

<!-- end_slide -->

## Derived dimensions

<!-- pause -->

Multiplication and division understand physics, not just numbers.

```python +line_numbers +exec
from kuchka import Volt, Ampere

power = Volt(5) * Ampere(2)
print(power)
print(type(power).__name__)
```

The result is a real `Power` instance.

Not a `float`.

Not a quantity object whose physical meaning exists only at runtime.

<!-- end_slide -->

## Some operations simply don't exist

<!-- pause -->

```python +line_numbers +exec
from kuchka import Celsius, MeasurementError

try:
    Celsius(20) + Celsius(5)
except MeasurementError as e:
    print(e)
```

<!-- pause -->

No.

<!-- pause -->

```python +exec
from kuchka import Celsius

try:
    Celsius(20) * 2
except TypeError as e:
    print(e)
```

<!-- pause -->

Also no.

<!-- pause -->

<!-- new_lines: 2 -->

Temperature has semantics.

An absolute temperature and a temperature difference are not interchangeable.

```python +exec
from kuchka import Celsius

dt = Celsius(20) - Celsius(15)

print(dt)
print(type(dt).__name__)
```

produces a temperature delta.

<!-- end_slide -->

## Decimal, not float

<!-- pause -->

This is not a claim that physical measurements are exact.

They aren't.

The point is narrower: decimal engineering units should not gain binary floating-point surprises as an accidental extra error source.

```python +line_numbers +exec
from kuchka import Volt, Millivolt

v = Volt(1) + Millivolt(200)

print(v)
print(v == Volt(1.2))
print(v == Millivolt(1_200))
```

The arithmetic is decimal.

The quantities are immutable.

<!-- end_slide -->

## Static typing matters too

<!-- pause -->

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

The first two are wrong.

The last two are valid.

<!-- pause -->

The important bit is not that a checker can produce an error message.

It is that the runtime model and the type model describe the same physics.

<!-- end_slide -->

## Runtime and static semantics

<!-- pause -->

Runtime arithmetic can use general dimension algebra.

Static typing needs explicit knowledge of the relationships we want tools to understand.

<!-- pause -->

For example:

```python {1-2|4-5|all} +line_numbers
@overload
def __mul__(self, other: Current) -> Power: ...


@overload
def __mul__(self, other: Numeric) -> Voltage: ...
```

<!-- pause -->

That is not beautiful metaprogramming.

It is a small, explicit bridge between Python's type system and the physical algebra.

<!-- pause -->

For v0.1, six such relationships cover the power triangle and Ohm's law.

Later, this can be generated.

<!-- end_slide -->

## The rule

<!-- pause -->

The architectural rule is simple:

> **Uninterpreted measurements may exist at I/O boundaries.**
>
> **Once interpreted, they must carry their physical meaning.**

Device input.

File input.

Database input.

Network packet.

It doesn't matter.

Interpret once.

Then keep the meaning attached.

<!-- end_slide -->

## What `kuchka` is deliberately not

<!-- pause -->

It is not:

```text
a scientific array framework
a NumPy replacement
a database representation
a universal unit registry
a complete SI implementation
```

<!-- pause -->

v0.1 is deliberately small:

<!-- pause -->

| In v0.1                              | Not yet                      |
| ------------------------------------ | ---------------------------- |
| Voltage, Current, Length, Mass       | NumPy / Pandas integration   |
| Power, Resistance, AmountOfSubstance | JSON / DB persistence        |
| Temperature, LuminousIntensity       | Autogenerated prefix classes |
| Immutable, `Decimal`-backed          |                              |

<!-- pause -->

Narrow scope is the point.

<!-- end_slide -->

## What is currently available?

<!-- pause -->

Before writing this, I went looking for the obvious answer.

There are plenty of unit libraries.

The strange part is that in more than a decade of engineering work, I have essentially never seen them used in the ordinary Python engineering code around me.

I have seen:

```text
voltage_mv
temperature_c
time_ms
```

I have seen small home-grown newtypes.

I had not seen the unit ecosystem become part of the daily vocabulary.

<!-- end_slide -->

## `units`

<!-- pause -->

```python +line_numbers
from units import unit

metre = unit("m")
print(metre(7) + metre(11))
```

The semantic unit is introduced from a string.

`kuchka` wants:

```python
Meter(7) + Meter(11)
```

where the physical identity _is_ the Python type.

<!-- end_slide -->

## Pint

<!-- pause -->

```python +line_numbers
import pint

ureg = pint.UnitRegistry()

3 * ureg.meter + 4 * ureg.cm
```

Pint is mature and powerful.

But compare that with:

```python
Meter(3) + Centimeter(4)
```

The first makes the engineer carry a registry-oriented runtime API.

The second makes the physical quantity itself the API.

<!-- pause -->

<!-- new_lines: 2 -->

That distinction is not cosmetic.

This project is explicitly trying to make the safe path the comfortable path.

<!-- end_slide -->

## unitpy

<!-- pause -->

```python +line_numbers
Unit("kilometer")
U("kilometer")
U("km")
U.kilometer
U.km
```

Again, several runtime spellings for a unit.

I want less discovery.

I want:

```python
Kilometer
```

to simply be the type.

<!-- end_slide -->

## The gap I am interested in

<!-- pause -->

I'm not claiming:

> "Python has no unit libraries."

<!-- pause -->

I'm claiming something narrower:

> **I want physical quantities to be ordinary, pleasant Python types that a static type checker can understand, without making an engineer interact with a registry or a stringly-typed unit system.**

That is the gap.

<!-- pause -->

<!-- new_lines: 2 -->

And that is why `kuchka` exists.

<!-- end_slide -->

## The carrot

<!-- pause -->

The whole argument comes back to this:

> **The problem isn't that engineers forget units.**
>
> **The problem is that the program has no way to remember them for them.**

Move the stick into the toolchain.

Hand the engineer a carrot:

```python +line_numbers
Volt(5) + Millivolt(200)
Volt(5) * Ampere(2)
Celsius(20) - Celsius(15)
```

Make the correct path the pleasant path.

<!-- end_slide -->

<!-- jump_to_middle -->

## Let's build the rest of the pile.
