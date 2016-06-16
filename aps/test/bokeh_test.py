#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from bokeh.plotting import figure, output_file, show
'''


__author__ = 'kmu'
'''

output_file("test.html")
p = figure()
p.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], line_width=2)
show(p)
