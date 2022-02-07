from regobslib import *
import datetime as dt
import pandas as pd
import matplotlib.pylab as plt


def get_data():
    regions = [
        SnowRegion.HELGELAND,
        SnowRegion.SALTEN,
        SnowRegion.OFOTEN,
        SnowRegion.LOFOTEN_OG_VESTERALEN,
    ]
    print("Fetching APS data from 2021 in Nordland")
    conn = Connection(prod=False)
    aps = conn.get_aps(dt.date(2021, 1, 1), dt.date(2022, 1, 1), regions)
    print("Writing all data to all_data.csv")
    aps.to_frame().to_csv("all_data.csv", sep=";")
    print("Writing data valid at 500 m to 500m.csv")
    five_hundred = aps.to_frame(elevation=500)
    five_hundred.to_csv("500m.csv", sep=";")
    print("Writing data from level 4 to level4.csv")
    level4 = aps.to_frame(level_index=4)
    level4.to_csv("level4.csv", sep=";")
    print("Writing data from Ofoten to ofoten.csv")
    april = aps[SnowRegion.OFOTEN].to_frame()
    april.to_csv("ofoten.csv", sep=";")
    print("Writing data from april to april.csv")
    april = aps[dt.date(2021, 4, 1): dt.date(2021, 5, 1)].to_frame()
    april.to_csv("april.csv", sep=";")
    print("Writing data from Salten in March to salten_march.csv")
    salten_march = aps[SnowRegion.SALTEN][dt.date(2021, 3, 1): dt.date(2021, 4, 1)].to_frame()
    salten_march.to_csv("salten_march.csv", sep=";")


def read_all_data():
    df = pd.read_csv("all_data.csv", sep=";", header=[0, 1, 2], index_col=[0, 1], infer_datetime_format=True)
    print(df.describe())
    for col in df.columns:
        print(col)
    print("DF --------------\n", df.head(10))
    a = df['new_snow', '50']
    print("A---------\n", a.head(10))
    a.plot()
    plt.show()
    pos='end'


if __name__ == "__main__":
    # get_data()
    read_all_data()