# Where the radian meets a length

`Dimension` counts angle as an axis, so torque is energy per angle and angular velocity is angle per time.
Rotational mechanics also measures lengths, a radius, a lever arm, a radius of gyration, and this page describes how `kuchka` carries a calculation across that edge.

## Angle and length

The arc-length relation `s = r * theta` ties the angle axis to length, and each formula asks the radius for a different exponent of angle:

| Formula               | Closes when the radius is L | Closes when the radius is L ∠⁻¹ |
| --------------------- | --------------------------- | ------------------------------- |
| `v = omega * r`       | no                          | yes                             |
| `a = alpha * r`       | no                          | yes                             |
| `I = m * r * r`       | no                          | yes                             |
| `a = v * v / r`       | yes                         | no                              |
| `Omega = A / (r * r)` | yes                         | no, it needs a ∠² solid angle   |
| `omega = v / r`       | no                          | yes                             |

Systems that count the angle as a dimension resolve this with a radian constant, the statement `1 rad = 1`, applied where geometry turns a length into an angle.
`kuchka` places that statement on declared relations, and a radius is a `Length`.
A length read from a configuration file or a datasheet is used as it is, in every formula above.

The torque units already work this way.
`NEWTON_METRE` is a unit of `Torque` with the scale `2 pi`, so a newton-metre is a joule per radian and displays as `N·m`, and `Torque.from_force(force, lever_arm)` multiplies by the same `2 pi`.

## Bridges

A bridge is a declared rule `left <operation> right -> result` whose result differs from the plain product or quotient on the angle axis alone.
Like a rule, it applies to the exact operand kinds it names.

The factor follows from the exponents.
The turn is the canonical angle, so with `a_p` the angle exponent of the plain product and `a_r` that of the result, the canonical magnitude is multiplied by `(2 pi) ** (a_p - a_r)`:

| Relation                                          | `a_p` | `a_r` | Factor        |
| ------------------------------------------------- | ----- | ----- | ------------- |
| `Torque.from_force(force, lever_arm)`             | 0     | -1    | `2 pi`        |
| `Mass * Area -> MomentOfInertia`                  | 0     | -2    | `(2 pi) ** 2` |
| `AngularVelocity * Length -> Velocity`            | 1     | 0     | `2 pi`        |
| `AngularVelocitySquared * Length -> Acceleration` | 2     | 0     | `(2 pi) ** 2` |

Pi is the pinned rational of `kuchka.internal.constants.PI`, so a bridge and its inverse quotient cancel exactly, and a value that crosses a bridge and comes back is unchanged.

Each bridge meets two conditions:

1. **It fills a gap.** The plain product or quotient has no registered kind and has a dimension, so a bridge adds a result where arithmetic had none.
   The registry checks this when it closes, and a kind registered later for the plain dimension stops the import with the bridge it conflicts with.
2. **Its operands have one reading.** Every physically meaningful use of the named kinds gives the declared result, and a test names that reading.

The second condition is the one that keeps a bridge a fact about the physics:

| Relation                              | Gap | Readings                                                  | Bridged            |
| ------------------------------------- | --- | --------------------------------------------------------- | ------------------ |
| `Mass * Area`                         | yes | one: the moment of inertia, in kg·m²                      | yes                |
| `FirstMomentOfMass * Length`          | yes | one: the moment of inertia                                | yes                |
| `MomentOfInertia / Mass`              | yes | one: the square of the radius of gyration                 | yes                |
| `AngularVelocity * Length`            | yes | one: the tangential speed                                 | yes                |
| `AngularAcceleration * Length`        | yes | one: the tangential acceleration                          | yes                |
| `AngularJerk * Length`                | yes | one: the tangential jerk                                  | yes                |
| `AngularVelocitySquared * Length`     | yes | one: the centripetal acceleration                         | yes                |
| `Torque / Force`, `Torque / Length`   | yes | one: the lever arm, and the force at it                   | yes                |
| `AngularVelocity * Velocity`          | yes | one: the centripetal acceleration                         | yes                |
| `AngularVelocity * Momentum`          | yes | one: the centripetal force                                | yes                |
| `FirstMomentOfMass * AngularVelocity` | yes | one: the momentum of an unbalance on its circle           | yes                |
| `AngularDisplacement * Length`        | yes | one: the length of the arc swept                          | yes                |
| `Force * Length`                      | no  | two: work, or torque                                      | by `from_force`    |
| `Velocity / Length`                   | no  | two: `v / r` in rad/s, or `v / lambda` in Hz              | by a constructor   |
| `Length / Length`                     | no  | two: a ratio, or the angle of an arc over its radius      | by a constructor   |
| `Acceleration / Length`               | yes | two: `a / r` in rad/s², or `g / l` as the square of rad/s | by a constructor   |
| `Momentum * Length`                   | yes | two: angular momentum, or action in J·s                   | by a constructor   |
| `Frequency * Time`                    | no  | cycles, which are a count                                 | stays a `Fraction` |

Bridges cross the angle axis alone.
The solid angle and information axes have no geometric relation of this kind, and the lumen closes through algebra.
The operands of a bridge are principal or contested kinds, and a role reaches one through its conversion.

