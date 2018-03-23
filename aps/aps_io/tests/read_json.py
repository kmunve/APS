import json

with open("../api/temperature_distribution_by_elevation.json") as fid:
    td = json.load(fid)
    for dt in td["Dates"]:
        print(dt["Date"])
        for reg in dt["Regions"]:
            print(reg["RegionName"])
            for eb in reg["ElevationBands"]:
                print(eb["Minimum"], eb["FirstQuartile"], eb["Median"], eb["ThirdQuartile"], eb["Maximum"])
