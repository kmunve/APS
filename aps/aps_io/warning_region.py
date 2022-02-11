import numpy as np
import xarray as xr


class SeNorgeDomain:

    def __init__(self):
        # XGEO grid set-up
        self.x_left = -75000.0
        self.x_right = 1119000.0
        self.y_bottom = 6450000.0
        self.y_top = 7999000.0
        self.cell_size = 1000.0
        self.nx = 1195
        self.ny = 1550


class MiniRegion:

    def __init__(self, irx, iry):
        # set grid index ranges
        self.irx = irx  # SeNorgeDomain index range in x-direction
        self.iry = iry  # SeNorgeDomain index range in y-direction
        self.nx = irx[1]-irx[0]
        self.ny = iry[1]-iry[0]

        # declare and set elevation information for the region
        self.elevations = None
        self.elevation_boundaries = None
        self.mean_elevation = None
        self.elevation_masks = None
        self.set_elevation_ranges()
        self.get_elevation_masks()

    def set_elevation_ranges(self, elevation_boundaries=[300, 600, 900, 1200, 1500, 1800, 2100, 2400]):
        self.elevation_boundaries = elevation_boundaries

    def get_elevation_masks(self):
        # TODO: place nc-file in config
        ncfile = r"Y:\metdata\config\xgeo_dem.nc"
        xds = xr.open_dataset(ncfile)

        self.elevations = xds["xgeo_dem_2"][self.iry[0]:self.iry[1], self.irx[0], self.irx[1]]
        self.mean_elevation = np.mean(self.elevations)

        # TODO: Make sure self.elevation_boundaries are in ascending order
        self.elevation_masks = {"below_{i}".format(i=self.elevation_boundaries[0]): np.where(self.elevations < self.elevation_boundaries[0], 1, np.nan),
                                "above_{i}".format(i=self.elevation_boundaries[0]): np.where(self.elevations < self.elevation_boundaries[0], np.nan, 1)}
        for i in range(1, len(self.elevation_boundaries)):
            # Now mask everything above the previous interval boundary and below the current interval boundary.
            self.elevation_masks["below_{i}".format(i=self.elevation_boundaries[i])] = np.where(
                self.elevations * self.elevation_masks["above_{i}".format(i=self.elevation_boundaries[i - 1])] < self.elevation_boundaries[i], 1, np.nan)
            self.elevation_masks["above_{i}".format(i=self.elevation_boundaries[i])] = np.where(
                self.elevations < self.elevation_boundaries[i], np.nan, 1)
