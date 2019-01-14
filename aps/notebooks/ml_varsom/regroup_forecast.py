import json
import numpy as np

def regroup(df_in):
    """
    Re-classification of some parameters in an avalanche warning from varsom.no to aid machine learning.

    :param df_in: pandas DataFrame containing avalanche warnings from varsom.no
    :return df: a copy of df_in with extra columns containing the re-classed parameters
    """
    with open(r'../../config/snoskred_keys.json') as jdata:
        snoskred_keys = json.load(jdata)

    df = df_in.copy()
    # change wind speeds to numerical values
    df['mountain_weather_wind_speed_num'] = df['mountain_weather_wind_speed'].apply(lambda i: snoskred_keys['beaufort_scale_no'][i])
    df['mountain_weather_wind_direction_num'] = df['mountain_weather_wind_direction'].apply(lambda i: 0 if i is None else snoskred_keys['wind_dir_conv_en'][i])

    # Re-group AvalancheProblemType
    for i in range(1, 4):
        # AvalancheProblemType grouped by PWL, wet slab, wet loose, dry loose, storm slab, and wind slab (and glide avalanche).
        df[f'avalanche_problem_{i}_problem_type_id_class'] = df[f'avalanche_problem_{i}_problem_type_id'].apply(
            lambda i: 0 if i == np.nan else np.int(snoskred_keys['Class_AvalancheProblemTypeId'][str(int(i))]))

        # Distribution is labeled _Propagation_ in the API and has five classes. Change name to _AvalDistribution and merge the upper three classes into one called _widespread_.
        #df[f'avalanche_problem_{i}_distribution_id'] = df[f'avalanche_problem_{i}_propagation_id'].apply(
        #    lambda i: 0 if str(i) == str(np.nan) else np.int(snoskred_keys['Class_AvalDistributionId'][str(int(i))]))

    return df