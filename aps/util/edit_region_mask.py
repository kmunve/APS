from pathlib import Path
import os
import netCDF4
import matplotlib.pyplot as plt
from aps.util.nc_index_by_coordinate import tunnel_fast

# Creates the mask over the small regions of 20x20 km size
def create_small_regions_mask():
    p = Path(os.path.dirname(os.path.abspath(__file__))).parent
    nc_file = p / 'data' / 'terrain_parameters' / 'VarslingsOmr_2017.nc'
    vr_nc = netCDF4.Dataset(nc_file, "r")

    regions = vr_nc.variables["VarslingsOmr_2017"][:]

    regions_small = regions
    regions_small[1197:1218, 202:223] = 4001

    plt.imshow(regions_small, vmin=3007, vmax=3040)
    plt.show()

def get_xgeo_indicies(lat, lon):
    # region mask is flipped up-down with regard to MET-data in netCDF files
    y_max = 1550
    nc = netCDF4.Dataset(r"\\hdata\grid\metdata\prognosis\meps\det\archive\2018\meps_det_pp_1km_20180127T00Z.nc", "r")

    y, x = tunnel_fast(nc.variables['lat'], nc.variables['lon'], lat, lon)
    return y_max-y, x


if __name__ == "__main__":

    print("BLING BLING")
    y, x = get_xgeo_indicies(61.0, 8.1)
    print(y, x)
    create_small_regions_mask()
