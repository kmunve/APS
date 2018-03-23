import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import folium
from folium.plugins import MarkerCluster, ImageOverlay

print(folium.__version__)

def get_aval_data(shp_file):
    dt = os.path.split(shp_file)[1].split('.')[0].split('_')

    aval = gpd.read_file(shp_file)

    # print(aval.head(5))
    # for a in aval:
    #     print(a)#, a['AREA m2'], a.area)

    # I think it is in UTM 33N
    aval.crs = {'init': 'EPSG:32633'}
    # print(aval.crs)

    aval['REGION'] = dt[1]
    aval['DATE'] = dt[2]
    aval['TIME'] = dt[3]


    #aval.plot()
    #plt.show()
    return aval


def get_aval_stats(gdf, plot_hist=False, plot_box=False):
    """
    gdf: geo-dataframe
    """
    stats = gdf['AREA m2'].describe()
    #print(stats)

    aval_volumes = np.array([100, 1_000, 10_000, 100_000])
    D30 = aval_volumes / 0.3  # avalanche size class at 30 cm slab thickness
    D50 = aval_volumes / 0.5  # avalanche size class at 50 cm slab thickness
    D100 = aval_volumes  # §avalanche size class at 100 cm slab thickness
    D200 = aval_volumes / 2.  # avalanche size class at 200 cm slab thickness

    print(D30, D100)

    if plot_hist:
        #sns.set_context('talk')

        f, axes = plt.subplots(2, 2, figsize=(7, 7), sharex=True, sharey=True)

        plt.subplots_adjust(top=0.9)
        f.suptitle('{2} {0}T{1} (#avalanches: {3})'.format(gdf['DATE'][0], gdf['TIME'][0], gdf['REGION'][0], len(gdf['AREA m2'])))  # can also get the figure from plt.gcf()
        c = 'lightgrey'

        for cax, D, l in zip([axes[0 ,0], axes[0 ,1], axes[1 ,0], axes[1 ,1]], [D30, D50, D100, D200], ["@ 0.3 m", "@ 0.5 m", "@ 1.0 m", "@ 2.0 m"]):
            cax.set(xscale="log")
            sns.distplot(gdf['AREA m2'], bins=D, color="skyblue", ax=cax, kde=False,
                         hist_kws={"edgecolor": "k", "linewidth": 1})
            cax.set_title(l)
            _s = 1
            for d in D:
                cax.axvline(x=d, ymin=0, ymax=0.9, linestyle='--', color=c)
                cax.text(d*0.5, 0.99*cax.get_ylim()[1], 'D{0}'.format(_s),
                                verticalalignment='top', horizontalalignment='center',
                                color=c, fontsize=9)
                _s += 1

        plt.savefig('{2}_{0}T{1}.png'.format(gdf['DATE'][0], gdf['TIME'][0], gdf['REGION'][0]), dpi=150)
        # plt.show()

    if plot_box:
        #sns.set_style("whitegrid")
        #stat_data = np.concatenate((stats[''], stats[''], stats[''], stats[''], stats['']), 0)
        ax = sns.boxplot(y=gdf['AREA m2'])
        # fig, ax = plt.boxplot(x=gdf['AREA m2'])

        ax.set_ylim([0, stats['max']])
        ax.set_xlabel('{0}T{1}'.format(gdf['DATE'][0], gdf['TIME'][0]))
        ax.set_ylabel('Debris area (m2)')

        plt.figtext(0.78, 0.95, stats, style='italic', fontsize=8,
                    verticalalignment='top', horizontalalignment='left',
                    bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})

        s = 1
        for d in D30:
            c = '#007F00'
            plt.axhline(y=d, xmin=0, xmax=0.25, linestyle='--', color=c)
            ax.text(-0.5, d, 'D{0} @ {1} m'.format(s, 0.3),
                    verticalalignment='bottom', horizontalalignment='left',
                    #transform=ax.transAxes,
                    color=c, fontsize=12)
            s += 1

        s = 1
        for d in D50:
            c = '#1F7C1F'
            plt.axhline(y=d, xmin=0.25, xmax=0.5, linestyle='--', color=c)
            ax.text(-0.25, d, 'D{0} @ {1} m'.format(s, 0.5),
                    verticalalignment='bottom', horizontalalignment='left',
                    # transform=ax.transAxes,
                    color=c, fontsize=12)
            s += 1

        s = 1
        for d in D100:
            c = '#3D7A3D'
            plt.axhline(y=d, xmin=0.5, xmax=0.75, linestyle='--', color=c)
            ax.text(0, d, 'D{0} @ {1} m'.format(s, 1.0),
                    verticalalignment='bottom', horizontalalignment='left',
                    # transform=ax.transAxes,
                    color=c, fontsize=12)
            s += 1

        s = 1
        for d in D200:
            c = '#597759'
            plt.axhline(y=d, xmin=0.75, xmax=1.0, linestyle='--', color=c)
            ax.text(0.25, d, 'D{0} @ {1} m'.format(s, 2.0),
                    verticalalignment='bottom', horizontalalignment='left',
                    # transform=ax.transAxes,
                    color=c, fontsize=12)
            s += 1

        plt.show()


