#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

from bokeh.io import gridplot
from bokeh.plotting import figure, output_file, show
from aps.data.season_dummy import seasonData
from aps.plotting.bokeh_plots import timeline_figure
'''


__author__ = 'kmu'
'''

sd = seasonData()
# check if you can filter out data: e.g. precip > 30 mm
# reduces also the amount of data to be plotted
mask = sd.data['Precipitation'] >= 20.0

filtered_sd = sd.data[mask]
tags = [filtered_sd['Precipitation']]

output_file("season_timeline.html", mode="cdn")


p1 = timeline_figure(title="Sesong oversikt", y_range=[-0.1, 60])
p1.segment(x0=filtered_sd['Time'], y0=filtered_sd['Dummy-y'], x1=filtered_sd['Time'], y1=filtered_sd['Precipitation'],
           line_width=4)
p1.yaxis.axis_label = 'Døgnnedbør [mm]'
p1.ygrid.band_fill_color = "grey"
p1.ygrid.band_fill_alpha = 0.1
# alternatives are 'rect' or 'circle'+'segment'


# Surface hoar example plot
mask = sd.data['SurfaceHoarObs'] != 0.0
sh_obs = sd.data[mask]
mask = sd.data['SurfaceHoarWarn'] != 0.0
sh_warn = sd.data[mask]

p2 = timeline_figure(x_range=p1.x_range, y_range=[-2, 2])
p2.inverted_triangle(x=sh_obs['Time'], y=sh_obs['SurfaceHoarObs'], size=10, color="red")
p2.inverted_triangle(x=sh_warn['Time'], y=sh_warn['SurfaceHoarWarn'], size=10, color="blue")
p2.yaxis.axis_label = 'VSL'
# TODO: remove y-axis ticks
# Use triangle for depth hoar and square for facets

p = gridplot([[p1], [p2]])#, toolbar_location=None)
show(p)

