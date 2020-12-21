def vel2grid():
    file = open('../nlloc/run/vel2grid.in', 'w')

    # =============================================================================
    # Generic control file statements
    # =============================================================================
    file.write('CONTROL 1 54321\n')

    # map projection / transformation
    lon_center = 124.93972194
    lat_center = -3.39514888
    file.write('TRANS  SIMPLE  %f  %f  0.0\n' %(lat_center, lon_center))

    # =============================================================================
    # Vel2Grid control file statements
    # =============================================================================
    # Layer 2DGrid
    file.write('VGOUT  ./model/layer\n')
    # wave type
    file.write('VGTYPE P\nVGTYPE S\n')

    # number of nodes along x/y/z axis
    num_grid_x = 501
    num_grid_y = 501
    num_grid_z = 81
    # x location of grid origin (0,0,0) in km pos east
    orig_grid_x = 0
    # y location of grid origin (0,0,0) in km pos north
    orig_grid_y = 0
    # z location of grid origin (0,0,0) in km pos down
    orig_grid_z = -0.2
    # grid spacing along  x/y/z axis
    d_grid_x = 1
    d_grid_y = 1
    d_grid_z = 1
    type_grid = 'SLOW_LEN'
    file.write('VGGRID  %i %i %i  %f %f %f  %f %f %f  %s\n' % (num_grid_x, num_grid_y, num_grid_z, orig_grid_x, orig_grid_y, orig_grid_z, d_grid_x, d_grid_y, d_grid_z, type_grid))
    # velocity model description
    # Model IASP-91
    file.write('LAYER   0.2  5.8000 0.00    3.3600  0.00  2.7200 0.0\n')
    file.write('LAYER   0.0  5.8000 0.00    3.3600  0.00  2.7200 0.0\n')
    file.write('LAYER  20.0  6.5000 0.00    3.7500  0.00  2.9200 0.0\n')
    file.write('LAYER  35.0  8.0400 0.00    4.4700  0.00  3.3198 0.0\n')
    file.write('LAYER  80.8  8.0450 0.00    4.4850  0.00  3.3455 0.0\n')

    file.close()