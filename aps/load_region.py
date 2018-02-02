import os
import numpy as np
from netCDF4 import Dataset


def load_region(region_id, local=False):
    _vr = Dataset(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), r"data/terrain_parameters/VarslingsOmr_2017.nc"), "r")
    if local:
        # flip up-down becuase Meps data is upside down
        _regions = np.flipud(_vr.variables["LokalOmr_2018"][:])

    else:
        # flip up-down becuase Meps data is upside down
        _regions = np.flipud(_vr.variables["VarslingsOmr_2017"][:])

    _region_mask = np.where(_regions == region_id)

    # get the lower left and upper right corner of a rectangle around the region
    y_min, y_max, x_min, x_max = min(_region_mask[0].flatten()), max(_region_mask[0].flatten()), \
                                 min(_region_mask[1].flatten()), max(_region_mask[1].flatten())

    reg_mask = np.ma.masked_where(_regions[y_min:y_max, x_min:x_max] == region_id, _regions[y_min:y_max, x_min:x_max]).mask

    _vr.close()

    return reg_mask, y_min, y_max, x_min, x_max


def clip_region(nc_variable, region_mask, t_index, y_min, y_max, x_min, x_max):
    s = len(nc_variable.shape)

    if s == 2:
        return np.flipud(region_mask * nc_variable[y_min:y_max, x_min:x_max])
    if s == 3:
        return np.flipud(region_mask * nc_variable[t_index, y_min:y_max, x_min:x_max])
    if s == 4:
        return np.flipud(region_mask * nc_variable[t_index, 0, y_min:y_max, x_min:x_max])


if __name__ == "__main__":
    region_mask, y_min, y_max, x_min, x_max = load_region(3012)
    print(region_mask, type(region_mask))

