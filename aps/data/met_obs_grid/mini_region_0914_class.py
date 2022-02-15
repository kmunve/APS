"""
Example on how to extract data from a miniregion at given elevations
"""
import matplotlib.pyplot as plt
import datetime as dt
from aps.aps_io.warning_region import MiniRegion, SeNorgeSubDomain

# Set-up for region 0914
ix = (195, 215)  # index along x-axis
iy = (285, 305)  # index along y-axis
day = dt.datetime(year=2022, month=1, day=16).date()


r0914 = MiniRegion(ix, iy, date=day, nwp_hour=6)
print("Mean: ", r0914.mean_elevation)

# r0914_1500 = r0914.elevations*r0914.elevation_masks["below_1500"]
# plt.imshow(r0914_1500)
# plt.show()

r0914_sd = SeNorgeSubDomain(9, 14)
print(r0914_sd)

pos = 'end'

