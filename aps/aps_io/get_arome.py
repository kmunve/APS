#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import netCDF4

__author__ = 'kmu'
"""
Retrieve data from netcdf files from thredds.met.no and do some statistics.
"""


def _nc_info(nc_data):
    print('### DIMENSIONS ###')
    print(nc_data.dimensions)
    for k in nc_data.dimensions.keys():
        print("-\t{0}".format(k))

    print('### VARIABLES ###')
    for k in nc_data.variables.keys():
        print("-\t{0}".format(k))


def nc_load(nc_object, vars, bounding_box=None, time_period=None):
    """

    Dimensions for the nc-files on thredds are y, x or time, y, x.

    :param nc_object: filename or URL of netCDF file, e.g. './Data/arome_metcoop_default2_5km_latest.nc' or 'http://thredds.met.no/thredds/dodsC/arome25/arome_metcoop_default2_5km_latest.nc'
    :param vars: list of variables that should be retrieved, e.g. []
    :param bounding_box: list of lat lons [S, N, E, W] to define a rectangular shape to be clipped out
    :param time_period: list of start and end time, e.g. []
    :return:
    """

    # Access netcdf file via OpenDAP
    nc = netCDF4.Dataset(nc_object)

    # Get content
    _nc_info(nc)

    # Get coordinates and other standard variables
    try:
        x_var = nc.variables['x']
        y_var = nc.variables['y']
    except KeyError:
        print("Variables 'x' and 'y' are not provided.")
    latitude_var = nc.variables['latitude']
    longitude_var = nc.variables['longitude']
    time_var = nc.variables['time']
    altitude_var = nc.variables['altitude']
    try:
        land_area_fraction_var = nc.variables['land_area_fraction']
    except KeyError:
        print("Variable 'land_area_fraction' is not provided.")

    nc_vars = {}

    # Apply bounding box if given
    if bounding_box is not None:
        lat1 = np.where(latitude_var[:] >= bounding_box[0])[1][0]
        lat2 = np.where(latitude_var[:] <= bounding_box[1])[1][-1]
        lon1 = np.where(longitude_var[:] >= bounding_box[2])[1][0]
        lon2 = np.where(longitude_var[:] <= bounding_box[3])[1][-1]

        print(lon1, lon2, lat1, lat2)

        altitude = altitude_var[lon1:lon2, lat1:lat2] # retrieve model topography
        try:
            land_area_fraction = land_area_fraction_var[lon1:lon2, lat1:lat2]
        except UnboundLocalError:
            land_area_fraction = None

        for var in vars:
            nc_vars[var] = nc.variables[var][:].squeeze()[time_period[0]:time_period[1], lon1:lon2, lat1:lat2]

    else:
        altitude = altitude_var[:, :]
        try:
            land_area_fraction = land_area_fraction_var[lon1:lon2, lat1:lat2]
        except UnboundLocalError:
            land_area_fraction = None
        for var in vars:
            nc_vars[var] = nc.variables[var][:].squeeze()[time_period[0]:time_period[1], :, :]

    times = time_var[time_period[0]:time_period[1]]
    jd = netCDF4.num2date(times[:], time_var.units)




    return jd, altitude, land_area_fraction, nc_vars


