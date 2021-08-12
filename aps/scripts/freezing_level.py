# coding: utf-8

# TODO: should negative values of freezing level be clipped to zero? How will this effect the mean or percentiles?

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
sns.set(style="dark")
import aps.aps_io.get_arome as ga
from aps.load_region import load_region, clip_region
from aps.util.make_gif import make_gif
from pathlib import Path

region_id = 3028

hour_range = [0, 24]
date_str = '20210313T18'
var_wet = 'altitude_of_isoTprimW_equal_0'
var_dry = 'altitude_of_0_degree_isotherm'
var_rr = 'precipitation_amount'
tmp_folder = Path(r'.\tmp')
met_folder = Path(r'\\nve.no\fil\grid\metdata\prognosis\meps\det\archive\2021')

nc_file1 = met_folder / 'meps_det_1km_{0}Z.nc'.format(date_str)
times, altitude, land_area_fraction, nc_vars = ga.nc_load(nc_file1, [var_dry, var_wet], time_period=hour_range)

print("{2} hours: from {0} to {1}".format(times[0], times[-1], len(times)))

# ## Calculating the freezing level
#
# We use the parameters "altitude_of_0_degree_isotherm" and "altitude_of_isoTprimW_equal_0" from [MEPS_extracted](http://thredds.met.no/thredds/catalog/meps25files/catalog.html).
# Under dry conditions we use altitude_of_0_degree_isotherm and for timing we use the period with the highest values. With precipitation we use altitude_of_isoTprimW_equal_0 and the period with the highest amount of precipitation.
#
# - split data into four chunks: 0-6, 6-12, 12-18, 18-24
# - compress time dimension to 1 by keeping only the maximum value in each cell for each chunk
# - calculate the 90-percentile for all max-values within a region
# - round 90-percentile for each region to the next 50 m

def get_periods_with_precip():
    """
    Check which parts of the day exceed a precipitation of 2 mm / 6h.
    :return: a list containing one or more of the periods [0-6, 6-12, 12-18, 18-24]
    """
    pass


precip_high = False

if precip_high:
    var_fl = var_wet
    calc_period = get_periods_with_precip()  # choose between 0-6, 6-12, 12-18, 18-24
else:
    var_fl = var_dry

# ### Compress time dimension

fl_max_00_06 = np.amax(nc_vars[var_fl][0:6,:,:], axis=0)
fl_max_06_12 = np.amax(nc_vars[var_fl][6:12,:,:], axis=0)
fl_max_12_18 = np.amax(nc_vars[var_fl][12:18,:,:], axis=0)
fl_max_18_24 = np.amax(nc_vars[var_fl][18:24,:,:], axis=0)
fl_max = np.amax(nc_vars[var_fl][0:24,:,:], axis=0)

plt.imshow(fl_max)
plt.savefig(tmp_folder / 'fl_max.png')
plt.clf()

# ### Extract regions

# Load region mask - only for data on 1km xgeo-grid

region_mask, y_min, y_max, x_min, x_max = load_region(region_id)
print(y_max-y_min, x_max-x_min)

print(np.unique(region_mask))
plt.imshow(region_mask)
plt.savefig(tmp_folder / 'region_mask.png')
plt.clf()

png_files = []
for t in range(len(times)):
    t2 = t+hour_range[0]
    t_str = times[t]
    _fl = clip_region(np.flipud(nc_vars[var_fl][t, :, :]), region_mask, t2, y_min, y_max, x_min, x_max)
    plt.imshow(_fl, vmin=0, vmax=500, cmap='magma')
    plt.axis('off')
    plt.text(5, 5, "{0}: {1}".format(region_id, t_str), bbox=dict(facecolor='white', edgecolor='white', alpha=1.0))
    cbar = plt.colorbar()
    cbar.ax.set_ylabel(var_fl)
    _png = tmp_folder / 'fl_{1:02}.png'.format(region_id, t)
    png_files.append(_png)
    plt.savefig(_png, bbox_inches='tight')
    plt.clf()

