from datetime import datetime
import math

phase = 0

with open('../nlloc/loc/microearthquake.sum.grid0.loc.hypo_inv') as f_hypoinverse:
    content = f_hypoinverse.read()
    events = content.split("\n\n")

    fileout = '../hypodd/phase.dat'
    f_hypodd = open(fileout, 'w')

    header = [None] * (len(events)-1)
    phase = [None] * (len(events)-1)
    tahun = [None] * (len(events)-1)
    bulan = [None] * (len(events)-1)
    tanggal = [None] * (len(events)-1)
    jam = [None] * (len(events)-1)
    menit = [None] * (len(events)-1)
    detik = [None] * (len(events)-1)
    lat = [None] * (len(events)-1)
    lon = [None] * (len(events)-1)
    depth = [None] * (len(events)-1)
    rms = [None] * (len(events)-1)
    for i in range(len(events)-1):
        event = events[i].split("\n")
        header[i] = event[0]
        phase[i] = event[1:]
        tahun[i] = int('20'+header[i][0:2])
        bulan[i] = int(header[i][2:4])
        tanggal[i] = int(header[i][4:6])
        jam[i] = int(header[i][6:8])
        menit[i] = int(header[i][8:10])
        detik[i] = int(header[i][10:14])/100.0
        if detik[i]==60:
           detik[i]=0
           menit[i]+=1
        origin_time = datetime(year=tahun[i], month=bulan[i], day=tanggal[i], hour=jam[i], minute=menit[i], second=int(math.floor(detik[i])),microsecond=int((detik[i]-math.floor(detik[i]))*1000000))
        if header[i][16]=='S':
            lat[i] = (int(header[i][14:16])+int(header[i][17:21])/100.0/60)*-1
        else:
            lat[i] = (int(header[i][14:16])+int(header[i][17:21])/100.0/60)
        if header[i][24]=='W':
            lon[i] = (int(header[i][21:24])+int(header[i][25:29])/100.0/60)*-1
        else:
            lon[i] = (int(header[i][21:24])+int(header[i][25:29])/100.0/60)
        depth[i] = int(header[i][29:34])/100.0
        rms[i] = int(header[i][45:49])/100.0
        
        header_hdd = ('#  %4s %2s %2s %2s %2s %5.2f %8.4f %9.4f  %6.2f 0.00 0.0 0.0 %4.2f %7i\n'%(tahun[i], bulan[i], tanggal[i], jam[i], menit[i], detik[i], lat[i], lon[i], depth[i], rms[i], i+1))
        f_hypodd.write(header_hdd)
        
        sta = [None] * (len(phase[i]))
        for j in range(len(phase[i])):
            sta[j] = str(phase[i][j][0:4]).lstrip()
            tahun_phase = int('20'+phase[i][j][9:11])
            bulan_phase = int(phase[i][j][11:13])
            tanggal_phase = int(phase[i][j][13:15])
            jam_phase = int(phase[i][j][15:17])
            menit_phase = int(phase[i][j][17:19])
            detik_phase_P = int(phase[i][j][20:24])/100.0

            if detik_phase_P==60.0:
                menit_phase = menit_phase+1
                detik_phase_P = 0
            pick_time_P = datetime(year=tahun_phase, month=bulan_phase, day=tanggal_phase, hour=jam_phase, minute=menit_phase, second=int(math.floor(detik_phase_P)),microsecond=int((detik_phase_P-math.floor(detik_phase_P))*1000000))
            phase_hdd_P = ('{:7}'.format(sta[j])+'%10.3f   1.000   P\n'%((pick_time_P-origin_time).total_seconds()))
            f_hypodd.write(phase_hdd_P)
            
            detik_phase_S = int(phase[i][j][32:36])/100.0

            if detik_phase_S != 0:
                if detik_phase_S < detik_phase_P:
                    menit_phase += 1
                if detik_phase_S == 60:
                    menit_phase += 1
                    detik_phase_S = 0
                if menit_phase == 60:
                    jam_phase += 1
                    menit_phase = 0
                pick_time_S = datetime(year=tahun_phase, month=bulan_phase, day=tanggal_phase, hour=jam_phase, minute=menit_phase, second=int(math.floor(detik_phase_S)),microsecond=int((detik_phase_S-math.floor(detik_phase_S))*1000000))
                phase_hdd_S = ('{:7}'.format(sta[j])+'%10.3f   1.000   S\n'%((pick_time_S-origin_time).total_seconds()))
                f_hypodd.write(phase_hdd_S)
    f_hypodd.close()
