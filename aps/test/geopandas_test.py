import geopandas as gpd
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster


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
    print(gdf_wgs84.geometry[20].centroid.x)

    #
    lat, lon = 69.6, 19.4
    m = folium.Map(location=[lat, lon], zoom_start=9, tiles="OpenStreetMap")

    topo4 = folium.features.WmsTileLayer(url="http://openwms.statkart.no/skwms1/wms.topo4?",
                                         layers="topo4_WMS", transparent=True, format="image/jpeg",
                                         name="Topo4")
    topo4.add_to(m)

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


if __name__ == '__main__':
    gdf = get_aval_data()
    show_on_map(gdf)
