import json

with open("../api/temperature_distribution_by_elevation.json") as fid:
    td = json.load(fid)
    for i in td["Dates"][0]["Temperatures"]["ElevationBands"]:
        print(i["Minimum"], i["FirstQuartile"], i["Median"], i["ThirdQuartile"], i["Maximum"])
