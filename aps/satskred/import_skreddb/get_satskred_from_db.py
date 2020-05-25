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


def get_aval_color(noySkredTidspunkt):
    if noySkredTidspunkt in ['Eksakt', '1 min', '1 time', '4 timer', '6 timer', '12 timer', '1 dag']:
        return 'red' #'#75B100'
    elif noySkredTidspunkt in ['1 dager', '2 dager']:#, '3 dager']:
        return 'orange' #'#FFCC33'
    else:
        return 'lightgray' #'#E3000F'


def get_avalanches_by_date(conn, from_date="2020-04-01", to_date="2020-04-30"):
    q = """SELECT h.[skredType] 
          ,h.[skredTidspunkt]
          ,h.[noySkredTidspunkt]
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
    df['preci_color'] = df['noySkredTidspunkt'].map(get_aval_color)
    epsg = 32633
    gdf = gpd.GeoDataFrame(df, crs={'init': 'epsg:' + str(epsg)})
    return gdf


def get_avalanche_stats(gdf):

    print(gdf.describe())

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

    print(gdf.groupby(['noySkredTidspunkt']).count())

    # TODO: add statistics per reion - intersect with fr_polygon, count of avalanches per precision level.
# def _fr_style(feature, gdf):
#     # Styling function for forecasting region polygons
#     a = employed_series.get(int(feature['id'][-5:]), None)
#     return {
#         'fillOpacity': 0.5,
#         'weight': 0,
#         'fillColor': '#black' if employed is None else colorscale(employed)
#     }
#     lambda feature: {
#         'fillColor': '#9BB9C2',
#         'color': '#044157', 'weight': 1,
#         'fillOpacity': 0.5}


def make_avalanche_map(gdf, out='ava_map.html'):
    """
    https://stackoverflow.com/questions/52428916/python-folium-markercluster-color-customization
    https://github.com/python-visualization/folium/blob/master/examples/MarkerCluster.ipynb
    https://www.kaggle.com/rachan/how-to-folium-for-maps-heatmaps-time-analysis
    

    :param gdf:
    :param out:
    :return:
    """

    _fr_style_1 = {
        'fillColor': '#9BB9C2',
        'color': '#033648', 'weight': 1,
        'fillOpacity': 0.2
    }

    _fr_style_2 = {
        'fillColor': '#9BB9C2',
        'color': '#033648', 'weight': 1,
        'fillOpacity': 0.0
    }

    # url = 'http://leafletjs.com/examples/custom-icons/{}'.format
    icon_image = 'avalanche.png'
    # shadow_image = url('leaf-shadow.png')

    ava_icon = folium.CustomIcon(icon_image=icon_image, icon_size=(64, 64), icon_anchor=(22, 94), popup_anchor=(-3, -76))


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

    forecast_reg = folium.GeoJson(
        r'C:\Users\kmu\PycharmProjects\APS\aps\data\forecasting_regions\Skred_Varsling.geojson',
        name='Forecasting regions',
        style_function=lambda feature: _fr_style_1 if feature['properties']['regionType'] == 'A' else _fr_style_2
    ).add_to(ava_map)

    _fields = {'skredTidspunkt': 'Tidspunkt (utløsning)',
               'noySkredTidspunkt': 'Nøyaktighet (Tid)',
               'registrertAv': 'Registrert av',
               'registrertDato': 'Dato (registrert)',
               'skredAreal_m2': 'Areal (m2)',
               'eksposisjonUtlopsomr': 'Eksposisjon',
               'snittHelningUtlopssomr_gr': 'Helning (snitt)',
               'maksHelningUtlopsomr_gr': 'Helning (maks)',
               'minHelningUtlopsomr_gr': 'Helning (min)',
               'hoydeStoppSkred_moh': 'Høyde (stopp)',
               'skredID': 'ID'
               }
    _t = _fields.keys()
    # TODO: set min zoom level
    a = folium.GeoJson(gdf,
                   name='Detected avalanches (polygon)',
                   style_function=lambda feature: {
                       # 'fillColor': '#EE7B04',
                       # 'color': '#EE7B04',
                       'weight': 1,
                       'color': feature['properties']['preci_color'],
                       'fillcolor': feature['properties']['preci_color'],
                       'fillOpacity': 0.2
                   },
                   tooltip=folium.features.GeoJsonTooltip(fields=list(_fields.keys()),
                                                          aliases=list(_fields.values()),
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
    # i = [folium.Icon(color='lightgray', icon='mountain', prefix='fa')] * m.shape[0]

    # TODO: loop once over GDF and create markers, polygons, popups and tooltips

    for row_label, row in gdf.iterrows():
        a=1
        _m = [row.geometry.centroid.y, row.geometry.centroid.x]
        folium.Marker(_m, icon=folium.Icon(color=get_aval_color(row['noySkredTidspunkt']))).add_to(marker_cluster)
        #
        # if row['noySkredTidspunkt'] in ['Eksakt', '1 min', '1 time', '4 timer', '6 timer', '12 timer', '1 dag']:
        #     folium.Marker(_m, icon=folium.Icon(color='red')).add_to(marker_cluster)
        # elif row['noySkredTidspunkt'] in ['1 dager', '2 dager']:
        #     folium.Marker(_m, icon=folium.Icon(color='orange')).add_to(marker_cluster)
        # else:
        #     folium.Marker(_m, icon=folium.Icon(color='lightgray')).add_to(marker_cluster)

    # for m_ in m:
    #     # marker_cluster.add_child(m_, name='') # does not work
    #     # folium.Marker(m_, icon=folium.Icon(color='lightgray', icon='mountain', prefix='fa')).add_to(marker_cluster)
    #     folium.Marker(m_, icon=folium.Icon(color='lightgray')).add_to(marker_cluster)
    #     # folium.Marker(m_, icon=ava_icon).add_to(marker_cluster)
    #     # other icons 'satellite', 'snowflake'

    # Add marker cluster to map
    marker_cluster.add_to(ava_map)

    folium.LayerControl().add_to(ava_map)
    ava_map.save(out)
    print('Open map: {0}'.format(out))

if __name__ == '__main__':
    conn = connect_to_skredprod()
    # _test_connection(conn)
    gdf = get_avalanches_by_date(conn, from_date="2019-11-01", to_date="2020-05-30")
    # for c in gdf.columns:
    #     print(c)
    conn.close()

    get_avalanche_stats(gdf)
    make_avalanche_map(gdf)
