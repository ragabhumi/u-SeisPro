import create_vel2grid, create_grid2time, create_nlloc
import os

os.chdir('../nlloc')
# create_vel2grid.vel2grid()
# os.system('../aux/NLLoc/Vel2Grid run/vel2grid.in')

# create_grid2time.grid2time()
# os.system('../aux/NLLoc/Grid2Time run/grid2time.in')

create_nlloc.nlloc()
os.system('../aux/NLLoc/NLLoc run/nlloc.in')