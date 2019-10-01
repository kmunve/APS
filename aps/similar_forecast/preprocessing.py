from pandas.api.types import is_numeric_dtype

import pandas as pd
import numpy as np

import warnings
try:
    import cPickle as pickle
except ImportError:
    import pickle
    print("Using pickle instead of cPickle!")

warnings.simplefilter('ignore')


# Load data
v_df = pd.read_csv('https://raw.githubusercontent.com/kmunve/APS/master/aps/notebooks/ml_varsom/varsom_ml_preproc_3y.csv', index_col=0) # where is the time stamp?)
v_df.drop_duplicates(keep='first', inplace=True) # for some reason all rows appear twice
# print(v_df.describe())


# Convert dates to correct format
v_df['date'] = v_df['date'].apply(lambda d: pd.to_datetime(d))
v_df['month'] = v_df['date'].apply(lambda d: d.month)
v_df.drop(v_df[v_df['month'].isin([6, 7, 8, 9, 10, 11])].index, inplace=True)

v_df['num_date'] = v_df['date'].apply(lambda d: d.timestamp())
v_df.sort_values(by='date', inplace=True)
# print(v_df.describe())


# Keep only numeric columns
num_cols = [var for var in v_df.columns.values if is_numeric_dtype(v_df[var])]
#print(len(num_cols))


# Drop features that are related to the forecast we want to predict and features that should have no influence
drop_list = [
    'danger_level',
    'aval_problem_1_combined',
    'avalanche_problem_1_cause_id',
    'avalanche_problem_1_destructive_size_ext_id',
    'avalanche_problem_1_distribution_id',
    'avalanche_problem_1_exposed_height_1',
    'avalanche_problem_1_exposed_height_2',
    'avalanche_problem_1_ext_id',
    'avalanche_problem_1_probability_id',
    'avalanche_problem_1_problem_id',
    'avalanche_problem_1_problem_type_id',
    'avalanche_problem_1_trigger_simple_id',
    'avalanche_problem_1_type_id',
    'avalanche_problem_2_cause_id',
    'avalanche_problem_2_destructive_size_ext_id',
    'avalanche_problem_2_distribution_id',
    'avalanche_problem_2_exposed_height_1',
    'avalanche_problem_2_exposed_height_2',
    'avalanche_problem_2_ext_id',
    'avalanche_problem_2_probability_id',
    'avalanche_problem_2_problem_id',
    'avalanche_problem_2_problem_type_id',
    'avalanche_problem_2_trigger_simple_id',
    'avalanche_problem_2_type_id',
    'avalanche_problem_3_cause_id',
    'avalanche_problem_3_destructive_size_ext_id',
    'avalanche_problem_3_distribution_id',
    'avalanche_problem_3_exposed_height_1',
    'avalanche_problem_3_exposed_height_2',
    'avalanche_problem_3_ext_id',
    'avalanche_problem_3_probability_id',
    'avalanche_problem_3_problem_id',
    'avalanche_problem_3_problem_type_id',
    'avalanche_problem_3_trigger_simple_id',
    'avalanche_problem_3_type_id',
    'avalanche_problem_1_problem_type_id_class',
    'avalanche_problem_1_sensitivity_id_class',
    'avalanche_problem_1_trigger_simple_id_class',
    'avalanche_problem_2_problem_type_id_class',
    'avalanche_problem_2_sensitivity_id_class',
    'avalanche_problem_2_trigger_simple_id_class',
    'avalanche_problem_3_problem_type_id_class',
    'avalanche_problem_3_sensitivity_id_class',
    'avalanche_problem_3_trigger_simple_id_class',
    'emergency_warning_Ikke gitt',
    'emergency_warning_Naturlig utløste skred',
    'author_Andreas@nve',
    'author_Eldbjorg@MET',
    'author_Espen Granan',
    'author_EspenN',
    'author_Halvor@NVE',
    'author_HåvardT@met',
    'author_Ida@met',
    'author_Ingrid@NVE',
    'author_John Smits',
    'author_JonasD@ObsKorps',
    'author_Julie@SVV',
    'author_Jørgen@obskorps',
    'author_Karsten@NVE',
    'author_MSA@nortind',
    'author_Matilda@MET',
    'author_Odd-Arne@NVE',
    'author_Ragnar@NVE',
    'author_Ronny@NVE',
    'author_Silje@svv',
    'author_Tommy@NVE',
    'author_ToreV@met',
    'author_anitaaw@met',
    'author_emma@nve',
    'author_haso@nve.no',
    'author_heidi@nve.no',
    'author_jan arild@obskorps',
    'author_jegu@NVE',
    'author_jostein@nve',
    'author_knutinge@svv',
    'author_magnush@met',
    'author_martin@svv',
    'author_ragnhildn@met',
    'author_rue@nve',
    'author_siri@met',
    'author_solveig@NVE',
    'author_torehum@svv',
    'author_torolav@obskorps',
    'mountain_weather_wind_direction_E',
    'mountain_weather_wind_direction_N',
    'mountain_weather_wind_direction_NE',
    'mountain_weather_wind_direction_NW',
    'mountain_weather_wind_direction_None',
    'mountain_weather_wind_direction_Not given',
    'mountain_weather_wind_direction_S',
    'mountain_weather_wind_direction_SE',
    'mountain_weather_wind_direction_SW',
    'mountain_weather_wind_direction_W'
]

# Take out region_id and date as reference
reference_names = ['region_id', 'num_date', 'date']
y_df = v_df[reference_names]
y = y_df.values

X_df = v_df.filter(num_cols).drop(drop_list, axis='columns')
X = X_df.values
feature_names = X_df.columns.values

# Store for further processing/usage
with open('knn_preprocessed.pck', 'wb') as f:
    pickle.dump((X, y), f)

# Continue with train_knn_model.py
