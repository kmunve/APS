# -*- coding: utf-8 -*-
__author__ = 'raek'
__updated__ = 'kmu'

import requests
# import datetime
# import getdangers as gd
# import makelogs as md
# import types


def get_warnings_as_json(region_ids, start_date, end_date, lang_key=1, simple=False, recursive_count=5):
    """Selects warnings and returns the json structured result as given on the api.

    :param region_id:       [int or list of ints] RegionID as given in the forecast api [1-99] or in regObs [101-199]
    :param start_date:      [date or string as yyyy-mm-dd]
    :param end_date:        [date or string as yyyy-mm-dd]
    :param simple:          [bool] default "False" - returns a minimum of data when True (used for speed-up)
    :param recursive_count  [int] by default atempt the same request # times before giving up
    :return warnings:       [string] String as json

    Eg. http://api01.nve.no/hydrology/forecast/avalanche/v2.0.2/api/AvalancheWarningByRegion/Detail/10/1/2013-01-10/2013-01-20
    """

    # If input isn't a list, make it so
    if not isinstance(region_ids, list):
        region_ids = [region_ids]

    warnings = []
    recursive_count_default = recursive_count   # need the default for later

    for region_id in region_ids:

        if len(region_ids) > 1:
            # if we are looping the initial list make sure each item gets the recursive count default
            recursive_count = recursive_count_default

        # if region_id > 100:
        #     region_id = region_id - 100

        if simple:
            api_type = 'Simple'
        else:
            api_type = 'Detail'

        # md.log_and_print("getForecastApi -> get_warnings_as_json: Getting AvalancheWarnings for {0} from {1} til {2}"\
        #     .format(region_id, start_date, end_date))

        url = "https://api01.nve.no/hydrology/forecast/avalanche/v4.0.0/api/AvalancheWarningByRegion/{4}/{0}/{3}/{1}/{2}"\
            .format(region_id, start_date, end_date, lang_key, api_type)

        # If at first you don't succeed, try and try again.
        try:
            warnings += requests.get(url).json()
            # md.log_and_print("getForecastApi -> get_warnings_as_json: {0} warnings found for {1}.".format(len(warnings), region_id))

        except:
            # md.log_and_print("getForecastApi -> get_warnings_as_json: EXCEPTION. RECURSIVE COUNT {0}".format(recursive_count))
            if recursive_count > 1:
                recursive_count -= 1        # count down
                warnings += get_warnings_as_json(region_id, start_date, end_date, lang_key, recursive_count=recursive_count)
                # TODO: remove line below and use proper logging
                print("Rec", recursive_count)

    return warnings, url

'''
def get_warnings(region_ids, start_date, end_date, lang_key=1):
    """Selects warnings and returns a list of AvalancheDanger Objects. This method does NOT add the
    avalanche problems to the warning.

    :param region_id:   [int or list of ints]       RegionID as given in the forecast api [1-99] or in regObs [101-199]
    :param start_date:  [date or string as yyyy-mm-dd]
    :param end_date:    [date or string as yyyy-mm-dd]

    :return avalanche_danger_list: List of AvalancheDanger objects
    """

    warnings = get_warnings_as_json(region_ids,start_date, end_date, lang_key=lang_key)
    avalanche_danger_list = []

    for w in warnings:
        region_id = int(w['RegionId'])
        region_name = w['RegionName']
        date = datetime.datetime.strptime(w['ValidFrom'][0:10], '%Y-%m-%d').date()
        danger_level = int(w['DangerLevel'])
        danger_level_name = w['DangerLevelName']
        author = w['Author']
        avalanche_forecast = w['AvalancheDanger']
        avalanche_nowcast = w['AvalancheWarning']

        danger = gd.AvalancheDanger(region_id, region_name, 'Forecast API', date, danger_level, danger_level_name)
        danger.set_source('Varsel')
        danger.set_nick(author)
        danger.set_avalanche_nowcast(avalanche_nowcast)
        danger.set_avalanche_forecast(avalanche_forecast)

        if lang_key == 1:
            danger.set_main_message_no(w['MainText'])
        if lang_key == 2:
            danger.set_main_message_en(w['MainText'])

        avalanche_danger_list.append(danger)

    # Sort by date
    avalanche_danger_list = sorted(avalanche_danger_list, key=lambda AvalancheDanger: AvalancheDanger.date)

    return avalanche_danger_list
'''

def get_valid_regids(region_id, start_date, end_date):
    """Method looks up all forecasts for a region and selects and returns the RegIDs used in regObs. Thus, the list of
    RegIDs are for published forecasts.

    :param region_id:   [int]       RegionID as given in the forecast api [1-99] or in regObs [101-199]
    :param start_date:  [string]    date as yyyy-mm-dd
    :param end_date:    [string]    date as yyyy-mm-dd
    :return:            {RegID:date, RegID:date, ...}
    """

    warnings = get_warnings_as_json(region_id, start_date, end_date)
    valid_regids = {}

    for w in warnings:
        danger_level = int(w["DangerLevel"])
        if danger_level > 0:
            valid_regids[w["RegId"]] = w["ValidFrom"]

    return valid_regids


if __name__ == "__main__":

    import datetime as dt
    import pandas as pd
    # get data for Bardu (112) and Tamokdalen (129)
    # warnings_for_129 = get_warnings([129, 118, 131], dt.date(2016, 4, 1), dt.date(2016, 4, 2))
    warns_json = get_warnings_as_json([129, 118, 131], dt.date(2016, 4, 1), dt.date(2016, 4, 2),
                                      simple=True, lang_key=1, recursive_count=5)
    # p = get_valid_regids(10, "2013-03-01", "2013-03-09")

    # Retrieve danger level for a specific region
    # TODO: make the output two separate lists - one containing DL the other date
    dl = [{warns['ValidFrom']: warns['DangerLevel']} for warns in warns_json if warns['RegionId']==29]

    df = pd.DataFrame(warns_json[0]) # all elements get doubled when converting to DataFrame
    # conversion to dataframe does not work with api_type='Simple' - but maybe I don't need the dataframe at all.
    print(warns_json[0]['DangerLevel'], warns_json[0]['AvalancheWarning'])
    print('---')
    print(df['DangerLevel'], df['AvalancheWarning'])
    a = 1