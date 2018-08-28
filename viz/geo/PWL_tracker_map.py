# -*- coding: utf-8 -*-
import folium
from folium import plugins
### use http://bboxfinder.com to get the bbox value
### see http://spatialreference.org/ref/epsg/4326/


lat, lon = 65.0, 13.0
m = folium.Map(location=[lat, lon], zoom_start=6, tiles="OpenStreetMap")

# topo4 = folium.features.WmsTileLayer(url="http://openwms.statkart.no/skwms1/wms.topo4?",
#                                      layers="topo4_WMS", transparent=True, fmt="image/jpeg",
#                                      name="Topo4")
#topo4.add_to(m)

pwl_data = r"data.geojson"
folium.GeoJson(pwl_data, name='Vedv. svake lag').add_to(m)


# add layer control functionality to map
folium.LayerControl().add_to(m)
# add lat/lon pop-up funcionality
folium.LatLngPopup().add_to(m)
# add measure functionality
#plugins.MeasureControl().add_to(m)
# add drawing functionality
folium.plugins.Draw(export=True).add_to(m)

m.save('PWL_tracker.html')
