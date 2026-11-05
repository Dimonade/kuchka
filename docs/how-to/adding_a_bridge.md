# Adding a bridge

A bridge is a rule whose result differs from the plain product or quotient on the angle axis alone, such as `AngularVelocity * Length -> Velocity`.
[Where the radian meets a length](../concepts/angle_bridges.md) explains why the library has them; this page describes how one is declared.

## Do you need one?

A product or quotient that already has a type needs no bridge, and one between two kinds of the same dimension is a [rule](adding_a_quantity.md#principal-specialisation-contested).
A bridge fits when arithmetic crosses from geometry into rotation and the result is missing a power of the angle.

The krakenpeople swing a tentacle two shells long at a quarter turn per bubble, and ask how fast its tip moves.
`AngularVelocity * Length` has the dimension T⁻¹ L ∠, which has no type, and the tip speed is a `Velocity` of dimension T⁻¹ L, one power of the angle away.

Check the two conditions before declaring it:

1. **The gap.** The plain dimension, T⁻¹ L ∠, has no registered kind, and it is not dimensionless.
2. **The reading.** An angular velocity times a length is the speed of a point at that radius, in every use of the two kinds.

When a pair has two readings, as `Velocity / Length` has (an angular velocity from a radius, or a frequency from a wavelength), it is a named constructor on the result type instead, in the `from_x` style of `Torque.from_force`.

## Declare it

A bridge is declared after the registrations, in the module of the newest kind it names, the one that can import all the others, with its inverse quotients beside it.
`AngularVelocity * Length -> Velocity` lives in `angular_velocity.py`, since `velocity.py` sits below it and `length.py` below both:

<!-- doc-test: skip a fragment of a quantity module, not a program -->

```python
_bridge(AngularVelocity, "*", Length, Velocity)
_bridge(Velocity, "/", AngularVelocity, Length)
```

`_bridge` checks that the result differs from the plain dimension on the angle axis alone, that the operands are principal or contested kinds, and that no other rule names the same operands.
It derives the factor from the angle exponents, so the declaration carries no number.
A product holds in both operand orders, as a rule does.
The gap condition is checked when the registry closes, since the kind that would fill the gap may be registered by a later module.

Each inverse quotient meets the two conditions on its own.
`Velocity / AngularVelocity` is the radius, with the plain dimension L ∠⁻¹, a gap.
`Velocity / Length` is a `Frequency` already, so the angular velocity from a tip speed is `AngularVelocity.from_tangential(velocity, radius)`.

## What follows

- `just generate-overloads` writes the `*` and `/` overloads, because the generator samples the arithmetic itself.
- The bridge inventory test lists every bridge with its reading, and fails on one it has not seen.
- The concept page's table of relations gains a row, and the changelog a line.

## Checklist

- [ ] the gap and the reading, checked,
- [ ] `_bridge(...)` in the module of the newest kind it names, with the inverse quotients that are gaps,
- [ ] `just generate-overloads`,
- [ ] the reading in the bridge inventory test, and a test of the value across the bridge and back,
- [ ] the row in [Where the radian meets a length](../concepts/angle_bridges.md),
- [ ] a changelog line.
