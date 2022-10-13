import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from netCDF4 import Dataset, num2date


#ax = plt.axes(projection=ccrs.PlateCarree())
# ax = plt.axes(projection=ccrs.LambertConformal(central_longitude=15.0, central_latitude=63.0, false_easting=0.0, false_northing=0.0, standard_parallels=(63, 63), globe=None, cutoff=-30))
#
# ax.set_extent([2, 28, 56, 72])
# ax.coastlines(resolution='110m')
# ax.add_feature(cfeature.BORDERS.with_scale('50m'))

nc_url = "https://thredds.met.no/thredds/dodsC/radarnowcasting/yrwms-nordic.mos.pcappi-0-rr.noclass-clfilter-novpr-clcorr-block.nordiclcc-1000.20221006T134500Z.nc"

nc = Dataset(nc_url)

time_v = nc.variables['time']

# Choose a time-step
t_index = 0

ts_start = num2date(time_v[0], time_v.units)
ts_stop = num2date(time_v[-1], time_v.units)

lat_v = nc.variables['lat']
lon_v = nc.variables['lon']
precip_rate_v = nc.variables['lwe_precipitation_rate']


lat = lat_v[:]
lon = lon_v[:]
precip = precip_rate_v[15, :, :]
#mm = ax.pcolormesh(lon, lat, precip, vmin=0, vmax=5, transform=ccrs.LambertConformal())


ax = plt.axes(projection=ccrs.PlateCarree())

plt.contourf(lon, lat, precip, 60, transform=ccrs.PlateCarree())

ax.coastlines()

# ax.stock_img()
# Save the plot by calling plt.savefig() BEFORE plt.show()
plt.savefig('coastlines.png')
