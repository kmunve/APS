
"""
Script for defining the elevation zones for each region.
Make sure that no outliers introduce a separate elevation zone with less than 2% area.
"""


import numpy as np
import netCDF4
import matplotlib.pyplot as plt

reg_nc = netCDF4.Dataset(r"D:\Dev\APS\aps\data\terrain_parameters\VarslingsOmr_2017.nc", "r")

lok = reg_nc.variables["LokalOmr_2018"][:]
reg = reg_nc.variables["VarslingsOmr_2017"][:]

DEM = "MEANHeight"
elev_nc = netCDF4.Dataset(r"D:\Dev\APS\aps\data\terrain_parameters\{0}.nc".format(DEM), "r")
elev = elev_nc.variables[DEM][:]\

met_nc = netCDF4.Dataset(r'Y:\metdata\prognosis\meps\det\archive\2018\meps_det_pp_1km_20180413T00Z.nc', 'r')
met_dem = np.flipud(met_nc.variables['altitude'][:])


elev_lok = np.where(lok == 4001, elev, np.nan)
for i in range(90, 101):
    print("{0}%: {1}".format(i, np.nanpercentile(elev_lok.flatten(), i)))

reg_id = np.arange(3007, 3036)

for id in reg_id:

    #print('=====================\n== {0}-{1} ==\n====================='.format(DEM, id))
    elev_reg = np.where(reg == id, elev, np.nan)
    #print("{0}%: {1}".format(i, np.nanpercentile(elev_reg.flatten(), i)))

    #print('=================\n== MetDEM-{0} ==\n================='.format(id))
    met_reg = np.where(reg == id, met_dem, np.nan)

    metdem100 = np.nanpercentile(met_reg.flatten(), 100)
    mean99 = np.nanpercentile(elev_reg.flatten(), 99)
    diff = metdem100 - mean99
    print("Id:{0}\tMetDEM (100):\t{1:.1f}\tMEAN (99):\t{2:.1f}\tDiff:\t{3:.1f}".format(id, metdem100,  mean99, diff))

#plt.plot(elev_reg.flatten(), color='r')
#plt.plot(elev_lok.flatten(), color='b')
#plt.show()

