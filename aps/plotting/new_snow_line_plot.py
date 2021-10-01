import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('seaborn-notebook')
plt.rcParams['figure.figsize'] = (14, 6)


# Load data for new snow line
nsl = pd.read_csv(r"C:\Users\kmu\PycharmProjects\APS\aps\scripts\tmp\new_snow_line_3024_20200201_20200401.csv", sep=";", parse_dates=['Date'])
nsl['Altitude_0'] = np.clip(nsl['Altitude'], a_min=0, a_max=None)
# group by day and keep only the highest value of 00, 06, 12, or 18 o'clock
nsl_gr = nsl.groupby(by='Date', as_index=False).max()

# Load data for new snow line from APS db
db = pd.read_csv(r"C:\Users\kmu\PycharmProjects\APS\aps\scripts\tmp\new_snow_line_db_90perc_3024_20200201_20200401.csv", sep=" ", parse_dates=['Date'])

# group by day and keep only the highest value of 00, 06, 12, or 18 o'clock
db_gr = db.groupby(by='Date', as_index=False).max()


aw = pd.read_csv(r"C:\Users\kmu\PycharmProjects\varsomdata\localstorage\norwegian_avalanche_warnings_season_19_20.csv", sep=";", header=0, index_col=0, parse_dates=['valid_from', 'date_valid'])
print(aw.columns)

date_filter = (aw['date_valid'] >= nsl['Date'].iloc[0]) & (aw['date_valid'] <= nsl['Date'].iloc[-1])
region_filter = aw['region_id'] == 3024
aw2 = aw[region_filter]
aw2 = aw2[date_filter]
aw2['precip'] = aw2['mountain_weather_precip_region']*10
#
# pd.join

aw3 = pd.merge(aw2, nsl_gr, how='right', left_on='date_valid', right_on='Date')
aw3 = pd.merge(aw3, db_gr, how='right', left_on='date_valid', right_on='Date')

aw3['diff_alt0'] = aw3['mountain_weather_freezing_level'] - aw3['Altitude_0']
aw3['diff_altdb'] = aw3['mountain_weather_freezing_level'] - aw3['Altitude_db']


fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)
aw2.plot.bar(x='date_valid', y='mountain_weather_freezing_level', alpha=0.5, ax=ax1)
nsl_gr.plot.bar(x='Date', y='Altitude_0', alpha=0.5, color='orange', ax=ax1)
db_gr.plot.bar(x='Date', y='Altitude_db', alpha=0.5, color='darkgrey', ax=ax1)

aw2.plot.bar(x='date_valid', y='mountain_weather_precip_region', ax=ax2)
# nsl_gr.plot.scatter(x='Date', y='Altitude_std', ax=ax2) # TODO: make as error bars yerr=[...]

aw3.plot.bar(x='date_valid', y='diff_alt0', alpha=0.5, color='orange', ax=ax3)
aw3.plot.bar(x='date_valid', y='diff_altdb', alpha=0.5, color='darkgrey', ax=ax3)
plt.tight_layout()
plt.grid()
plt.show()

print(nsl['Date'].iloc[-1])
print(aw2['date_valid'].iloc[-1])