"""
Simply opens an zipped shapefile - like the one SatSkred detection algorithm outputs - and prints a short summary.
Use debugger to explore the *gdf* variable.
"""

import geopandas as gpd

shpfile = r'zip://S:\SatSkred\output\toFMEImport/AvalDet_20200517_155917_ref_20200511_trno_160_VV.zip'
gdf = gpd.GeoDataFrame.from_file(shpfile)

print(gdf.head())
