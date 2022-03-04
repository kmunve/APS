"""
Example on how to extract data from a miniregion at given elevations
"""
import matplotlib.pyplot as plt
import datetime as dt
from aps.aps_io.warning_region import MiniRegion, SeNorgeSubDomain

# Set-up for region 0914
ix = (195, 215)  # index along x-axis
iy = (285, 305)  # index along y-axis
day = dt.datetime(year=2022, month=2, day=22).date()


r0914 = MiniRegion(ix, iy, date=day, nwp_hour=0)
print("Mean: ", r0914.mean_elevation)

r0914.get_meteorology_3h()
r0914.get_meteorology_24h()
# plt.step(r0914.nc_time, r0914.precip_acc[1:, 10, 10])
plt.step(r0914.nc_time, r0914.precip_hour[:, 10, 10])
# plt.step(r0914.nc_time, r0914.precip_3h[:, 10, 10])
# r0914_1500 = r0914.elevations*r0914.elevation_masks["below_1500"]
# plt.imshow(r0914_1500)
plt.show()

# r0914.to_json()
#
# r0914_sd = SeNorgeSubDomain(9, 14)
# print(r0914_sd)

pos = 'end'

