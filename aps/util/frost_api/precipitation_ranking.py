"""
This script will provide a sorted list of Norwegian precipitation gauges sorted after the amount of precipitation measured over the last 24 hours.
"""
import requests
import pandas as pd
import json
import datetime
from frost_client_id import get_client_id


print(pd.__version__)
CLIENT_ID = get_client_id()

# Use todays date - precip-day goes from 06 the previous day to 06 today. So it is mainly yesterday's precip.
REFERENCE_TIME = datetime.date.today().strftime('%Y-%m-%d')
# In case you want one day back swap datetime.date.today() by (datetime.date.today() - datetime.timedelta(days=1)).

try:
    """
    Try to load the list of precip stations from file.
    If the file does not exists it retrieves the list via the Frost API.
    """
    with open('precip_stations.json', 'r') as fh:
        station_list = json.load(fh)

except FileNotFoundError:
    # Get station list via Frost-API
    # Define endpoint and parameters for station request
    endpoint = 'https://frost.met.no/observations/availableTimeSeries/v0.jsonld'
    parameters = {
        'elements': 'sum(precipitation_amount P1D)',
        'timeoffsets': 'PT6H',  # can also use 'default'
        'referencetime': REFERENCE_TIME
    }
    # Issue an HTTP GET request
    r = requests.get(endpoint, parameters, auth=(CLIENT_ID, ''))
    # Extract JSON data
    rj = r.json()

    # Check if the request worked, print out any errors
    if r.status_code == 200:
        data = rj['data']
        print('Data retrieved from frost.met.no!')
    else:
        print('Error! Returned status code %s' % r.status_code)
        print('Message: %s' % rj['error']['message'])
        print('Reason: %s' % rj['error']['reason'])

    # This will return a Dataframe with all of the observations in a table format
    df = pd.DataFrame(data)
    station_list = df['sourceId'].apply(lambda x: x[:-2]).tolist()  # removes the ":0" part from the station ID string
    # Open output file for writing
    with open('precip_stations.json', 'w') as fh:
        json.dump(station_list, fh)

# Make request for precip data from all stations within station_list
# Define endpoint and parameters for observation request
endpoint = 'https://frost.met.no/observations/v0.jsonld'
parameters = {
    'sources': ",".join(station_list),
    'elements': 'sum(precipitation_amount P1D)',
    'timeoffsets': 'PT6H',  # can also use 'default'
    'referencetime': REFERENCE_TIME,  # e.g. '2022-10-06'
    'levels': 'default',
    'qualities': '0,1,2,3,4'
}
# Issue an HTTP GET request
# TODO: split up station list such that I make multiple requests and stack them at the end. Otherwise the URL gets too long.
r = requests.get(endpoint, parameters, auth=(CLIENT_ID, ''))
rj = r.json()

# Check if the request worked, print out any errors
if r.status_code == 200:
    data = rj['data']
    print('Data retrieved from frost.met.no!')
else:
    print('Error! Returned status code %s' % r.status_code)
    print('Message: %s' % rj['error']['message'])
    print('Reason: %s' % rj['error']['reason'])

# This will return a Dataframe with all of the observations in a table format
df = pd.DataFrame()
for i in range(len(data)):
    row = pd.DataFrame(data[i]['observations'])
    row['referenceTime'] = data[i]['referenceTime']
    row['sourceId'] = data[i]['sourceId']
    df = df.append(row)
    # TODO: replace df.append by pandas.concat()

df = df.reset_index()

# These additional columns will be kept
columns = ['elementId', 'timeOffset', 'referenceTime', 'sourceId', 'value', 'unit']
df2 = df[columns].copy()
# Convert the time value to something Python understands
df2['referenceTime'] = pd.to_datetime(df2['referenceTime'])
df2.sort_values('value', ascending=False, inplace=True)
df2.to_csv("precip_ranking_date.csv", index=False)
a = 1



