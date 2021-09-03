# Calculation of new snow line

- Load latest 24h-period from _altitude_of_isoTprimW_equal_0_ for given date and split into 6h-chunks (00-05, 06-11, 12-17, 18-23)
 - Keep only the highest value for each cell within each 6h period [0-6, 6-12, 12-18, 18-24]
 - Calculate median of the highest values in each 6h period
 - Determine if precipitation sum within at least 5% of the cells within a region and chunk exceeds 1mm/6h
 - Round the the values for each period to the nearest 100 m (negative values a clipped to 0)
 - Provide highest elevation and its respective period to the mountain-weather in regVarsel
 
 
 ## Data:
 
 Folder: \\nve.no\fil\grid\metdata\prognosis\meps\det\archive\
 Precipitation: *precipitation_amount* in *meps_det_pp_1km_<data>.nc*
 New snow line: *altitude_of_isoTprimW_equal_0* in *meps_det_extracted_1km_<date>.nc*
 

## Results

- Altitude for each region for 4 periods a day
- Neglect periods with less than 3mm/6h-period
- Check for variations of more then 300 m in altitude between periods
 - if no variation: use highest altitude value e.g., "Snow above 900 m."
 - if variation >300 m: use highest value and period (night, morning, afternoon, evening) e.g., "Snow above 900 m in the afternoon."  