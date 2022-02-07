"""
Extract a 20 by 20 km grid based on x-y coordinates from a netCDF file containing data on the xgeo-grid.
"""
# Input
INFILE = r"/mnt/grid/metdata/prognosis/meps/det/archive/2022/meps_det_1km_20220207T00Z.nc" #"/mnt/grid/metdata/config/xgeo_dem.nc"
VAR = "air_temperature_2m" #"xgeo_dem_2"
IX = 10  # number between 0 and 59  ------IX=10 and IY=15 is Hemsedal
IY = 15  # number between 0 and 77
TIME_START = 24  # usually the 24h minus model run time e.g., 24-6=18 for the 06-run.
TIME_STOP = TIME_START+23

# Config
X_LEFT = -75000.0
X_RIGHT = 1119000.0
Y_BOTTOM = 6450000.0
Y_TOP = 7999000.0
CELL_SIZE = 1000.0
NX = 1195
NY = 1550
X_START, Y_START, XY_STEP = 15, 5, 20


 #TODO: Currently both commands create 21x21 pixel grids, should be 20x20

# ncks using coordinates
print("\nncks using coordinates:")
xl = X_LEFT+X_START*CELL_SIZE+CELL_SIZE*XY_STEP*IX
xr = xl+CELL_SIZE*XY_STEP
yb = Y_BOTTOM+Y_START*CELL_SIZE+CELL_SIZE*XY_STEP*IY
yt = yb+CELL_SIZE*XY_STEP
ncks_cmd_coord = "ncks -v {var} -d time,{t0},{t1} -d x,{xl:0.1f},{xr:0.1f} -d y,{yb:0.1f},{yt:0.1f} {infile} {var}_extr{ix}{iy}.nc".format(
    var=VAR, xl=xl, xr=xr, yb=yb, yt=yt, ix=IX, iy=IY, t0=TIME_START, t1=TIME_STOP,
    infile=INFILE
)
print(ncks_cmd_coord)

# ncks using indicies
print("\nncks using indicies:")
xl = X_START+XY_STEP*IX
xr = xl+XY_STEP
yb = Y_START+XY_STEP*IY
yt = yb+XY_STEP
ncks_cmd_coord = "ncks -v {var} -d time,{t0},{t1} -d x,{xl},{xr} -d y,{yb},{yt} {infile} {var}_extr{ix}{iy}.nc".format(
    var=VAR, xl=xl, xr=xr, yb=yb, yt=yt, ix=IX, iy=IY, t0=TIME_START, t1=TIME_STOP,
    infile=INFILE
)
print(ncks_cmd_coord)

"""
ncks can also be run with a selection of cells/points by repeating the "-d" option e.g.:
ncks -v air_temperature_2m -d time,24,48 -d x,245 -d y,300 -d x,260 -d y,320 -d x,300 -d y,400 /mnt/grid/metdata/prognosis/meps/det/archive/2022/meps_det_1km_20220207T00Z.nc air_temperature_2m_cells.nc
Note: if x, or y are given without decimal they indicate an index, using decimals will indicate coordinates.
"""
