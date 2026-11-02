"""Radiation weighting factors of ICRP Publication 103, as plain proportions.

    from kuchka import Milligray
    from kuchka.constants.icrp_103 import ALPHA_PARTICLES
    from kuchka.quantities import EquivalentDose

    dose = EquivalentDose.from_absorbed_dose(Milligray(3), ALPHA_PARTICLES)   # 60 mSv

The radiation weighting factor, w_R, scales the absorbed dose of one kind of radiation
by how much more harm it does to tissue than a gamma ray does, and the product is the
equivalent dose.
Each constant is a `Proportion`, and `EquivalentDose.from_absorbed_dose` takes it
together with an `AbsorbedDose`.

These are recommendations of the International Commission on Radiological Protection,
a convention for radiological protection, and not measured constants.
The Commission has changed them before: Publication 60 (1990) gave protons a factor of
5, and Publication 103 (2007) gives them 2.
A regulation, a dosimetry standard, or a clinical protocol names the publication and
the value it requires, and takes it from that source, not from here.

Neutrons are not here: Publication 103 gives their factor as a continuous function of
the neutron energy, and not as a value.
The tissue weighting factors, w_T, that turn equivalent doses into an effective dose
are not here either.

Source: ICRP Publication 103, *The 2007 Recommendations of the International
Commission on Radiological Protection*, Annals of the ICRP 37 (2-4), Table 2.
https://www.icrp.org/publication.asp?id=ICRP%20Publication%20103
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Final

from kuchka.units import Ratio as _Ratio

if TYPE_CHECKING:
    from kuchka.quantities import Proportion

PHOTONS: Final[Proportion] = _Ratio(1)
"""Radiation weighting factor of photons: X-rays and gamma rays.

Accuracy: Recommended.
Value: 1.
Source: ICRP Publication 103, Table 2.
"""

ELECTRONS: Final[Proportion] = _Ratio(1)
"""Radiation weighting factor of electrons, and so of beta particles.

Accuracy: Recommended.
Value: 1.
Source: ICRP Publication 103, Table 2.
Note: the Commission treats Auger electrons emitted from nuclei bound to DNA as a
special case (paragraph 116 and Annex B.3.3), and this value does not cover them.
"""

MUONS: Final[Proportion] = _Ratio(1)
"""Radiation weighting factor of muons.

Accuracy: Recommended.
Value: 1.
Source: ICRP Publication 103, Table 2.
"""

PROTONS: Final[Proportion] = _Ratio(2)
"""Radiation weighting factor of protons.

Accuracy: Recommended.
Value: 2.
Source: ICRP Publication 103, Table 2.
Note: Publication 60 gave 5.
"""

CHARGED_PIONS: Final[Proportion] = _Ratio(2)
"""Radiation weighting factor of charged pions.

Accuracy: Recommended.
Value: 2.
Source: ICRP Publication 103, Table 2.
"""

ALPHA_PARTICLES: Final[Proportion] = _Ratio(20)
"""Radiation weighting factor of alpha particles.

Accuracy: Recommended.
Value: 20.
Source: ICRP Publication 103, Table 2.
"""

FISSION_FRAGMENTS: Final[Proportion] = _Ratio(20)
"""Radiation weighting factor of fission fragments.

Accuracy: Recommended.
Value: 20.
Source: ICRP Publication 103, Table 2.
"""

HEAVY_IONS: Final[Proportion] = _Ratio(20)
"""Radiation weighting factor of heavy ions.

Accuracy: Recommended.
Value: 20.
Source: ICRP Publication 103, Table 2.
"""

__all__ = [
    "ALPHA_PARTICLES",
    "CHARGED_PIONS",
    "ELECTRONS",
    "FISSION_FRAGMENTS",
    "HEAVY_IONS",
    "MUONS",
    "PHOTONS",
    "PROTONS",
]
