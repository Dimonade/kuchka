"""ICRP Publication 103 radiation weighting factors, as ordinary `kuchka` quantities.

Access is via this dataset's own namespace (`kuchka.constants.icrp_103`, or
`kuchka.icrp_103`).
"""

from kuchka.constants.icrp_103.weighting import ALPHA_PARTICLES
from kuchka.constants.icrp_103.weighting import CHARGED_PIONS
from kuchka.constants.icrp_103.weighting import ELECTRONS
from kuchka.constants.icrp_103.weighting import FISSION_FRAGMENTS
from kuchka.constants.icrp_103.weighting import HEAVY_IONS
from kuchka.constants.icrp_103.weighting import MUONS
from kuchka.constants.icrp_103.weighting import PHOTONS
from kuchka.constants.icrp_103.weighting import PROTONS

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
