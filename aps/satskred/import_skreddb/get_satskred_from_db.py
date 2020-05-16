import pyodbc
import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.wkt import loads
import folium
import folium.plugins


def connect_to_skredprod():
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=tst-skred.sql.nve.no;'
                          'Database=skredprod;'
                          'Trusted_Connection=yes;')
    return conn


def _test_connection(conn):
    tbls = {"sh": "skred.SKREDHENDELSE",
            "ut": "skred.UTLOPUTLOSNINGOMR",
            "tek": "skred.SKREDTEKNISKEPARAMETRE"
            }

    cursor = conn.cursor()
    for k, v in tbls.items():
        print('Data from {0}'.format(v))
        cursor.execute('SELECT TOP (10) * FROM {0}'.format(v))
        for row in cursor:
            print(row)
        print('\n###\n')


def get_avalanches_by_date(conn, from_date="2020-04-01", to_date="2020-04-30"):
    q = """SELECT h.[skredTidspunkt]
          ,h.[registrertDato]
          ,h.[registrertAv]
          ,t.[skredAreal_m2]
          ,t.[eksposisjonUtlopsomr]
          ,t.[snittHelningUtlopssomr_gr]
          ,t.[maksHelningUtlopsomr_gr]
          ,t.[minHelningUtlopsomr_gr]
          ,t.[hoydeStoppSkred_moh]
          ,t.[noyHoydeStoppSkred]
          --,h.[SHAPE] --just the point
          ,h.[skredID]
          ,u.[SHAPE].STGeometryN(1).ToString() AS SHAPE
    FROM [skredprod].[skred].[SKREDHENDELSE] AS h
    LEFT JOIN [skredprod].[skred].[SKREDTEKNISKEPARAMETRE] AS t ON t.[skredID] = h.[skredID]
    LEFT JOIN [skredprod].[skred].[UTLOPUTLOSNINGOMR] AS u ON u.[skredID] = h.[skredID]
    WHERE h.[registrertAv] = 'Sentinel-1' and h.[regStatus] != 'Slettet' and h.skredTidspunkt >= '{from_date}' and h.skredTidspunkt < '{to_date}'
    ORDER BY t.[registrertDato] DESC""".format(from_date=from_date, to_date=to_date)

    df = pd.read_sql_query(q, conn)
    df['geometry'] = [loads(s) for s in df['SHAPE']]
    epsg = 32633
    gdf = gpd.GeoDataFrame(df, crs={'init': 'epsg:' + str(epsg)})
    return gdf


def get_avalanche_stats(gdf):
    gdf['area'] = gdf.area
    # Maximum area
    max_area = gdf['area'].max()
    # Minimum area
    min_area = gdf['area'].min()
    # Mean area
    mean_area = gdf['area'].mean()

    print("Max area: {maximum} square meters".format(maximum=round(max_area, 0)))
    print("Min area: {minimum} square meters".format(minimum=round(min_area, 0)))
    print("Mean area: {mean} square meters".format(mean=round(mean_area, 0)))


def make_avalanche_map(gdf, out='ava_map.html'):
    # gdf.to_crs({'init': 'EPSG:3857'}, inplace=True)
    gdf.to_crs({'init': 'EPSG:4326'}, inplace=True)

    # b = gdf.bounds
    # mx = min(b['minx']) + (max(b['maxx']) - min(b['minx'])) / 2
    # my = min(b['miny']) + (max(b['maxy']) - min(b['miny'])) / 2

    ava_map = folium.Map(prefer_canvas=True,
                         # tiles='Stamen Terrain',
                         location=[69, 20],
                         zoom_start=10,
                         control_scale=True)

    _fields = {'registrertAv': 'Registrert av',
               'skredAreal_m2': 'Areal (m2)'}
    _t = _fields.keys()
    # TODO: set min zoom level
    a = folium.GeoJson(gdf,
                       name='Detected avalanches (polygon)',
                       style_function=lambda feature: {
                           'fillColor': '#EE7B04',
                           #         'color' : feature['properties']['RGBA'],
                           'color': '#EE7B04', 'weight': 1,
                           'fillOpacity': 0.5
                       },
                       tooltip=folium.features.GeoJsonTooltip(fields=list(_fields.keys()),#['registrertAv', 'skredAreal_m2'],
                                                              aliases=list(_fields.values()), #['Registered by:', 'Area (m2):'],
                                                              labels=True,
                                                              sticky=False
                                                              )
                       )

    a.add_to(ava_map)

    # Create a folium marker cluster
    marker_cluster = folium.plugins.MarkerCluster(name='Detected avalanches (point)')

    # # Get x and y coordinates for each point
    m = np.vstack([gdf.centroid.y, gdf.centroid.x]).T

    # Create icons for the marker cluster
    i = [folium.Icon(color='lightgray', icon='mountain', prefix='fa')] * m.shape[0]

    # TODO: loop once over GDF and create markers, polygons, popups and tooltips
    for m_ in m:
        m_
        folium.Marker(m_, icon=folium.Icon(color='lightgray', icon='mountain', prefix='fa')).add_to(marker_cluster)
    # other icons 'satellite', 'snowflake'


    # Add marker cluster to map
    marker_cluster.add_to(ava_map)

    folium.LayerControl().add_to(ava_map)
    ava_map.save(out)
    print('Open map: {0}'.format(out))


if __name__ == '__main__':
    conn = connect_to_skredprod()
    # _test_connection(conn)
    gdf = get_avalanches_by_date(conn)
    conn.close()

    get_avalanche_stats(gdf)
    make_avalanche_map(gdf)
