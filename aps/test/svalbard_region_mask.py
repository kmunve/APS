import netCDF4
import numpy as np
import matplotlib.pyplot as plt

import georaster as gr




# data_nc = netCDF4.Dataset(r'Y:\tmp\kmu\meps\arome_arctic_pp_1km_latest.nc')
# la = data_nc.variables['land_area_fraction'][:]
#
# mask_nc = netCDF4.Dataset(r'N:\Prosjekter\APS\VarslinOmr2018Svalbard2.nc')
#
# m = mask_nc.variables['VarslingsOmr2018Land'][:]
#
# mask3003 = np.ma.masked_not_equal(m, 3003)
#
# la3003 = np.where(m==3003, 2, np.flipud(la))
# m3003 = np.where(m==3003, np.flipud(la), m)


# plt.imshow(m3003, vmin=3000, vmax= 3005)
# plt.show()


raster = r'N:\Prosjekter\APS\svalbard_regions\VarslingsOmr2018Land.tif'
rdata = gr.SingleBandRaster(raster)
#(xmin, xsize, x, ymax, y, ysize) = data.geot

#print(rdata.projection)
print(rdata.extent, type(rdata.srs))


print(rdata.srs)
plt.imshow(rdata.r, vmin=3000, vmax=3005)
plt.show()

### ...export to netCDF