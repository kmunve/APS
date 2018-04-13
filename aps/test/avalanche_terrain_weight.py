"""
Testing weighting of different meteorological parameters based on the percentage of avalanche terrain within a pixel.
"""


import numpy as np
import netCDF4
import matplotlib.pyplot as plt

reg_nc = netCDF4.Dataset(r"C:\Users\kmu\Dev\APS\aps\data\terrain_parameters\VarslingsOmr_2017.nc", "r")

#lok = reg_nc.variables["LokalOmr_2018"][:]
reg = reg_nc.variables["VarslingsOmr_2017"][:]

at_nc = netCDF4.Dataset(r"C:\Users\kmu\Dev\APS\aps\data\terrain_parameters\PercAval.nc", "r")
at = at_nc.variables["PercAval"][:]


region_id = 3014
_region_mask = np.where(reg == region_id)

plt.imshow(at[1000:1200, 0:200])
#plt.colorbar()
plt.savefig("perc_aval_terrain_part.png", dpi=96)
#plt.show()

