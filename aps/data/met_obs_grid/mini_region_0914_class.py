"""
Example on how to extract data from a miniregion at given elevations
"""
import matplotlib.pyplot as plt
from aps.aps_io.warning_region import MiniRegion

# Set-up for region 0914
ix = (195, 215)  # index along x-axis
iy = (285, 305)  # index along y-axis

r0914 = MiniRegion(ix, iy)
print("Mean: ", r0914.mean_elevation)

r0914_900 = r0914.elevations*r0914.elevation_masks["below_900"]
# plt.imshow(r0914_900)
# plt.show()

pos = 'end'

