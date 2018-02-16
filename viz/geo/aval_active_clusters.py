### Adapted from https://blog.dominodatalab.com/creating-interactive-crime-maps-with-folium/
import folium
import pandas as pd

SF_COORDINATES = (69.74, 19.38)
crimedata = pd.read_csv('SFPD_Incidents_-_Current_Year__2015_.csv')

# for speed purposes
MAX_RECORDS = 1000

# create empty map zoomed in on San Francisco
map = folium.Map(location=SF_COORDINATES, zoom_start=12)

# add a marker for every record in the filtered data, use a clustered view
for each in crimedata[0:MAX_RECORDS].iterrows():
    map.simple_marker(
        location=[each[1]['Y'], each[1]['X']],
        clustered_marker=True)

display(map)

# definition of the boundaries in the map
district_geo = r'sfpddistricts.geojson'

# calculating total number of incidents per district
crimedata2 = pd.DataFrame(crimedata['PdDistrict'].value_counts().astype(float))
crimedata2.to_json('crimeagg.json')
crimedata2 = crimedata2.reset_index()
crimedata2.columns = ['District', 'Number']

# creation of the choropleth
map1 = folium.Map(location=SF_COORDINATES, zoom_start=12)
map1.geo_json(geo_path=district_geo,
              data_out='crimeagg.json',
              data=crimedata2,
              columns=['District', 'Number'],
              key_on='feature.properties.DISTRICT',
              fill_color='YlOrRd',
              fill_opacity=0.7,
              line_opacity=0.2,
              legend_name='Number of incidents per district')

display(map1)
