# -*- coding: utf-8 -*-
import folium
from folium import plugins
### use http://bboxfinder.com to get the bbox value
### see http://spatialreference.org/ref/epsg/4326/

s_reg = {"Hemsedal": {"Id": 4001, "Lat": 60.95, "Lon": 8.28},
         "Tyin": {"Id": 4002, "Lat": 61.255, "Lon": 8.2},
         "Kattfjordeidet": {"Id": 4003, "Lat": 69.65, "Lon": 18.5},
         "Lavangsdalen": {"Id": 4004, "Lat": 69.46, "Lon": 19.24}}

r = 10_000


lat, lon = 65.0, 13.0
m = folium.Map(location=[lat, lon], zoom_start=6, tiles="OpenStreetMap")

topo4 = folium.features.WmsTileLayer(url="http://openwms.statkart.no/skwms1/wms.topo4?",
                                     layers="topo4_WMS", transparent=True, format="image/jpeg",
                                     name="Topo4")
# topo4.add_to(m)

for key in s_reg:
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

m.save('small_region.html')
