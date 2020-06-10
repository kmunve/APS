import pyodbc
import re
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from shapely.wkt import loads
import folium
import folium.plugins

plt.style.use('ggplot')


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


def get_forecasting_regions():
    fr_df = gpd.read_file(r'C:\Users\kmu\PycharmProjects\APS\aps\data\forecasting_regions\Skred_Varsling.geojson')
    return fr_df

def get_aval_color(noySkredTidspunkt, css=False):
    if noySkredTidspunkt in ['Eksakt', '1 min', '1 time', '4 timer', '6 timer', '12 timer', '1 dag']:
        c = 'red'  # '#75B100'
    elif noySkredTidspunkt in ['1 dager', '2 dager']:  # , '3 dager']:
        c = 'orange'  # '#FFCC33'
    else:
        c = 'lightgray'  # '#E3000F'
    if css:
        return 'background-color: {0}'.fomrat(c)
    else:
        return c


def get_avalanches_by_date(conn, from_date="2020-04-01", to_date="2020-04-30", include_deleted=False, print_sql=False):
    if include_deleted:  # if True only the avalanches with reStatus == 'Sletted' are retrieved.
        del_sql = ""
    else:
        del_sql = " and h.[regStatus] != 'Slettet'"

    q = """SELECT h.[skredType] 
          ,h.[skredTidspunkt]
          ,h.[noySkredTidspunkt]
          ,h.[registrertDato]
          ,h.[registrertAv]
          ,h.[regStatus]
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
    WHERE h.[registrertAv] = 'Sentinel-1'{del_sql} and h.skredTidspunkt >= '{from_date}' and h.skredTidspunkt < '{to_date}'
    ORDER BY t.[registrertDato] DESC""".format(from_date=from_date, to_date=to_date, del_sql=del_sql)

    if print_sql:
        print(q)

    df = pd.read_sql_query(q, conn)
    df['geometry'] = [loads(s) for s in df['SHAPE']]
    df['preci_color'] = df['noySkredTidspunkt'].map(get_aval_color)
    epsg = 32633
    gdf = gpd.GeoDataFrame(df, crs={'init': 'epsg:' + str(epsg)})
    return gdf


def _color_html_table(s):
    if s in ['Eksakt', '1 min', '1 time', '4 timer', '6 timer', '12 timer', '1 dag']:
        c = 'bg-danger'
    elif s in ['1 dager', '2 dager']:  # , '3 dager']:
        c = 'bg-warning'
    else:
        c = 'bg-info'

    return '<p class="{0}">{1}</p>'.format(c, s)


def _table_hover(hover_color="#ffff99"):
    return dict(selector="tr:hover",
                props=[("background-color", "%s" % hover_color)])


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

    stats_dict = {'n_aval': len(gdf),
                  'avg_size': round(mean_area, 0),
                  'min_size': round(min_area, 0),
                  'max_size': round(max_area, 0)
                  }

    df_stats = gdf.filter(
        ['skredTidspunkt', 'noySkredTidspunkt', 'area', 'maksHelningUtlopsomr_gr', 'hoydeStoppSkred_moh', 'registrertDato',
         'regStatus', 'registrertAv'])

    col_names = {'skredTidspunkt': 'Tidspunkt (utløsning)',
                 'noySkredTidspunkt': 'Nøyaktighet (tidspunkt)',
                 'area': 'Area (m2)',
                 'maksHelningUtlopsomr_gr': 'Maks helning (utløp)',
                 'hoydeStoppSkred_moh': 'Høyde (stopp)',
                 'registrertDato': 'Tidspunkt (registrert)',
                 'reStatus': 'Status',
                 'registrertAv': 'Registrert av'}

    df_stats.rename(columns=col_names, inplace=True)
    # s = df_stats.style.apply(_table_hover, axis=1)#, subset=['noySkredTidspunkt'])

    # df_stats.to_html('ava_stats.html', index=False, classes=['table', 'table-striped'],
    #                  formatters={'noySkredTidspunkt': _color_html_table})

    df_html = df_stats.to_html(index=False, classes=['table', 'table-hover', 'table-condensed']
                     # formatters={'noySkredTidspunkt': _color_html_table}
                               )

    return df_html, stats_dict

    # random_id = 'id%d' % np.random.choice(np.arange(1000000))
    #
    # style = """
    #         <style>
    #             table#{random_id} {{color: blue}}
    #         </style>
    #         """.format(random_id=random_id)
    #
    # df_html = re.sub(r'<table', r'<table id=%s ' % random_id, df_html)
    #
    # with open('ava_stats.html', 'w') as f:
    #     f.write(style + df_html)


