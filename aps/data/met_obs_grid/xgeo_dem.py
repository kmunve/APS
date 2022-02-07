"""
Reads and transforms the digital elevation model used on www.xgeo.no

Create a netCDF file containing the DEM and coordinates.
1) Run >>>ncks -v air_temperature_2m /mnt/grid/metdata/prognosis/meps/det/archive/2022/meps_det_1km_20220102T00Z.nc tmp_xgeo_dem.nc
2 ) Add a xge0_dem_# and mask variables. Code below
3)* Run >>>ncks -v xgeo_dem_1,xgeo_dem_2,xgeo_mask,lon,lat /mnt/grid/metdata/config/tmp_xgeo_dem.nc /mnt/grid/metdata/config/xgeo_dem.nc
4) Copy xgeo_dem.nc also to \\nve.no\fil\hdrift\production\snowgrid\config (it is alos used from here operationally)

*Step 3 removes the air_temp... variable from the temporary netcdf file
"""
import numpy as np
from pathlib import Path
from aps.aps_io.bil import BILdata
import matplotlib.pyplot as plt
from netCDF4 import Dataset

# CONFIG
DEM_DIR = r"Y:\metdata\config"
XGEO_DEM_1 = "xgeo_dem_1.bil"
XGEO_DEM_2 = "xgeo_dem_2.bil"
XGEO_MASK = "xgeo_mask_1.bil"
XGEO_DEM_NC = "tmp_xgeo_dem.nc"


# Using BIL file format
dem_dir = Path(DEM_DIR)
xgeo_dem_1 = BILdata(dem_dir / XGEO_DEM_1, "uint16")
xgeo_dem_1.read()
xgeo_dem_2 = BILdata(dem_dir / XGEO_DEM_2, "uint16")
xgeo_dem_2.read()
xgeo_mask = BILdata(dem_dir / XGEO_MASK, "uint16")
xgeo_mask.read()

fill_value = xgeo_dem_1.data[0, 0]
print(fill_value, "fill?")
# plt.imshow(xgeo_dem.data, vmin=0, vmax=2500)
# plt.show()

ncfile = Dataset(dem_dir / XGEO_DEM_NC, "r+")
print(ncfile.variables['air_temperature_2m'])
print(ncfile.dimensions)

dem_1_var = ncfile.createVariable("xgeo_dem_1", datatype='l', dimensions=('y', 'x'), fill_value=fill_value)
dem_1_var.standard_name = "xgeo_dem_1"
dem_1_var.units = 'm'
dem_1_var.long_name = "Xgeo DEM version 1"
dem_1_var[:, :] = np.flipud(xgeo_dem_1.data)
dem_1_var.coordinates = "lon lat"
dem_1_var.grid_mapping = "projection_utm"

dem_2_var = ncfile.createVariable("xgeo_dem_2", datatype='l', dimensions=('y', 'x'), fill_value=fill_value)
dem_2_var.standard_name = "xgeo_dem_2"
dem_2_var.units = 'm'
dem_2_var.long_name = "Xgeo DEM version 2 including neighboring countries"
dem_2_var[:, :] = np.flipud(xgeo_dem_2.data)
dem_2_var.coordinates = "lon lat"
dem_2_var.grid_mapping = "projection_utm"

dem_mask_var = ncfile.createVariable("xgeo_mask", datatype='l', dimensions=('y', 'x'), fill_value=fill_value)
dem_mask_var.standard_name = "xgeo_mask"
dem_mask_var.units = 'm'
dem_mask_var.long_name = "Xgeo mask over Norway"
dem_mask_var[:, :] = np.flipud(xgeo_mask.data)
dem_mask_var.coordinates = "lon lat"
dem_mask_var.grid_mapping = "projection_utm"

ncfile.close()



pos = 'end'
