#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from bokeh.plotting import figure
from bokeh.models import Span
from datetime import datetime
'''


__author__ = 'kmu'
'''

# defines the color palette for danger levels
label_danger_levels = ['0 - no rating', '1 - low', '2 - moderate', '3 - considerable', '4 - high', '5 - very high']
pal_danger_levels = ['0.5', '#ccff66', '#ffff00', '#ff9900', '#ff0000', 'k']

def timeline_figure(title=None, x_range=None, y_range=None):

    # TODO: align x-axis

    # TOOLS = "resize,crosshair,pan,wheel_zoom,box_zoom,reset,box_select,lasso_select,save"
    TOOLS = "resize,crosshair,pan,wheel_zoom,box_zoom,reset,save"

    # Setting up the bokeh figure
    fig = figure(width=800, height=250, title=title, x_axis_type="datetime",
                 x_range=x_range, y_range=y_range, tools=TOOLS)

    # make the outline "invisible"
    fig.outline_line_color = 'white'

    # change just some things about the x-grid
    fig.xgrid.grid_line_color = None
    fig.ygrid.grid_line_color = None
    # change just some things about the y-grid

    fig.yaxis.minor_tick_line_color = None

    year = 2016
    dec = Span(location=datetime(year-1, 12, 1, 0, 0, 0).timestamp() * 1000,
                    dimension='height', line_color='grey', line_dash='dashed', line_width=1)
    jan = Span(location=datetime(year, 1, 1, 0, 0, 0).timestamp() * 1000,
               dimension='height', line_color='grey', line_dash='dashed', line_width=1)
    feb = Span(location=datetime(year, 2, 1, 0, 0, 0).timestamp() * 1000,
               dimension='height', line_color='grey', line_dash='dashed', line_width=1)
    mar = Span(location=datetime(year, 3, 1, 0, 0, 0).timestamp() * 1000,
               dimension='height', line_color='grey', line_dash='dashed', line_width=1)
    apr = Span(location=datetime(year, 4, 1, 0, 0, 0).timestamp() * 1000,
               dimension='height', line_color='grey', line_dash='dashed', line_width=1)
    may = Span(location=datetime(year, 5, 1, 0, 0, 0).timestamp() * 1000,
               dimension='height', line_color='grey', line_dash='dashed', line_width=1)

    fig.renderers.extend([dec, jan, feb, mar, apr, may])

    return fig
