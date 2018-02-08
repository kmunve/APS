# -*- coding: utf-8 -*-

import os
from jinja2 import Environment, FileSystemLoader

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

env = Environment(loader=FileSystemLoader(THIS_DIR))


def render_zc_dangerlevel():
    # Render json file containing plot configurations
    json_tmpl_file = 'tmpl_zc_dangerlevel.json'
    json_tmpl = env.get_template(json_tmpl_file)

    var = {
        'time_axis': {"min-value": 1420232400000,
                      "step": "day",
                      "transform": {"type": "date", "all": "%D<br>%d %M %y"}
                      },
        'danger_level': [1,2,3,3,4,3,2,2,2,3,2,1,1,1,2,2,3,4,4]
    }

    json_conf_file = os.path.join(THIS_DIR, json_tmpl_file.split('tmpl_')[1])
    json_tmpl.stream(var).dump(json_conf_file)

    # Render HTML file containing page information
    html_tmpl_file = 'tmpl_zc_base.html'
    html_tmpl = env.get_template(html_tmpl_file)

    var = {
        'page_title': 'Danger level',
        'zing_chart_id': 'dl_chart_1',
        'json_conf_file': json_conf_file
    }

    html_file = os.path.join(THIS_DIR, html_tmpl_file.split('tmpl_')[1])
    html_tmpl.stream(var).dump(html_file)


if __name__ == "__main__":
    render_zc_dangerlevel()