# Use _make_gif.py_ in folder _img_ to generate a gif animation.
make_gif(png_files, tmp_folder / 'fl.gif')

# ### Clip to region
t_index = 0
fl_region = clip_region(np.flipud(fl_max), region_mask, t_index, y_min, y_max, x_min, x_max)
print(np.count_nonzero(np.isnan(fl_region)))
print(np.unique(fl_region))
plt.imshow(fl_region)
plt.colorbar()
plt.savefig(tmp_folder / 'fl_region.png')
plt.clf()

fl_region_mean = np.nanmean(fl_region.flatten())
print("Mean\t: ", fl_region_mean)
for p in [0, 5, 25, 50, 75, 80, 85, 90, 95, 100]:
    print(p, "\t: ", np.nanpercentile(fl_region.flatten(), p))

# fl_region_flat = fl_region[~np.isnan(fl_region)].data.flatten()
# sns.distplot(fl_region_flat)
# plt.savefig(tmp_folder / 'fl_dist.png')
# plt.clf()

# ## Calculating freezing level with regard to precipitation

nc_file2 = r"Y:\metdata\prognosis\met_pp_nordic\forecast\archive\2021\met_forecast_1_0km_nordic_{0}Z.nc".format(date_str)
times, altitude, land_area_fraction, nc_vars2 = ga.nc_load(nc_file2, [var_rr], time_period=hour_range)

precip_sum = np.sum(nc_vars2['precipitation_amount'][0:24, :, :], axis=0)

t_index = 0
precip_sum_region = clip_region(np.flipud(precip_sum), region_mask, t_index, y_min, y_max, x_min, x_max)

print(np.count_nonzero(np.isnan(precip_sum_region)))
print(np.unique(precip_sum_region))
plt.imshow(precip_sum_region)
plt.colorbar()
plt.savefig(tmp_folder / 'precip_sum region.png')
plt.clf()

# Mask where the precipitation during the day exceeds a given value.
psr_mask = np.where(precip_sum_region > 5., 1, np.nan)

plt.imshow(psr_mask)
plt.savefig(tmp_folder / 'psr_mask.png')
plt.clf()

fl_region_wet = fl_region * psr_mask
fl_region_wet_mean = np.nanmean(fl_region_wet.flatten())
print("Mean\t: ", fl_region_wet_mean)
for p in [0, 5, 25, 50, 75, 80, 85, 90, 95, 100]:
    print(p, "\t: ", np.nanpercentile(fl_region_wet.flatten(), p))

fl_region_wet_flat = fl_region_wet[~np.isnan(fl_region_wet)].data.flatten()
sns.distplot(fl_region_wet_flat)
plt.savefig(tmp_folder / 'fl_wet_dist.png')
plt.clf()

png_files = []
for t in range(len(times)):
    t2 = t+hour_range[0]
    t_str = times[t]
    _rr = clip_region(np.flipud(nc_vars2[var_rr][t, :, :]), region_mask, t2, y_min, y_max, x_min, x_max)
    plt.imshow(_rr, vmin=0, vmax=3, cmap='magma')
    plt.axis('off')
    plt.text(5, 5, "{0}: {1}".format(region_id, t_str), bbox=dict(facecolor='white', edgecolor='white', alpha=1.0))
    cbar = plt.colorbar()
    cbar.ax.set_ylabel(var_rr)
    _png = tmp_folder / 'rr_{1:02}.png'.format(region_id, t)
    png_files.append(_png)
    plt.savefig(_png, bbox_inches='tight')
    plt.clf()

make_gif(png_files, tmp_folder / 'rr.gif')

print('####################\n# Mean (all): {0:.2} #\n# Mean (wet): {0:.2} #\n####################'.format(fl_region_mean, fl_region_wet_mean))