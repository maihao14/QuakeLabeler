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
    if not user_interface.benchmark_flag:
        # run normal mode: beginner / advanced
        query = QueryArrival(**user_interface.params)

    else:
        # run benchmark mode
        query = BuiltInCatalog(user_interface)
    # init custom options    
    custom = CustomSamples(user_interface.receipe_flag)
    # run custom of dataset structure
    custom.init()
    # autp-production of dataset
    auto_dataset = QuakeLabeler(query, custom)
    # data collect and process
    auto_dataset.fetch_all_waveforms(auto_dataset.recordings)
    # save relevant seismic features
    auto_dataset.csv_writer()
    # waveform graph
    auto_dataset.waveform_display()
    # stats graph
    auto_dataset.stats_figure()
    # subfolder generator
    subfolder_option = input("Do you want to create training data and validation data: [y]/n?")
    if subfolder_option.lower() == 'y':
        auto_dataset.subfolder()
    
if __name__ == '__main__':
    # run QuakeLabler package
    main()
