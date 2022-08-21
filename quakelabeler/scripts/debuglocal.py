#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 21:17:12 2022
Debug Local mode
@author: hao
"""
#%% import packages
from __future__ import (absolute_import, division, print_function)
from quakelabeler import *
import logging


# dependent packages
import os
import shutil
import logging
import csv
from obspy.core.utcdatetime import UTCDateTime
from obspy.clients.fdsn import Client
import warnings
import random
import numpy as np
import pandas as pd
import time
from scipy.io import savemat
LOGGER = logging.getLogger(__name__)
# terminal figure
import termplotlib as tpl
# regular expression
import re
# get arrival information from webpages
import requests
# command line progress
from progress.bar import Bar
import matplotlib.pyplot as plt
# art font
from art import *
from obspy import read
import pygmt
import h5py
#%%Interactive

user_interface = Interactive()
#%%QueryArrival
query = QueryArrival(**user_interface.params)
#%%CustomSamples
# init custom options
custom = CustomSamples(user_interface.receipe_flag)
# run custom of dataset structure
custom.init()
#%% Main process
auto_dataset = QuakeLabeler(query, custom)
#%%local_label
auto_dataset.local_label(auto_dataset.recordings)

#%% local label detail
records = auto_dataset.recordings
#%%
print('Initialize samples producer module...')
# selet user preference

# count loop number, when loop>100 & no available waveform found, break the loop
loopnum = 0
if auto_dataset.custom_export['export_filename'] == '':
    # if user doesn;t have a preffered folder name:
    today = UTCDateTime()
    FileName = 'MyDataset' + str(today)[:-11]  #filename option —— custom class UPDATE
else:
    FileName = auto_dataset.custom_export['export_filename']
# num: stream(samples) volume
num = 0
# amount of the samples
if not auto_dataset.custom_dataset['volume'] == 'MAX':
    maxnum = int(auto_dataset.custom_dataset['volume'])
else:
    #use every thread in records to produce samples
    maxnum = len(records)
#create a dict save every sample information
auto_dataset.available_samples = []
auto_dataset.custom_export['folder_name'] = FileName
if not os.path.exists(FileName):
    os.mkdir(FileName)
os.chdir(FileName)
auto_dataset.hdf = False

#%%
thread = records.iloc[6]

#%%
path = auto_dataset.params['datafolder']
st = read(path+thread['FILENAME'])
sample_rate = st[0].stats.sampling_rate # 100.0
sample_length = auto_dataset.custom_dataset['sample_length'] #3000
#%%
if auto_dataset.custom_dataset['fixed_length'] == False:
    sample_length = st[0].stats.npts
    
if not auto_dataset.custom_waveform['sample_rate'] =='':
    sample_rate = float(auto_dataset.custom_waveform['sample_rate'])

sample_time = sample_length / sample_rate
#%% resample option
if not sample_rate == st[0].stats.sampling_rate:
    st = st.resample(sample_rate)                
npts = st[0].stats.npts#8000
# int32 option
for i in range(len(st)):
    st[i].data.dtype = 'int32'
    
#%% detrend
# detred option
if auto_dataset.custom_waveform['detrend']:
    st.detrend("demean")
#%%
if auto_dataset.custom_waveform['filter_type'] == '1':
    st.filter('lowpass',freq = auto_dataset.custom_waveform['filter_freqmin'], corners=2, zerophase = True)
if auto_dataset.custom_waveform['filter_type'] == '2':
    st.filter('highpass',freq = auto_dataset.custom_waveform['filter_freqmax'], zerophase = True)
if auto_dataset.custom_waveform['filter_type'] == '3':
    st.filter('bandpass', freqmin = auto_dataset.custom_waveform['filter_freqmin'], freqmax = auto_dataset.custom_waveform['filter_freqmax'],corners=2, zerophase=True)            
#%%
t0 = st[0].stats.starttime
te = st[0].stats.endtime
# init p s arrival time
#%%
p_time = None
s_time = None
# standardize sample
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
            starttime, endtime = auto_dataset.picktimewindow(npts/sample_rate,sample_length/sample_rate, p_time, s_time, t0, te )
            st = auto_dataset.sample_generator(st,starttime, endtime, p_time, s_time)
        else:
            starttime, endtime = auto_dataset.picktimewindow(npts/sample_rate,sample_length/sample_rate, p_time, p_time, t0, te )
            # only P phase sample
            st = auto_dataset.sample_generator(st,starttime, endtime, p_time, None)
    else:
        # only P phase sample
        # UTCDate
        p_time = UTCDateTime(p_phase)
        starttime, endtime = auto_dataset.picktimewindow(npts/sample_rate,sample_length/sample_rate, p_time, p_time, t0, te )
        st = auto_dataset.sample_generator(st,starttime, endtime, p_time, None)
#%% S phase
if thread['PHASE'] == 'S':
    s_phase = thread['ARRIVAL_DATE'] + 'T' + thread['ARRIVAL_TIME']
    p_thread = records.loc[(records['FILENAME']==thread['FILENAME'] )&( records['PHASE']=='P') ]
    if not p_thread.empty:
        p_thread = p_thread.squeeze()
        p_phase = p_thread['ARRIVAL_DATE'] + 'T' + p_thread['ARRIVAL_TIME']
        # UTCDate
        p_time = UTCDateTime(p_phase)
        s_time = UTCDateTime(s_phase)
        if (s_time - p_time) < sample_time:
            # satisfy for make a paired sample
            pass
        else:
            # only S phase sample
            starttime, endtime = auto_dataset.picktimewindow(npts/sample_rate,sample_length/sample_rate, s_time, s_time, t0, te )
            st = auto_dataset.sample_generator(st,starttime, endtime, None, s_time)
    else:
        # only S phase sample
        s_time = UTCDateTime(s_phase)
        starttime, endtime = auto_dataset.picktimewindow(npts/sample_rate,sample_length/sample_rate, s_time, s_time, t0, te )
        st = auto_dataset.sample_generator(st,starttime, endtime, None, s_time)
        
#%% save
# bar proecess
num += 1
updatethread = thread.copy()
multi_filename = auto_dataset.creatsamplename(st)
#add record to csv file
updatethread['filename'] = multi_filename
if p_time != None:
    p_arr = (p_time-starttime) * st[0].stats.sampling_rate
    updatethread['p_arrival_sample'] = int(p_arr)     
else:
    updatethread['p_arrival_sample'] = np.nan
if s_time != None:
    s_arr = (s_time-starttime) * st[0].stats.sampling_rate
    updatethread['s_arrival_sample'] = int(s_arr)     
else:
    updatethread['s_arrival_sample'] = np.nan
updatethread['npts'] = st[0].stats.npts
updatethread['sampling_rate'] = st[0].stats.sampling_rate
auto_dataset.local_sample_export(st, multi_filename, thread)
auto_dataset.available_samples.append(updatethread)
print("Save to target folder: {0}".format(FileName))