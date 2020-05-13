import pyodbc
import pandas as pd
import geopandas as gpd
from shapely.wkt import loads
import folium


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
    gdf.to_crs({'init': 'EPSG:3857'}, inplace=True)

    b = gdf.bounds
    mx = min(b['minx']) + (max(b['maxx']) - min(b['minx'])) / 2
    mx = min(b['miny']) + (max(b['maxy']) - min(b['miny'])) / 2

    ava_map = folium.Map(prefer_canvas=True,
                         location=[69, 20],
                         zoom_start=10)

    # m = folium.GeoJson(gdf)
    # m.add_to(ava_map)

    a = folium.GeoJson(gdf,
                       style_function=lambda feature: {
                           'fillColor': 'red',
                           #         'color' : feature['properties']['RGBA'],
                           'color': 'red', 'weight': 1,
                           'fillOpacity': 0.5,
                           #         'popup': '{0}'.format(feature['properties']['regStatus'])
                           'tooltip': 'Click me!'
                       })

    a.add_to(ava_map)

    ava_map.save(out)



if __name__ == '__main__':
    conn = connect_to_skredprod()
    # _test_connection(conn)
    gdf = get_avalanches_by_date(conn)
    conn.close()

    get_avalanche_stats(gdf)
    make_avalanche_map(gdf)
