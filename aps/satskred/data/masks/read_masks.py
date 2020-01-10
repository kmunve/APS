import gdal
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

# import folium
# from folium import plugins


# filepath = r"S1C_IWH_aggregated_mask_087_mask.tif"
filepath = r"S1C_IWH_aggregated_mask_066_mask.tif"

# Open the file:
raster = gdal.Open(filepath)

# Check type of the variable 'raster'
print(type(raster))

# Projection
print(raster.GetProjection())

# Dimensions
print(raster.RasterXSize)
print(raster.RasterYSize)

# Number of bands
print(raster.RasterCount)

# Metadata for the raster dataset
print(raster.GetMetadata())

# Get coordinates, cols and rows
geotransform = raster.GetGeoTransform()
cols = raster.RasterXSize
rows = raster.RasterYSize

# Get extent
xmin = geotransform[0]
ymax = geotransform[3]
xmax = xmin + cols * geotransform[1]
ymin = ymax + rows * geotransform[5]

# Get Central point
centerx = (xmin + xmax) / 2
centery = (ymin + ymax) / 2

# Raster convert to array in numpy
bands = raster.RasterCount
band = raster.GetRasterBand(1)
dataset = band.ReadAsArray(0, 0, cols, rows)
dataimage = dataset
dataimage[dataimage[:, :] == 128] = 1
dataimage[dataimage[:, :] == 200] = 1

print(np.unique(dataimage, return_index=False, return_inverse=False, return_counts=True, axis=None))

# plt.imshow(dataimage, cmap=cm.hot)
plt.imshow(dataimage, cmap=cm.get_cmap('hot', 2))
# plt.title()
plt.colorbar(ticks=[0, 1], orientation='horizontal', label="0: visible; 1:not visible")
#plt.hist(dataimage)
plt.show()
"""
# Visualization in folium - https://github.com/GISerDaiShaoqing/My-Studies-of-Urban-GIS/blob/master/3.Spatial%20visualization%20demo%20in%20folium(for%20Python)/src/foliumrastervisdemo.py
map = folium.Map(location=[centery, centerx], zoom_start=7, tiles='Stamen Terrain')
plugins.ImageOverlay(
    image=dataimage,
    bounds=[[ymin, xmin], [ymax, xmax]],
    colormap=lambda x: (1, 0, x, x),  # R,G,B,alpha
).add_to(map)

# Save html
map.save('mask.html')

"""
