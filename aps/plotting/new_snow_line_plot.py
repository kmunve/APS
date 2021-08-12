import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('seaborn-notebook')
import matplotlib.patches as patches
plt.rcParams['figure.figsize'] = (14, 6)


# Load data for new snow line
nsl = pd.read_csv(r"C:\Users\kmu\PycharmProjects\APS\aps\scripts\tmp\new_snow_line_20200201.csv", sep=";")

nsl.plot(x='Date', y='Altitude')
plt.show()


aw = pd.read_csv(r"C:\Users\kmu\PycharmProjects\varsomdata\localstorage\norwegian_avalanche_warnings_season_19_20.csv")
print
