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

"""
Created on Sun Mar 21 10:00:06 2021
Query event / station information from ISC website by request package
Fetch EVENTID, STATION, ISCPHASE, REPPHASE, ARRIVALTIME, ORIGINALTIME


@author: hao
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from seiscreator import QueryArrival

def main():
    param = {
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
        'stn_bot_lat':'11.78', #    -90 to 90   #Bottom latitude of rectangular region
        'stn_top_lat':'43.48',  #-90 to 90  #Top latitude of rectangular region
        'stn_left_lon': '119.47',   #-180 to 180    Left longitude of rectangular region
        'stn_right_lon':'153.60',   #-180 to 180    Right longitude of rectangular region
        'start_year':'2010',
        'start_month':'1',
        'start_day':'7',
        'start_time':'01:00:00',
        'end_year':'2010',
        'end_month':'1',
        'end_day':'7',
        'end_time':'03:00:00',
        'min_mag':'1.0',
        'req_mag_agcy':'Any',
        'req_mag_type':'Any',
        }

    #%%
    params= {
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
    # query1 = QueryArrival(params)
    # recordings1 = query1.generate_arrival_records()
    query = QueryArrival(**params)

    #print(query.event_id)
    #recordings = query.generate_arrival_records()

#%%
if __name__ == '__main__':

    main()
