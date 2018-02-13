import geopandas as gpd
import matplotlib.pyplot as plt
import folium

aval = gpd.read_file(r'D:\Dev\APS\aps\data\satskred\S1_Tromsoe_20180116_052732\S1_Tromsoe_20180116_052732.shp')

print(aval.head(5))
for a in aval:
    print(a)#, a['AREA m2'], a.area)

aval.crs = {'init': 'EPSG:32633'}
print(aval.crs)

#aval.plot()
#plt.show()

def show_on_map(gdf):
    gdf_wgs84 = gdf.to_crs({'init': 'epsg:4326'})

    lat, lon = 68.0, 16.0
    m = folium.Map(location=[lat, lon], zoom_start=9, tiles="OpenStreetMap")

    topo4 = folium.features.WmsTileLayer(url="http://openwms.statkart.no/skwms1/wms.topo4?",
                                         layers="topo4_WMS", transparent=True, format="image/jpeg",
                                         name="Topo4")
    # topo4.add_to(m)

    for s in gdf.geometry:
        reg_marker = folium.Circle(
            location=[s_reg[key]['Lat'], s_reg[key]['Lon']],
            radius=r,
            color='blue',
            weight=1,
            fill_opacity=0.4,
            # opacity=1,
            fill_color='blue',
            fill=True,  # gets overridden by fill_color
            popup='{0} (Id: {1})'.format(key, s_reg[key]['Id'])
        )
        reg_marker.add_to(m)

        folium.Marker([s_reg[key]['Lat'], s_reg[key]['Lon']], popup='{0} (Id: {1})'.format(key, s_reg[key]['Id'])).add_to(m)


    # add layer control functionality to map
    folium.LayerControl().add_to(m)
    # add lat/lon pop-up funcionality
    folium.LatLngPopup().add_to(m)
    # add measure functionality
    plugins.MeasureControl().add_to(m)
    # add drawing functionality
    #folium.plugins.Draw().add_to(m)

    m.save('aval_activity.html')




