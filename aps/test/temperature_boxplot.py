from numpy import ma
from aps.aps_io.get_arome import nc_load
import matplotlib.pyplot as plt

"""
DEPRECATED see notebooks/regional_temperature_distribution
"""


jd, altitude, land_area_fraction, nc_vars = nc_load('http://thredds.met.no/thredds/dodsC/arome25/arome_metcoop_default2_5km_latest.nc',
                                                    ['air_temperature_2m'], [59.9, 60.0, 8.5, 9.0], [6, 30])

# create land mask
land_mask = ma.masked_less_equal(land_area_fraction, 0.0).mask

# create elevation masks
below500 = ma.masked_less_equal(altitude, 500.0).mask * land_mask

temp = ma.masked_array(nc_vars['air_temperature_2m'][6, :, :], below500)
plt.imshow(temp)
plt.show() # - doesn't look like it is the right place, but at least it works technically

# calc daily average


a = 0