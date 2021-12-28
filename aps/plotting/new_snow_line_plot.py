import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('seaborn-notebook')
plt.rcParams['figure.figsize'] = (14, 12)

"""
Procedure

Calculate new snow line based on wetBulb_altitude using the script new_snow_line.py.

Execute GetTimeSerieData in SQL Studio and save result as <region_id>_newsnoline<year>.csv
Execute GetTimeSerieData in SQL Studio and save result as <region_id>_0isoterm<year>.csv
"""

REGION_ID = 3035

# Load data for new snow line calculated in *new_snow_line.py*
nsl = pd.read_csv(r"C:\Users\kmu\PycharmProjects\APS\aps\scripts\tmp\new_snow_line_{0}_20201201_20210531.csv".format(REGION_ID), sep=";", parse_dates=['Date'])
nsl['Altitude_nsl'] = np.clip(nsl['Altitude'], a_min=0, a_max=None)
# group by day and keep only the highest value of 00, 06, 12, or 18 o'clock
nsl_gr = nsl.groupby(by='Date', as_index=False).max()

# Load data for new snow line from APS db
# Used for extraction: exec GetTimeSerieData @RegionId='3034.0', @parameter='2014', @FromDate='2020-12-01', @ToDate='2021-05-31', @Model='met_obs_v2.0'
db = pd.read_csv(r"C:\Users\kmu\PycharmProjects\APS\aps\scripts\tmp\{0}_newsnowline2021.csv".format(REGION_ID), sep=";", parse_dates=['Time'])
db['Altitude_wetB'] = np.clip(db['Value'], a_min=0, a_max=None)
db['Date'] = db['Time'].apply(lambda x: pd.Timestamp(x.date()))
db['Hour'] = db['Time'].apply(lambda x: x.hour)
# group by day and keep only the highest value of 00, 06, 12, or 18 o'clock
db_gr = db.groupby(by='Date', as_index=False).max()

# Load data for 0-isotherm from APS db
db_0iso = pd.read_csv(r"C:\Users\kmu\PycharmProjects\APS\aps\scripts\tmp\{0}_0isoterm2021.csv".format(REGION_ID), sep=";", parse_dates=['Time'])
db_0iso['Altitude_0iso'] = np.clip(db_0iso['Value'], a_min=0, a_max=None)
db_0iso['Date'] = db_0iso['Time'].apply(lambda x: pd.Timestamp(x.date()))
db_0iso['Hour'] = db_0iso['Time'].apply(lambda x: x.hour)
# group by day and keep only the highest value of 00, 06, 12, or 18 o'clock
db_0iso_gr = db_0iso.groupby(by='Date', as_index=False).max()

# Load varsom-data containing published mountain-weather
aw2 = pd.read_csv(r"C:\Users\kmu\PycharmProjects\varsomdata\varsomdata\{0}_forecasts_20_21.csv".format(REGION_ID), sep=";", header=0, index_col=0, parse_dates=['valid_from', 'date_valid'])
aw2['Date'] = aw2['date_valid']

# Merge all into one dataframe for plotting and analysis
_merged = pd.merge(nsl_gr, db_gr, how='left', on='Date', suffixes=['_nsl', '_wetB'])
_merged2 = pd.merge(_merged, db_0iso_gr, how='left', on='Date', suffixes=['_nsl', '_APSwetB'])
_merged3 = pd.merge(_merged2, aw2, how='left', on='Date', suffixes=['_nsl', '_APS0iso'])

_merged3.set_index('Date', inplace=True)
_merged3['precip10'] = _merged3['mountain_weather_precip_region'] * 10

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)
_merged3.filter(['mountain_weather_freezing_level', 'Altitude_nsl', 'precip10']).plot.area(alpha=0.5, stacked=False, ax=ax1, title=REGION_ID)
_merged3.filter(['mountain_weather_freezing_level', 'Altitude_wetB', 'precip10']).plot.area(alpha=0.5, stacked=False, ax=ax2)
_merged3.filter(['mountain_weather_freezing_level', 'Altitude_0iso', 'precip10']).plot.area(alpha=0.5, stacked=False, ax=ax3)

_merged3['diff_nsl'] = _merged3['mountain_weather_freezing_level'] - _merged3['Altitude_nsl']
_merged3['diff_wetB'] = _merged3['mountain_weather_freezing_level'] - _merged3['Altitude_wetB']
_merged3['diff_0iso'] = _merged3['mountain_weather_freezing_level'] - _merged3['Altitude_0iso']

plt.tight_layout()
#plt.grid()
plt.savefig('{0}_nsl_comparison.png'.format(REGION_ID), dpi=90)
plt.show()

print(_merged3['diff_nsl'].where(_merged3['mountain_weather_precip_region'] > 1.0).describe())
print(_merged3['diff_wetB'].where(_merged3['mountain_weather_precip_region'] > 1.0).describe())
print(_merged3['diff_0iso'].where(_merged3['mountain_weather_precip_region'] > 1.0).describe())

print(nsl['Date'].iloc[0])
print(aw2['Date'].iloc[0])
print(db_gr['Date'].iloc[0])
print(db_0iso_gr['Date'].iloc[0])

print(nsl['Date'].iloc[-1])
print(aw2['Date'].iloc[-1])
print(db_gr['Date'].iloc[-1])
print(db_0iso_gr['Date'].iloc[-1])

def print_stats(var):
    print("{0}: Mean: {1:.1f} +/-{2:.1f} [Min:{2:.1f}, Max:{3:.1f}]".format(var.name, var.mean(), var.std(), var.min(), var.max()))

print("\nOverall stats:")
print_stats(_merged3['diff_nsl'])
print_stats(_merged3['diff_wetB'])
print_stats(_merged3['diff_0iso'])
precip_threshold = 1.0
print("\nFor days with precip > {0}mm:".format(precip_threshold))
print_stats(_merged3['diff_nsl'].where(_merged3['mountain_weather_precip_region'] > precip_threshold))
print_stats(_merged3['diff_wetB'].where(_merged3['mountain_weather_precip_region'] > precip_threshold))
print_stats(_merged3['diff_0iso'].where(_merged3['mountain_weather_precip_region'] > precip_threshold))
