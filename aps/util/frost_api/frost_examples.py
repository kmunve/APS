import requests
import pandas as pd

from frost_client_id import get_client_id


"""
from https://frost.met.no/langex_python
"""


def get_stations_with_element(elem='sum(precipitation_amount P1D)'):

    client_id = get_client_id()
    # "https://frost.met.no/observations/availableTimeSeries/v0.jsonld?referencetime=2017-01-01&elements=sum(precipitation_amount%20PT10M)"
    # Define endpoint and parameters
    endpoint = 'https://frost.met.no/observations/availableTimeSeries/v0.jsonld'
    parameters = {
        'elements': elem,
        'timeoffsets': 'PT6H',
        'referencetime': '2022-10-02'
    }
    # Issue an HTTP GET request
    r = requests.get(endpoint, parameters, auth=(client_id, ''))
    # Extract JSON data
    json = r.json()

    # Check if the request worked, print out any errors
    if r.status_code == 200:
        data = json['data']
        print('Data retrieved from frost.met.no!')
    else:
        print('Error! Returned status code %s' % r.status_code)
        print('Message: %s' % json['error']['message'])
        print('Reason: %s' % json['error']['reason'])

    # This will return a Dataframe with all of the observations in a table format
    df = pd.DataFrame(data)
    # for i in range(len(data)):
    #     # row = pd.DataFrame(data[i]['sourceId'])
    #     # row['referenceTime'] = data[i]['referenceTime']
    #     row['sourceId'] = data[i]['sourceId']
    #     df = df.append(row)

    # df = df.reset_index()

    print(df.head)
    df.to_csv("precip24h_stations.csv", index=False)

    return df['sourceId']




def get_element_info():
    """
    retrieve information about a certain element (parameter) or search for part of element-name.
    :return:
    """
    client_id = get_client_id()
    # Get all elements that hav "precipitation" in their id
    url = r"https://frost.met.no/elements/v0.jsonld?ids=*precipitation*&lang=en-US"

    rsp = requests.get(url, auth=(client_id, ''))

    print(rsp.text)


def get_time_series():
    """

    :return:
    """
    client_id = get_client_id()
    url = r"https://frost.met.no/observations/v0.jsonld?referencetime=2019-12-16/2019-12-17&elements=sum(precipitation_amount%20PT10M)&sources=SN55420"
    rsp = requests.get(url, auth=(client_id, ''))
    print(rsp.json())
    data = rsp.json()

    print("{0} observations".format(data["currentItemCount"]))

    for d in data["data"]:
        station_id = d["sourceId"]
        dt = d["referenceTime"]
        for o in d["observations"]:
            element_id = o["elementId"]
            value = o["value"]
            unit = o["unit"]

            print("{0}\t{1}\t{2}: {3} {4}".format(station_id, element_id, dt, value, unit))


def get_timeseries_df():
    """
    NOT WORKING YET!!!
    :return:
    """
    client_id = get_client_id()

    # Define endpoint and parameters
    endpoint = 'https://frost.met.no/observations/v0.jsonld'
    parameters = {
        'sources': 'SN18700,SN90450',
        'elements': 'mean(air_temperature P1D),sum(precipitation_amount P1D),mean(wind_speed P1D)',
        'referencetime': '2022-10-01/2022-10-02',
    }
    # Issue an HTTP GET request
    r = requests.get(endpoint, parameters, auth=(client_id, ''))
    # Extract JSON data
    json = r.json()

    # Check if the request worked, print out any errors
    if r.status_code == 200:
        data = json['data']
        print('Data retrieved from frost.met.no!')
    else:
        print('Error! Returned status code %s' % r.status_code)
        print('Message: %s' % json['error']['message'])
        print('Reason: %s' % json['error']['reason'])

    # This will return a Dataframe with all of the observations in a table format
    df = pd.DataFrame()
    for i in range(len(data)):
        row = pd.DataFrame(data[i]['observations'])
        row['referenceTime'] = data[i]['referenceTime']
        row['sourceId'] = data[i]['sourceId']
        df = df.append(row)

    df = df.reset_index()

    print(df.head)

    # These additional columns will be kept
    columns = ['sourceId', 'referenceTime', 'elementId', 'value', 'unit', 'timeOffset']
    df2 = df[columns].copy()
    # Convert the time value to something Python understands
    df2['referenceTime'] = pd.to_datetime(df2['referenceTime'])

    print(df2.head)


