import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as manimation
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from netCDF4 import Dataset, num2date


# TODO: check if this works - http://tech.weatherforce.org/blog/ecmwf-data-animation/index.html

nc_url = "https://thredds.met.no/thredds/dodsC/radarnowcasting/yrwms-nordic.mos.pcappi-0-rr.noclass-clfilter-novpr-clcorr-block.nordiclcc-1000.20221016T134500Z.nc"

nc = Dataset(nc_url)

time_v = nc.variables['time']

# Choose a time-step
t_index = 0

ts_start = num2date(time_v[0], time_v.units)
ts_stop = num2date(time_v[-1], time_v.units)

lat_v = nc.variables['lat']
lon_v = nc.variables['lon']
precip_rate_var = nc.variables['lwe_precipitation_rate']

lat = lat_v[:]
lon = lon_v[:]
precip_rate = precip_rate_var[:]  # can also get a sub-set e.g. [:, 200:1000, 100:500]
#precip_rate = precip_rate_var[:, 800:1400, 600:1400]

# Set values below a threshold to NaN so the plot shows only data where there is significant precip.
precip_rate[precip_rate < 0.2] = np.NaN

# Define the meta data for the movie
metadata = dict(title='Radar animation', artist='Matplotlib',
                comment='Nedbør radar over Norge')
writer = manimation.PillowWriter(fps=5, metadata=metadata)

# Initialize the movie
plot_aspect = 0.8
plot_height = 12.0
plot_width = int(plot_height*plot_aspect)

# ----------------------------- #

fig = plt.figure(figsize=(plot_width, plot_height), dpi=100)
# plt.subplots_adjust(left=0.10, right=1.00, top=0.90, bottom=0.06, hspace=0.30)
# subplot1 = plt.subplot(111)

# ----------------------------- #
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax.set_extent([2, 30, 56, 75])
# ax = plt.axes(projection=ccrs.PlateCarree())
ax.add_feature(cfeature.COASTLINE)

# fig = plt.gcf()
# fig = plt.figure()

cbar_max = 10.0
cbar_min = 0.0
cbar_step = 1.0
cbar_num_colors = 6
cbar_num_format = "%d"

precip_layer = ax.contourf(lon, lat, precip_rate[0, :, :], levels=[1, 2, 3, 4, 5], transform=ccrs.PlateCarree())
cbar = plt.colorbar(precip_layer, orientation='horizontal', ticks=np.arange(cbar_min, cbar_max + cbar_step, cbar_step),
                       format=cbar_num_format)
cbar.ax.set_xlabel('Intensitet [mm/t]', fontsize=16, weight="bold")
for coll in precip_layer.collections:
    coll.remove()

with writer.saving(fig, "precip_radar.gif", 100):
    for i in range(24):
        plot_title = num2date(time_v[i], time_v.units).strftime("%Y-%m-%d %H:%M")
        # precip_layer = plt.imshow(precip_rate[i, :, :], vmin=0, vmax=5)
        precip_layer = ax.contourf(lon, lat, precip_rate[i, :, :], levels=[1, 2, 3, 4, 5])#, transform=ccrs.PlateCarree())
        plt.title(plot_title)
        writer.grab_frame()
        for coll in precip_layer.collections:
            coll.remove()  # clear the previous precipitation layer (with contourf this is a collection)

plt.close(fig)

