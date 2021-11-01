#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 10:29:25 2021
Transfer QuakeLabeler CSV to PhaseNet CSV
@author: hao
"""
import pandas as pd
filename = "./phasenet/cascade_features.csv"
#def qltophasenet(filename):
df = pd.read_csv(filename)
df.filename.head()
    
