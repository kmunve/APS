import threddsclient
import xarray as xr
from netCDF4 import Dataset, num2date


def read_netcdfs(files, dim, transform_func=None):
    def process_one_path(path):
        # use a context manager, to ensure the file gets closed after use
        with xr.open_dataset(path) as ds:
            # transform_func should do some sort of selection or
            # aggregation
            if transform_func is not None:
                ds = transform_func(ds)
            # load all data from the transformed dataset, to ensure we can
            # use it after closing each original file
            ds.load()
            return ds

    #paths = sorted(glob(files))
    paths = files
    datasets = [process_one_path(p) for p in paths]
    combined = xr.concat(datasets, dim)
    return combined


urls = threddsclient.opendap_urls(r'https://thredds.met.no/thredds/catalog/radarnowcasting/catalog.html')
url_list = list(reversed(urls[:144]))
nc1 = xr.open_dataset(urls[0], decode_times=True)
t = nc1.time[:]
nc2 = nc1.isel(time=[0])

# here we suppose we only care about the combined mean of each file;
# you might also use indexing operations like .sel to subset datasets
combined = read_netcdfs(url_list, dim='time',
                        transform_func=lambda ds: ds.isel(time=[0]))  # keep only the last time index from each dataset

# from https://docs.xarray.dev/en/stable/user-guide/io.html

#ds = Dataset(r"https://thredds.met.no/thredds/fileServer/radarnowcasting/yrwms-nordic.mos.pcappi-0-rr.noclass-clfilter-novpr-clcorr-block.nordiclcc-1000.20221021T194500Z.nc")
#ds = Dataset(r"https://thredds.met.no/thredds/dodsC/radarnowcasting/yrwms-nordic.mos.pcappi-0-rr.noclass-clfilter-novpr-clcorr-block.nordiclcc-1000.20221021T193500Z.nc")

# for i in range(24):
#     nc = xr.open_dataset(urls[i], decode_times=True)

a = 1

combined.to_netcdf("radar_precip.nc")
