#!/usr/bin/env python3
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

"""Core fuctions of QuakeLabeler
Created on Sun Feb 21 20:22:25 2021
@author: Hao

"""

from quakelabeler import *
import logging

def main():
    r"""QuakeLabeler toolbox
    This is all functions for QuakeLabeler package. Running on command line
    interface. Follow user custom design to automatic generate datasets. It
    might raise errors if you skip some of the modules to direct use the later
    ones.

    Methods
    -------
    Interactive()
        Command line tool for retrieve user's input research region and event
    time range. 'Interactive()' also includes interactive module to confirm
    which modes(beginner/advanced) should ql run in the following functions.
    QueryArrival(**kwargs)
        Fetch arrivals information from ISC website by above user's input research
    region and time range.
    CustomSamples()
        Retrieve cutomized samples options by command line input.
    QuakeLabeler(query, custom)
        Calling sample production functions by above input options. All available
    samples will be automatically created and save as set format.
    Returns
    -------
    None.

    """

    user_interface = Interactive()
    # set logging 
    logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='a')
    # print user input params
    logging.info(user_interface.params)
    if not user_interface.benchmark_flag:
        # run normal mode: beginner / advanced
        query = QueryArrival(**user_interface.params)
    else:
        # run benchmark mode
        query = BuiltInCatalog(user_interface)
    # print query params
    logging.info("Created dataset folder: "+query.record_folder)      
    logging.info("Meta data filename: "+query.record_filename)
    # earthquake maps
    map_option = input("Do you want to display query results: [y]/n?")
    if not map_option.lower() == 'n':
        MT = MergeMetadata(query.record_folder)
        filelist = MT.select_folder()
        temp_pd = MT.merge_event(filelist)
        event_pd = MT.event_clean(temp_pd)
    # test station modules
        total_station = MT.merge_station(filelist)
        sta_cat = MT.station_clean(total_station)
        GM = GlobalMaps(sta_cat,event_pd)
        GM.hist_plot(event_pd)
        GM.event_station_map(event_pd,total_station)
        GM.event_map(event_pd)
        GM.station_map(sta_cat)
    # init custom options
    custom = CustomSamples(user_interface.receipe_flag)
    # run custom of dataset structure
    custom.init()
    # print custom info
    logging.info("custom_dataset options: \n")
    logging.info(custom.custom_dataset)
    logging.info("custom_waveform options: \n")
    logging.info(custom.custom_waveform)    
    logging.info("custom_export options: \n")
    logging.info(custom.custom_export)    
    
    # auto-production of dataset
    auto_dataset = QuakeLabeler(query, custom)
    # data collect and process
    if auto_dataset.params['local']:
        # local mode
        auto_dataset.local_label(auto_dataset.recordings)
    else:
        # normal mode    
        auto_dataset.fetch_all_waveforms(auto_dataset.recordings)
    # waveform graph
    if custom.custom_export['export_type'] == 'SAC':
        auto_dataset.waveform_display()
        
    # stats graph
    auto_dataset.stats_figure()
    if auto_dataset.custom_export['noise_trace']:
        auto_dataset.noisegenerator()
    # save relevant seismic features
    auto_dataset.csv_writer()
    # subfolder generator
    subfolder_option = input("Do you want to create training, test and validation sub-sets: [y]/n?")
    if not subfolder_option.lower() == 'n':
        auto_dataset.subfolder()

if __name__ == '__main__':
    # run QuakeLabler package
    main()
