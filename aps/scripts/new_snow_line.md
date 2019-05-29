# Calculation of new snow line

 1. Split latest precipitation for a given date into 6h-chunks
 2. Determine if precipitation sum within at least 5% of the cells within a region and chunk exceeds 1mm/6h
 3. Load latest 24h-period from _altitude_of_isoTprimW_equal_0_ for given date
 4. Keep only the highest value for each cell within each 6h period [0-6, 6-12, 12-18, 18-25]
 5. Calculate the 90%-percentile of the highest values in each 6h period that exceeds a precipitation of 1mm/6h
 6. Round the the values for each period to the nearest 100 m (negative values a clipped to 0)
 7. Provide highest elevation and its respective period to the mountain-weather in regVarsel
 
 
 ## Data:
 
 Folder: \\nve.no\fil\grid\metdata\prognosis\meps\det\archive\
 Precipitation: *precipitation_amount* in *meps_det_pp_1km_<data>.nc*
 New snow line: *altitude_of_isoTprimW_equal_0* in *meps_det_extracted_1km_<date>.nc*