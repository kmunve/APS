import geopandas as gpd


gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'

# Filepath to KML file
fp = "Sentinel-1A_MP_20200108T170000_20200131T190000.kml"

tracks = gpd.read_file(fp, driver='KML')

#Check the data
print("Number of rows:", len(tracks))
tracks.head(11)
