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
p1.ygrid.grid_line_alpha = 0.5
p1.ygrid.grid_line_dash = [6, 4]
p1.ygrid.band_fill_color = "grey"
p1.ygrid.band_fill_alpha = 0.1
# alternatives are 'rect' or 'circle'+'segment'


# Persistent weak layers example plot
mask = sd.data['SurfaceHoarObs'] != 0.0
sh_obs = sd.data[mask]
mask = sd.data['SurfaceHoarWarn'] != 0.0
sh_warn = sd.data[mask]

mask = sd.data['DepthHoarObs'] != 0.0
dh_obs = sd.data[mask]
mask = sd.data['DepthHoarWarn'] != 0.0
dh_warn = sd.data[mask]

mask = sd.data['FacetsObs'] != 0.0
fc_obs = sd.data[mask]
mask = sd.data['FacetsWarn'] != 0.0
fc_warn = sd.data[mask]

p2 = timeline_figure(x_range=p1.x_range, y_range=[0, 9])
p2.inverted_triangle(x=sh_obs['Time'], y=sh_obs['SurfaceHoarObs'], size=10, color="red", legend="SH obs")
p2.inverted_triangle(x=sh_warn['Time'], y=sh_warn['SurfaceHoarWarn'], size=10, color="blue", legend="SH var")

p2.triangle(x=dh_obs['Time'], y=dh_obs['DepthHoarObs'], size=10, color="red", legend="DH obs")
p2.triangle(x=dh_warn['Time'], y=dh_warn['DepthHoarWarn'], size=10, color="blue", legend="DH var")

p2.square(x=fc_obs['Time'], y=fc_obs['FacetsObs'], size=10, color="red", legend="FC obs")
p2.square(x=fc_warn['Time'], y=fc_warn['FacetsWarn'], size=10, color="blue", legend="FC var")

p2.yaxis.axis_label = 'VSL'
p2.yaxis.major_tick_line_color = None
p2.yaxis.axis_line_color = None
p2.yaxis.major_label_text_color = None

# TODO: get legend out of the way
p = gridplot([[p1], [p2]])#, toolbar_location=None)
show(p)

