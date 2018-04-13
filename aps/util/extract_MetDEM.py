import netCDF4

nc = netCDF4.Dataset(r'Y:\metdata\prognosis\meps\det\archive\2018\meps_det_pp_1km_20180413T00Z.nc', 'r')

dem = nc.variables['altitude']



