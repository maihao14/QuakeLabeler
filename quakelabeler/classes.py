# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2021 Hao Mai & Pascal Audet
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
Created on Sun Feb 21 20:22:25 2021
core classes
@author: Hao Mai & Pascal Audet
"""
from __future__ import (absolute_import, division, print_function)

# dependent packages
import os
import logging
import csv
from obspy.core.utcdatetime import UTCDateTime
from obspy.clients.fdsn import Client
import warnings
import random
import numpy as np
from scipy.io import savemat
LOGGER = logging.getLogger(__name__)
# terminal figure
import termplotlib as tpl
# regular expression
import re
# get arrival information from webpages
import requests
# command line progress
from progress.spinner import Spinner
from progress.bar import Bar
import matplotlib.pyplot as plt

class QuakeLabeler():
    r""" A QuakeLabeler object contains Class attributes that design and create
    seismic datasets by custom settings. QuakeLabeler has a series of methods
    to automatic finish datasets production:

    #. Initialize research area and time range;
    #. Retrieve available waveforms from data center;
    #. Pre-process (optional): detrend, denoise, resampling, filter;
    #. Transfer waveforms to standard labels;
    #. Post-process (optional): add noise, seperate input/output channels, crop;
    #. Save datsets informations as CSV files;
    #. Export distribution histogram.

    .. note::
    This is intended to be the core QuakeLabeler functionality, without any
    reference to the interactive interface. The original intent was to allow
    this to run independently, eg. from a script or interactive shell.

    Parameters
    ----------
    params : dict
        `params` containing research region and time options in a dictionary
        which receive from interactive shell or scripts. `params` includes:

        #. station region;
        #. event time range;
        #. event magnitude limits(optional);
        #. arrival limits(optional);
    recordings : dict
        All founded event-based records (arrivals). Note that these arrivals
        do not gurantee they are downloadable from certain data centers.
        `recordings` includes:

        #. event ID;
        #. event magnitude;
        #. phase name;
        #. arrival time;
        #. original event time;
        #. event location (optional).
    inventory : Obspy object
        `inventory` is from class:`obspy.core.inventory.Inventory`. A container
        for one or more networks.
    network : str
        Available network names.
    """
    def __init__(self, query, custom):
        # init
        self.params = query.param
        self.recordings = query.arrival_recordings
        self.custom_dataset = custom.custom_dataset
        self.custom_waveform = custom.custom_waveform
        self.custom_export = custom.custom_export
        # target network and station names
        self.inventory = self.search_stations()
        # targe network names
        self.network = "*"
        if not self.inventory == False:
            self.network = self.search_network()

    def search_catalog(self, clientname="IRIS"):
        r''' Catalog Search
        If input data center does not have available seismograms, this module
        will reminder to change data center.
        '''
        client = Client(clientname)
        try:
            cat = client.get_events(starttime=self.starttime,
                                    endtime=self.endtime,
                                    minmagnitude=self.minmag,
                                    maxmagnitude=self.maxmag,
                                    minlatitude=self.minlatitude,
                                    maxlatitude=self.maxlatitude,
                                    minlongitude=self.minlongitude,
                                    maxlongitude=self.maxlongitude
                                    )
        except Exception:
            print("Cannot fetch catalog from {0} ! Please select another data\
                center: ".format(clientname))
            print(r'"BGR", "EMSC", "ETH", "GEONET", "GFZ", "ICGC", "INGV",\
                "IPGP", "IRIS", "ISC", KNMI", "KOERI", "LMU", "NCEDC", "NIEP",\
                "NOA", "ODC", "ORFEUS", "RASPISHAKE", "RESIF", "SCEDC",\
                "TEXNET", "USGS", "USP"')
        else:
            print("From {0} data center : ".format(clientname))
            print(cat)
            return (cat)

    def search_stations(self, clientname="IRIS"):
        r''' Search all available station in the target research region
        This method accepts rectangular or circular range options.
        Parameters
        ----------
        clientname : str, optional
            Data center name. The default is "IRIS".
        Returns
        -------
        inventory : Inventory object
            Return an Inventory object which stored available stations.
        '''
        client = Client(clientname)
        sta_params = {}
        if self.params['stnsearch'] == 'RECT':
            sta_params['minlatitude'] = self.params['stn_bot_lat']
            sta_params['maxlatitude'] = self.params['stn_top_lat']
            sta_params['minlongitude'] = self.params['stn_left_lon']
            sta_params['maxlongitude'] = self.params['stn_right_lon']
        else:
            if self.params['stnsearch'] == 'CIRC':
                sta_params['latitude'] = self.params['stn_ctr_lat']
                sta_params['minlongitude'] = self.params['stn_ctr_lon']
                if self.params['max_stn_dist_units'] == 'deg':
                    sta_params['maxradius'] = self.params['stn_radius']
                else:
                    sta_params['maxradius'] = self.params['stn_radius']/111
            else:
                return False
        sta_params['level'] = "station"
        inventory = client.get_stations(**sta_params)
        return inventory

    def judge_time_range(self, thread, t1, t2, clientname="IRIS"):
        r"""Check seismograms time window
        This method is to examine if there's available waveform from target
        data center.
        Returns
        -------
        trace : `Obspy` trace object
        False : bool
        """
        client = Client(clientname)
        (network, station, location, channel) = self.related_station_info(
                                                thread['STA'])
        try:
            st = client.get_waveforms(
                                network, station, location, channel, t1, t2)
        except Exception:
            return False
        else:
            return st[0]

    def waveform_timewindow(self, thread, sample_points=50*60):
        r"""Calculate waveform startime and endtime
        Method to ensure retrieve enought length waveform.
        Parameters
        ----------
        thread : dict
            *thread* stores a specific seismogram information.
        sample_points : int, optional
            Waveform length. The default is 50*60 = 3000.
        Returns
        -------
        starttime : UTCTime
            Start time for this waveform.
        endtime : UTCTime
            End time for this waveform.
        """
        eventTime = thread['ARRIVAL_DATE'] + 'T' + thread['ARRIVAL_TIME']
        if self.custom_dataset['fixed_length']:
            # random start time option
            if self.custom_waveform['random_arrival']:
                # set a random stattime for each event(waveform)
                # default: 10~180 s before first arrival
                #  30~90 s after arrival
                start = random.randint(10, 180)
                starttime = UTCDateTime(eventTime) - start
                end = random.randint(30, 90)
                endtime = UTCDateTime(eventTime) + end
                trace = self.judge_time_range(thread, starttime, endtime)
                if not trace == False:
                    try:
                        resample_rate = int(
                                self.custom_waveform['sample_rate'])
                    except Exception:
                        pass
                    else:
                        trace.stats.sampling_rate = resample_rate
                    # loop: calculate a reasonal starttime
                    while not trace.stats.sampling_rate*(UTCDateTime(eventTime) - starttime) < self.custom_dataset['sample_length']:
                        start = random.randint(1,int(self.custom_dataset['sample_length']/trace.stats.sampling_rate))
                        starttime = UTCDateTime(eventTime) - start
                        endtime = starttime + int(self.custom_dataset['sample_length']/trace.stats.sampling_rate)
                    else:
                        endtime = starttime + int(self.custom_dataset['sample_length']/trace.stats.sampling_rate)
            else:
                #fixed startime: t1 sec before arrival
                #time range might not satisfy fixed npts, need examine and re-crop
                starttime = UTCDateTime(eventTime) - self.custom_waveform['start_arrival']
                endtime =  UTCDateTime(eventTime) + self.custom_waveform['end_arrival']
                trace = self.judge_time_range(thread, starttime, endtime)
                if not trace == False:
                    try:
                        resample_rate = int(self.custom_waveform['sample_rate'])
                    except Exception as e:
                        pass
                    else:
                        trace.stats.sampling_rate = resample_rate
                    endtime = starttime + int(self.custom_dataset['sample_length']/trace.stats.sampling_rate)
        else:
            # flexible waveform length
            if self.custom_waveform['random_arrival']:
                # set a random stattime for each event(waveform) default: 10~180 s before first arrival ~ 30~90 s after arrival
                start = random.randint(10, 90)
                starttime = UTCDateTime(eventTime) - start
                end = random.randint(30, 90)
                endtime = UTCDateTime(eventTime) + end
            else:
                starttime = UTCDateTime(eventTime) - self.custom_waveform['start_arrival']
                endtime = UTCDateTime(eventTime) + self.custom_waveform['end_arrival']
        self.eventtime = UTCDateTime(eventTime)

        return (starttime, endtime)

    def search_network(self):
        # collect network names in a research region
        network = ""
        for net in self.inventory:
            network = network + str(net._code) + ","
        network = network[:-1]
        return network

    def related_station_info(self, sta):
        # search available station / channel for target events
        station = str(sta)
        network = self.network
        location = "*"
        # all channel codes:
        # https://ds.iris.edu/ds/nodes/dmc/data/formats/seed-channel-naming/
        channel = "BH?"
        # drop low sampling rate channels which might not be useful
        return (network, station, location, channel)

    def check_export_stream(self, st):
        if self.custom_dataset['fixed_length']:
            for tr in st:
                if tr.stats.npts < self.custom_dataset['sample_length']:
                    st.remove(tr)
                if tr.stats.npts > self.custom_dataset['sample_length']:
                    tr.data = tr.data[:self.custom_dataset['sample_length']]
        return st

    def fetch_waveform(self, thread, clientname="IRIS"):
        r"""Retrieve a target stream of waveforms from specific data center
        This stream can includes mutiple-component seismic traces
        which from only one station with one event.  They can be spilt as
        single trace mode or keep as a 3-C sample or multiple-component sample.
        Note that for now we remove those low-sampling-rate (<1.0Hz) samples
        which might not help our project.
        Parameters
        ----------
        thread : dict
            Waveform information recording.
        clientname : str, optional
            Name of data center. The default is "IRIS".
        Returns
        -------
        st : Obspy Stream Object
            Downloaded waveform which save as a obspy.stream object.
        `No data available for request.` : str
            Failed request message.
        """
        client = Client(clientname)
        # calculate startime and endtime, must consider trace length, sampling rate to satisfy custom parameters

        (start_time, end_time) = self.waveform_timewindow(thread)
        # (start_time,end_time) = self.waveform_timewindow(thread)
        (network, station, location, channel) = self.related_station_info(thread['STA'])
        try:
            st = client.get_waveforms(network, station, location, channel, start_time, end_time+10)
            # param attach_response  NEED UPDATE ONE INTERACTIVE PARAMTER HERE
        except Exception:
            return "No data available for request."
        else:
            # resample mode
            try:
                resample_rate = float(self.custom_waveform['sample_rate'])
            except Exception:
                pass
            else:
                st.resample(resample_rate)
            # filter option
            if self.custom_waveform['filter_type'] == '1':
                st.filter('lowpass',freq = self.custom_waveform['filter_freqmin'], corners=2, zerophase = True)
            if self.custom_waveform['filter_type'] == '2':
                st.filter('highpass',freq = self.custom_waveform['filter_freqmax'], zerophase = True)
            if self.custom_waveform['filter_type'] == '3':
                st.filter('bandpass', freqmin = self.custom_waveform['filter_freqmin'], freqmax = self.custom_waveform['filter_freqmax'])
            # add noise
            # self.custom_waveform['add_noise'] = 1.0
            if self.custom_waveform['add_noise'] != 0 :
                # add noise to trace
                for tr in st:
                    length = len(tr.data)
                    amplitude = max(tr.data)
                    noise_arr = amplitude*self.custom_waveform['add_noise']*(-1+2*np.random.rand(length))
                    tr.data = noise_arr + tr.data
            st = self.check_export_stream(st)
            if len(st) == 0:
                return "No data available for request."
            else:
                #valid waveform as a new sample
                self.starttime = st[0].stats.starttime
                self.npts = st[0].stats.npts
                self.sampling_rate = st[0].stats.sampling_rate
                return st

    def creatsamplename(self, stream):
        r'''Creat filename for each sample
        Creat filenames for each available waveform.
        Parameters
        ----------
        stream : Obspy stream object
            Availble data stream waited to be transferred to label.
        Returns
        -------
        filename : str
            creat a name for the waveform.
        '''
        st = str(stream[0].stats.starttime)
        st_name = st[0:13]+st[15:16]+st[18:19]

        filename = stream[0].stats.network + '.' + stream[0].stats.station
        if self.custom_export['single_trace'] == True:
            filename = filename + '.' + stream[0].stats.channel + '.'+st_name
        else:
            for tr in stream:
                filename = filename + '.' + tr.stats.channel
            filename = filename + '.' + st_name
        return filename

    def output_bell_dist(self, npts, it, window):
        r'''Create bell-like output channel
        Use bell-like (Gaussian) distribution to form output labels.
        '''
        # npts: sample length
        # it: peak point
        # window:  width
        x = np.arange(0, npts)
        fx = np.zeros(npts)
    #    fx = np.exp(-(x-it)**2/2/(window/4)**2)
        fx = np.exp(-8*(x - it)**2/(window)**2)
        return fx

    def output_rect_dist(self, npts, it, window):
        r'''Create rectangular output channel
        Use rectangulardistribution to form output labels.
        The positive data points = 1.0
        The negative data points = 0.0
        '''
        fx = np.zeros(npts)
        fx[it - window//2: it + window//2] = 1
        return fx

    def single_sample_export(self, st, filename, pick_win=100, detect_win=200):
        r''' Export sample in single channel mode
        '''
        it = int((self.eventtime - self.starttime) * self.sampling_rate)
        self.arr_point = it

        # if user need create independent output channel:
        if self.custom_export['export_inout']:
            st1 = st
            st1[0].data = self.output_bell_dist(self.npts, it, pick_win)
            st2 = st
            st2[0].data = self.output_rect_dist(self.npts, it, detect_win)

        if 'SAC' in self.custom_export['export_type']:
            st.write(filename + ".sac", format="SAC")
            # if user need create independent output channel:
            if self.custom_export['export_inout']:
                st1.write(filename + 'out_bell' + ".sac", format="SAC")
                st2.write(filename + 'out_rect' + ".sac", format="SAC")
        # export as MSEED format
        if 'MSEED' in self.custom_export['export_type']:
            st.write(filename + ".mseed", format="MSEED")
            if self.custom_export['export_inout']:
                st1.write(filename +'out_bell'+ ".mseed", format="MSEED")
                st2.write(filename +'out_rect'+ ".mseed", format="MSEED")
        # export as SEGY format
        if 'SEGY' in self.custom_export['export_type']:
            st.write(filename + ".sgy", format="SEGY")
            if self.custom_export['export_inout']:
                st1.write(filename +'out_bell'+ ".sgy", format="SEGY")
                st2.write(filename +'out_rect'+ ".sgy", format="SEGY")
        #export as Python Numpy format
        if 'NPZ' in self.custom_export['export_type']:
            npzdict = {'data': st[0].data}
            np.savez(filename + ".npz", **npzdict)
            if self.custom_export['export_inout']:
                npzdict = {'data': st1[0].data}
                np.savez(filename +'out_bell' + ".npz", **npzdict)
                npzdict = {'data': st2[0].data}
                np.savez(filename +'out_rect' + ".npz", **npzdict)
        #export as MATLAB format
        if 'MAT' in self.custom_export['export_type']:
            mdic = {st[0].stats.channel : st[0].data}
            savemat(filename + ".mat", mdic)
            if self.custom_export['export_inout']:
                mdic = {st1[0].stats.channel : st1[0].data}
                savemat(filename +'out_bell'+ ".mat", mdic)
                mdic = {st2[0].stats.channel : st2[0].data}
                savemat(filename +'out_rect'+ ".mat", mdic)
    def multi_sample_export(self, st, filename,pick_win = 100, detect_win = 200):
        r''' Export sample in multiple channel mode
        '''
        it = int((self.eventtime - self.starttime) * self.sampling_rate)
        self.arr_point = it

        # if user need create independent output channel:
        if self.custom_export['export_inout']:
            st1 = st
            for tr in st1:
                tr.data = self.output_bell_dist(self.npts, it, pick_win)
            st2 = st
            for tr in st2:
                tr.data = self.output_rect_dist(self.npts, it, detect_win)

        if 'SAC' in self.custom_export['export_type']:
            st.write(filename + ".sac", format="SAC")
            if self.custom_export['export_inout']:
                st1.write(filename +'out_bell'+ ".sac", format="SAC")
                st2.write(filename +'out_rect'+ ".sac", format="SAC")
        if 'MSEED' in self.custom_export['export_type']:
            st.write(filename + ".mseed", format="MSEED")
            if self.custom_export['export_inout']:
                st1.write(filename +'out_bell'+ ".mseed", format="MSEED")
                st2.write(filename +'out_rect'+ ".mseed", format="MSEED")
        if 'SEGY' in self.custom_export['export_type']:
            st.write(filename + ".sgy", format="SEGY")
            if self.custom_export['export_inout']:
                st1.write(filename +'out_bell'+ ".sgy", format="SEGY")
                st2.write(filename +'out_rect'+ ".sgy", format="SEGY")
        if 'NPZ' in self.custom_export['export_type']:
            npzdict = {}
            for tr in st:
                npzdict[tr.stats.channel] = tr.data
            np.savez(filename + ".npz", **npzdict)
            if self.custom_export['export_inout']:
                for tr in st1:
                    npzdict[tr.stats.channel] = tr.data
                np.savez(filename +'out_bell' + ".npz", **npzdict)
                for tr in st2:
                    npzdict[tr.stats.channel] = tr.data
                np.savez(filename +'out_rect' + ".npz", **npzdict)
        if 'MAT' in self.custom_export['export_type']:
            for tr in st:
                mdic = {tr.stats.channel : tr.data}
            savemat(filename + ".mat", mdic)
            if self.custom_export['export_inout']:
                for tr in st1:
                    mdic = {tr.stats.channel : tr.data}
                savemat(filename +'out_bell'+ ".mat", mdic)
                for tr in st2:
                    mdic = {tr.stats.channel : tr.data}
                savemat(filename +'out_rect'+ ".mat", mdic)

    def fetch_all_waveforms(self, records, clientname="IRIS"):
        r"""Auto fetch seismograms to produce samples
        This module manage all potential waveforms as threads. Retrive waveform
        from specific data centers, revise trace by customized parameters and
        produce required samples continuous until reach the volume.

        This function contains:
            1. Load/Import: Requests to data centers to find available data;
            2. Custom: Use user's preferrence parameters to form the samples;
            3. Process: (resample, filter, denoise, add noise);
            4. Revise: fix trace format to satify datasets;
            5. Label: Annotate arrival time and phase name;
            6. Export: Save samples in certain file format.

        Parameters
        ----------
        records : list
            `records` saves all potential downloadable waveform.
        clientname : str, optional
            The default is "IRIS". Specific data center's name.

        Returns
        -------
        available_samples : list
            Return every samples in the datasets.
        """
        print('Initialize samples producer module...')
        # selet user preference

        # count loop number, when loop>100 & no available waveform found, break the loop
        loopnum = 0
        if self.custom_export['export_filename'] == '':
            # if user doesn;t have a preffered folder name:
            today = UTCDateTime()
            FileName = 'MyDataset' + str(today)[:-11]  #filename option —— custom class UPDATE
        else:
            FileName = self.custom_export['export_filename']
        # num: stream(samples) volume
        num = 0
        if not self.custom_dataset['volume'] == 'MAX':
            maxnum = int(self.custom_dataset['volume'])
        else:
            maxnum = len(records)
        #create a dict save every sample information
        self.available_samples = []

        if not os.path.exists(FileName):
            os.mkdir(FileName)
        os.chdir(FileName)
        #set progress bar
        bar = Bar('Processing', max=maxnum)
        for thread in records:
            #check this step: one thread one stream, multiple traces
            st = self.fetch_waveform(thread, clientname )
            if st == "No data available for request.":
                loopnum = loopnum+1
                if loopnum>50:
                    warnings.warn('50+ continuous failed data requests, please quit process and check your parameters.')
            else:
                loopnum = 0
                if self.custom_export['single_trace'] == True:
                    num = num+ len(st)
                    # split each stream as independent trace component
                    for tr in st:
                        bar.next()
                        # detrend (optional)
                        if self.custom_waveform['detrend']:
                            tr.detrend()
                        singlesample = st.select(channel=tr.stats.channel)
                        single_filename = self.creatsamplename(singlesample)
                        self.single_sample_export(singlesample, single_filename)
                        #add record to csv file
                        thread['filename'] = single_filename
                        thread['arr_point'] = self.arr_point
                        thread['npts'] = self.npts
                        thread['sampling_rate'] = self.sampling_rate
                        if not self.custom_waveform['label_type']:
                            if 'S' in thread['ISCPHASE']:
                                thread['ISCPHASE'] = 'S'
                            else:
                                thread['ISCPHASE'] = 'P'
                        self.available_samples.append(thread)
                else:
                    num += 1
                    bar.next()
                    # detrend (optional)
                    if self.custom_waveform['detrend']:
                        for tr in st:
                            tr.detrend()
                    multi_filename = self.creatsamplename(st)
                    self.multi_sample_export(st, multi_filename)
                    #add record to csv file
                    thread['filename'] = multi_filename
                    thread['arr_point'] = self.arr_point
                    thread['npts'] = self.npts
                    thread['sampling_rate'] = self.sampling_rate
                    if not self.custom_waveform['label_type']:
                        if 'S' in thread['ISCPHASE']:
                            thread['ISCPHASE'] = 'S'
                        else:
                            thread['ISCPHASE'] = 'P'
                    self.available_samples.append(thread)
                print("Save to target folder: {0}".format(FileName))
                print(st)
                if num >= maxnum:
                    bar.finish()
                    break

        print("All available waveforms are ready!")
        print("{0} of event-based samples are successfully downloaded! ".format(num))
        os.chdir('../')
        self.FolderName = FileName
        return self.available_samples


    def csv_writer(self):
        r""" Method to export information of the dataset.
        """
        if not self.custom_export['export_arrival_csv']:
            return
        print('Save waveform information into CSV file...')
        CSV_Name = self.FolderName + '.csv'
        dict1 = self.available_samples[0]
        field_names = []
        for k, v in dict1.items():
            field_names.append(k)
        with open(CSV_Name, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(self.available_samples)

    def stats_figure(self):
        r""" Output statistical figures
        """
        if not self.custom_export['export_stats']:
            return
        # create image folder
        ImgFolder = 'Image'
        if not os.path.exists(ImgFolder):
            os.mkdir(ImgFolder)
        os.chdir(ImgFolder)
        #terminal plotting
        print("Magnitude Distribution")
        sample_mag = []
        for thread in self.available_samples:
            sample_mag.append(thread['EVENT_MAG'])
        bins=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        counts, bin_edges = np.histogram(sample_mag, bins)
        fig = tpl.figure()
        fig.hist(counts, bin_edges, orientation="horizontal", force_ascii=False)
        fig.show()
        #export plotting
        n, bins, patches = plt.hist(x=sample_mag, bins=bins, color='#0504aa',
                                    alpha=0.7, rwidth=0.85)
        plt.grid(axis='y', alpha=0.75)
        plt.xlabel('Magnitude')
        plt.ylabel('Frequency')
        plt.title('Magnitude Histogram')
        maxfreq = n.max()
        # Set a clean upper y-axis limit.
        plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
        plt.savefig('MagDist.jpeg', dpi = 300)
        #station overview
        # self.inventory.plot(projection="local", label=False,
        #     color_per_network=True, size=20,
        #     outfile="stationpreview.png")
        os.chdir('../')


class Interactive():
    r""" Interactive tool for target stations and time range
    Receive user's interest search options from command line inteface (CLI).
    Automatic search arrivals associated to events in the ISC Bulletin
    on the input stations and time range.

    Options includes:
        #. station region
        #. time range
        #. magnitude range
        #. phase names

    Refference
    ----------
    ISC Bulletin: arrivals search
    International Seismological Centre (20XX), On-line Event Bibliography,
    https://doi.org/10.31905/EJ3B5LV6

    Parameters
    ----------
    params : dict
        `params` saves all customized options which defines the research region
        and time. `params` contains region latitude and longitude, start time
        and end time, magnitudes(optional), etc.
    """
    def __init__(self):
        self.welcome() #brief introduction of this tool
        self.params = {} #save params as a dictionary; send to following classes
        self.select_mode()

    def welcome(self):
        print("Welcome to QuakeLabeler----Fast AI Earthquake Dataset Deployment Tool!")


    def input_stn_stn(self):
        r"""Station Region Mode: <STN>:
        """
        self.params['stnsearch'] = 'STN'
        self.params['sta_list'] = input('Please enter the station codes:  \n ')

        confirm = input('Input parameters confirm?  [y/n] \n')
        if confirm.lower() == 'y':
            return self.params
        else:
            print('Reset parameters... \n')
            self.input_stn_stn()


    def input_stn_rect(self):
        r"""Input station region in rectangular mode
        """
        self.params['stnsearch'] = 'RECT'
        print('Please enter the latitudes(-90 ~ 90) at the bottom and top, the longitudes(-180 ~ 180) on the left and the right of the rectangular boundary. \n ')
        self.params['stn_bot_lat'] = input('Input rectangular bottom latitude: ')
        self.params['stn_top_lat'] = input('Input rectangular top latitude: ')
        self.params['stn_left_lon'] = input('Input rectangular left longitude: ')
        self.params['stn_right_lon'] = input('Input rectangular right longitude: ')
        print('The input region is:  \n ')

        #print update params
        print('stnsearch: ' + self.params['stnsearch'] + '\n' +  \
        'stn_bot_lat: '+ self.params['stn_bot_lat'] + '\n' + \
        'stn_top_lat: '+ self.params['stn_top_lat'] + '\n' + \
        'stn_left_lon: '+ self.params['stn_left_lon'] + '\n' + \
        'stn_right_lon: '+ self.params['stn_right_lon'] +'\n'  )

        confirm = input('Input parameters confirm?  [y/n] \n')
        if confirm.lower() == 'y':
            return self.params
        else:
            print('Reset parameters... \n')
            self.input_stn_rect()


    def input_stn_circ(self):
        r"""Input station region in circular mode
        """
        self.params['stnsearch'] = 'CIRC'
        print('Please enter the latitude(-90 ~ 90) and longitude(-180 ~ 180) at the central of  the circular region, the unit for max distance and the related radius. \n \
              Note: Acceptable units of distance for a circular search: degrees or kilometres. \n \
              Radius for circular search region: \n \
              0 to 180 if max_dist_units=deg  \n \
              0 to 20015 if max_dist_units=km  \n ')
        self.params['stn_ctr_lat'] = input('Central latitude of circular region, possible value: -90 ~ 90: ')
        self.params['stn_ctr_lon'] = input('Central longitude of circular region, possible value: -180 ~ 180: ')
        self.params['max_stn_dist_units'] = input('Units of distance for a circular search (degrees or kilometres): [deg/km] ')
        if self.params['max_stn_dist_units'] == 'deg':
            self.params['stn_radius'] = input('Please enter radius for circular search region (0~180) degree: ')
        elif self.params['max_stn_dist_units'] == 'km':
            self.params['stn_radius'] = input('Please enter radius for circular search region (0~20015) km: ')
        else:
            print('Invalid distance unit input! ')
        #print update params
        print('stnsearch: ' + self.params['stnsearch'] + '\n' +  \
        'stn_ctr_lat: '+ self.params['stn_ctr_lat'] + '\n' + \
        'stn_ctr_lon: '+ self.params['stn_ctr_lon'] + '\n' + \
        'max_stn_dist_units: '+ self.params['max_stn_dist_units'] + '\n' + \
        'stn_radius: '+ self.params['stn_radius'] +'\n'  )

        confirm = input('Input parameters confirm?  [y/n] \n')
        if confirm.lower() == 'y':
            return self.params
        else:
            print('Reset parameters... \n')
            self.input_stn_circ()

    def input_stn_fe(self):
        self.params['stnsearch'] = 'FE'
        print('Enter parameters for a Flinn-Engdahl search region. \n')
        self.params['stn_srn'] = input('Seismic region number for a Flinn-Engdahl region search, possible value: 1 to 50: ')
        self.params['stn_grn'] = input('Geographic region number for a Flinn-Engdahl region search possible value: 1 to 757: ')

        #print update params
        print('stnsearch: ' + self.params['stnsearch'] + '\n' +  \
        'stn_srn: '+ self.params['stn_srn'] + '\n' + \
        'stn_grn: '+ self.params['stn_grn'] + '\n' )

        confirm = input('Input parameters confirm?  [y/n] \n')
        if confirm.lower() == 'y':
            return self.params
        else:
            print('Reset parameters... \n')
            self.input_stn_fe()

    def input_stn_poly(self):
        self.params['stnsearch'] = 'POLY'
        self.params['stn_coordvals'] = input('please enter [lat1,lon1,lat2,lon2,lat3,lon3,lat4,lon4,lat1,lon1]: \n \
                                             Comma seperated list of coordinates for a desired polygon. Latitude needs to be before longitude. Coordinates in the western and southern hemispheres should be negative.')

        #print update params
        print('stnsearch: ' + self.params['stnsearch'] + '\n' +  \
        'stn_coordvals: '+ self.params['stn_coordvals'] + '\n' )

        confirm = input('Input parameters confirm?  [y/n] \n')
        if confirm.lower() == 'y':
            return self.params
        else:
            print('Reset parameters... \n')
            self.input_stn_poly()

    def input_time(self):
        r"""Input <event-time-range> params
        """
        print('Please enter time range: \n')
        self.params['start_year'] = input('Input start year (1900-):  \n')
        self.params['start_month'] = input('Input start month(1-12): \n')
        self.params['start_day'] = input('Input start day (1-31):  \n')
        self.params['start_time'] = input('Input start time(00:00:00-23:59:59): \n')
        self.params['end_year'] = input('Input end year (1900-):  \n')
        self.params['end_month'] = input('Input end month(1-12): \n')
        self.params['end_day'] = input('Input end day (1-31):  \n')
        self.params['end_time'] = input('Input end time(00:00:00-23:59:59): \n')
        #print update params
        print('start_year: ' + self.params['start_year'] + '\n' +  \
        'start_month: '+ self.params['start_month'] + '\n' + \
        'start_day: '+ self.params['start_day'] + '\n' + \
        'start_time: '+ self.params['start_time'] + '\n' + \
        'end_year: '+ self.params['end_year'] + '\n' + \
        'end_month: '+ self.params['end_month'] + '\n' + \
        'end_day: '+ self.params['end_day'] + '\n' + \
        'end_time: '+ self.params['end_time'] + '\n'  )

        confirm = input('Input parameters confirm?  [y/n] \n')
        if confirm.lower() == 'y':
            return self.params
        else:
            print('Reset parameters... \n')
            self.input_time()

    def input_mag(self):
        r"""Input <event-magnitude-limits> (Optional) params
        """
        print('Enter event-maginitude limits (optional, enter blankspace for default sets)')
        default = input('Input minmum magnitude (0.0-9.0 or blankspace for skip this set):  \n')
        if not (default.isspace() or default == '\n'):
            self.params['min_mag'] = default

        default = input('Input maxmum magnitude (0.0-9.0 or blankspace for skip this set):  \n')
        if not (default.isspace() or default == '\n'):
            self.params['max_mag'] = default

        default = input('Enter specific magnitude types. Please note: the selected magnitude type will search for all possible magnitudes in that category: \n \
                        E.g. MB will search for mb, mB, Mb, mb1mx, etc \n \
                        Availble input: \n \
                        <Any>|<MB>|<MS>|<MW>|<ML>|<MD> or blankspace for skip this set  \n')
        if not (default.isspace() or default == '\n'):
            self.params['req_mag_type'] = default

    def select_stnsearch(self):
        r"""Choose mode for station region search
        """
        # default <request-type> & <arrivals-limits> (http://www.isc.ac.uk/iscbulletin/search/webservices/arrivals/)
        self.params['out_format'] = 'CSV'
        self.params['request'] = 'STNARRIVALS'
        self.params['ttime'] = 'on'
        self.params['ttres'] = 'on'
        self.params['tdef'] = 'on'
        self.params['iscreview'] = 'on'


        mode = input('Please select one : [STN/GLOBAL/RECT/CIRC/FE/POLY] \n \
                        [STN]: Stations are restricted to specific station code(s); \n \
                        [GLOBAL]: Stations are not restricted by region (i.e. all available stations); \n \
                        [RECT]: Rectangular search of stations (recommended); \n \
                        [CIRC]: Circular search of stations(recommended); \n \
                        [FE]: Flinn-Engdahl region search of stations; \n \
                        [POLY]: Customised polygon search. \n  ')
        if mode.lower() == 'stn':
            self.input_stn_stn()
        elif mode.lower() == 'global':
            self.params['stnsearch'] = 'GLOBAL'
        elif mode.lower() == 'rect':
            self.input_stn_rect()
        elif mode.lower() == 'circ':
            self.input_stn_circ()
        elif mode.lower() == 'fe':
            self.input_stn_fe()
        elif mode.lower() == 'poly':
            self.input_stn_poly()
        else:
            error = input('Invalid input, would you like to try input option again?  [y/n]')
            if error.lower() == 'y':
                self.select_stnsearch
            else:
                print('Exit process...')
        return self.params


    def input_event_rect(self):
        r"""Event Region Mode: <RECT>: Rectangular search of stations
        """
        self.params['searchshape'] = 'RECT'
        print('Please enter the latitudes(-90 ~ 90) at the bottom and top, the longitudes(-180 ~ 180) on the left and the right of the rectangular boundary. \n ')
        self.params['bot_lat'] = input('Input rectangular bottom latitude: ')
        self.params['top_lat'] = input('Input rectangular top latitude: ')
        self.params['left_lon'] = input('Input rectangular left longitude: ')
        self.params['right_lon'] = input('Input rectangular right longitude: ')
        print('The input region is:  \n ')

        #print update params
        print('searchshape: ' + self.params['searchshape'] + '\n' +  \
        'bot_lat: ' + self.params['bot_lat'] + '\n' + \
        'top_lat: ' + self.params['top_lat'] + '\n' + \
        'left_lon: ' + self.params['left_lon'] + '\n' + \
        'right_lon: ' + self.params['right_lon'] +'\n'  )

        confirm = input('Input parameters confirm?  [y/n] \n')
        if confirm.lower() == 'y':
            return self.params
        else:
            print('Reset parameters... \n')
            self.input_event_rect()


    def input_event_circ(self):
        r"""Event Region Mode: <CIRC>: Rectangular search of Events
        """
        self.params['searchshape'] = 'CIRC'
        print('Please enter the latitude(-90 ~ 90) and longitude(-180 ~ 180) at the central of  the circular region, the unit for max distance and the related radius. \n \
              Note: Acceptable units of distance for a circular search: degrees or kilometres. \n \
              Radius for circular search region: \n \
              0 to 180 if max_dist_units=deg  \n \
              0 to 20015 if max_dist_units=km  \n ')
        self.params['ctr_lat'] = input('Central latitude of circular region, possible value: -90 ~ 90: ')
        self.params['ctr_lon'] = input('Central longitude of circular region, possible value: -180 ~ 180: ')
        self.params['max_dist_units'] = input('Units of distance for a circular search (degrees or kilometres): [deg/km] ')
        if self.params['max_dist_units'] == 'deg':
            self.params['radius'] = input('Please enter radius for circular search region (0~180) degree: ')
        elif self.params['max_dist_units'] == 'km':
            self.params['radius'] = input('Please enter radius for circular search region (0~20015) km: ')
        else:
            print('Invalid distance unit input! ')
        #print update params
        print('searchshape: ' + self.params['searchshape'] + '\n' +  \
        'ctr_lat: ' + self.params['ctr_lat'] + '\n' + \
        'ctr_lon: ' + self.params['ctr_lon'] + '\n' + \
        'max_dist_units: '+ self.params['max_dist_units'] + '\n' + \
        'radius: ' + self.params['radius'] + '\n'  )

        confirm = input('Input parameters confirm?  [y/n] \n')
        if confirm.lower() == 'y':
            return self.params
        else:
            print('Reset parameters... \n')
            self.input_event_circ()

    def input_event_fe(self):
        self.params['searchshape'] = 'FE'
        print('Enter parameters for a Flinn-Engdahl search region. \n')
        self.params['srn'] = input('Seismic region number for a Flinn-Engdahl region search, possible value: 1 to 50: ')
        self.params['grn'] = input('Geographic region number for a Flinn-Engdahl region search possible value: 1 to 757: ')

        #print update params
        print('searchshape: ' + self.params['searchshape'] + '\n' +  \
        'srn: ' + self.params['srn'] + '\n' + \
        'grn: ' + self.params['grn'] + '\n' )

        confirm = input('Input parameters confirm?  [y/n] \n')
        if confirm.lower() == 'y':
            return self.params
        else:
            print('Reset parameters... \n')
            self.input_event_fe()


    def input_event_poly(self):
        self.params['searchshape'] = 'POLY'
        self.params['coordvals'] = input('please enter [lat1,lon1,lat2,lon2,lat3,lon3,lat4,lon4,lat1,lon1]: \n \
                                          Comma seperated list of coordinates for a desired polygon. Latitude needs to be before longitude. Coordinates in the western and southern hemispheres should be negative.')

        #print update params
        print('searchshape: ' + self.params['searchshape'] + '\n' +  \
        'coordvals: '+ self.params['coordvals'] + '\n' )

        confirm = input('Input parameters confirm?  [y/n] \n')
        if confirm.lower() == 'y':
            return self.params
        else:
            print('Reset parameters... \n')
            self.input_event_poly()


    def select_eventsearch(self):
        print('Enter event region parameters: \n ')
        mode = input('Please select one : [GLOBAL/RECT/CIRC/FE/POLY] \n \
                        [GLOBAL]: Events are not restricted by region; \n \
                        [RECT]: Rectangular search of events(recommended); \n \
                        [CIRC]: Circular search of events(recommended); \n \
                        [FE]: Flinn-Engdahl region search of events; \n \
                        [POLY]: Customised polygon search. \n  ')
        if mode.lower() == 'global':
            self.params['searchshape'] = 'GLOBAL'
        elif mode.lower() == 'rect':
            self.input_event_rect()
        elif mode.lower() == 'circ':
            self.input_event_circ()
        elif mode.lower() == 'fe':
            self.input_event_fe()
        elif mode.lower() == 'poly':
            self.input_event_poly()
        else:
            error = input('Invalid input, would you like to try input option again?  [y/n]')
            if error.lower() == 'y':
                self.select_eventsearch()
            else:
                print('Exit process...')
        return self.params

    def beginner_mode(self, field=1):
        r"""Run beginner mode
        User can use this method to select one example region to create dataset
        """
        # default params case[1] in Cascadia subduction zone
        self.params = {
            'out_format':'CSV',  #<QuakeML>|<CSV>|<IMS1.0>
        #    """<request-type>"""
            'request':'STNARRIVALS', #Specifies that the ISC Bulletin should be searched for arrivals.
        #    """<arrivals-limits>"""
            'ttime':'on', # arrivals will be only be output if they have an arrival-time.
            'ttres':'on', #  they have a travel-time residual computed.
            'tdef':'on', # if they are time-defining phases.
            'iscreview':'on', # in the Reviewed ISC Bulletin
        #    """station-region"""
            'stnsearch':'RECT',  #<STN>|<GLOBAL>|<RECT>|<CIRC>|<FE>|<POLY>
            'stn_bot_lat':'31.78', #    -90 to 90   #Bottom latitude of rectangular region
            'stn_top_lat':'46.48',  #-90 to 90  #Top latitude of rectangular region
            'stn_left_lon': '-128.47',  #-180 to 180    Left longitude of rectangular region
            'stn_right_lon':'-114.60',  #-180 to 180    Right longitude of rectangular region
            'start_year':'2010',
            'start_month':'1',
            'start_day':'7',
            'start_time':'01:00:00',
            'end_year':'2010',
            'end_month':'1',
            'end_day':'10',
            'end_time':'03:00:00',
            'min_mag':'3.0',
            'req_mag_agcy':'Any',
            'req_mag_type':'Any',
            }

        print('Initialize Beginner Mode...')
        field = input('Select one of the following sample fields:  [1/2/3/4] \n \
                      [1] 2010 Cascadia subduction zone earthquake activities \n \
                      [2] 2011 Tōhoku earthquake and tsunami \n \
                      [3] 2016 Oklahoma human activity-induced earthquakes \n \
                      [4] 2018 Big quakes in Southern California \n \
                      [0] Re-direct to Advanced mode. \n  '  )
        # input default parameters for specific case
        if field == '2':
            # 2011 Tōhoku earthquake and tsunami, Japan
            self.params = {
            #    """<output-format>"""
                'out_format':'CSV',  #<QuakeML>|<CSV>|<IMS1.0>
            #    """<request-type>"""
                'request':'STNARRIVALS', #Specifies that the ISC Bulletin should be searched for arrivals.
            #    """<arrivals-limits>"""
                'ttime':'on', # arrivals will be only be output if they have an arrival-time.
                'ttres':'on', #  they have a travel-time residual computed.
                'tdef':'on', # if they are time-defining phases.
                'iscreview':'on', # in the Reviewed ISC Bulletin
            #    """station-region"""
                'stnsearch':'RECT',  #<STN>|<GLOBAL>|<RECT>|<CIRC>|<FE>|<POLY>
                'stn_bot_lat':'30.0', #  -90 to 90   #Bottom latitude of rectangular region
                'stn_top_lat':'44.0',    #-90 to 90  #Top latitude of rectangular region
                'stn_left_lon': '135.0', #-180 to 180    Left longitude of rectangular region
                'stn_right_lon':'150.0',     #-180 to 180    Right longitude of rectangular region
                'start_year':'2011',
                'start_month':'3',
                'start_day':'11',
                'start_time':'08:00:00',
                'end_year':'2011',
                'end_month':'3',
                'end_day':'11',
                'end_time':'23:00:00',
                'min_mag':'1.0',
                'req_mag_agcy':'Any',
                'req_mag_type':'Any',
                }

        if field == '3':
            #2016 Oklahoma human activity-induced earthquakes
            self.params = {
            #    """<output-format>"""
                'out_format':'CSV',  #<QuakeML>|<CSV>|<IMS1.0>
            #    """<request-type>"""
                'request':'STNARRIVALS', #Specifies that the ISC Bulletin should be searched for arrivals.
            #    """<arrivals-limits>"""
                'ttime':'on', # arrivals will be only be output if they have an arrival-time.
                'ttres':'on', #  they have a travel-time residual computed.
                'tdef':'on', # if they are time-defining phases.
                'iscreview':'on', # in the Reviewed ISC Bulletin
            #    """station-region"""
                'stnsearch':'RECT',  #<STN>|<GLOBAL>|<RECT>|<CIRC>|<FE>|<POLY>
                'stn_bot_lat':'33.0', #  -90 to 90   #Bottom latitude of rectangular region
                'stn_top_lat':'36.0',    #-90 to 90  #Top latitude of rectangular region
                'stn_left_lon': '-100.0', #-180 to 180    Left longitude of rectangular region
                'stn_right_lon':'-95.0',     #-180 to 180    Right longitude of rectangular region
                'start_year':'2016',
                'start_month':'7',
                'start_day':'1',
                'start_time':'08:00:00',
                'end_year':'2016',
                'end_month':'7',
                'end_day':'30',
                'end_time':'23:00:00',
                'min_mag':'1.0',
                'req_mag_agcy':'Any',
                'req_mag_type':'Any',
                }
        if field == '1':
            #2010 Cascadia subduction zone earthquake activities, NA
            self.params= {
            #    """<output-format>"""
                'out_format':'CSV',  #<QuakeML>|<CSV>|<IMS1.0>
            #    """<request-type>"""
                'request':'STNARRIVALS', #Specifies that the ISC Bulletin should be searched for arrivals.
            #    """<arrivals-limits>"""
                'ttime':'on', # arrivals will be only be output if they have an arrival-time.
                'ttres':'on', #  they have a travel-time residual computed.
                'tdef':'on', # if they are time-defining phases.
                'iscreview':'on', # in the Reviewed ISC Bulletin
            #    """station-region"""
                'stnsearch':'RECT',  #<STN>|<GLOBAL>|<RECT>|<CIRC>|<FE>|<POLY>
                'stn_bot_lat':'40.00', #    -90 to 90   #Bottom latitude of rectangular region
                'stn_top_lat':'55.00',  #-90 to 90  #Top latitude of rectangular region
                'stn_left_lon': '-130.00',  #-180 to 180    Left longitude of rectangular region
                'stn_right_lon':'-120.00',  #-180 to 180    Right longitude of rectangular region
                'start_year':'2010',
                'start_month':'9',
                'start_day':'7',
                'start_time':'01:00:00',
                'end_year':'2010',
                'end_month':'9',
                'end_day':'20',
                'end_time':'03:00:00',
                'min_mag':'3.0',
                'req_mag_agcy':'Any',
                'req_mag_type':'Any',
                }
        if field == '4':
            # 2018 Big quakes in Southern California
            self.params= {
            #    """<output-format>"""
                'out_format':'CSV',  #<QuakeML>|<CSV>|<IMS1.0>
            #    """<request-type>"""
                'request':'STNARRIVALS', #Specifies that the ISC Bulletin should be searched for arrivals.
            #    """<arrivals-limits>"""
                'ttime':'on', # arrivals will be only be output if they have an arrival-time.
                'ttres':'on', #  they have a travel-time residual computed.
                'tdef':'on', # if they are time-defining phases.
                'iscreview':'on', # in the Reviewed ISC Bulletin
            #    """station-region"""
                'stnsearch':'RECT',  #<STN>|<GLOBAL>|<RECT>|<CIRC>|<FE>|<POLY>
                'stn_bot_lat':'32.00', #    -90 to 90   #Bottom latitude of rectangular region
                'stn_top_lat':'42.00',  #-90 to 90  #Top latitude of rectangular region
                'stn_left_lon': '-124.00',  #-180 to 180    Left longitude of rectangular region
                'stn_right_lon':'-114.00',  #-180 to 180    Right longitude of rectangular region
                'start_year':'2018',
                'start_month':'1',
                'start_day':'1',
                'start_time':'01:00:00',
                'end_year':'2018',
                'end_month':'12',
                'end_day':'31',
                'end_time':'00:00:00',
                'min_mag':'6.5',
                'req_mag_agcy':'Any',
                'req_mag_type':'Any',
                }

        if field == '0':
            # run advanced mode
            self.params = {}
            self.advanced_mode()


    def advanced_mode(self):
        r"""Run advanced mode
        This method is to run a command line interactive module to let user to
        design their own research region and time range settings.
        """
        print('Initialize Advanced Mode...')
        print('Alternative region options are provided. Please select your preferred input function: \n ')

        # 1.select stnsearch mode ;
        # 2.input <station-region> params;
        # 3.input <event-region> params (note that station / event region can be different);
        # 4.input <event-time-range> & <event-magnitude-limits> (Optional)
        self.select_stnsearch()
        self.select_eventsearch()
        self.input_time()
        self.input_mag()

    def select_mode(self):
        r"""Mode selection
        Returns
        -------
        beginner_mode : function
            Run beginner mode `self.beginner_mode()` with default parameters.
        advanced_mode : function
            Run advanced mode `self.advanced_mode()` with various customized
            options.

        """
        print('QuakeLabeler provides multiple modes for different levels of Seismic AI researher \n ')
        print('[Beginner] mode -- well prepared case studies; \n' +\
               '[Advanced] mode -- produce earthquake samples based on Customized parameters. \n')
        mode = input("Please select a mode: [1/Beginner/2/Advanced] ")
        if (mode == '1') or (mode.lower() == 'beginner'):
            return self.beginner_mode()
        else:
            if mode =='2' or mode.lower() == 'advanced':
                return self.advanced_mode()
            else:
                error = input('Invalid input, would you like restart choosing mode?  [y/n]')
                if error == 'y':
                    self.select_mode()
                else:
                    print('exit the process! ')

#%%
class CustomSamples():
    r"""Command line interactive tool for custom dataset options
    Input paratemter to standardize retrived waveform.
    Parameters
    ----------
    default_option : bool
        if `default_option` is True, apply default options.
    """
    def __init__(self, default_option = False):

        print('Please define your own expection for Seismic labled samples: \n')
        if default_option:
            self.custom_dataset = {'volume': '10', 'fixed_length': True, 'sample_length': 5000}
            self.custom_waveform = {'label_type': True, 'sample_rate': '', 'filter_type': '0', 'detrend': False, 'random_arrival': True, 'add_noise': 0}
            self.custom_export = {'export_type': 'SAC', 'single_trace': True, 'export_inout': True, 'export_arrival_csv': True, 'export_filename': 'SampleDataset', 'export_stats': True}
        else:
            self.custom_dataset = {}
            self.custom_dataset = {}
            self.custom_waveform = {}
            self.custom_export = {}

        self.default_option = default_option

    def init(self):
        if not self.default_option:
            self.define_dataset()
            self.define_waveform()
            self.define_export()

    def define_dataset(self):
        r"""Dataset options

        Returns
        -------
        custom_dataset : dict
            `custom_dataset` returns a dict which saves all dataset options.
        """
        # set default volume
        self.custom_dataset['volume'] = '5'
        self.custom_dataset['volume'] = input('How many samples do you wish to create? [1- ] (input MAX for all available waveform):')
        default = input('Do you want fixed sample length? [y/n] (default: y):')
        if not default.lower() == 'n':
            self.custom_dataset['fixed_length'] = True
            length = input('Enter sample length (how many sample points do you wish in a trace)?(default 5000): ')
            try:
                self.custom_dataset['sample_length'] = int(length)
            except Exception:
                self.custom_dataset['sample_length'] = 5000
        else:
            self.custom_dataset['fixed_length'] = False
        return self.custom_dataset

    def define_waveform(self):
        r"""Waveform options
        Receive waveform format

        Returns
        -------
        custom_waveform : dict
            Returns a dictionary which saves all waveform options.

        """
        label_type = input('Select label type: [simple/specific]? \n' + \
                           '[simple]: P/S; \n'+'[specific]: P/Pn/Pb/S/Sn,etc. \n ')
        if label_type.lower() == 'simple':
            self.custom_waveform['label_type'] = False
        else:
            self.custom_waveform['label_type'] = True
        #set default
        self.custom_waveform['sample_rate'] = ''
        self.custom_waveform['sample_rate'] = input('Enter a fixed sampling rate(i.e.: 100.0) or skip for keep original sampling rate: ')
        #set default
        self.custom_waveform['filter_type'] = '0'
        self.custom_waveform['filter_type'] = input('Select filter function for preprocess? [0/1/2/3]: \n' + \
                                                    ' [0]: Do not apply filter function; \n ' +
                                                    '[1]: Butterworth-Lowpass; \n ' + \
                                                    '[2]: Butterworth-Highpass; \n ' + \
                                                    '[3]: Butterworth-Bandpass. ')

        if self.custom_waveform['filter_type'] == '1':
            self.custom_waveform['filter_freqmin'] = float(input('Pass band low corner frequency.'))
        if self.custom_waveform['filter_type'] == '2':
            self.custom_waveform['filter_freqmax'] = float(input('Pass band high corner frequency.'))
        if self.custom_waveform['filter_type'] == '3':
            self.custom_waveform['filter_freqmin'] = float(input('Pass band low corner frequency.'))
            self.custom_waveform['filter_freqmax'] = float(input('Pass band high corner frequency.'))

        detrend = input('Do you want to detrend the waveforms ? [y/n]')
        if detrend == 'y':
            self.custom_waveform['detrend'] = True
        else:
            self.custom_waveform['detrend'] = False

        random_arrival = input('Would you like random input? [y/n]')
        if random_arrival == 'y':
            self.custom_waveform['random_arrival'] = True
        else:
            self.custom_waveform['random_arrival'] = False
        if self.custom_waveform['random_arrival'] == False:
            #set default
            self.custom_waveform['start_arrival'] = 30.0
            self.custom_waveform['end_arrival'] = 90.0
            self.custom_waveform['start_arrival'] = input('Input waveforms start at: __ seconds before arrival.') #  set  30/60/90 s before P arrival ~  30/60/90 s after S arrival ; may raise conflict with fixed sample points (i.e.: 5000points for each trace)
            self.custom_waveform['start_arrival'] = float(self.custom_waveform['start_arrival'])
            self.custom_waveform['end_arrival'] = input('Input waveforms end at: __ seconds after arrival.') #  set  30/60/90 s before P arrival ~  30/60/90 s after S arrival ; may raise conflict with fixed sample points (i.e.: 5000points for each trace)
            self.custom_waveform['end_arrival'] = float(self.custom_waveform['end_arrival'])
        add_noise = input('Do you want to add random noise: [y/n] ')
        if add_noise == 'y':
            noiselevel = input('Enter noise level(i.e.: [0.3 /0.5 / 0.8 / 1.0 / 2.0]  ):')
            self.custom_waveform['add_noise'] = float(noiselevel)
        else:
            self.custom_waveform['add_noise'] = 0

        return self.custom_waveform


    def define_export(self):
        r""" Export options for dataset
            Receive interactive arguements to choose export format, include:
                #. export_type: SAC, Mini-Seed, NPZ, MAT, etc.
                #. export_inout: True/False seperate input / output traces
                #. export_out_form: gaussian / peak / rect
                #. export_arrival_csv: True / False
                save arrival information as a independent csv file
                #. export_stats: True / False

        Returns
        -------
        custom_export : dict
            Export options for dataset.

        """
        # seperate dataset as: input and output trace
        # input: Original trace
        # output: Probability density function
        self.custom_export['export_type'] = input('Select export file format: [SAC/MSEED/SEGY/NPZ/MAT]')
        self.custom_export['export_type'] = self.custom_export['export_type'].upper()
        if 'NPZ' in self.custom_export['export_type'] or 'MAT' in self.custom_export['export_type']:
            warnings.warn('Export to external format might lose traces information! ')

        # single trace: 1 sample 1 trace
        # multiple traces: 1 sample 1 stream 1+ traces (i.e. 3 traces: BHZ,BHE,BHN)
        self.custom_export['single_trace'] = input('Save as single trace or mutiple-component seismic data? [y/n]')
        if self.custom_export['single_trace'].lower() == 'y':
            self.custom_export['single_trace'] = True
        else:
            self.custom_export['single_trace'] = False

        in_out = input('Do you want to seperate save traces as input and output? [y/n]')
        if in_out == 'y':
            self.custom_export['export_inout'] = True
        else:
            self.custom_export['export_inout'] = False

        # save each label information into csv files for validation
        # i.e.: arrival time, magnitude, etc.
        arrival_csv = input('Do you want to seperate save arrival information as a CSV file? [y/n]')
        if arrival_csv == 'y':
            self.custom_export['export_arrival_csv'] = True
        else:
            self.custom_export['export_arrival_csv'] = False

        # filename option
        self.custom_export['export_filename'] = input('Please input a folder name for your dataset (optional): ')

        # export statistical figures
        stats = input('Do you want to generate statistical charts after creating the dataset? [y/n]')
        if stats == 'y':
            self.custom_export['export_stats'] = True
        else:
            self.custom_export['export_stats'] = False


        return self.custom_export


class QueryArrival():
    r"""Auto request online arrivals catalog
    This class fetch users's target arrivals from ISC Bulletin website.

    References
    ----------
    [1] International Seismological Centre (20XX), On-line Bulletin,
    https://doi.org/10.31905/D808B830

    """
    def __init__(self, **kwargs ):
        # ISC Bulletin url
        URL = 'http://www.isc.ac.uk/cgi-bin/web-db-v4'
        # init params dict
        self.param = {}
        # save params
        for k in kwargs:
            self.param[k] = kwargs[k]
        print("Loading time varies on your network connections, search region scale, time range, etc. Please be patient, estimated time: 3 mins ")
        self.response = requests.get(url = URL, params=self.param)
        self.page_text = self.response.text

        if "No phase data was found." in self.page_text:
            print("Error: No phase data was found. \n")
            exit("Please change your parameters and restart of the tool ... \n")

        try:
            self.find_all_vars(self.page_text, 'EVENTID', 'STA', 'ISCPHASE',
            'ARRIVAL_DATE', 'ARRIVAL_TIME', 'ORIGIN_DATE', 'ORIGIN_TIME',
            'EVENT_TYPE', 'EVENT_MAG')
        except IndexError:
            print('Please try it later. Request failed.')
        else:
            print('Request completed！！！')
            print("%d events have been found!"% len(self.arrival_recordings))


    def find_all_vars(self, text, *args):
        r"""Store all arrival information
        This method save all fetched information into `recordings`:
            #. EVENTID
            #. STA
            #. PHASE NAME
            #. ARRIVAL DATE
            #. ARRIVAL TIME
            #. ORIGIN DATE
            #. ORIGIN TIME
            #. EVENT TYPE
            #. EVENT MAG
        """
        ex = r'MAG (.*) '
        all_variables = re.findall(ex, text, re.S)
        all_vars = re.split(r',', all_variables[0])
        #find last index
        for index in range(len(all_vars) - 1, 0, -1):
            if 'STOP' in all_vars[index]:
                break
        # initialization of recording, include all webset information
        recordings = {
        'EVENTID' : [] ,
        'STA' : [],
        'CHN' : [],
        'ISCPHASE' : [],
        'REPPHASE' : [],
        'ARRIVAL_LAT' : [],
        'ARRIVAL_LON' : [],
        'ARRIVAL_ELEV' : [],
        'ARRIVAL_DIST' : [],
        'ARRIVAL_BAZ' : [],
        'ARRIVAL_DATE' : [],
        'ARRIVAL_TIME' : [],
        'ORIGIN_LAT' : [],
        'ORIGIN_LON' : [],
        'ORIGINL_DEPTH' : [],
        'ORIGIN_DATE' : [],
        'ORIGIN_TIME' : [],
        'EVENT_TYPE' :[],
        'EVENT_MAG' : [] }

        for i in range(0, index, 25):
            recordings['EVENTID'].append(int(re.split('\n',all_vars[i])[1]))
            recordings['STA'].append(str.strip(all_vars[i+2]))
            recordings['CHN'].append(str.strip(all_vars[i+6]))
            recordings['ISCPHASE'].append(str.strip(all_vars[i+9]))
            recordings['REPPHASE'].append(str.strip(all_vars[i+10]))
            recordings['ARRIVAL_LAT'].append(float(all_vars[i+3]))
            recordings['ARRIVAL_LON'].append(float(all_vars[i+4]))
            recordings['ARRIVAL_ELEV'].append(float(all_vars[i+5]))
            recordings['ARRIVAL_DIST'].append(float(all_vars[i+7]))
            recordings['ARRIVAL_BAZ'].append(float(all_vars[i+8]))
            recordings['ARRIVAL_DATE'].append(str.strip(all_vars[i+11]))
            recordings['ARRIVAL_TIME'].append(str.strip(all_vars[i+12]))
            recordings['ORIGIN_LAT'].append(float(all_vars[i+20]))
            recordings['ORIGIN_LON'].append(float(all_vars[i+21]))
            recordings['ORIGINL_DEPTH'].append(float(all_vars[i+22]))
            recordings['ORIGIN_DATE'].append(str.strip(all_vars[i+18]))
            recordings['ORIGIN_TIME'].append(str.strip(all_vars[i+19]))
            recordings['EVENT_TYPE'].append(str.strip(all_vars[i+24]))
            if str.isspace(re.split('\n', all_vars[i+25])[0]):
                recordings['EVENT_MAG'].append(float('NaN'))
            else:
                recordings['EVENT_MAG'].append(float(re.split('\n', all_vars[i+25])[0]))

        self.arrival_recordings = []
        for i in range(len(recordings['EVENTID'])):
            tempdict = {}
            for var in args:
                tempdict[var] = recordings[var][i]
            self.arrival_recordings.append(tempdict)
        return self.arrival_recordings
