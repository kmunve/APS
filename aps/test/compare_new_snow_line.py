import requests
import pandas as pd

dr = pd.date_range('2018-12-01', periods=180, freq='D')
print(dr)

api_url_base = 'http://tst-h-int-api01.nve.no/APSServices/TimeSeriesReader.svc/MountainWeather/<region_id>.0/<date>/no/true'

region_id = 3011

api_url = api_url_base.replace('<region_id>', str(region_id))
print(dr[120].strftime('%Y-%m-%d'))
req = requests.get(api_url.replace('<date>', dr[120].strftime('%Y-%m-%d')))
print(req.json())
#for d in dr:
#    req = requests.get(api_url.replace('<date>', d.strftime('%Y-%m-%d')))


