import os
import numpy as np
from netCDF4 import Dataset


def load_region(region_id):
    _vr = Dataset(os.path.join(os.path.dirname(os.path.abspath(__file__)), r"data/terrain_parameters/VarslingsOmr_2017.nc"), "r")

    _regions = _vr.variables["VarslingsOmr_2017"][:]

    _region_mask = np.where(_regions == region_id)

    # get the lower left and upper right corner of a rectangle around the region
    y_min, y_max, x_min, x_max = min(_region_mask[0].flatten()), max(_region_mask[0].flatten()), \
                                 min(_region_mask[1].flatten()), max(_region_mask[1].flatten())

    reg_mask = np.ma.masked_where(_regions[y_min:y_max, x_min:x_max] == region_id, _regions[y_min:y_max, x_min:x_max]).mask

    return reg_mask, y_min, y_max, x_min, x_max


def clip_region(nc_variable, region_mask, y_min, y_max, x_min, x_max):
    return region_mask * nc_variable[0, y_min:y_max, x_min:x_max]


if __name__ == "__main__":
    region_mask, y_min, y_max, x_min, x_max = load_region(3012)
    print(region_mask, type(region_mask))

