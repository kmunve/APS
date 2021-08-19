# coding: utf-8

# TODO: The resulting CSV file can be ploted using ../plotting/new_snow_line_plot.py

# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('seaborn-notebook')
import matplotlib.patches as patches
plt.rcParams['figure.figsize'] = (14, 6)

import datetime as dt
import numpy as np
import netCDF4
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

import csv
from pathlib import Path

from aps.load_region import load_region, clip_region
from aps.analysis import describe

# check versions (overkill, but why not?)
print('Numpy version: ', np.__version__)
print('Matplotlib version: ', matplotlib.__version__)
print('Today: ', dt.date.today())

# Select region and date
region_id = 3007
date_range = pd.date_range(start="2020-12-01",end="2021-01-30")

# Load region mask - only for data on 1km xgeo-grid
region_mask, y_min, y_max, x_min, x_max = load_region(region_id)

# Set path
nc_dir = Path(r"\\DM-CIFS-01\grid5\metdata\prognosis\meps\det\archive")
tmp_folder = Path(r'./tmp')
csv_file = tmp_folder / "new_snow_line_{0}_{1}.csv".format(region_id, date_range[0].strftime("%Y%m%d"))
new_snow_line = {"Date": [], "Hour": [], "Altitude": []}

for d in date_range:
    # Use the 6 o'clock file
    nc_date = dt.datetime(year=d.year, month=d.month, day=d.day, hour=6)
    nc_datestring = nc_date.strftime("%Y%m%dT%HZ")
    nc_file = "meps_det_1km_{0}.nc".format(nc_datestring)
    nc_path = nc_dir / str(nc_date.year) / nc_file

    # Load data
    try:
        nc_data = netCDF4.Dataset(nc_path, "r")
        # Choose a time-step
        t_index = 18
    except FileNotFoundError:
        # if 6 o'clock is not available try the 9 o'clock
        nc_date = dt.datetime(year=d.year, month=d.month, day=d.day, hour=9)
        nc_datestring = nc_date.strftime("%Y%m%dT%HZ")
        nc_file = "meps_det_1km_{0}.nc".format(nc_datestring)
        nc_path = nc_dir / str(nc_date.year) / nc_file
        nc_data = netCDF4.Dataset(nc_path, "r")
        # Choose a time-step
        t_index = 15
        print("Using 9 o'clock run.")
    except:
        print("No data available for {0}".format(nc_date))

    time_v = nc_data.variables['time']
    # Choose a pressure level (if applicable)
    p_index = 12 # 12=1000hPa, 11=925hPa, 10=850hPa, ..., 7=500hPa, ..., 0=50hPa in arome_metcoop_test

    x_dim = nc_data.dimensions['x'].size
    y_dim = nc_data.dimensions['y'].size

    ts = netCDF4.num2date(time_v[t_index], time_v.units)
    print("\n", ts)

    # precip
    precip_clip = region_mask * np.flipud(
        nc_data.variables['precipitation_amount_acc'][t_index, (y_dim - y_max):(y_dim - y_min), x_min:x_max])
    print(describe(precip_clip))

    #
    wetb_clip = region_mask * np.flipud(nc_data.variables['altitude_of_isoTprimW_equal_0'][t_index, (y_dim-y_max):(y_dim-y_min), x_min:x_max])
    print(describe(wetb_clip))

    plt.imshow(wetb_clip, vmin=-500, vmax=2500)
    plt.colorbar()
    plt.title(ts)
    plt.tight_layout()
    plt.savefig(tmp_folder / "wet_bulb_alt_{0}_{1}.png".format(region_id, nc_datestring))
    plt.clf()

    for k, f in enumerate(range(t_index, t_index+24, 6), start=1):
        t = []
        sl = []
        for i, d in enumerate(range(f, f + 6), start=1):
            wetb_clip = region_mask * np.flipud(
                nc_data.variables['altitude_of_isoTprimW_equal_0'][d, (y_dim - y_max):(y_dim - y_min), x_min:x_max])
            _t = netCDF4.num2date(time_v[d], time_v.units)
            _sl = np.nanmedian(wetb_clip)
            #         print("\t", i, f, d, _t, _sl, np.nanmean(wetb_clip))
            t.append(_t)
            sl.append(_sl)

        sl = np.array(sl)
        print(_t, np.mean(sl), np.max(sl))
        _i = np.argmax(sl)

        new_snow_line["Date"].append(t[_i].strftime("%Y-%m-%d"))
        new_snow_line["Hour"].append(t[_i].hour)
        new_snow_line["Altitude"].append(sl[_i])

