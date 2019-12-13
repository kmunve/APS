from datetime import datetime, timedelta
import geopandas as gp
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sb
from shapely.geometry import Polygon
import os

plt.rcParams['figure.figsize'] = (10, 20)

import logging

# Set up the logger and log-file.
logging.basicConfig(filename='import_test.log',
                    # format='%(levelname)s: [%(asctime)s] %(message)s',
                    format='%(levelname)s [%(asctime)s] %(message)s',
                    datefmt='%Y-%m-%dT%H:%M:%S',
                    level=logging.DEBUG)


# Load a shape file as a geopandas dataframe
def load_shp_file(scn):
    scns = {
        'scn0': '../data/AvalDet_20190822_155124_ref_20190816_trno_087_ZZ/AvalDet_20190822_155124_ref_20190816_trno_087_ZZ.shp',
        'scn1': '../data/AvalDet_20190824_155214_ref_20190818_trno_087_ZZ/AvalDet_20190824_155214_ref_20190818_trno_087_ZZ.shp',
        'scn2': '../data/AvalDet_20190825_155227_ref_20190819_trno_087_ZZ/AvalDet_20190825_155227_ref_20190819_trno_087_ZZ.shp',
        'scn3': '../data/AvalDet_20190829_155131_ref_20190823_trno_087_ZZ/AvalDet_20190829_155131_ref_20190823_trno_087_ZZ.shp'
        }

    gdf = gp.read_file(scns[scn])
    return gdf


def scenario_0():
    scn_list = ['scn0']
    scn_d = {}
    for scn in scn_list:
        scn_d[scn] = load_shp_file(scn)
        logging.info('{0}: {1} objects loaded into dataframe'.format(scn, len(scn_d[scn].index)))

    for scn in scn_d.keys():
        # print(scn_d[scn].head())
        scn_d[scn].plot(edgecolor='black', alpha=0.6)
        plt.savefig('{0}.png'.format(scn), dpi=90)
        plt.cla()
        logging.info('{0} plotted and saved to {0}.png'.format(scn))


if __name__ == "__main__":
    scenario_0()

