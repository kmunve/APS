#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
from aps.aps_io.bil import BILdata

'''


__author__ = 'kmu'
'''
bd = BILdata(r"Y:\snowsim\fsw\2017\fsw_2017_01_23.bil", "uint8")

bd.read()

a = 1
data = np.float32(bd.data)

plt.figure(facecolor='lightgrey')
plt.imshow(data, interpolation='nearest', alpha=1.0,
           vmin=-1, vmax=30
           )

plt.colorbar()
plt.show()