df = pd.DataFrame(new_snow_line)
df.to_csv(csv_file, sep=";", index=False)
#
# hour_range = [0, 24]
# date_str = '20190405T00Z'
# var_wet = 'altitude_of_isoTprimW_equal_0'
# var_dry = 'altitude_of_0_degree_isotherm'
# var_rr = 'precipitation_amount'
#
# met_folder = Path(r'\\nve.no\fil\grid\metdata\prognosis\meps\det\archive\2019')
#
# nc_file1 = met_folder / 'meps_det_extracted_1km_{0}.nc'.format(date_str)
# times, altitude, land_area_fraction, nc_vars = ga.nc_load(nc_file1, [var_dry, var_wet], time_period=hour_range)
#
# print("{2} hours: from {0} to {1}".format(times[0], times[-1], len(times)))
#
# # ## Calculating the freezing level
# #
# # We use the parameters "altitude_of_0_degree_isotherm" and "altitude_of_isoTprimW_equal_0" from [MEPS_extracted](http://thredds.met.no/thredds/catalog/meps25files/catalog.html).
# # Under dry conditions we use altitude_of_0_degree_isotherm and for timing we use the period with the highest values. With precipitation we use altitude_of_isoTprimW_equal_0 and the period with the highest amount of precipitation.
# #
# # - split data into four chunks: 0-6, 6-12, 12-18, 18-24
# # - compress time dimension to 1 by keeping only the maximum value in each cell for each chunk
# # - calculate the 90-percentile for all max-values within a region
# # - round 90-percentile for each region to the next 50 m
#
# def get_periods_with_precip():
#     """
#     Check which parts of the day exceed a precipitation of 2 mm / 6h.
#     :return: a list containing one or more of the periods [0-6, 6-12, 12-18, 18-24]
#     """
#     pass
#
#
# precip_high = True
#
# if precip_high:
#     var_nsl = var_wet
#     calc_period = get_periods_with_precip()  # choose between 0-6, 6-12, 12-18, 18-24
# else:
#     var_nsl = var_dry
#
# # ### Compress time dimension
#
# nsl_max_00_06 = np.amax(nc_vars[var_nsl][0:6,:,:], axis=0)
# nsl_max_06_12 = np.amax(nc_vars[var_nsl][6:12,:,:], axis=0)
# nsl_max_12_18 = np.amax(nc_vars[var_nsl][12:18,:,:], axis=0)
# nsl_max_18_24 = np.amax(nc_vars[var_nsl][18:24,:,:], axis=0)
# nsl_max = np.amax(nc_vars[var_nsl][0:24,:,:], axis=0)
#
# nsl_list = [nsl_max_00_06, nsl_max_06_12, nsl_max_12_18,nsl_max_18_24, nsl_max]
# # ### Extract regions
#
# # Load region mask - only for data on 1km xgeo-grid
#
# region_mask, y_min, y_max, x_min, x_max = load_region(region_id)
# print(y_max-y_min, x_max-x_min)
#
# print(np.unique(region_mask))
# plt.imshow(region_mask)
# plt.savefig(tmp_folder / 'region_mask_nsl.png')
# plt.clf()
#
# # ### Clip to region
#
# ## TODO: Do this for each 6h-period and make distplots.
# t_index = 0
# nsl_region = clip_region(np.flipud(nsl_max), region_mask, t_index, y_min, y_max, x_min, x_max)
# print(np.count_nonzero(np.isnan(nsl_region)))
# print(np.unique(nsl_region))
# plt.imshow(nsl_region)
# plt.colorbar()
# plt.savefig(tmp_folder / 'nsl_region.png')
# plt.clf()
#
# nsl_region_mean = np.nanmean(nsl_region.flatten())
# print("Mean\t: ", nsl_region_mean)
# for p in [0, 5, 25, 50, 75, 80, 85, 90, 95, 100]:
#     print(p, "\t: ", np.nanpercentile(nsl_region.flatten(), p))
#
# nsl_region_flat = nsl_region[~np.isnan(nsl_region)].data.flatten()
# sns.distplot(nsl_region_flat)
# plt.savefig(tmp_folder / 'nsl_dist.png')
# plt.clf()
#
# # ## Determine cells with precipitation
#
# nc_file2 = r"\\hdata\grid\metdata\prognosis\meps\det\archive\2019\meps_det_pp_1km_{0}.nc".format(date_str)
# times, altitude, land_area_fraction, nc_vars2 = ga.nc_load(nc_file2, [var_rr], time_period=hour_range)
#
# precip_sum = np.sum(nc_vars2[var_rr][0:24, :, :], axis=0)
#
# t_index = 0
# precip_sum_region = clip_region(np.flipud(precip_sum), region_mask, t_index, y_min, y_max, x_min, x_max)
#
# print(np.count_nonzero(np.isnan(precip_sum_region)))
# print(np.unique(precip_sum_region))
# plt.imshow(precip_sum_region)
# plt.colorbar()
# plt.savefig(tmp_folder / 'precip_sum_region.png')
# plt.clf()
#
# # Mask where the precipitation during the day exceeds a given value.
# psr_mask = np.where(precip_sum_region > 1., 1, np.nan)
#
# plt.imshow(psr_mask)
# plt.savefig(tmp_folder / 'psr_mask.png')
# plt.clf()
#
# nsl_region_wet = nsl_region * psr_mask
# nsl_region_wet_mean = np.nanmean(nsl_region_wet.flatten())
# print("Mean\t: ", nsl_region_wet_mean)
# for p in [0, 5, 25, 50, 75, 80, 85, 90, 95, 100]:
#     print(p, "\t: ", np.nanpercentile(nsl_region_wet.flatten(), p))
#
# nsl_region_wet_flat = nsl_region_wet[~np.isnan(nsl_region_wet)].data.flatten()
# sns.distplot(nsl_region_wet_flat)
# plt.savefig(tmp_folder / 'nsl_wet_dist.png')
# plt.clf()
#
# print('####################\n# Mean (all): {0:.2} #\n# Mean (wet): {0:.2} #\n####################'.format(fl_region_mean, fl_region_wet_mean))