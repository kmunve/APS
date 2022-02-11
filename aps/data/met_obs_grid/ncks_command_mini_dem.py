"""
Extract a 20 by 20 km grid based on x-y coordinates from a netCDF file containing data on the xgeo-grid.
"""
# Input
INFILE = r"/mnt/grid/metdata/config/xgeo_dem.nc"
VAR = "xgeo_dem_2"
IX = 9  # number between 0 and 59  ------IX=10 and IY=15 is Hemsedal
IY = 14  # number between 0 and 77

# Config
X_LEFT = -75000.0
X_RIGHT = 1119000.0
Y_BOTTOM = 6450000.0
Y_TOP = 7999000.0
CELL_SIZE = 1000.0
NX = 1195
NY = 1550
X_START, Y_START = 15, 5
XY_STEP = 20
XY_OFFSET = 19

# ncks using coordinates
print("\nncks using coordinates:")
xl = X_LEFT+X_START*CELL_SIZE+CELL_SIZE*XY_STEP*IX
xr = xl+CELL_SIZE*XY_OFFSET
yb = Y_BOTTOM+Y_START*CELL_SIZE+CELL_SIZE*XY_STEP*IY
yt = yb+CELL_SIZE*XY_OFFSET
ncks_cmd_coord = "ncks -v {var} -d x,{xl:0.1f},{xr:0.1f} -d y,{yb:0.1f},{yt:0.1f} {infile} {var}_extr{ix:02}{iy:02}.nc".format(
    var=VAR, xl=xl, xr=xr, yb=yb, yt=yt, ix=IX, iy=IY,
    infile=INFILE
)
print(ncks_cmd_coord)

# ncks using indicies
print("\nncks using indicies:")
xl = X_START+XY_STEP*IX
xr = xl+XY_OFFSET
yb = Y_START+XY_STEP*IY
yt = yb+XY_OFFSET
ncks_cmd_coord = "ncks -v {var} -d x,{xl},{xr} -d y,{yb},{yt} {infile} {var}_extr{ix:02}{iy:02}i.nc".format(
    var=VAR, xl=xl, xr=xr, yb=yb, yt=yt, ix=IX, iy=IY,
    infile=INFILE
)
print(ncks_cmd_coord)

"""
ncks can also be run with a selection of cells/points by repeating the "-d" option e.g.:
ncks -v air_temperature_2m -d time,24,48 -d x,245 -d y,300 -d x,260 -d y,320 -d x,300 -d y,400 /mnt/grid/metdata/prognosis/meps/det/archive/2022/meps_det_1km_20220207T00Z.nc air_temperature_2m_cells.nc
Note: if x, or y are given without decimal they indicate an index, using decimals will indicate coordinates.
"""
