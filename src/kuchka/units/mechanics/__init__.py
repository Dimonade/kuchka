"""Unit constructors for common mechanical quantities.

The module brings together quantities used to describe forces, motion, material
properties, and mechanical energy:

- `Force`, `Pressure`, and `Stress` describe mechanical loading.
- `Momentum` and `Impulse` describe motion and the effects of applied forces.
- `Torque` describes rotational loading, and `MomentOfInertia`, `AngularMomentum`,
  and `FirstMomentOfMass` the rotating body and its unbalance.
- `Energy` and `Power` describe mechanical work and its rate of transfer.
- `MassFlowRate` and `VolumetricFlowRate` describe how much material passes a section
  per unit of time, of a liquid, a gas, or a solid.
- `Density`, `EnergyDensity`, and `SpecificEnergy` describe material and energy
  properties.
- `VelocitySquared` provides the squared-velocity quantity used in energy and
  dynamics calculations.

Examples
--------
Hydraulic systems use pressure acting over an area to generate substantial forces.
A hydraulic press operating at 300 bar applies a force of 18 kN to a piston with a
cross-sectional area of 6 cm²:

>>> from kuchka import Bar, SquareCentimetre
>>> Bar(300) * SquareCentimetre(6)
18000 N

Momentum and impulse describe two sides of a change in motion.
Consider a 1200 kg car travelling at 20 m/s that comes to a complete stop over
four seconds.
Its initial momentum determines the magnitude of the average braking force:

>>> from kuchka import Kilogram, Metre, Newton, Second
>>> initial_momentum = Kilogram(1200) * (Metre(20) / Second(1))
>>> initial_momentum / Second(4)
6000 N

The corresponding braking impulse has the same magnitude as the change in momentum:

>>> Newton(6000) * Second(4)
24000 N·s

Mechanical power describes how quickly work is performed or energy is transferred.
A 750 W electric motor running continuously for 20 seconds supplies 15 kJ of energy:

>>> from kuchka import Watt
>>> Watt(750) * Second(20)
15000 J

Material density is particularly useful when estimating the mass of manufactured
components and structural materials.
A solid steel billet occupying 0.25 m³, assuming a density of 7850 kg/m³, has a mass
of:

>>> from kuchka import CubicMetre, KilogramPerCubicMetre
>>> KilogramPerCubicMetre(7850) * CubicMetre(0.25)
1962.5 kg

Notes
-----
The module covers several important relationships in classical mechanics:

    force = pressure * area
    impulse = force * time
    momentum = mass * velocity
    energy = power * time
    mass = density * volume
    volume = area * velocity * time

Some mechanical quantities share physical dimensions without representing the same
concept.
This is particularly important in mechanics, where mathematical dimensional equivalence
does not necessarily imply physical interchangeability:

- `Energy` and `Torque` both have dimension ML²T⁻².
- `Pressure`, `Stress`, and `EnergyDensity` all have dimension ML⁻¹T⁻².
- `SpecificEnergy` and `VelocitySquared` both have dimension L²T⁻².

The quantities retain their distinct meanings and types even when their SI dimensions
coincide.
For example, torque is not energy, stress is not pressure, and specific energy is not
velocity squared.

The individual submodules provide the corresponding unit systems, including
international and customary engineering units.

`DENSITY_UNITS`, `ENERGY_UNITS`, `FORCE_UNITS`, `IMPULSE_UNITS`,
`MOMENTUM_UNITS`, `POWER_UNITS`, `PRESSURE_UNITS`, `STRESS_UNITS`,
`TORQUE_UNITS`, and the other family-specific mappings expose unit symbols
and their constructors for applications that resolve units dynamically.

See Also
--------
~kuchka.quantities.Force
Quantity type representing mechanical force.

~kuchka.quantities.Pressure
Quantity type representing force per unit area.

~kuchka.quantities.Momentum
Quantity type representing the motion of a body.

~kuchka.quantities.Impulse
Quantity type representing the effect of force over time.

~kuchka.quantities.Energy
Quantity type representing mechanical work and energy transfer.

~kuchka.quantities.Power
Quantity type representing energy transferred per unit time.

~kuchka.quantities.Density
Quantity type representing mass per unit volume.

"""

from __future__ import annotations

from kuchka.units.mechanics import angular_momentum
from kuchka.units.mechanics import density
from kuchka.units.mechanics import dynamic_viscosity
from kuchka.units.mechanics import energy
from kuchka.units.mechanics import energy_density
from kuchka.units.mechanics import first_moment_of_mass
from kuchka.units.mechanics import force
from kuchka.units.mechanics import impulse
from kuchka.units.mechanics import kinematic_viscosity
from kuchka.units.mechanics import mass_flow_rate
from kuchka.units.mechanics import moment_of_inertia
from kuchka.units.mechanics import momentum
from kuchka.units.mechanics import power
from kuchka.units.mechanics import pressure
from kuchka.units.mechanics import specific_energy
from kuchka.units.mechanics import specific_power
from kuchka.units.mechanics import stress
from kuchka.units.mechanics import torque
from kuchka.units.mechanics import velocity_squared
from kuchka.units.mechanics import volumetric_flow_rate
from kuchka.units.mechanics.angular_momentum import *
from kuchka.units.mechanics.density import *
from kuchka.units.mechanics.dynamic_viscosity import *
from kuchka.units.mechanics.energy import *
from kuchka.units.mechanics.energy_density import *
from kuchka.units.mechanics.first_moment_of_mass import *
from kuchka.units.mechanics.force import *
from kuchka.units.mechanics.impulse import *
from kuchka.units.mechanics.kinematic_viscosity import *
from kuchka.units.mechanics.mass_flow_rate import *
from kuchka.units.mechanics.moment_of_inertia import *
from kuchka.units.mechanics.momentum import *
from kuchka.units.mechanics.power import *
from kuchka.units.mechanics.pressure import *
from kuchka.units.mechanics.specific_energy import *
from kuchka.units.mechanics.specific_power import *
from kuchka.units.mechanics.stress import *
from kuchka.units.mechanics.torque import *
from kuchka.units.mechanics.velocity_squared import *
from kuchka.units.mechanics.volumetric_flow_rate import *

__all__: list[str] = []
__all__ += angular_momentum.__all__
__all__ += density.__all__
__all__ += dynamic_viscosity.__all__
__all__ += energy.__all__
__all__ += energy_density.__all__
__all__ += first_moment_of_mass.__all__
__all__ += force.__all__
__all__ += impulse.__all__
__all__ += kinematic_viscosity.__all__
__all__ += mass_flow_rate.__all__
__all__ += moment_of_inertia.__all__
__all__ += momentum.__all__
__all__ += power.__all__
__all__ += pressure.__all__
__all__ += specific_energy.__all__
__all__ += specific_power.__all__
__all__ += stress.__all__
__all__ += torque.__all__
__all__ += velocity_squared.__all__
__all__ += volumetric_flow_rate.__all__
