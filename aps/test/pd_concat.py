def add_prevday_features(df):
    ### danger level
    df['danger_level_prev1day'] = df['danger_level'].shift(1)
    df['danger_level_name_prev1day'] = df['danger_level_name'].shift(1)
    df['danger_level_prev2day'] = df['danger_level'].shift(2)
    df['danger_level_name_prev2day'] = df['danger_level_name'].shift(2)
    df['danger_level_prev3day'] = df['danger_level'].shift(3)
    df['danger_level_name_prev3day'] = df['danger_level_name'].shift(3)

    ### avalanche problem
    df['avalanche_problem_1_cause_id_prev1day'] = df['avalanche_problem_1_cause_id'].shift(1)
    df['avalanche_problem_1_problem_type_id_prev1day'] = df['avalanche_problem_1_problem_type_id'].shift(1)
    df['avalanche_problem_1_cause_id_prev2day'] = df['avalanche_problem_1_cause_id'].shift(2)
    df['avalanche_problem_1_problem_type_id_prev2day'] = df['avalanche_problem_1_problem_type_id'].shift(2)
    df['avalanche_problem_1_cause_id_prev3day'] = df['avalanche_problem_1_cause_id'].shift(3)
    df['avalanche_problem_1_problem_type_id_prev3day'] = df['avalanche_problem_1_problem_type_id'].shift(3)

    df['avalanche_problem_2_cause_id_prev1day'] = df['avalanche_problem_2_cause_id'].shift(1)
    df['avalanche_problem_2_problem_type_id_prev1day'] = df['avalanche_problem_2_problem_type_id'].shift(1)
    df['avalanche_problem_2_cause_id_prev2day'] = df['avalanche_problem_2_cause_id'].shift(2)
    df['avalanche_problem_2_problem_type_id_prev2day'] = df['avalanche_problem_2_problem_type_id'].shift(2)
    df['avalanche_problem_2_cause_id_prev3day'] = df['avalanche_problem_2_cause_id'].shift(3)
    df['avalanche_problem_2_problem_type_id_prev3day'] = df['avalanche_problem_2_problem_type_id'].shift(3)

    ### weather
    df['mountain_weather_temperature_max_prev1day'] = df['mountain_weather_temperature_max'].shift(1)
    df['mountain_weather_temperature_max_prev2day'] = df['mountain_weather_temperature_max'].shift(2)
    df['mountain_weather_temperature_max_prev3day'] = df['mountain_weather_temperature_max'].shift(3)

    df['mountain_weather_temperature_min_prev1day'] = df['mountain_weather_temperature_min'].shift(1)
    df['mountain_weather_temperature_min_prev2day'] = df['mountain_weather_temperature_min'].shift(2)
    df['mountain_weather_temperature_min_prev3day'] = df['mountain_weather_temperature_min'].shift(3)

    df['mountain_weather_precip_region_prev1day'] = df['mountain_weather_precip_region'].shift(1)
    df['mountain_weather_precip_most_exposed_prev1day'] = df['mountain_weather_precip_most_exposed'].shift(1)
    df['mountain_weather_precip_region_prev3daysum'] = df['mountain_weather_precip_region'].shift(1) + df['mountain_weather_precip_region'].shift(2) + df['mountain_weather_precip_region'].shift(3)


    return df

    df[''] = df[''].shift()

    [
        'danger_level_prev3day',
        'avalanche_problem_1_problem_type_id_prev3day',
        'avalanche_problem_2_problem_type_id_prev3day',
        'avalanche_problem_2_cause_id_prev3day',
        'avalanche_problem_1_cause_id_prev3day',
        'danger_level_prev2day',
        'avalanche_problem_1_cause_id_prev2day',
        'avalanche_problem_1_problem_type_id_prev2day',
        'avalanche_problem_2_cause_id_prev2day',
        'avalanche_problem_2_problem_type_id_prev2day',
        'avalanche_problem_2_cause_id_prev1day',
        'avalanche_problem_2_problem_type_id_prev1day',
        'avalanche_problem_1_problem_type_id_prev1day',
        'avalanche_problem_1_cause_id_prev1day',
        'danger_level_prev1day'
    ]