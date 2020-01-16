from osgeo import gdal
from osgeo import osr
# import gdal
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm


def array2raster(newRasterfn, dataset, array, dtype):
    """
    Function from https://gist.github.com/jkatagi/a1207eee32463efd06fb57676dcf86c8
    Save GeoTiff file from numpy.array
    input:
        newRasterfn: save file name
        dataset : original tif file
        array : numpy.array
        dtype: Byte or Float32.
    """
    cols = array.shape[1]
    rows = array.shape[0]
    originX, pixelWidth, b, originY, d, pixelHeight = dataset.GetGeoTransform()

    driver = gdal.GetDriverByName('GTiff')

    # set data type to save.
    GDT_dtype = gdal.GDT_Unknown
    if dtype == "Byte":
        GDT_dtype = gdal.GDT_Byte
    elif dtype == "Float32":
        GDT_dtype = gdal.GDT_Float32
    else:
        print("Not supported data type.")

    # set number of band.
    if array.ndim == 2:
        band_num = 1
    else:
        band_num = array.shape[2]

    outRaster = driver.Create(newRasterfn, cols, rows, band_num, GDT_dtype)
    outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))

    # Loop over all bands.
    for b in range(band_num):
        outband = outRaster.GetRasterBand(b + 1)
        # Read in the band's data into the third dimension of our array
        if band_num == 1:
            outband.WriteArray(array)
        else:
            outband.WriteArray(array[:, :, b])

    # setteing srs from input tif file.
    prj = dataset.GetProjection()
    outRasterSRS = osr.SpatialReference(wkt=prj)
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    outband.FlushCache()


# import folium
# from folium import plugins


# filepath = r"S1C_IWH_aggregated_mask_087_mask.tif"
filepath = r"S1C_IWH_aggregated_mask_087_mask.tif"

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

# 0
dataimage = dataset
dataimage[dataimage[:, :] == 128] = 1
dataimage[dataimage[:, :] == 200] = 1

print(np.unique(dataimage, return_index=False, return_inverse=False, return_counts=True, axis=None))

# plt.imshow(dataimage, cmap=cm.hot)
plt.imshow(dataimage, cmap=cm.get_cmap('hot', 2))
# plt.title()
plt.colorbar(ticks=[0, 1], orientation='horizontal', label="0: visible; 1:not visible")
# plt.hist(dataimage)
plt.savefig(filepath[:-4] + '.jpg')

array2raster(filepath[:-4] + '_bin.tif', raster, dataimage, "Byte")

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
