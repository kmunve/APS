#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

'''


__author__ = 'kmu'
'''

url = "http://api01.nve.no/hydrology/forecast/avalanche/test/api/AvalancheWarningByRegion/Detail"
payload = {'regionid': '3016', 'langkey': '1', 'startdate': '2017-01-02', 'enddate': '2017-01-05'}

#r = requests.get(url, params=payload)
r = requests.post(url, data=payload)
print(r.url)
print(r.text)
