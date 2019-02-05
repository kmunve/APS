from numpy import arange, meshgrid, empty
from abc import ABCMeta, abstractmethod
from pyproj import Proj


class ModelGrid(metaclass=ABCMeta):
    """Creates a spatial grid"""
    def __init__(self):
        self.var_name = ''  # name of the modelled variable

    @abstractmethod # flags method that MUST be implemented by all subclasses
    def to_netCDF(self, filename):
        pass

    @property
    @abstractmethod
    def _convert_to_CS(self):
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}, Abstract base class for model grids."


class SeNorgeGrid(ModelGrid):
    def __init__(self, var_name: str):
        super(ModelGrid, self).__init__()
        self.var_name = var_name
        # lower left corner in m
        self.LowerLeftEast = -75000
        self.LowerLeftNorth = 6450000
        # upper right corner in m
        self.UpperRightEast = 1120000
        self.UpperRightNorth = 8000000
        # interval
        self.dx = 1000
        self.dy = 1000

        self.x = arange(self.LowerLeftEast, self.UpperRightEast, self.dx)
        self.y = arange(self.LowerLeftNorth, self.UpperRightNorth, self.dy)

        self.number_of_cells = len(self.x) * len(self.y)

        self.values = empty(shape=(len(self.x), len(self.y)), dtype=float)

    def _convert_to_CS(self):
        # Converts vector into coordinate system
        self.xgrid, self.ygrid = meshgrid(self.x, self.y)
        self.p = Proj('+proj=utm +zone=33 +ellps=WGS84 +datum=WGS84 +units=m +no_defs')
        self.lon, self.lat = self.p(self.xgrid, self.ygrid, inverse=True)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.var_name}: #cells: x({len(self.x)}) by y({len(self.y)}) = {self.number_of_cells}," \
               f" resolution: {self.dx} by {self.dy} m)"

    def to_netCDF(self, filename):
        """
        Saves the data in netCDF format
        :return: a netCDF file containing the data and metadata of the grid
        """
        pass

    def from_netCDF(self, netcdf_file):
        """
        Import data and metadata from a netCDF file
        :param netcdf_file: NetCDF file to load
        """
        pass

    def from_BIL(self, bil_file):
        """
        Import grid data from a BIL file.
        :param bil_file: Binary data file
        """
        pass

    def from_ndarray(self, arr):
        """

        :param arr: numpy array of shape (self.y, self.x)
        :return:
        """
        self.values = arr

if __name__ == "__main__":
    sg = SeNorgeGrid('Temperature')
    print(sg)
