import numpy as np
import xarray as xr
import datetime as dt

from netCDF4 import Dataset, num2date
from pathlib import Path


class SeNorgeDomain:
    # TODO: write docs
    def __init__(self):
        # XGEO grid set-up
        self.senorge_x_left = -75000.0
        self.senorge_x_right = 1119000.0
        self.senorge_y_bottom = 6450000.0
        self.senorge_y_top = 7999000.0
        self.senorge_cell_size = 1000.0
        self.senorge_nx = 1195
        self.senorge_ny = 1550

    def __repr__(self):
        return f"{self.__class__.__name__}, class describing the SeNorge grid domain. More information on www.senorge.no"


class SeNorgeSubDomain(SeNorgeDomain):
    # TODO: write docs
    def __init__(self, ix, iy, x_step=20, y_step=20):
        """
        ix: number between 0 and 59
        iy: number between 0 and 77
        E.g. ix=10 and iy=15 is Hemsedal

        x_step: extent in number of cells in x-direction
        y_step: extent in number of cells in y-direction
        """
        SeNorgeDomain.__init__(self)
        self.region_id = f"{ix:02}{iy:02}"
        self.x_step = x_step
        self.y_step = y_step

        # set boundaries and increments
        self.x_start = 15  # number of cells to ignore on the left side of the SeNorge domain
        self.y_start = 5  # number of cells to ignore on the bottom of the SeNorge domain
        self.x_offset = 20  # same as x/y_step - might be needed when using ncks and non-python indexing
        self.y_offset = 20

        # using indices
        self.xli = self.x_start + self.x_step * ix
        self.xri = self.xli + self.x_offset
        self.ybi = self.y_start + self.y_step * iy
        self.yti = self.ybi + self.y_offset

        # using coordinates
        self.xlc = self.senorge_x_left + self.xli * self.senorge_cell_size
        self.xrc = self.xlc + self.x_offset * self.senorge_cell_size
        self.ybc = self.senorge_y_bottom + self.ybi * self.senorge_cell_size
        self.ytc = self.ybc + self.y_offset * self.senorge_cell_size

    def __repr__(self):
        info_str = f"{self.__class__.__name__}, class describing a rectangular sub-doman of the SeNorge grid.\n" \
                   f"More information on www.senorge.no\n" \
                   f"\n" \
                   f"Index: Lower left (x, y): {self.xli}, {self.ybi}. Upper right (x,y):  {self.xri}, {self.yti}\n" \
                   f"UTM33N: Lower left (x, y): {self.xlc}, {self.ybc}. Upper right (x,y):  {self.xrc}, {self.ytc}."
        return info_str


class MiniRegion:
    # TODO: write docs
    def __init__(self, irx, iry, date=dt.datetime.now().date(), nwp_hour=0):
        # set grid index ranges
        self.irx = irx  # SeNorgeDomain index range in x-direction
        self.iry = iry  # SeNorgeDomain index range in y-direction
        self.nx = irx[1]-irx[0]
        self.ny = iry[1]-iry[0]
        self.nt = 24  # number of time intervals, TODO: ensure that it is correct for 3-h data

        # set date information
        self.date = date  # Date of the weather and snow pack variables are valid for, default: current day.
        self.nwp_hour = nwp_hour  # Hour the numerical weather prediction (NWP) model was initiated, default: 0.
        self.date_filestr = "{d}T{h:02}Z".format(d=self.date.strftime("%Y%m%d"), h=self.nwp_hour)
        self.met_prognosis_path = Path(r"Y:\metdata\prognosis\meps\det\archive") / str(self.date.year)  # TODO: move to config file
        self.met_prognosis_file = "meps_det_1km_{df}.nc".format(df=self.date_filestr)
        self.irt = (self.nt-nwp_hour, (2*self.nt)-nwp_hour)  # set the time index, based on NWP initiation time. Is 00-00 the day after self.date.
        self.nci = np.s_[self.irt[0]:self.irt[1], self.iry[0]:self.iry[1], self.irx[0]:self.irx[1]]  # set the index slice, size (24, 20, 20)

        # declare and set elevation information for the region
        self.elevations = None
        self.elevation_boundaries = None
        self.mean_elevation = None
        self.elevation_masks = None
        self.set_elevation_ranges()
        self.get_elevation_masks()

        # retrieve meteorological data from corresponding netCDF file(s)
        self.get_meteorology()

    def __repr__(self):
        return f"{self.__class__.__name__}, class describing an APS mini region."

    def set_elevation_ranges(self, elevation_boundaries=[300, 600, 900, 1200, 1500, 1800, 2100, 2400]):  # TODO: move to config file
        self.elevation_boundaries = elevation_boundaries

    def get_elevation_masks(self):
        # TODO: place nc-file in config
        ncfile = r"Y:\metdata\config\xgeo_dem.nc"  # TODO: move to config file
        xds = xr.open_dataset(ncfile)

        self.elevations = xds["xgeo_dem_2"][self.iry[0]:self.iry[1], self.irx[0]:self.irx[1]]
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

    def get_meteorology(self):
        nc_file = Dataset(self.met_prognosis_path / self.met_prognosis_file, 'r')

        self.nc_time = nc_file.variables["time"][self.irt[0]:self.irt[1]]
        self.nc_time_dt = num2date(nc_file.variables["time"][self.irt[0]:self.irt[1]], nc_file.variables["time"].units)
        # temperature data
        air_temperatures = nc_file.variables["air_temperature_2m"][self.nci]
        self.air_temperature_mean = air_temperatures.mean()

        # wind data
        x_wind = nc_file.variables["x_wind_10m"][self.nci]
        y_wind = nc_file.variables["y_wind_10m"][self.nci]
        wind_speed = np.sqrt(x_wind**2 + y_wind**2)
        self.wind_speed_mean = wind_speed.mean()
        self._wsp = wind_speed

        # cloudiness
        cloud_fraction = nc_file.variables["cloud_area_fraction"][self.nci]
        self.cloud_fraction_mean = cloud_fraction.mean()

        # Freezing level and rain-snow boundary
        # altitude_of_0_degree_isotherm = nc_file.variables["altitude_of_0_degree_isotherm"][self.nci]
        # self.altitude_of_0_degree_isotherm_mean = altitude_of_0_degree_isotherm.mean()
        altitude_of_isoTprimW_equal_0 = nc_file.variables["altitude_of_isoTprimW_equal_0"][self.nci]
        self.altitude_of_isoTprimW_equal_0_mean = altitude_of_isoTprimW_equal_0.mean()

        # Precipitation
        # Since we need to subtract element-wise form the accumulated values we need the previous acc.precip. values.
        __precip_i = np.s_[self.irt[0]:self.irt[1]+1, self.iry[0]:self.iry[1], self.irx[0]:self.irx[1]]  # index of precip values before the time-slice we are using
        precipitation_amount_acc = nc_file.variables["precipitation_amount_acc"][__precip_i]
        self.precip_acc = precipitation_amount_acc[:]
        self.precip_hour = np.diff(precipitation_amount_acc[:, :, :], n=1, axis=0)#, prepend=__precip_amount_prev)

        self.precip_acc_1 = precipitation_amount_acc[:, 10, 10]
        self.precip_hour_1 = np.diff(self.precip_acc_1, n=1, axis=0)  # TODO: need to include the previous value
        # TODO: need to calculate the precip per hour instead of accumulated.











