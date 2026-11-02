"""The generic quantity engine and the named engineering types built on it.

Application code should not need to read this package.

It exists so that ``Voltage``, ``Current``, ``Power``, ``Resistance``,
``TemperatureDelta``, and the rest of the vocabulary do not each have to hand-roll
their own arithmetic, conversion, and comparison logic:
they share one implementation (:class:`LinearQuantity`, in ``kuchka.quantities.base``)
and differ only in their :class:`~kuchka.dimensions.Dimension` and, where relevant,
their multiplication and division overloads.

The base dimensions and the axes that are not dimensions of their own each have a
module at this level, and `temporal` is one module because its types construct one
another.
Related derived types live in themed packages that mirror those of `kuchka.units`.

Runtime arithmetic (`+`, `-`, `*`, `/`) is fully general and lives on `LinearQuantity`:
it derives any product or quotient from `Dimension` exponent-vector algebra.
Type checkers cannot infer "Voltage times Current is Power" from that algebra, so each
type declares its relationships as explicit `@overload`s, which
`tools/generate_overloads.py` writes from the registry, and every overload list ends
with a fallback matching the signature declared on `LinearQuantity`, which keeps the
overrides compatible with the base class under strict checking.
"""

from __future__ import annotations

from kuchka.quantities import amount
from kuchka.quantities import angular
from kuchka.quantities import base
from kuchka.quantities import chemistry
from kuchka.quantities import current
from kuchka.quantities import electromagnetics
from kuchka.quantities import geometry
from kuchka.quantities import information
from kuchka.quantities import kinematics
from kuchka.quantities import length
from kuchka.quantities import logarithmic
from kuchka.quantities import luminous_intensity
from kuchka.quantities import mass
from kuchka.quantities import mechanics
from kuchka.quantities import photometry
from kuchka.quantities import proportion
from kuchka.quantities import radiation
from kuchka.quantities import solid_angle
from kuchka.quantities import temporal
from kuchka.quantities import thermal
from kuchka.quantities import thermodynamics
from kuchka.quantities.amount import *
from kuchka.quantities.angular import *
from kuchka.quantities.base import *
from kuchka.quantities.chemistry.catalytic_activity import *
from kuchka.quantities.chemistry.entities_per_amount import *
from kuchka.quantities.chemistry.molality import *
from kuchka.quantities.chemistry.molar_charge import *
from kuchka.quantities.chemistry.molar_concentration import *
from kuchka.quantities.chemistry.molar_energy import *
from kuchka.quantities.chemistry.molar_flow_rate import *
from kuchka.quantities.chemistry.molar_mass import *
from kuchka.quantities.chemistry.molar_volume import *
from kuchka.quantities.current import *
from kuchka.quantities.electromagnetics.ac_power import *
from kuchka.quantities.electromagnetics.capacitance import *
from kuchka.quantities.electromagnetics.charge import *
from kuchka.quantities.electromagnetics.conductance import *
from kuchka.quantities.electromagnetics.inductance import *
from kuchka.quantities.electromagnetics.magnetic_field_strength import *
from kuchka.quantities.electromagnetics.magnetic_flux import *
from kuchka.quantities.electromagnetics.magnetic_flux_density import *
from kuchka.quantities.electromagnetics.permeability import *
from kuchka.quantities.electromagnetics.permittivity import *
from kuchka.quantities.electromagnetics.resistance import *
from kuchka.quantities.electromagnetics.specific_charge import *
from kuchka.quantities.electromagnetics.specific_current import *
from kuchka.quantities.electromagnetics.voltage import *
from kuchka.quantities.geometry.area import *
from kuchka.quantities.geometry.volume import *
from kuchka.quantities.information.data import *
from kuchka.quantities.information.data_rate import *
from kuchka.quantities.kinematics.acceleration import *
from kuchka.quantities.kinematics.angular_velocity import *
from kuchka.quantities.kinematics.velocity import *
from kuchka.quantities.length import *
from kuchka.quantities.logarithmic import *
from kuchka.quantities.luminous_intensity import *
from kuchka.quantities.mass import *
from kuchka.quantities.mechanics.density import *
from kuchka.quantities.mechanics.energy import *
from kuchka.quantities.mechanics.energy_density import *
from kuchka.quantities.mechanics.force import *
from kuchka.quantities.mechanics.impulse import *
from kuchka.quantities.mechanics.mass_flow_rate import *
from kuchka.quantities.mechanics.momentum import *
from kuchka.quantities.mechanics.power import *
from kuchka.quantities.mechanics.pressure import *
from kuchka.quantities.mechanics.specific_energy import *
from kuchka.quantities.mechanics.specific_power import *
from kuchka.quantities.mechanics.torque import *
from kuchka.quantities.mechanics.velocity_squared import *
from kuchka.quantities.mechanics.volumetric_flow_rate import *
from kuchka.quantities.photometry.illuminance import *
from kuchka.quantities.photometry.luminance import *
from kuchka.quantities.photometry.luminous_efficacy import *
from kuchka.quantities.photometry.luminous_energy import *
from kuchka.quantities.photometry.luminous_exposure import *
from kuchka.quantities.photometry.luminous_flux import *
from kuchka.quantities.proportion import *
from kuchka.quantities.radiation.absorbed_dose import *
from kuchka.quantities.radiation.absorbed_dose_rate import *
from kuchka.quantities.radiation.activity import *
from kuchka.quantities.radiation.activity_concentration import *
from kuchka.quantities.radiation.equivalent_dose import *
from kuchka.quantities.radiation.equivalent_dose_rate import *
from kuchka.quantities.radiation.exposure import *
from kuchka.quantities.radiation.exposure_rate import *
from kuchka.quantities.radiation.specific_activity import *
from kuchka.quantities.radiation.surface_activity import *
from kuchka.quantities.solid_angle import *
from kuchka.quantities.temporal import *
from kuchka.quantities.thermal import *
from kuchka.quantities.thermodynamics.heating_rate import *

__all__: list[str] = []
__all__ += amount.__all__
__all__ += angular.__all__
__all__ += base.__all__
__all__ += chemistry.__all__
__all__ += current.__all__
__all__ += electromagnetics.__all__
__all__ += geometry.__all__
__all__ += information.__all__
__all__ += kinematics.__all__
__all__ += length.__all__
__all__ += logarithmic.__all__
__all__ += luminous_intensity.__all__
__all__ += mass.__all__
__all__ += mechanics.__all__
__all__ += photometry.__all__
__all__ += proportion.__all__
__all__ += radiation.__all__
__all__ += solid_angle.__all__
__all__ += temporal.__all__
__all__ += thermal.__all__
__all__ += thermodynamics.__all__
