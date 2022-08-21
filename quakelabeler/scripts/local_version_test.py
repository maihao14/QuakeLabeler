#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 30 16:49:05 2022

@author: hao
"""
import pandas as pd
from obspy.core.utcdatetime import UTCDateTime
from obspy.core import read
#%% load pandas

records = pd.read_csv("/Users/hao/Downloads/dataset_test/catalog_test_1.csv",index_col=0)
#%%
def picktimewindow(total, windowtime, p_time, s_time, t0, te):
    if total== windowtime:
        return t0,te
    interval = s_time - p_time
    rest_time = windowtime - interval
    start_p = np.random.uniform(0,np.min([rest_time,p_time-t0]))
    while p_time -  start_p + windowtime > te:
        start_p = np.random.uniform(0,np.min([rest_time,p_time-t0]))
    starttime = p_time -  start_p
    endtime = starttime + windowtime
    return starttime, endtime
#%% check p-s interval
sample_rate = 100.0
sample_length = 3000
sample_time = sample_length / sample_rate
npts = 8000
path = '/Users/hao/Downloads/dataset_test/seismic1/'
st = read(path+thread['FILENAME'])
t0 = st[0].stats.starttime
te = st[0].stats.endtime
#%%
def sample_generator(st,t0,te,p,s):
    pass
    return
    
#%%
for ind,thread in records.iterrows():
    if thread['PHASE'] == 'P':
        # pick a P event
        p_phase = thread['ARRIVAL_DATE'] + 'T' + thread['ARRIVAL_TIME']
        # check if S exists
        s_thread = records.loc[(records['FILENAME']==thread['FILENAME'] )&( records['PHASE']=='S') ]
        if not s_thread.empty:
            s_thread = s_thread.squeeze()
            s_phase = s_thread['ARRIVAL_DATE'] + 'T' + s_thread['ARRIVAL_TIME']
            # UTCDate
            p_time = UTCDateTime(p_phase)
            s_time = UTCDateTime(s_phase)
            if (s_time - p_time) < sample_time:
                # satisfy for make a paired sample
                starttime, endtime = picktimewindow(npts/sample_rate,sample_length/sample_rate, p_time, s_time, t0, te )
                sample_generator(st,starttime, endtime, p_time, s_time)
            else:
                starttime, endtime = picktimewindow(npts/sample_rate,sample_length/sample_rate, p_time, p_time, t0, te )
                # only P phase sample
                sample_generator(st,starttime, endtime, p_time, None)
        else:
            # only P phase sample
            # UTCDate
            p_time = UTCDateTime(p_phase)
            starttime, endtime = picktimewindow(npts/sample_rate,sample_length/sample_rate, p_time, p_time, t0, te )
            sample_generator(st,starttime, endtime, p_time, None)
    if thread['PHASE'] == 'S':
        s_phase = thread['ARRIVAL_DATE'] + 'T' + thread['ARRIVAL_TIME']
        p_thread = records.loc[(records['FILENAME']==thread['FILENAME'] )&( records['PHASE']=='P') ]
        if not p_thread.empty:
            p_thread = p_thread.squeeze()
            p_phase = p_thread['ARRIVAL_DATE'] + 'T' + _thread['ARRIVAL_TIME']
            # UTCDate
            p_time = UTCDateTime(p_phase)
            s_time = UTCDateTime(s_phase)
            if (s_time - p_time) < sample_time:
                # satisfy for make a paired sample
                pass
            else:
                # only S phase sample
                starttime, endtime = picktimewindow(npts/sample_rate,sample_length/sample_rate, s_time, s_time, t0, te )
                sample_generator(st,starttime, endtime, None, s_time)
        else:
            # only S phase sample
            s_time = UTCDateTime(s_phase)
            starttime, endtime = picktimewindow(npts/sample_rate,sample_length/sample_rate, s_time, s_time, t0, te )
            sample_generator(st,starttime, endtime, None, s_time)
            
                
                
                
            
    


#%%
p_phase = thread['ARRIVAL_DATE'] + 'T' + thread['ARRIVAL_TIME']
temp = records.loc[records['FILENAME']==thread['FILENAME']]
if len(temp)>1:
    s_thread = temp.loc[temp.index(temp['PHASE']=='S').tolist()]
    s_phase = s_thread['ARRIVAL_DATE'] + 'T' + s_thread['ARRIVAL_TIME']
    print(s_phase)
    
#%% UTCDate
p_time = UTCDateTime(p_phase)
s_time = UTCDateTime(s_phase)


#%% process
        st.merge(method=1, fill_value='interpolate')
      #  st.interpolate(sampling_rate=100)
        st[0].resample(100)
        st[0].data.dtype = 'int32'            
        st.detrend("demean")
        pre_filt = [0.8, 9.5, 40, 45] 
        st.remove_response(pre_filt=pre_filt,water_level=10,taper=True,taper_fraction=0.05)
      #  st.filter('bandpass',freqmin = 1.0, freqmax = 45, corners=2, zerophase=True) 
        st.write(filename=kwargs['dirn']+kwargs['net']+'.'+kwargs['station']+'..'+kwargs['chan']+"__"+str(kwargs['starttime']).split('T')[0].replace("-", "")+"T000000Z__"+str(kwargs['tend']).split('T')[0].replace("-", "")+"T000000Z.SAC",format="SAC")
        
#%% debug local mode
