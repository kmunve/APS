from pathlib import Path
import os
import numpy as np
import netCDF4
import matplotlib.pyplot as plt
from aps.util.nc_index_by_coordinate import tunnel_fast

# Creates the mask over the small regions of 20x20 km size
def create_small_regions_mask():
    p = Path(os.path.dirname(os.path.abspath(__file__))).parent
    nc_file = p / 'data' / 'terrain_parameters' / 'VarslingsOmr_2017.nc'
    nc = netCDF4.Dataset(nc_file, "a")

    # removes inconsistencies wrt fill_value in VarslingsOmr_2017
    vr = nc.variables["VarslingsOmr_2017"]
    regions = vr[:]
    regions[regions == 0] = 65536
    regions[regions == 65535] = 65536

    vr[:] = regions

    # create mask based on dictionary with small regions to monitor
    regions_small = regions
    regions_small[regions > 3000] = 65536

    # extend in each direction from center in km
    ext_x, ext_y = 10, 10

    # dict over smaller region with Id and coordinates of center-point
    # VarslingsOmr have Id in range 3000-3999 - LokalOmr in 4000-4999
    s_reg = {"Hemsedal": {"Id": 4001, "Lat": 60.95, "Lon": 8.28},
             "Tyin": {"Id": 4002, "Lat": 61.255, "Lon": 8.2},
             "Kattfjordeidet": {"Id": 4003, "Lat": 69.65, "Lon": 18.5},
             "Lavangsdalen": {"Id": 4004, "Lat": 69.46, "Lon": 19.24}}

    for key in s_reg:
        y, x = get_xgeo_indicies(s_reg[key]['Lat'], s_reg[key]['Lon'])
        regions_small[y - ext_y : y + ext_y + 1, x - ext_x : x + ext_x + 1] = s_reg[key]['Id']

    # set up new netCDF variable and attributes
    lr = nc.createVariable('LokalOmr_2018', np.int32, ('y', 'x'))
    lr.units = vr.units
    lr.long_name = 'Mindre test omraader'
    lr.missing_value = vr.missing_value
    lr.coordinates = vr.coordinates
    lr.grid_mapping = vr.grid_mapping
    lr.esri_pe_string = vr.esri_pe_string
    lr[:] = regions_small

    nc.close()
    print('Dataset is closed!')

def add_lat_lon():
    p = Path(os.path.dirname(os.path.abspath(__file__))).parent
    nc_file = p / 'data' / 'terrain_parameters' / 'VarslingsOmr_2017.nc'
    nc = netCDF4.Dataset(nc_file, "a")

    nc_ref = netCDF4.Dataset(r"\\hdata\grid\metdata\prognosis\meps\det\archive\2018\meps_det_pp_1km_20180127T00Z.nc", "r")
    lat_ref = nc_ref.variables['lat']
    lon_ref = nc_ref.variables['lon']

    lat = nc.createVariable('lat', np.float64, ('y', 'x'))
    lat.units = lat_ref.units
    lat.standard_name = lat_ref.standard_name
    lat.long_name = lat_ref.long_name

    lon = nc.createVariable('lon', np.float64, ('y', 'x'))
    lon.units = lon_ref.units
    lon.standard_name = lon_ref.standard_name
    lon.long_name = lon_ref.long_name

    nc.close()
    nc_ref.close()





def get_xgeo_indicies(lat, lon):
    # region mask is flipped up-down with regard to MET-data in netCDF files
    y_max = 1550
    nc = netCDF4.Dataset(r"\\hdata\grid\metdata\prognosis\meps\det\archive\2018\meps_det_pp_1km_20180127T00Z.nc", "r")

    y, x = tunnel_fast(nc.variables['lat'], nc.variables['lon'], lat, lon)
    return y_max-y, x


if __name__ == "__main__":

    print("BLING BLING")
    #y, x = get_xgeo_indicies(60.95, 8.28); print(y, x)
    #create_small_regions_mask()
    add_lat_lon()
