#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from PIL import Image
import numpy as np

'''


__author__ = 'kmu'
'''


im = Image.open(r'DTM10_1.tiff')

imarr = np.array(im)

print(type(imarr), imarr.shape)
