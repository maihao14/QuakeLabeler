#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Core fuctions of SeisLabelCreator
Created on Sun Feb 21 20:22:25 2021
@author: Hao

"""

from seiscreator import *

def main():
    r"""command line SeisLabelCreator(slc) tools
    This is all command line modules for slc. Modules rely on previous command
    line interactive parameters (data retrieved from users on command line). It 
    might raise errors if you skip some of the modules to direct use the later 
    ones.
    
    Methods
    -------    
    Interactive()
        Command line tool for retrieve user's input research region and event 
    time range. 'Interactive()' also includes interactive module to confirm 
    which modes(beginner/advanced) should slc run in the following functions.
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
    creatlabels = SeisCreator(query, custom)
    creatlabels.fetch_all_waveforms(creatlabels.recordings)
    

    creatlabels.csv_writer() 
    
    creatlabels.stats_figure()    
    #Neither Basemap nor Cartopy could be imported.

#%%    
if __name__ == '__main__':

    main()

