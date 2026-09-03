# Saving the Martian Rover Again

_Or: A Yet Another Units-of-Measurement Package for Python?_

Comrades in arms.
Colleagues of the kitchenette.
Fellow sufferers of `# this time the units are correct, trust me`.

Gather close, because I have a proposal, and like all good proposals from people who should probably know better, it begins with a cautionary tale you already know.

In 1999, NASA lost a $125 million spacecraft because one team's software spoke pound-force-seconds and another team's software assumed newton-seconds, and nobody in between noticed the two systems were having two completely different conversations about the same numbers.
The craft didn't explode on the launchpad.
It didn't get shot down by aliens.
It just quietly drifted into an orbit forty times too aggressive and burned up, because a `float` doesn't know what it means, and neither, it turns out, did the pipeline carrying it.
If you want the full, embarrassing detail, [JPL will tell you themselves](https://www.jpl.nasa.gov/missions/mars-climate-orbiter/).

I bring this up not because our reports are going to Mars.
They are going to a PDF that a regulatory auditor will open once, six months from now, squint at, and forward to someone else.
But the failure mode is identical, just smaller and slower: a number loses track of what it means somewhere between acquisition and the printed page, and nobody notices until it's someone's job to explain why.

## The Problem, Stated Plainly

Engineers are an unruly bunch.
Strong opinions, a preference for doing things their own way, and -- I say this with love, because I am one -- allergic to anything standing between them and the thing they're actually trying to build.
This is, on balance, a virtue.
Impatience with friction is where most good tools come from.

My argument with this instinct is narrower than "engineers are lazy, therefore bad."
It's this: **Python will let you get away with it.**
Hand it a float, a string, or an unsigned nuclear submarine where a voltage was expected, and Python will shrug and compute something anyway.
Unlike Rust, which would stare at you in stony silence until you either fixed the type or gave up entirely.
Rust would never let a `float(5.0)` get within arithmetic distance of `4.2 NuclearSubmarines`.
Python doesn't care.
Python will happily hand you an answer.
It will just occasionally be the wrong one, quietly, at 2 AM, in a report nobody proofreads because "that looks sensible".

I would love to tell you the fix is "everyone learns Rust."
I love Rust.
I write Rust.
Most of my personal tools are Rust.
I am, like a genuinely alarming number of people on the internet, building a small game in Bevy, in my spare time, for reasons I have made peace with.
But Rust at work, on this project, for these teams? No way.
Not everyone knows it.
Not everyone wants to learn it under deadlines.
The equipment vendors ship Python bindings, not Rust ones.

So: Python is what we have, and with Python, we are going to try to win anyway.

_[meme: SpongeBob, two panels. Panel one — suspicious, narrowed eyes —
"Rust, when I am one atom of type-difference away from what was
expected." Panel two — gleefully handing over money — "Python, casting a
float into an unsigned 2023 Toyota Yaris."]_

## We Already Tried Sticks

Not literally -- nobody's proposed a whip _(maybe we should have?..)_.
But every team that's cared about this problem has tried some version of the stick: a linter rule, a style guide nobody quite reads, a comment in code review saying "please, for the love of the Lord, use `volt` here," a type hint that only some paths actually go through.

And it holds, for a while.
Right up until:

- the type hint was optional, and the deadline wasn't, so it got skipped;
- the linter rule only caught the obvious cases, and the interesting bugs were never the obvious ones;
- whoever was doing code review on this got pulled onto something else, and nobody replaced them;
- a bug quietly resurfaces three months later in a report a manager is now asking uncomfortable questions about, and the postmortem says "we had a rule about this," and everyone already knows that isn't going to be a satisfying answer.

Sticks work exactly as long as someone is holding them.
The moment they're not -- and someone always eventually isn't -- everyone drifts back to `measurement_mv`, `time_ms`, `t_c`, and the eternal question of which of your six variously-named temperature variables is actually in Celsius this week.
Not because engineers are careless.
Because a rule you have to _remember_ is a rule you will, eventually, forget, and a type-checked boundary you have to _choose_ to route through is a boundary someone will eventually route around.

## So: Carrots

The fix isn't a better stick.
It's not having one at all.
Not even behind my back, go ahead and check it.

Give engineers something that's simply more attractive to reach for than a raw `float` -- every time, not just when someone's watching -- and the regression problem stops being a discipline problem, because there's nothing left to be disciplined about.

`Voltage`, `Volt`, `Millivolt`, `Kilovolt`, `Current`, `Ampere`, `Power`, `Celsius`, `TemperatureDelta` - these need to exist as first-class, unapologetic citizens, not registry lookups wearing a type-hint costume.

The arithmetic has to just work:

```python
Volt(5) + Millivolt(200)  # -> Volt(5.2)
Millivolt(5200)  # -> equal to the above, if they'd rather see it that way
Volt(5) * Ampere(2)  # -> Power, computed, not asserted in a comment
```

No stringly typed registries.
No guessing which spelling of "millivolt" the registry accepts in this version.
`mypy` and `ty` both need to agree with what actually happens at runtime - not "probably agree," not "agree if you squint," agree.
And never, ever again should `4.2 NuclearSubmarines` be quietly subtracted from `float(5.0)` because both of them technically fit in a number.

Engineers respond better to carrots than to sticks.
This is, as far as I can tell, universally true of engineers, toddlers, and horses.

### Tinkerers, Unite

A comfortable front door doesn't mean the back door gets welded shut.
Anyone who wants to reach past the friendly interface and build their own tooling, inspect a raw magnitude, write a custom conversion, should be able to.
We are not building a walled garden.
We're building a pile with a well-marked entrance and no locked doors.
The goal is to cater to everyone, or, more honestly, to disappoint the fewest people possible.

### Why This Carrot Doesn't Rot

The part that actually answers the sticks problem, not just avoids the word: an ordinary carrot -- a nicer function name, a friendlier wrapper -- is still just sugar on top of the same unsafe thing underneath, and it decays the same way a stick does, because someone can still reach past it the moment it's inconvenient.

This one is different because the correctness isn't sitting _next to_ the pleasant interface, waiting to be bypassed.
It's load-bearing.
`Voltage`, `Current`, and the rest are structurally incapable of holding a value that doesn't mean what it says -- not because a rule says so, but because that's what the object _is_.
Deciding which submarine can legally be cast into which orbiter, producing an error that actually says what went wrong instead of `TypeError: unsupported operand type(s)` -- that's unglamorous, permanent work that happens once, here, so nobody using the library ever has to remember a rule to get it right.

There's no separate enforcement step to eventually stop happening, because the ergonomics and the correctness were never two different things to begin with.

While we're on the subject of things that are non-negotiable: measurements are immutable, and they're backed by `Decimal`, not `float`.
Nobody on this team or elsewhere should expect `0.1 + 0.2` to hand back `0.30000000000000004`, and nobody should have to explain a report discrepancy with "well, technically, IEEE 754."

That's the pitch.
Now let's see if it survives contact with an actual undocumented part.

## The Spec We're Actually Living With

This isn't hypothetical, and I'd rather not let it stay abstract for one more section.

The diode driver on the current board came from a supplier in Shenzhen, chosen because it was a few dollars cheaper than the alternative and nobody wanted to have that budget conversation twice.
The Python bindings were written by a contractor in Shanghai, on a fixed-scope contract that ended two years ago.
He does not work there anymore.
Nobody there does, as far as we've been able to tell.

The documentation is one PDF.
Half of it is in English.
The numbers in that half don't always agree with the numbers in the half that isn't.
`read_status()` -- the function that actually matters -- has exactly one comment above it in the entire file:

```python
# 太老了
def read_status(): ...
```

_Welp._
That does not look like documentation, does it?
What if I squint harder?
Still no.

This is what `GuideFinal_2021_last_Copy Copy (4).docx` grows up to become, if you let it.
Not a doc that merely went stale.
A doc that was never written in the first place, for a driver you didn't write, wrapping a chip you didn't choose, that some other team is depending on you having already understood correctly last sprint.

## I Ran The Numbers

I didn't just complain about this in the abstract.
I took the actual shape of the problem and ran it as a live exercise, on three language models and some real engineers, with no hint given about what I was fishing for.
Here is the entire task, verbatim, not a paraphrase, with that familiar `read_status()` from above:

```text
Quick task: diode pre-flight check.

We're prototyping a pre-flight safety check for the new diode
driver before it goes into the acquisition pipeline. Nothing
fancy - just a first pass.

Time box: 10 minutes. Don't overthink it, don't go looking
things up, just write what you'd normally write.

What you're given
------------------
1. `read_status()` which returns the `status` of the diode.
2. From the datasheet, section 4.2 (Absolute Maximum Ratings):
    MAX_CURRENT_MA = 250
    MAX_CASE_TEMP_C = 45
    MAX_POWER_MW = 500
```

And here is what `read_status()` actually returns, and the whole
function signature everyone was given to fill in:

```python
status = {
    "i_meas": 187500,
    "v_meas": 2350,
    "t_case": 314.85,
}


def check_diode_status(status: dict) -> None: ...
```

The results were quite interesting.

Two of the models read it carefully and got every check right: converted microamps to milliamps, subtracted 273.15 for Kelvin, multiplied correctly to land on milliwatts.
Both flagged, entirely unprompted, the exact thing we'd built the exercise around: _"the units aren't explicitly stated in the code..."_, _"... that is inferred rather than specified."_
That's not a point in favor of raw floats.
That's the two most careful readers -- and this whole task fit comfortably inside their context window, so "I didn't have room to think about it" isn't an excuse either of them gets to reach for -- telling us, on their own, that the interface itself is the problem.

A third model read the same fields and quietly decided the case temperature was in milli-Celsius.
`314.85 / 1000` prints `0.31 °C`.
A diode, supposedly under load, reported a third of a degree above freezing -- colder than your fridge.
Nothing about running that code says anything went wrong.
There is no exception, no warning, and no red blinking lights with Hell March 2 music gradually getting louder in the background.
Just a clean `PASS` next to a number that should have raised an eyebrow, if there'd been anyone looking for one to raise.

Then I asked people around to try it out.

First engineer -- the current check: exactly right.
The temperature check:

```python
temp_check = "PASS" if status["t_case"] <= MAX_CASE_TEMP_C else "FAIL"
```

Kelvin, compared straight against a Celsius limit, no conversion at all.
`314.85` is not less than or equal to `45`, so the report says FAIL on a diode that is, in reality, a comfortable 41.7°C.

The power check is the one none of us saw coming:

```python
power_check = "PASS" if power_in_w / 1000 > MAX_POWER_MW else "FAIL"
print(f"power, {power_in_w * 1000}, {power_check}")
```

Look at what actually printed: `power, 440.625..., FAIL`.
The number is exactly right -- 440.6 mW, comfortably under the 500 mW limit.
The verdict sitting right next to it was computed from a different expression entirely, scaled the wrong way, compared with the wrong operator.
Nobody mixed up a prefix here.
Two lines of code that were supposed to describe the same value quietly stopped agreeing with each other, and nothing about the output tells you that happened -- the number you'd trust is attached to the wrong label.

Two more volunteers turned up after the first draft of this made its rounds, because apparently nothing invites additional test subjects quite like publicly cataloguing everyone else's mistakes.

The first one left a comment above every conversion, stating the assumed unit outright -- and got one of the three wrong:

```python
# assuming i_meas is in milliamps
# assuming v_meas is in millivolts
# assuming t_case is in celsius
i = status["i_meas"] / 1000
v = status["v_meas"] / 1000
t = status["t_case"]
```

`i_meas` is, in fact, microamps, not milliamps -- but dividing microamps by a thousand also gets you milliamps, so the arithmetic came out right despite the comment above it being wrong about what it was dividing.
The voltage comment happened to be correct, so that one landed right for the right reason.
The temperature got no conversion at all, on the stated assumption that `t_case` "is in celsius" -- it isn't -- so the report says `FAIL` on a diode running at a perfectly reasonable 41.7 °C, same failure shape as the Kelvin/Celsius mixup two paragraphs up, same root cause.

Here's the part I find more unsettling than any mistake so far: a wrong comment sitting directly above code that happens to work is worse than no comment at all.
A reviewer reads "assuming milliamps," checks that the code divides by 1000, nods, and moves on -- the comment and the code agree with each other.
They're just both quietly wrong about the same input, in a way that happens to cancel out.

The second volunteer applied no unit handling whatsoever -- no division, no conversion, nothing -- and printed the raw fields straight through:

```text
Current = 187500 mA, FAIL
Temperature = 314.85 °C, FAIL
Power = 440625000 mW, FAIL
```

Every single check fails.
The diode, which is fine on all three counts, gets flunked across the board, because a microamp reading got compared directly against a milliamp limit, a Kelvin reading got compared directly against a Celsius limit, and a power figure off by six orders of magnitude got compared against a milliwatt budget as though it already were one.

I want to be precise about what all of this does and doesn't show.

And no, sorry techbros, it is not "the AI is better than the engineer", it never is (for many, many reasons).
Two models got it completely right and said why, out loud.
One got it completely wrong and said nothing at all -- confidently, cleanly, with a `PASS` sitting right there to back it up.
Three separate engineers, working independently, produced three separate flavors of wrong: a comparison run against the wrong reference scale, a printed number attached to a verdict computed from an entirely different expression, and a comment that lied just convincingly enough to make the line beneath it look reviewed.

Six attempts. Five distinct ways to get it wrong, and not one of them was a skill problem.

Every one of them traces back to the same problem: a plain number carries no memory of what it means, and nothing forces the value you print, the value you compare, and the value you meant, to all be the same value.
That's not a reason to go find better engineers.
It's the reason this needs to be structural.

## How `kuchka` Solves This

Same driver. Same three raw fields. Typed once, at the boundary:

```python
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

```
current: 187.500 mA PASS
temp:    41.70 °C PASS
power:   440.625000 mW PASS
```

Three `PASS`es, correctly, on the first try, with no conversion arithmetic scattered through the function body to get subtly wrong.

But here's the part I actually want to stress on:
the exact line `status["t_case"] <= MAX_CASE_TEMP_C` -- a Kelvin float compared straight against a Celsius-flavored int -- shows up, essentially unchanged, in three separate submissions.
Try to write that same comparison against typed values:

```python
temp <= 45
```

```
error: Unsupported operand types for <= ("Temperature" and "int")  [operator]
```

That is much better.
The comparison is not even flying to begin with.
Not because I sat down and banned it -- because a `Temperature` and a bare `int` were never the same kind of thing to begin with, and the type checker is just saying so out loud, before anyone gets the chance to be careful or careless about it.

And if the mistake ever does slip past `mypy` -- an untyped boundary, a suppressed warning, a `# type: ignore` someone added under deadline and never removed -- the runtime is not left guessing either:

```python
from kuchka import Volt, Ampere

Volt(12) - Ampere(2)
```

```
kuchka.errors.IncompatibleDimensionError: Cannot subtract Voltage and Current.
Voltage has dimension [M L^2 T^-3 I^-1].
Current has dimension [I].
```

_Nice._

Compare that against the `TypeError: unsupported operand type(s)`.
This one names both quantities, names both dimensions, and says exactly why they don't belong in the same sentence -- not a stack trace to go spelunking through, an actual answer.

## More Carrots

Since the first draft of this went around, a few more carrots got planted.
They aren't load-bearing to the argument above, they are the kind of thing you only notice is missing once you go looking for it.

**Constants, so the universe doesn't need a `# in m/s, I checked` comment either.**

```python
from kuchka import Hertz
from kuchka.constants import SPEED_OF_LIGHT

wifi_wavelength = SPEED_OF_LIGHT / Hertz(2_400_000_000)
print(f"{wifi_wavelength:.4f}")
```

```
0.1249 m
```

`SPEED_OF_LIGHT` is a `Velocity`.
`Hertz(2_400_000_000)` is a `Frequency`.
Dividing one by the other produces a `Length` -- correctly, because that's what dividing a velocity by a frequency has always meant, and the type system had already agreed on that before I typed a single line of this example.

**Formatting, for the reports that started this whole argument.**

```python
from kuchka import Volt

voltage = Volt(1234.5)
print(f"{voltage:.2f}")
print(f"{voltage:.2e}")
```

```
1234.50 V
1.23e+3 V
```

Every quantity understands Python's own format spec now, the same one `float` has always had.
No new syntax to learn, no `.format_as("scientific")` method to go hunting for -- the digits format the way digits already know how to format, and the unit symbol rides along after.

## Ending Notes

I genuinely don't know what trench I'm digging myself into with this one.
But I'd like to try, on a small, deliberately narrow set of units and conversions first, and see how it holds up before promising the moon, or in this case, Mars.

Here's what I keep coming back to:
engineers who didn't choose Python, those who are using it because the acquisition hardware shipped a Python library and a manager wants the reports automated deserve better than:

```python
p = (
    current_ma * v
)  # this time the units are correct, trust me, I prefixed them, I checked 4 times.
```

The rule I want us to hold ourselves to is simple: raw floats are allowed to exist in exactly one place -- the input boundary.

The instant a number crosses into the application, the analysis pipeline, the report generator, or a stored calculation, it has to carry its physical meaning with it.

Nobody should ever again have to reconstruct, from source comments and a file called `GuideFinal_2021_last_Copy Copy (4).docx`, that is a Fw of a Fw from some Outlook email that the first half of a calculation assumed millivolts, storage assumed volts, and the dashboard re-assumed millivolts on the way out.
Is that the final version of that doc file?
I don't know.
And I sincerely doubt you do either.
The person who wrote it has since left the company, or been promoted, or -- in the grand tradition of undocumented tribal knowledge -- both.

_[meme: the "must resist urge" format - "must resist urge to use Rust."]_

For the record: yes, I love Rust.
Yes, I use it constantly, for practically everything I get to choose the language for, including a video game nobody asked for.
No, I am not going to suggest we rewrite this in Rust.
I've done the math on what that costs in missed deadlines, onboarding, retooling, retraining, and goodwill, and the number is not small.
We're staying in Python.
For this one.

For now.

One day, though. One day.