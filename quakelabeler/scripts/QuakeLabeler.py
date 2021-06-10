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
    r"""command line QuakeLabeler(ql) tools
    This is all command line modules for ql. Modules rely on previous command
    line interactive parameters (data retrieved from users on command line). It
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
    SeisCreator(query, custom)
        Calling sample production functions by above input options. All available
    samples will be automatically created and save as set format.
    Returns
    -------
    None.

    """


    InteractiveTest = Interactive()
    query = QueryArrival(**InteractiveTest.params)
    #use default options
    custom = CustomSamples()
    custom.init()
    creatlabels = QuakeLabeler(query, custom)
    creatlabels.fetch_all_waveforms(creatlabels.recordings)
    creatlabels.waveform_display()
    creatlabels.csv_writer()
    creatlabels.stats_figure()
    creatlabels.subfolder()
    #Neither Basemap nor Cartopy could be imported.

#%%
if __name__ == '__main__':

    main()
