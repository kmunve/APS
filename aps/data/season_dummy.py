#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from __future__ import print_function
from datetime import datetime, timedelta
import numpy as np
from pandas import DataFrame

'''
Creates a test data for the seasonal time line.

__author__ = 'kmu'
'''

class seasonData:

    def __init__(self):

        d_start = datetime(2015, 12, 1)
        d_end = datetime(2016, 3, 31)
        d_step = timedelta(days=1)

        self.timearr = [d_start+ (i * d_step) for i in range(0, 121)]
        # self.timearr = np.arange(0,100,2)
        self.precipitation()
        self.surface_hoar()
        self.depth_hoar()
        self.facets()
        dummy_y = np.zeros_like(self.preciparr)
        self.data = DataFrame(data={'Time': self.timearr, 'Precipitation': self.preciparr, 'Dummy-y': dummy_y,
                                    'SurfaceHoarObs': self.sh_obs_arr, 'SurfaceHoarWarn': self.sh_warn_arr,
                                    'DepthHoarObs': self.dh_obs_arr, 'DepthHoarWarn': self.dh_warn_arr,
                                    'FacetsObs': self.fc_obs_arr, 'FacetsWarn': self.fc_warn_arr})


    def precipitation(self):

        preciparr = np.zeros_like(self.timearr, dtype=float)
        i = np.random.random_integers(0, len(self.timearr)-1, 7)
        preciparr[i] = 20.0
        i = np.random.random_integers(0, len(self.timearr) - 1, 7)
        preciparr[i] = [40.0, 25.3, 15.0, 33.2, 41.0, 27.0, 29.9]

        self.preciparr = preciparr

    def surface_hoar(self):
        sh_obs_arr = np.zeros_like(self.timearr, dtype=float)
        i = np.random.random_integers(0, len(self.timearr)-1, 7)
        sh_obs_arr[i] = 1.0

        sh_warn_arr = np.zeros_like(self.timearr, dtype=float)
        i = np.random.random_integers(0, len(self.timearr) - 1, 3)
        sh_warn_arr[i] = 2.0

        self.sh_obs_arr = sh_obs_arr
        self.sh_warn_arr = sh_warn_arr

    def depth_hoar(self):
        dh_obs_arr = np.zeros_like(self.timearr, dtype=float)
        i = np.random.random_integers(0, len(self.timearr) - 1, 12)
        dh_obs_arr[i] = 4.0

        dh_warn_arr = np.zeros_like(self.timearr, dtype=float)
        i = np.random.random_integers(0, len(self.timearr) - 1, 6)
        dh_warn_arr[i] = 5.0

        self.dh_obs_arr = dh_obs_arr
        self.dh_warn_arr = dh_warn_arr

    def facets(self):
        fc_obs_arr = np.zeros_like(self.timearr, dtype=float)
        i = np.random.random_integers(0, len(self.timearr) - 1, 23)
        fc_obs_arr[i] = 7.0

        fc_warn_arr = np.zeros_like(self.timearr, dtype=float)
        i = np.random.random_integers(0, len(self.timearr) - 1, 17)
        fc_warn_arr[i] = 8.0

        self.fc_obs_arr = fc_obs_arr
        self.fc_warn_arr = fc_warn_arr


def usage():
    sd = seasonData()
    a = 1

if __name__ == "__main__":
    usage()
