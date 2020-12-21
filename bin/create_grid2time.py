def grid2time():
    file = open('../nlloc/run/grid2time.in', 'w')

    # =============================================================================
    # Generic control file statements
    # =============================================================================
    file.write('CONTROL 1 54321\n')

    # map projection / transformation
    lon_center = 124.93972194
    lat_center = -3.39514888
    file.write('TRANS  SIMPLE  %f  %f  0.0\n' %(lat_center, lon_center))

    # =============================================================================
    # Grid2Time control file statements
    # =============================================================================
    wave_type = 'P'
    file.write('GTFILES  ./model/layer  ./time/layer %s\n' % wave_type)

    # time grid modes
    file.write('GTMODE GRID3D ANGLES_YES\n')

    # source description 
    file.write('GTSRCE MEQ1   LATLON   -0.6295      127.5912     0.0  0.047\n')
    file.write('GTSRCE MEQ2   LATLON   -0.6424      127.6447     0.0  0.028\n')
    file.write('GTSRCE MEQ3   LATLON   -0.6825      127.6441     0.0  0.115\n')
    file.write('GTSRCE MEQ4   LATLON   -0.7185      127.6637     0.0  0.017\n')
    file.write('GTSRCE MEQ5   LATLON   -0.7375      127.6306     0.0  0.014\n')

    # Podvin & Lecomte FD params
    file.write('GT_PLFD  1.0e-3  0\n')

    file.close()