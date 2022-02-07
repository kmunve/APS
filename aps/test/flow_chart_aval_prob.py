"""
Manual decision tree to choose avalanche problems.
"""

from abc import ABC

### Inputs
HNS72 = float  # 3-days new snow sum in cm
MAX_WSP72
OLD_SLAB72 = bool  # relevant new snow or wind slab from last 72 hours
PWL = bool  # prominent persistent weak layer exists
TEMP_TREND = []

AP = []  # list over relevant avalanche problems


class AvalancheProblem(ABC):

    def __init__(self, sensitivity, distribution, size):
        self.size = size
        self.sensitivity = sensitivity
        self.distribution = distribution
        self.name_EN = ""
        self.name_NO = ""


class WindSlab(AvalancheProblem):
    pass


class PersistentWeakLayer(AvalancheProblem):
    pass


class AvalancheProblemSolver:


    def is_wind_slab(self):
        # check if winds are strong enough to produce wind slabs
        if self.HNS72 >= 10 or self.MOVEABLE_SNOW >=10:
            if self.WSP >= 8:
                AP.append(WindSlab())

    def is_pwl(self):
        if self.PWL:
            AP.append(PersistentWeakLayer())



    def is_new_snow(self):
        # 3-day sum of new snow
        if HNS72 > 30:
            AP.append("New snow")
        elif HNS72 < 10:
            AP.append("Wind slab")
        else:






