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
        dummy_y = np.zeros_like(self.preciparr)
        self.data = DataFrame(data={'Time': self.timearr, 'Precipitation': self.preciparr, 'Dummy-y': dummy_y, 'SurfaceHoar': self.sharr})


    def precipitation(self):

        preciparr = np.zeros_like(self.timearr, dtype=float)
        i = np.random.random_integers(0, len(self.timearr)-1, 7)
        preciparr[i] = 20.0
        i = np.random.random_integers(0, len(self.timearr) - 1, 7)
        preciparr[i] = 40.0

        self.preciparr = preciparr

    def surface_hoar(self):
        sharr = np.zeros_like(self.timearr, dtype=float)
        i = np.random.random_integers(0, len(self.timearr)-1, 12)
        sharr[i] = 1.0

        self.sharr = sharr


def usage():
    sd = seasonData()
    a = 1

if __name__ == "__main__":
    usage()
