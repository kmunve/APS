import netCDF4
import os
from nco import Nco

###
# UNDER CONSTRUCTION
###


def xgeo_multifile_load(nc_wildcard, nc_dir=None):
    """
    Read data from multiple (e.g. hourly xgeo data) netcdf files
    :param nc_wildcard: common section of the filenams, e.g. mf_files*.nc
    :return:
    """
    if dir:
        nc_path = os.path.join(nc_dir, nc_wildcard)
    else:
        nc_path = nc_wildcard

    nco = Nco()
    nc_temp = nco.ncrcat(input=nc_path)
    nc = netCDF4.Dataset(nc_temp)

    #add function to restrict dates and times
    return nc


def _test_31jan2018_precip():
    nc_dir = r'Y:\metdata\met_obs_v2.0\rr1h\2018\01'
    nc_wildcard = r'rr1h_2018_01_31_?.nc'
    nc = xgeo_multifile_load(nc_wildcard, nc_dir)

    print(nc)


if __name__ == "__main__":
    _test_31jan2018_precip()