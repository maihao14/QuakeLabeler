from seiscreator import *

#2010 Cascadia subduction zone earthquake activities, NA
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

def test_query_arrival():
	query = QueryArrival(**params)
	return query

def test_custom_samples():
    custom = CustomSamples(True)
    custom.init()
    return custom

def test_SeisCreator():
	query = test_query_arrival()
	custom = test_custom_samples()
	creatlabels = SeisCreator(query, custom)
	creatlabels.fetch_all_waveforms(creatlabels.recordings)
	return creatlabels