def show_on_map(gdf):

    gdf_wgs84 = gdf.to_crs({'init': 'epsg:4326'})

    #
    lat, lon, zs = 69.6, 19.4, 13#9
    m = folium.Map(location=[lat, lon], zoom_start=zs, tiles="OpenStreetMap")

    topo4 = folium.features.WmsTileLayer(url="http://openwms.statkart.no/skwms1/wms.topo4?",
                                         layers="topo4_WMS", transparent=True, fmt="image/jpeg",
                                         name="Topo4")
    topo4.add_to(m)

    faresoner = folium.features.WmsTileLayer(url="https://gis3.nve.no/map/services/SkredSnoAktR/MapServer/WmsServer?",
                                         layers="Utlopsomrade", transparent=True, fmt="image/png",
                                         name="Avalanche run-out sone")
    faresoner.add_to(m)

    """
    Can request WMS data as geojson
    e.g.
    https://gis3.nve.no/map/rest/services/SkredSnoAktR/MapServer/2/query?where=1%3D1&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=*&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&resultOffset=&resultRecordCount=&queryByDistance=&returnExtentsOnly=false&datumTransformation=&parameterValues=&rangeValues=&f=geojson
    
    """

    kwargs = {"attribution": "NVE", "minZoom": "10"}
    # seems like a bug in folium prohibits that these parameters
    # are passed on to leaflet - can be set manually in the .html file

    bratthet = folium.features.WmsTileLayer(url="https://gis3.nve.no/map/services/Bratthet/MapServer/WmsServer?",
                                            layers="Bratthet_snoskred", transparent=True,
                                            fmt="image/png", name='Bratthet',
                                            **kwargs)
    bratthet.add_to(m)

    skredlop = folium.features.WmsTileLayer(url="https://www.vegvesen.no/kart/ogc/geodata_1_0/ows?",
                                            layers="Skredlop", transparent=True, fmt="image/png", name='SVV Skredløp')
    skredlop.add_to(m)

    #varslingsregioner = ImageOverlay(image='http://gis3.nve.no/map/rest/services/Mapservices/XgeoStatic/MapServer/export?dpi=96&transparent=true&format=png8&layers=show%3A25%2C26%2C29&bbox=-635878.2758445519%2C6520140.001693336%2C1616936.8964524597%2C7851779.998306664&bboxSR=32633&imageSR=32633&size=1663%2C983&f=image',
     #                                bounds=[[lat_min, lon_min], [lat_max, lon_max]])

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
    m.save('aval_activity_{2}_{0}T{1}.html'.format(gdf['DATE'][0], gdf['TIME'][0], gdf['REGION'][0]))


def compare_subregions():
    pass
    # create choropleth maps like in https://blog.dominodatalab.com/creating-interactive-crime-maps-with-folium/


if __name__ == '__main__':
    shp_file = r'D:\Dev\APS\aps\data\satskred\S1_Voss_20180224_170949\S1_Voss_20180224_170949.shp'
    gdf = get_aval_data(shp_file)
    print(gdf.describe())
    get_aval_stats(gdf, plot_hist=True)
    # print(gdf['AREA m2'].describe()['75%'])
    # print(type(gdf['AREA m2'].describe()))
    show_on_map(gdf)