def make_area_histogram(gdf):
    fig, ax = plt.subplots(1, 1)

    # sm_1day = gdf[(gdf['area'] <= 20000) & (gdf['preci_color'] == 'red')]

    gdf.groupby('preci_color').hist(column=['area'], stacked=True, bins=8, alpha=0.5, ax=ax)
    # sm_1day.hist(column=['area'], bins=8, ax=ax)
    ax.set_xlabel('Area ($m^2$)')
    ax.set_ylabel('Count')
    ax.set_title('')
    plt.legend()
    plt.savefig('area_hist.svg')


def make_area_histogram_alt(gdf):
    import altair
    # from altair_saver import save
    base = altair.Chart(gdf)

    bar = base.mark_bar().encode(
        x=altair.X('area', bin=True, axis=None),
        y='count()'
    )

    bar.save('area_hist.html')


# TODO: add statistics per region - intersect with fr_polygon, count of avalanches per precision level.
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


def in_region(gdf, region_id=3013):
    # Test if the centroid of an avalanche polygon lies within the forecasting region with ID region_id.
    fr_df = get_forecasting_regions()
    reg = fr_df[fr_df['omradeID'] == 3013]
    p = gdf.centroid
    a = gpd.overlay(reg, gdf, how='intersection')
    a = p.intersects(reg)
    print(a)
    for c in gdf.columns:
        print(c)


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

    ava_icon = folium.CustomIcon(icon_image=icon_image, icon_size=(64, 64), icon_anchor=(22, 94),
                                 popup_anchor=(-3, -76))

    # gdf.to_crs({'init': 'EPSG:3857'}, inplace=True)
    gdf.to_crs({'init': 'EPSG:4326'}, inplace=True)

    # b = gdf.bounds
    # mx = min(b['minx']) + (max(b['maxx']) - min(b['minx'])) / 2
    # my = min(b['miny']) + (max(b['maxy']) - min(b['miny'])) / 2

    ava_map = folium.Map(prefer_canvas=True,
                         # tiles='Stamen Terrain',
                         location=[65, 16],
                         zoom_start=5,
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
        a = 1
        _m = [row.geometry.centroid.y, row.geometry.centroid.x]
        folium.Marker(_m, icon=folium.Icon(color=get_aval_color(row['noySkredTidspunkt']))).add_to(marker_cluster)

    # Add marker cluster to map
    marker_cluster.add_to(ava_map)

    folium.LayerControl().add_to(ava_map)
    ava_map.save(out)
    print('Open map: {0}'.format(out))


def make_html_from_template(satskred_table, stats_dict):
    from jinja2 import Template
    with open('ava_info_template.html', 'r') as f:
        t = Template(f.read())

    with open('ava_info.html', 'w') as f:
        f.write(t.render(satskred_table=satskred_table,
                         n_aval=stats_dict['n_aval'],
                         avg_size=stats_dict['avg_size'],
                         min_size=stats_dict['min_size'],
                         max_size=stats_dict['max_size'],
                         ))


if __name__ == '__main__':
    conn = connect_to_skredprod()
    # _test_connection(conn)
    gdf = get_avalanches_by_date(conn, from_date="2020-01-01", to_date="2020-06-30", include_deleted=True, print_sql=True)
    conn.close()

    table_html, stats_dict = get_avalanche_stats(gdf)

    make_area_histogram(gdf)
    # make_area_histogram_alt(gdf)

    make_html_from_template(table_html, stats_dict)
    make_avalanche_map(gdf)
