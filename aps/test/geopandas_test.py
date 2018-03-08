import geopandas as gpd
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster, ImageOverlay

print(folium.__version__)

def get_aval_data():
    aval = gpd.read_file(r'D:\Dev\APS\aps\data\satskred\S1_Tromsoe_20180116_052732\S1_Tromsoe_20180116_052732.shp')

    # print(aval.head(5))
    # for a in aval:
    #     print(a)#, a['AREA m2'], a.area)

    # I think it is in UTM 33N
    aval.crs = {'init': 'EPSG:32633'}
    # print(aval.crs)

    #aval.plot()
    #plt.show()
    return aval


def show_on_map(gdf):

    gdf_wgs84 = gdf.to_crs({'init': 'epsg:4326'})

    #
    lat, lon, zs = 69.6, 19.4, 13#9
    m = folium.Map(location=[lat, lon], zoom_start=zs, tiles="OpenStreetMap")

    topo4 = folium.features.WmsTileLayer(url="http://openwms.statkart.no/skwms1/wms.topo4?",
                                         layers="topo4_WMS", transparent=True, fmt="image/jpeg",
                                         name="Topo4")
    topo4.add_to(m)

    faresoner = folium.features.WmsTileLayer(url="https://gis3.nve.no/map/services/SkredSnoAktR/MapServer/WmsServer?",
                                         layers="Utlopsomrade", transparent=True, fmt="image/png",
                                         name="Avalanche run-out sone")
    faresoner.add_to(m)

    """
    Can request WMS data as geojson
    e.g.
    https://gis3.nve.no/map/rest/services/SkredSnoAktR/MapServer/2/query?where=1%3D1&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=*&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&resultOffset=&resultRecordCount=&queryByDistance=&returnExtentsOnly=false&datumTransformation=&parameterValues=&rangeValues=&f=geojson
    
    """


    kwargs = {"attribution": "NVE", "minZoom": "10"}
    # seems like a bug in folium prohibits that these parameters
    # are passed on to leaflet - can be set manually in the .html file

    bratthet = folium.features.WmsTileLayer(url="https://gis3.nve.no/map/services/Bratthet/MapServer/WmsServer?",
                                            layers="Bratthet_snoskred", transparent=True,
                                            fmt="image/png", name='Bratthet',
                                            **kwargs)
    bratthet.add_to(m)

    skredlop = folium.features.WmsTileLayer(url="https://www.vegvesen.no/kart/ogc/geodata_1_0/ows?",
                                            layers="Skredlop", transparent=True, fmt="image/png", name='SVV Skredløp')
    skredlop.add_to(m)

    #varslingsregioner = ImageOverlay(image='http://gis3.nve.no/map/rest/services/Mapservices/XgeoStatic/MapServer/export?dpi=96&transparent=true&format=png8&layers=show%3A25%2C26%2C29&bbox=-635878.2758445519%2C6520140.001693336%2C1616936.8964524597%2C7851779.998306664&bboxSR=32633&imageSR=32633&size=1663%2C983&f=image',
     #                                bounds=[[lat_min, lon_min], [lat_max, lon_max]])

    mc = MarkerCluster(name='Avalanches 2018-01-16').add_to(m)
    # for a in gdf_wgs84.geometry[:]:
    #     folium.Marker(location=[a.centroid.y, a.centroid.x]).add_to(mc)

    for a in gdf_wgs84.itertuples():
        # print(a, type(a))
        folium.Marker(location=[a.geometry.centroid.y, a.geometry.centroid.x],
                      popup='Størrelse: {area}<br>Lengde: {length}<br>Bredde: {width}'.format(area=a._11, length=a.LENGTH, width=a.WIDTH)).add_to(mc)

    folium.GeoJson(gdf, name='Avalanches shapes 2018-01-16').add_to(m)

    # add layer control functionality to map
    folium.LayerControl().add_to(m)
    # # add lat/lon pop-up funcionality
    # folium.LatLngPopup().add_to(m)
    # # add measure functionality
    # plugins.MeasureControl().add_to(m)
    # # add drawing functionality
    # #folium.plugins.Draw().add_to(m)

    m.save('aval_activity.html')


def compare_subregions():
    pass
    # create choropleth maps like in https://blog.dominodatalab.com/creating-interactive-crime-maps-with-folium/

if __name__ == '__main__':
    gdf = get_aval_data()
    show_on_map(gdf)
