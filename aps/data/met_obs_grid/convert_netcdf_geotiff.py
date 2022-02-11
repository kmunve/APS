import rioxarray
import xarray
from pathlib import Path
from glob import glob

ncdir = Path("D:\APS")

# ncfiles = glob(ncdir / "*.nc")
# print(ncfiles)

ncfile = "xgeo_dem_2_extr1014i.nc"
xds = xarray.open_dataset(ncdir / ncfile)
print(xds)

#TODO: CRS lacking
# xds.rio.write_crs("epsg:4326", inplace=True)
xds["xgeo_dem_2"].rio.to_raster(ncdir / "test.tif")
