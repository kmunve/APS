import requests
import pandas as pd
import matplotlib.pyplot as plt


# Get the predication and put them in a dataframe
URL_pred = "http://skred01.dmz.nve.no/model/pred"

req = requests.get(URL_pred)
pred = pd.DataFrame.from_dict(req.json(), orient='index')
pred.index = pd.to_datetime(pred.index)

# Make a dataframe for each region and compare danger levels from models with published DLs.
IDS = [
    3003,
    3006,
    3007,
    3009,
    3010,
    3011,
    3012,
    3013,
    3014,
    3015,
    3016,
    3017,
    3022,
    3023,
    3024,
    3027,
    3028,
    3029,
    3031,
    3032,
    3034,
    3035,
    3037
]

DL_correlations = dict()

for REGION_ID in IDS:

    pred_reg = pd.DataFrame(pred[str(REGION_ID)].tolist(), index=pred.index)

    pred_dl = pd.DataFrame(pred_reg['dl'].tolist(), index=pred_reg.index)

    pred_dl.plot()
    # plt.tight_layout()

    pred_detailed = pd.DataFrame(pred_reg['detailed'].tolist(), index=pred_reg.index)

    pred_detailed['danger_level'].plot(label='DL modelled')
    # plt.tight_layout()

    # Get published data
    start_date = pred.index[0].date()
    stop_date = pred.index[-1].date()
    URL_pub = 'https://api01.nve.no/hydrology/forecast/avalanche/v6.0.1/api/AvalancheWarningByRegion/Simple/{0}/1/{1}/{2}'.format(REGION_ID, start_date, stop_date)
    req = requests.get(URL_pub)

    pub = pd.DataFrame(req.json())
    pub['Date'] = pub["ValidFrom"].apply(pd.Timestamp)
    pub['DangerLevel'] = pub['DangerLevel'].apply(int)
    pub.set_index('Date', inplace=True)
    pub['DangerLevel'].plot(label='DL published')
    plt.legend()
    plt.title(REGION_ID)
    plt.tight_layout()

    plt.savefig("ML_{0}.png".format(REGION_ID))
    plt.close()

    DL_correlations[REGION_ID] = pub.filter(['DangerLevel']).corrwith(pred_detailed['danger_level'])
    # plt.show()


# print(DL_correlations)
DL_correlations = pd.DataFrame.from_dict(DL_correlations, orient='index')
DL_correlations.plot.bar()
plt.savefig('DL_correlations.png')
pos = "end"
