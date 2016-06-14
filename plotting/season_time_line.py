#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

from bokeh.io import gridplot
from bokeh.plotting import figure, output_file, show
from data.season_dummy import seasonData
'''


__author__ = 'kmu'
'''

sd = seasonData()
# check if you can filter out data: e.g. precip > 30 mm
# reduces also the amount of data to be plotted
mask = sd.data['Precipitation'] >= 30.0

filtered_sd = sd.data[mask]
tags = [filtered_sd['Precipitation']]

output_file("season_timeline.html")

# Setting up the figure
p1 = figure(title="Seasonal overview", x_axis_type="datetime", tools='hover')

# make the outline "invisible"
p1.outline_line_color = 'white'

# change just some things about the x-grid
p1.xgrid.grid_line_color = None

# change just some things about the y-grid
p1.ygrid.grid_line_alpha = 0.5
p1.ygrid.grid_line_dash = [6, 4]


p1.segment(x0=filtered_sd['Time'], y0=filtered_sd['Dummy-y'], x1=filtered_sd['Time'], y1=filtered_sd['Precipitation'], line_width=4)
# alternatives are 'rect' or 'circle'+'segment'




# Setting up the figure
p2 = figure(x_axis_type="datetime", tools='hover')

# make the outline "invisible"
p2.outline_line_color = 'white'

# change just some things about the x-grid
p2.xgrid.grid_line_color = None

# change just some things about the y-grid
p2.ygrid.grid_line_alpha = 0.5
p2.ygrid.grid_line_dash = [6, 4]

mask = sd.data['SurfaceHoar'] > 0.0
sh_sd = sd.data[mask]

p2.inverted_triangle(x=sh_sd['Time'], y=sh_sd['SurfaceHoar'], size=10, color="#DE2D26")


p = gridplot([[p1], [p2]])
show(p)

