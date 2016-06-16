#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from bokeh.plotting import figure
'''


__author__ = 'kmu'
'''


def timeline_figure(title=None, x_range=None, y_range=None):

    # TODO: align x-axis

    # TOOLS = "resize,crosshair,pan,wheel_zoom,box_zoom,reset,box_select,lasso_select"
    TOOLS = "resize,crosshair,pan,wheel_zoom,box_zoom,reset"

    # Setting up the bokeh figure
    fig = figure(width=800, height=250, title=title, x_axis_type="datetime",
                 x_range=x_range, y_range=y_range, tools=TOOLS)

    # make the outline "invisible"
    fig.outline_line_color = 'white'

    # change just some things about the x-grid
    fig.xgrid.grid_line_color = None

    # change just some things about the y-grid
    fig.ygrid.grid_line_alpha = 0.5
    fig.ygrid.grid_line_dash = [6, 4]

    return fig