[Adding a bridge](../how-to/adding_a_bridge.md) describes how one is declared.

## The rotational chain

The dimensions of the rotational quantities are chosen so that dynamics closes by algebra, and bridges appear where a length enters:

| Quantity                 | Dimension    | Units                                | Displays as |
| ------------------------ | ------------ | ------------------------------------ | ----------- |
| `AngularAcceleration`    | ∠ T⁻²        | rad/s², tr/s², °/s², rpm/s           | rad/s²      |
| `AngularJerk`            | ∠ T⁻³        | rad/s³, tr/s³, °/s³                  | rad/s³      |
| `AngularVelocitySquared` | ∠² T⁻²       | rad²/s², tr²/s², °²/s²               | rad²/s²     |
| `MomentOfInertia`        | M L² ∠⁻²     | kg·m², kg·cm², g·cm², lb·ft², lb·in² | kg·m²       |
| `AngularMomentum`        | M L² ∠⁻¹ T⁻¹ | kg·m²/s, N·m·s                       | kg·m²/s     |
| `FirstMomentOfMass`      | M L          | kg·m, g·cm, g·mm, oz·in              | kg·m        |

`kg·m²` carries the scale `(2 pi) ** 2` the way `N·m` carries `2 pi`, so a datasheet value is typed as written.
`FirstMomentOfMass` is the unbalance of a rotor, in gram-millimetres, and it is also the step `m * r` of `m * r * r` in the order Python evaluates it.

```python
from kuchka import Kilogram
from kuchka import KilogramSquareCentimetre
from kuchka import Metre
from kuchka import RadianPerSecond
from kuchka import RadianPerSecondSquared

rotor = KilogramSquareCentimetre(30)  # a MomentOfInertia, from a datasheet
disc = 0.5 * Kilogram(2) * Metre(0.2) * Metre(0.2)  # a MomentOfInertia of 0.04 kg·m²
omega = RadianPerSecond(300)

rotor * RadianPerSecondSquared(400)  # a Torque
rotor * omega  # an AngularMomentum
0.5 * rotor * omega * omega  # an Energy
speed = omega * Metre(0.2)  # a Velocity of 60 m/s
speed * speed / Metre(0.2)  # an Acceleration, the centripetal one
omega * speed  # the same Acceleration
omega * omega  # an AngularVelocitySquared of 90000 rad²/s²
omega**2 * Metre(0.2)  # the same Acceleration, in any order
omega**2 * rotor  # an Energy
```

`omega * omega` is an `AngularVelocitySquared` (∠² T⁻²), so a product of three factors has one value in every order.
`omega * omega * r`, `r * omega * omega`, and `omega * (omega * r)` are the same `Acceleration`, the first by a bridge with `a_p - a_r = 2`.
`omega * omega * rotor` and `rotor * omega * omega` are the same `Energy` by algebra.

## Named relations

A relation with two readings is a constructor or a conversion that names the one meant:

- `Torque.from_force(force, lever_arm)`, since `Force * Length` is the work a force does along a length.
- `AngularVelocity.from_tangential(velocity, radius)`, since `Velocity / Length` is the `Frequency` of a wave of that wavelength.
- `AngularDisplacement.from_arc(arc, radius)`, since `Length / Length` is a ratio, a strain or a scale.

```python
from kuchka import AngularDisplacement
from kuchka import AngularVelocity
from kuchka import Metre
from kuchka import MetrePerSecond

AngularVelocity.from_tangential(MetrePerSecond(60), Metre(0.2))  # 300 rad/s
AngularDisplacement.from_arc(Metre(0.5), Metre(0.25))  # 2 rad
```

A natural frequency, `sqrt(k / m)`, is a radian rate whose dimension has no angle in it.
`Frequency.to_angular_velocity()` reads a hertz as one turn per second, which fits a frequency counted in cycles.
A speed over a radius arrives as a `Frequency` that counts radians, and `(v / r).to_angular_velocity()` reads it two pi times too fast, so the method's docstring points such a rate to `from_tangential`, and a natural frequency to `RadianPerSecond`.

## Choices behind the model

**A radius of dimension L ∠⁻¹.**
It closes `omega * r` and `m * r * r` by algebra and asks every boundary to choose between a `Length` and a radius.
The choice fails `v * v / r` and `SolidAngle.from_area`, which would then need the solid angle folded into ∠², and `Mass * Area` has no result, since an area is no radius squared.
Bridges keep the radius a `Length`, and the solid angle keeps its own axis.

**A moment of inertia of dimension M L².**
`Mass * Area` closes by algebra, and then each dynamic relation needs a bridge: `I * alpha`, `I * omega`, `I * omega * omega`, and their quotients.
With M L² ∠⁻², the bridges sit at the edge where a length enters, a handful of relations, and the dynamics is plain algebra.

**A radius as a role of `Length`.**
A specialisation of dimension L that a rule divides into, so that `Velocity / Radius` is an `AngularVelocity`.
It would make the quotient direction algebra, it fits this model, and it can be added when a calculation needs it.
