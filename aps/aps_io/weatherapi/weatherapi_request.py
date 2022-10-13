import requests
import json
import datetime


def weatherapi_request(endpoint, parameters):
    # Issue an HTTP GET request
    r = requests.get(endpoint, parameters)

    # Check if the request worked, print out any errors
    if r.status_code == 200:
        print('Data retrieved from {0}'.format(endpoint))
        return r
    else:
        print('Error! Returned status code %s' % r.status_code)
        return r


def subjective_forecasts_available(download=True):
    r = requests.get("https://api.met.no/weatherapi/subjectiveforecast/1.0/available.json")
    rj = r.json()
    with open(r"./output/subjective_map_avail.json", "w") as f:
        json.dump(rj, f)

    if download:
        # Loop over items in list rj
        for i in rj:
            print(i['uri'])
            print(i['params']['product'], i['params']['time'])
            png_r = requests.get(i['uri'])
            # Check if the request worked, print out any errors
            if png_r.status_code == 200:
                with open(r"./output/{0}_{1}.png".format(i['params']['product'], i['params']['time'][:-7]), "wb") as f:
                    f.write(png_r.content)
            else:
                print('Error! Returned status code %s' % png_r.status_code)


def subjective_forecast_latest():
    endpoint = "https://api.met.no/weatherapi/subjectiveforecast/1.0/"

    parameters = {
        'content_type': "image/png",
        'product': "analyse_map"
    }
    # with open(r"./output/subjective_map.png", "wb") as f:
    # f.write(resp.content)
    return weatherapi_request(endpoint, parameters)


def radar():
    endpoint = "https://api.met.no/weatherapi/radar/2.0/"
    parameters = {'area': "norway", 'content': "image", 'typ': "5level_reflectivity"}
    resp = weatherapi_request(endpoint, parameters)
    with open(r"./output/radar_5l_reflectivity.png", "wb") as f:
        f.write(resp.content)


def radar_accumulated(area="western_norway"):
    endpoint = "https://api.met.no/weatherapi/radar/2.0/"

    td = datetime.date.today().strftime('%Y-%m-%d')
    tdh = datetime.datetime.strptime("{0} 00".format(td), "%Y-%m-%d %H")
    h24 = tdh + datetime.timedelta(hours=6)
    h18 = tdh + datetime.timedelta(hours=0)
    h12 = tdh - datetime.timedelta(hours=6)
    h06 = tdh - datetime.timedelta(hours=12)
    h00 = tdh - datetime.timedelta(hours=18)

    t_fmt = '%Y-%m-%dT%H:%M:%SZ'

    parameters = [
        {'area': area, 'time': h06.strftime(t_fmt), 'type': "accumulated_06h", 'content': "image"},
        {'area': area, 'time': h12.strftime(t_fmt), 'type': "accumulated_12h", 'content': "image"},
        {'area': area, 'time': h18.strftime(t_fmt), 'type': "accumulated_18h", 'content': "image"},
        {'area': area, 'time': h24.strftime(t_fmt), 'type': "accumulated_24h", 'content': "image"}
    ]

    for p in parameters:
        resp = weatherapi_request(endpoint, p)
        print(resp.url)
        with open(r"./output/radar_acc_{0}.png".format(p['time'][:-7]), "wb") as f:
            f.write(resp.content)

    a = 1