def get_latest_daily_precip():
    """
    Get a list of stations that measure daily precipitation sum.
    Return that list sorted after 24h precipitation descending.

    Steps:
    - get a list of all station in Norway (or a subregion) that measure 24h precipitation sum.
    - retrieve precippitation sum for last 24h from all these stations
    - sort this list by precipitation descending
    """
    client_id = get_client_id()
    station_list = get_stations_with_element().tolist()


    # Define endpoint and parameters
    endpoint = 'https://frost.met.no/observations/v0.jsonld'
    parameters = {
        'sources': ",".join(station_list),
        'elements': 'mean(air_temperature P1D),sum(precipitation_amount P1D),mean(wind_speed P1D)',
        'referencetime': '2022-10-01/2022-10-02',
    }
    # Issue an HTTP GET request
    r = requests.get(endpoint, parameters, auth=(client_id, ''))
    # Extract JSON data
    json = r.json()

    # Check if the request worked, print out any errors
    if r.status_code == 200:
        data = json['data']
        print('Data retrieved from frost.met.no!')
    else:
        print('Error! Returned status code %s' % r.status_code)
        print('Message: %s' % json['error']['message'])
        print('Reason: %s' % json['error']['reason'])

    # This will return a Dataframe with all of the observations in a table format
    df = pd.DataFrame()


#
# """
#
# This program shows how to retrieve info for a single source from the Frost service.
#
# The HTTP request essentially consists of the following components:
#   - the endpoint, frost.met.no/sources
#   - the source ID to get information for
#   - the client ID used for authentication
#
# The source ID is read from a command-line argument, while the client ID is read from
# the environment variable CLIENTID.
#
# Save the program to a file example.py, make it executable (chmod 755 example.py),
# and run it e.g. like this:
#
#   $ CLIENTID=8e6378f7-b3-ae4fe-683f-0db1eb31b24ec ./example.py SN18700
#
# or like this to get info for sources matching a pattern:
#
#   $ CLIENTID=8e6378f7-b3-ae4fe-683f-0db1eb31b24ec ./example.py SN187*
#
# (Note: the client ID used in the example should be replaced with a real one)
#
# The program has been tested on the following platforms:
#   - Python 2.7.3 on Ubuntu 12.04 Precise
#   - Python 2.7.12 and 3.5.2 on Ubuntu 16.04 Xenial
#
# """
#
# import sys, os
# import requests # See http://docs.python-requests.org/
#
# def get_source_info():
#
#     # extract command-line argument
#     if len(sys.argv) != 2:
#        sys.stderr.write('usage: ' + sys.argv[0] + ' <source ID>\n')
#        sys.exit(1)
#     source_id = sys.argv[1]
#
#     # extract environment variable
#     if not 'CLIENTID' in os.environ:
#         sys.stderr.write('error: CLIENTID not found in environment\n')
#         sys.exit(1)
#     client_id = os.environ['CLIENTID']
#
#     # issue an HTTP GET request
#     r = requests.get(
#         'https://frost.met.no/sources/v0.jsonld',
#         {'ids': source_id},
#         auth=(client_id, '')
#     )
#
#     def codec_utf8(s):
#         #return s.encode('utf-8').decode('utf-8') # should be used for Python 3
#         return s.encode('utf-8') # should be used for Python 2
#
#     # extract some data from the response
#     if r.status_code == 200:
#         for item in r.json()['data']:
#             sys.stdout.write('ID: {}\n'.format(item['id']))
#             sys.stdout.write('Name: {}\n'.format(codec_utf8(item['name'])))
#             if 'geometry' in item:
#                 sys.stdout.write('longitude: {}\n'.format(item['geometry']['coordinates'][0]))
#                 sys.stdout.write('latitude: {}\n'.format(item['geometry']['coordinates'][1]))
#             if 'municipality' in item:
#                 sys.stdout.write('Municipality: {}\n'.format(codec_utf8(item['municipality'])))
#             if 'county' in item:
#                 sys.stdout.write('County: {}\n'.format(codec_utf8(item['county'])))
#             sys.stdout.write('Country: {}\n'.format(codec_utf8(item['country'])))
#             if 'externalIds' in item:
#                 for ext_id in item['externalIds']:
#                     sys.stdout.write('external ID: {}\n'.format(ext_id))
#             else:
#                 sys.stdout.write('no external IDs found\n')
#     else:
#         sys.stdout.write('error:\n')
#         sys.stdout.write('\tstatus code: {}\n'.format(r.status_code))
#         if 'error' in r.json():
#             assert(r.json()['error']['code'] == r.status_code)
#             sys.stdout.write('\tmessage: {}\n'.format(r.json()['error']['message']))
#             sys.stdout.write('\treason: {}\n'.format(r.json()['error']['reason']))
#         else:
#             sys.stdout.write('\tother error\n')



if __name__ == "__main__":
    # a = get_client_id()
    # get_element_info()
    # get_time_series()
    # get_timeseries_df()
    station_series = get_stations_with_element()
    station_list = station_series.tolist()
    # get_latest_daily_precip()

    a = 1
