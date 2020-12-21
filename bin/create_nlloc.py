import glob
import os

def nlloc():
    file = open('../nlloc/run/nlloc.in', 'w')

    # =============================================================================
    # Generic control file statements
    # =============================================================================
    file.write('CONTROL 1 54321\n')

    # map projection / transformation
    lon_center = 124.93972194
    lat_center = -3.39514888
    file.write('TRANS  SIMPLE  %f  %f  0.0\n' %(lat_center, lon_center))

    # =============================================================================
    # NLLoc control file statements
    # =============================================================================
    file.write('LOCSIG u-SeisPro\n')
    file.write('LOCCOM Microearthquake Project\n')

    # input  grid filenames root, output filename
    list_pick = glob.glob('.././pick/*')
    pick_filename = max(list_pick, key=os.path.getctime) # Newest pick file
    file.write('LOCFILES %s NLLOC_OBS  ./time/layer  ./loc/microearthquake\n' %pick_filename)

    # output hypocenter file types
    file.write('LOCHYPOUT SAVE_NLLOC_ALL  SAVE_HYPOINV_SUM\n')

    # search type
    init_num_cells_x = 10
    init_num_cells_y = 10
    init_num_cells_z =5
    min_node_size = 0.01
    max_num_nodes = 50000
    num_scatter = 8000
    use_stations_density = 0
    stop_on_min_node_size = 0
    file.write('LOCSEARCH  OCT %i %i %i %f %i %i %i %i\n' % (init_num_cells_x, init_num_cells_y, init_num_cells_z, min_node_size, max_num_nodes, num_scatter, use_stations_density, stop_on_min_node_size))

    # location grids description
    num_grid_x = 501
    num_grid_y = 501
    num_grid_z = 81
    orig_grid_x = 0
    orig_grid_y = 0
    orig_grid_z = -0.2
    d_grid_x = 1
    d_grid_y = 1
    d_grid_z = 1
    type_grid = 'PROB_DENSITY'
    save_flag = 'SAVE'
    file.write('LOCGRID  %i %i %i  %f %f %f %f %f %f   %s  %s\n' % (num_grid_x, num_grid_y, num_grid_z, orig_grid_x, orig_grid_y, orig_grid_z, d_grid_x, d_grid_y, d_grid_z, type_grid, save_flag))

    # Location Method
    file.write('LOCMETH GAU_ANALYTIC 9999.0 3 -1 -1 -1 6\n')

    # gaussian model error parameters
    Sigma_T = 0.25
    CorrLen = 0
    file.write('LOCGAU %f %f\n' % (Sigma_T, CorrLen))

    # phase identifier mapping
    file.write('LOCPHASEID  P   P p G PN PG\n')
    file.write('LOCPHASEID  S   S s G SN SG\n')

    # quality to error mapping (for HYPO71, etc)
    file.write('LOCQUAL2ERR 0.1 0.5 1.0 2.0 99999.9\n')

    # take-off angles mode & minimum quality
    file.write('LOCANGLES ANGLES_YES 5\n')

    # magnitude calculation method
    file.write('LOCMAG ML_HB 0.138 1.110 0.00189\n')

    # phase statistics parameters
    file.write('LOCPHSTAT 9999.0 -1 9999.0 1.0 1.0 9999.9 -9999.9 9999.9\n')

    file.close()