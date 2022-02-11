"""
Example on how to extract data from a miniregion at given elevations
"""
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

ncfile = r"Y:\metdata\config\xgeo_dem.nc"
xds = xr.open_dataset(ncfile)
print(xds)


# Set-up for region 0914
ix = (195, 214)  # index along x-axis
iy = (285, 304)  # index along y-axis

r0914 = xds["xgeo_dem_2"][285:305, 195:215]
print("Mean: ", np.mean(r0914))


def get_elevation_masks(elevations, intervals):
    # TODO: Make sure intervals are in ascending order
    elevation_masks = {"below_{i}".format(i=intervals[0]): np.where(elevations < intervals[0], 1, np.nan),
                       "above_{i}".format(i=intervals[0]): np.where(elevations < intervals[0], np.nan, 1)}
    for i in range(1, len(intervals)):
        # Now mask everything above the previous interval boundary and below the current interval boundary.
        curr = intervals[i]
        prev = intervals[i-1]
        elevation_masks["below_{i}".format(i=intervals[i])] = np.where(elevations*elevation_masks["above_{i}".format(i=intervals[i-1])] < intervals[i], 1, np.nan)
        elevation_masks["above_{i}".format(i=intervals[i])] = np.where(elevations < intervals[i], np.nan, 1)
        # elevation_masks["above_{i}".format(i=intervals[i])] = np.where(elevations*elevation_masks["above_{i}".format(i=intervals[i-1])] < intervals[i], np.nan, 1)
        b = 'point'

    return elevation_masks


elev_masks = get_elevation_masks(r0914, [300, 600, 900, 1200, 1500, 1800, 2100, 2400])

for key in elev_masks.keys():
    plt.figure()
    plt.imshow(elev_masks[key])
    plt.title(key)

r0914_300 = r0914*elev_masks["below_300"]
r_300 = (r0914_300.min(), r0914_300.max())
r0914_600 = r0914*elev_masks["below_600"]
r_600 = (r0914_600.min(), r0914_600.max())
r0914_900 = r0914*elev_masks["below_900"]
r_900 = (r0914_900.min(), r0914_900.max())
r0914_1200 = r0914*elev_masks["below_1200"]
r_1200 = (r0914_1200.min(), r0914_1200.max())
r0914_1500 = r0914*elev_masks["below_1500"]
r_1500 = (r0914_1500.min(), r0914_1500.max())

plt.imshow(r0914_900)
plt.figure()
plt.imshow(r0914_1200)
plt.show()
pos = 'end'

