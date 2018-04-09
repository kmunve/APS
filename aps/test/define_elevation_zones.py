
"""
Script for defining the elevation zones for each region.
Make sure that no outliers introduce a separate elevation zone with less than 2% area.
"""


import numpy as np
import netCDF4
import matplotlib.pyplot as plt

reg_nc = netCDF4.Dataset(r"C:\Users\kmu\Dev\APS\aps\data\terrain_parameters\VarslingsOmr_2017.nc", "r")

lok = reg_nc.variables["LokalOmr_2018"][:]
reg = reg_nc.variables["VarslingsOmr_2017"][:]

DEM = "MEANHeight"
elev_nc = netCDF4.Dataset(r"C:\Users\kmu\Dev\APS\aps\data\terrain_parameters\{0}.nc".format(DEM), "r")

elev = elev_nc.variables[DEM][:]\

elev_lok = np.where(lok == 4001, elev, np.nan)
for i in range(90, 101):
    print("{0}%: {1}".format(i, np.nanpercentile(elev_lok.flatten(), i)))

elev_reg = np.where(reg == 3035, elev, np.nan)
for i in range(90, 101):
    print("{0}%: {1}".format(i, np.nanpercentile(elev_reg.flatten(), i)))

#plt.plot(elev_reg.flatten(), color='r')
#plt.plot(elev_lok.flatten(), color='b')
#plt.show()

