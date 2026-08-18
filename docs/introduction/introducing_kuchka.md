---
title: kuchka
sub_title: a small pile of physically-typed units for Python
author: dimonade
---

## kuchka

<!-- new_lines: 8 -->

_A small pile of units._

_Deliberately small._

<!-- pause -->

<!-- new_lines: 2 -->

Voltage, Current, Power, Resistance, Temperature.

<!-- new_lines: 2 -->

Nothing else, on purpose. Yet.

<!-- pause -->

<!-- new_lines: 2 -->

Everything on the following slides actually runs.
No screenshots. No "trust me."

<!-- end_slide -->

## The problem

The year 1999. NASA loses a $125M spacecraft.

<!-- pause -->

Not an explosion. Not aliens. One team's software spoke
`pound-force-seconds`. The other assumed `newton-seconds`.
Nobody in between noticed.

<!-- pause -->

> [!caution]
> Our reports aren't going to Mars.
> But the failure mode is identical, just smaller and slower:
> a number quietly loses track of what it means, somewhere between acquisition and the printed page.

<!-- end_slide -->

## The Python problem specifically

```python
p = current_ma * v  # this time the units are correct, trust me,  I prefixed them, I checked 4 times!
```

<!-- pause -->

Python will happily let you subtract an Ampere from a Volt.

It will compute an answer.

It will just be **wrong**, quietly, at 2am, in a report nobody proofreads.

<!-- pause -->

<!-- new_lines: 2 -->

_Voice in my head:_ _Rust wouldn't let this near a compiler..._

<!-- pause -->

_The other voice in my head:_ We don't have Rust here. We have Python, and a manager who wants reports to go brrr.

<!-- end_slide -->

## We already tried sticks

Linter rules. Style guides nobody reads. "Please use `Volt()` here" in a PR comment.

<!-- pause -->

It holds -- right up until whoever's enforcing it gets pulled onto something else, and everyone quietly drifts back to `measurement_mv`.

<!-- pause -->

<!-- new_lines: 2 -->

_Voice in my head:_ Is `mv` "milli" or "micro"-Volts, though?

<!-- pause -->

<!-- new_lines: 2 -->

> [!caution]
> A rule you have to _remember_ is a rule you will, eventually, forget.
> Three months later it's a bug in a report, and a manager asking why "we had a rule about this" wasn't enough.

<!-- end_slide -->

## So: carrots

Not a better stick. Not a bot or an agent. No PR police patrol.

<!-- pause -->

Give engineers something more attractive to reach for than a raw `float` -- every time, not just when someone's watching -- and there's nothing left to be disciplined about.

<!-- pause -->

<!-- new_lines: 2 -->

```python
Volt(5) + Millivolt(200)   # -> Volt(5.2)
Volt(5) * Ampere(2)        # -> Power, computed, not asserted in a comment
```

<!-- pause -->

The correctness isn't sitting _next to_ the nice interface, waiting to be bypassed.

It's load-bearing -- `mypy`, `ty`, and runtime all agree, because there was never a separate rule to begin with.

<!-- end_slide -->

## Demo: Decimal, not float

`0.1 + 0.2` should never surprise anyone.

SI prefixes are powers of ten -- exact in `Decimal`, not exact in binary `float`.

```python {1|3-4|all} +exec
from kuchka import Volt, Millivolt

print(Volt(1) + Millivolt(500))
print(Volt(1) + Millivolt(500) == Volt(1.5))
```

<!-- end_slide -->

## Demo: derived dimensions

Multiplication and division understand physics, not just numbers.

```python +exec
from kuchka import Volt, Ampere

power = Volt(5) * Ampere(2)
print(power)
print(type(power).__name__)
```

<!-- pause -->

That's a real `Power` instance. Not a `float`.

Not a `Quantity` wearing a trench coat.

<!-- end_slide -->

## Demo: incompatible dimensions

```python +exec
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

```python +exec
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

```python +exec
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

```bash +exec
cat > /tmp/kuchka_demo.py <<'EOF'
from kuchka import Ampere, Volt, Voltage


def analyse(voltage: Voltage) -> None: ...


analyse(4.2)         # naked float
analyse(Ampere(2))   # wrong dimension
analyse(Volt(4.2))   # the only one that should pass
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

```python {1-2|4-9|all} +line_numbers
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

## Scope, on purpose

| In v0.1                     | Not yet, and that's fine     |
| --------------------------- | ---------------------------- |
| Voltage, Current            | Length, Mass, Time           |
| Power, Resistance           | NumPy / Pandas integration   |
| Temperature (Celsius, K)    | JSON / DB persistence        |
| Immutable, `Decimal`-backed | Autogenerated prefix classes |

<!-- pause -->

> [!note]
> Narrow scope isn't a limitation here -- it's what makes the whole thing tractable.
>
> It's also why nobody else has shipped exactly this.

<!-- end_slide -->

<!-- jump_to_middle -->

## Let's build the rest of the pile.
