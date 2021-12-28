"""
This script extracts the time-variable from matching netCDF files and prints them to command line.
"""

import netCDF4
from glob import glob
from pathlib import Path
import matplotlib.pyplot as plt

NC_DIR = r"\\nve.no\fil\grid\metdata\prognosis\met_pp_nordic\forecast\archive\2021"
NC_FILES = "met_forecast_1_0km_Norway_*T*Z.nc"

def print_time_info(f):
    nc = netCDF4.Dataset(f, 'r')
    t = nc.variables['time']
    print(f.name, len(t))
    return len(t)

nc_path = Path(NC_DIR) # / NC_FILES
nc_list = sorted(nc_path.glob(NC_FILES))

len_t = []
for nc in nc_list:
    len_t.append(print_time_info(nc))

plt.hist(len_t)
plt.show()



