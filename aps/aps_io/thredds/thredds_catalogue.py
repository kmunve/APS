import threddsclient
import xarray as xr
from netCDF4 import Dataset, num2date


def read_netcdfs(files, dim, transform_func=None):
    def process_one_path(path):
        with xr.open_dataset(path) as ds:
            # transform_func should do some sort of selection or aggregation
            if transform_func is not None:
                ds = transform_func(ds)
            # use it after closing each original file
            ds.load()
            return ds

    #paths = sorted(glob(files))
    paths = files
    datasets = [process_one_path(p) for p in paths]
    combined = xr.concat(datasets, dim)
    return combined


urls = threddsclient.opendap_urls(r'https://thredds.met.no/thredds/catalog/radarnowcasting/catalog.html')
url_list = list(reversed(urls[:288]))
nc1 = xr.open_dataset(urls[0], decode_times=True)
t = nc1.time[:]
nc2 = nc1.isel(time=[0])

combined = read_netcdfs(url_list, dim='time',
                        transform_func=lambda ds: ds.isel(time=[0]))  # keep only the last time index from each dataset

combined.to_netcdf("radar_precip.nc")
