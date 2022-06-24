import requests
import json
from frost_client import get_client_id


def get_radiation_stations():
    """
    Provide elements and see which stations (sources) have available time series.
    ElementIds can be retrieved from https://frost.met.no/elementtable.
    """
    client_id = get_client_id()
    url = r"https://frost.met.no/observations/availableTimeSeries/v0.jsonld?elements=mean(surface_downwelling_shortwave_flux_in_air PT1H)&fields=sourceId,validFrom,unit,timeResolution"
    rsp = requests.get(url, auth=(client_id, ''))
    print(rsp.text)
    data = rsp.json()
    print(data["totalItemCount"], "stations measuring radiation.")
    station_list, *_ = zip(*data["data"])
    a = 1


if __name__ == "__main__":
    get_radiation_stations()
