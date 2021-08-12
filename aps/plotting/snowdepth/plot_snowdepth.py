import numpy as np
import pandas as pd
from jinja2 import Template, Environment, FileSystemLoader

sd_data = pd.read_csv('SnowDepthGridTimeSerieFromXgeo.csv', sep=';', header=1, parse_dates=['Date'])
print(sd_data.head())


file_loader = FileSystemLoader('.')
env = Environment(loader=file_loader)

html = env.get_template('snowdepth.html')

out = html.render(data=sd_data.values)
print(out)
a = 1