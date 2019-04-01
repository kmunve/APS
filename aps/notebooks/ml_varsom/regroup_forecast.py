import json
import numpy as np


def get_sensitivity(trigger, probability):
    t = int(trigger)
    p = int(probability)

    if t == 10 and p == 2:
        s = 1  # very difficult to trigger
    elif t == 10 and p == 3:
        s = 2  # difficult to trigger
    elif t == 21 and p == 3:
        s = 3  # easy to trigger
    elif t == 21 and p == 5:
        s = 4  # very easy to trigger
    elif t == 21 and p == 7:
        s = 4  # very easy to trigger
    elif t == 22 and p == 2:
        s = 5  # very difficult / difficult / easy to trigger + natural
    elif t == 22 and p == 3:
        s = 5  # very difficult / difficult / easy to trigger + natural
    elif t == 22 and p == 5:
        s = 6  # very easy to trigger + natural
    elif t == 22 and p == 7:
        s = 6  # very easy to trigger + natural
    else:
        s = 0
    return s


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
    df['mountain_weather_wind_speed_num'] = df['mountain_weather_wind_speed'].apply(
        lambda val: snoskred_keys['beaufort_scale_no'][val])
    df['mountain_weather_wind_direction_num'] = df['mountain_weather_wind_direction'].apply(
        lambda val: 0 if val is None else snoskred_keys['wind_dir_conv_en'][val])

    # Re-group AvalancheProblemType
    for i in range(1, 4):
        # AvalancheProblemType grouped by PWL, wet slab, wet loose, dry loose, storm slab, and wind slab
        # (and glide avalanche).
        df[f'avalanche_problem_{i}_problem_type_id_class'] = df[f'avalanche_problem_{i}_problem_type_id'].apply(
            lambda val: 0 if val == np.nan else np.int(snoskred_keys['Class_AvalancheProblemTypeId'][str(val)]))

        # Adding a sensitivity class based on trigger and probability.
        df[f'avalanche_problem_{i}_sensitivity_id_class'] = df.apply(
            lambda row: get_sensitivity(row[f'avalanche_problem_{i}_trigger_simple_id'],
                                        row[f'avalanche_problem_{i}_probability_id']), axis=1)

        # Class_AvalTriggerSimple grouped to 1, 2, 3 instead of 10, 21, 22.
        df[f'avalanche_problem_{i}_trigger_simple_id_class'] = df[f'avalanche_problem_{i}_trigger_simple_id'].apply(
            lambda val: 0 if val == np.nan else np.int(snoskred_keys['Class_AvalTriggerSimpleId'][str(val)]))

        # Distribution is labeled _Propagation_ in the API and has five classes. Change name to _AvalDistribution and merge the upper three classes into one called _widespread_.
        # df[f'avalanche_problem_{i}_distribution_id'] = df[f'avalanche_problem_{i}_propagation_id'].apply(
        #    lambda i: 0 if str(i) == str(np.nan) else np.int(snoskred_keys['Class_AvalDistributionId'][str(int(i))]))

    # Group the forecasting regions
    df['region_group_id'] = df['region_id'].apply(lambda i: snoskred_keys['region_group'][str(i)])
    return df


if __name__ == "__main__":
    import pandas as pd
    varsom_df = pd.read_csv(r'..\..\data\varsom\norwegian_avalanche_warnings_season_17_18.csv', index_col=0)
    varsom_df['mountain_weather_wind_speed'] = varsom_df['mountain_weather_wind_speed'].fillna('None')
    varsom_df['mountain_weather_wind_direction'] = varsom_df['mountain_weather_wind_direction'].fillna('None')
    df = regroup(varsom_df)

    k = 'm'
