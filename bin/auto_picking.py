from obspy import read, Stream
from obspy.signal.trigger import coincidence_trigger, recursive_sta_lta, ar_pick
from obspy.core import UTCDateTime
from datetime import datetime, timedelta
from createFolder import createFolder

awal = datetime(year=2019,month=1,day=1,hour=0)
tanggal = awal+timedelta(hours=4)

# Read data
data = "../data/%s/%s.*.*.SON.*.*.BH*.R.SAC" %(tanggal.strftime('%Y%j'),tanggal.strftime('%Y.%j.%H'))
st = read(data,format='SAC') 

# Select Z component
st_cp = st.copy()
st_Z = st_cp.select(component="Z")

# Bandpass filter
df = st_Z[0].stats.sampling_rate
st_Z.taper(max_percentage=0.05, type='hann', max_length=None, side='both')
st_Z.filter("bandpass", freqmin=1, freqmax=20, corners=4, zerophase=False)

# Earthquake detection
triggers = coincidence_trigger("recstalta", 10, 2, st_Z, 3, sta=0.5, lta=10, details=True) 
# Trigger type=recursive STA/LTA
# Threshold on=10s, off=2s
# Stream=st_Z
# Threshold for coincidence sum=3
# STA=0.5s, LTA=10s
print(len(triggers), "events triggered.")

# Output phase file
time=st[0].stats.starttime
phase_file = '../pick/%s.pick'%(time.strftime('%Y%m%d_%H%M%S'))
f_phase = open(phase_file, 'w')

# Pick P and S arrivals with an AR-AIC + STA/LTA algorithm
for trigger in triggers:
    st_trig = Stream()
    t = trigger['time']
    print("#" * 80)
    print("Trigger time:", t)

    for sta in trigger['stations']:
        st_trig = st_cp.select(station=sta).copy()
        # Limiting time span for picking
        st_trig = st_trig.trim(t-30, t+120)
        for trc in st_trig:
            start = trc.stats.starttime
            sta = trc.stats.station
            loc = trc.stats.location
            chn = trc.stats.channel  
            inst = trc.stats.sac.kinst.replace(" ", "_")      

            createFolder('../event/%s'%(start.strftime('%Y.%m.%d.%H.%M.%S')))
            trc.write('../event/%s/%s.%s.%s.%s.R.sac'%(start.strftime('%Y.%m.%d.%H.%M.%S'),start.strftime('%Y.%m.%d.%H.%M.%S'),sta,loc,chn), format='SAC')

        st_trig.detrend(type='demean')
        pick = ar_pick(st_trig[2], st_trig[1], st_trig[0], df, 1, 20, 1, 0.1, 4, 1, 2, 8, 0.1, 0.35)
        # Frequency of the lower bandpass window = 1
        # Frequency of the upper bandpass window = 20
        # Length of LTA for the P arrival in seconds = 1s
        # Length of STA for the P arrival in seconds = 0.1s
        # Length of LTA for the S arrival in seconds = 4s
        # Length of STA for the S arrival in seconds = 1 s
        # Number of AR coefficients for the P arrival = 2
        # Number of AR coefficients for the S arrival = 8
        # Length of variance window for the P arrival in seconds = 0.1
        # Length of variance window for the S arrival in seconds = 0.2
        pick_P = st_trig[2].stats.starttime + pick[0]
        pick_S = st_trig[2].stats.starttime + pick[1]

        # Calculate maximum amplitude for P phase from Z component only, trim waveform from pick P and next 0.5 second
        ampl_P = max(abs(st_trig[2].copy().trim(pick_P, pick_P + 0.5).data))
        channel = st_trig[2].stats.channel  

        # Print P phase in NLLoc format
        f_phase.write('%s %s %s ? P ? %s GAU 0.0 0.0 %9.8G 0.0\n' %(sta, inst, channel, pick_P.strftime('%Y%m%d %H%M %S.%f')[:-3],ampl_P))

        # Calculate maximum amplitude for S phase, trim waveform from pick S and next 2 second
        # Only calculate pick S if 0.5s < S-P < 5.0s
        if pick_S != 0 and pick_S-pick_P > 0.5 and pick_S-pick_P < 5:
            ampl_Sn = max(abs(st_trig[0].copy().trim(pick_S, pick_S + 2).data))
            ampl_Se = max(abs(st_trig[1].copy().trim(pick_S, pick_S + 2).data))
            ampl_Sz = max(abs(st_trig[2].copy().trim(pick_S, pick_S + 2).data))
            ampl_S = [ampl_Sn, ampl_Se, ampl_Sz]
            max_S = max(ampl_S)

            # Return channel which has the max amplitude
            channel = st_trig[ampl_S.index(max_S)].stats.channel

            # Print S phase in NLLoc format
            f_phase.write('%s %s %s ? S ? %s GAU 0.0 0.0 %9.8G 0.0\n' %(sta, inst, channel, pick_S.strftime('%Y%m%d %H%M %S.%f')[:-3],max_S))

    f_phase.write('\n')
f_phase.close()