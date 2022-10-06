import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as manimation
from netCDF4 import Dataset, num2date

nc_url = "https://thredds.met.no/thredds/dodsC/radarnowcasting/yrwms-nordic.mos.pcappi-0-rr.noclass-clfilter-novpr-clcorr-block.nordiclcc-1000.20221006T134500Z.nc"

nc = Dataset(nc_url)

time_v = nc.variables['time']

# Choose a time-step
t_index = 0

ts_start = num2date(time_v[0], time_v.units)
ts_stop = num2date(time_v[-1], time_v.units)

lat_v = nc.variables['lat']
lon_v = nc.variables['lon']
precip_rate_var = nc.variables['lwe_precipitation_rate']

precip_rate = precip_rate_var[:]  # can also get a sub-set e.g. [:, 200:1000, 100:500]
#precip_rate = precip_rate_var[:, 800:1400, 600:1400]

# Set values below a threshold to NaN so the plot shows only data where there is significant precip.
precip_rate[precip_rate < 0.2] = np.NaN

# plt.imshow(precip_rate[5, :, :], vmin=0, vmax=5)
# plt.savefig("radar_5.png")


# Define the meta data for the movie
metadata = dict(title='Radar animation', artist='Matplotlib',
                comment='Nedbør radar over Norge')
writer = manimation.PillowWriter(fps=5, metadata=metadata)

# Initialize the movie
fig = plt.figure()

with writer.saving(fig, "precip_radar.gif", 100):
    for i in range(24):
        plt.imshow(precip_rate[i, :, :], vmin=0, vmax=5)
        writer.grab_frame()
        plt.clf()

# n = 1000
# x = np.linspace(0, 6*np.pi, n)
# y = np.sin(x)
#
# # plot the sine wave line
# sine_line, = plt.plot(x, y, 'b')
# red_circle, = plt.plot([], [], 'ro', markersize = 10)
# plt.xlabel('x')
# plt.ylabel('sin(x)')
#
# # Update the frames for the movie
# with writer.saving(fig, "sine_animation.gif", 100):
#     for i in range(n):
#         x0 = x[i]
#         y0 = y[i]
#         red_circle.set_data(x0, y0)
#         writer.grab_frame()

a = 1
