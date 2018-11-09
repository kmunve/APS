# -*- coding: utf-8 -*-
import math
import folium
from folium import plugins
### use http://bboxfinder.com to get the bbox value
### see http://spatialreference.org/ref/epsg/4326/


A = 100_000_000 # m2
r = math.sqrt(A/(2*math.pi))


lat, lon = 60.928, 8.1937
m = folium.Map(location=[lat, lon], zoom_start=13, tiles="OpenStreetMap")

kwargs = {"attribution": "NVE", "minZoom": "10"}
topo4 = folium.raster_layers.WmsTileLayer(url="http://openwms.statkart.no/skwms1/wms.topo4?",
                                     layers="topo4_WMS", transparent=True, fmt="image/jpeg",
                                     name="Topo4")
topo4.add_to(m)

bratthet = folium.raster_layers.WmsTileLayer(url="https://gis3.nve.no/map/services/Bratthet/MapServer/WmsServer?",
                                            layers="Bratthet_snoskred", transparent=True,
                                            fmt="image/png", name='Bratthet',
                                            **kwargs)
bratthet.add_to(m)

faresoner = folium.raster_layers.WmsTileLayer(url="https://gis3.nve.no/map/services/SkredSnoAktR/MapServer/WmsServer?",
                                         layers="Utlosningsomrade", transparent=True, fmt="image/png",
                                         name="Avalanche run-out zone", **kwargs) #Layers: Utlopsomrade / Utlosningsomrade
faresoner.add_to(m)

reg_marker = folium.Circle(
    location=[lat, lon],
    radius=r,
    color='blue',
    weight=1,
    fill_opacity=0.04,
    # opacity=1,
    fill_color='blue',
    fill=True,  # gets overridden by fill_color
)
reg_marker.add_to(m)


folium.vector_layers.Rectangle(bounds, popup=None, tooltip=None, **kwargs)

#folium.Marker([s_reg[key]['Lat'], s_reg[key]['Lon']], popup='{0} (Id: {1})'.format(key, s_reg[key]['Id'])).add_to(m)


# add layer control functionality to map
folium.LayerControl().add_to(m)
# add lat/lon pop-up funcionality
folium.LatLngPopup().add_to(m)
# add measure functionality
plugins.MeasureControl().add_to(m)
# add drawing functionality
#folium.plugins.Draw().add_to(m)

m.save('spatial_distribution.html')
