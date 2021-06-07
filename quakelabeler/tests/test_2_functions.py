#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 09:24:49 2021

@author: hao
"""

#from obspy import *
import numpy as np
import os
import shutil

class testfunc():
    def __init__(self):
        #self.testsegy()
        self.custom_export = {'folder_name': "MyDataset2021-06-07"}
        self.test_subfolder()
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
    def testsegy(self):
        pass
        # st = read()
        # st1 = st
        # st2 = st
        # # st1 = st
        # it =500
        # pick_win =100
        # detect_win = 200
        # for tr in st1:
        #     tr.data = self.output_bell_dist(100, it, pick_win)
        # # st2 = st
        # for tr in st2:
        #     tr.data = self.output_rect_dist(100, it, detect_win)
        #         # require float32
        # for tr in st:
        #     tr.data = np.require(tr.data, dtype=np.float32)
        # for tr in st1:
        #     tr.data = np.require(tr.data, dtype=np.float32)
        # for tr in st2:
        #     tr.data = np.require(tr.data, dtype=np.float32)
        # filename = "testsegy" 
        # filename1 = "testsegybell"
        # st.write(filename + ".sgy", format="SEGY")
        # st1.write(filename1+ ".sgy", format="SEGY")
        # st2.write(filename +'out_rect'+ ".sgy", format="SEGY")
    def test_subfolder(self, trainratio=0.8):
        r"""Split dataset
        Divide dataset as a training dataset(80%) and a validation dataset(20%)
        """
        FileName = self.custom_export['folder_name']
        orgin_path = FileName
        os.chdir(orgin_path)
        if not os.path.exists('Training'):
            os.mkdir('Training')
        moved_path =  "Training"
        dir_files = os.listdir()
        filessum = len(dir_files)
        trainnum = int(filessum * trainratio)
        for file in dir_files[:trainnum]:
            #file_path = os.path.join(orgin_path, file)
            if os.path.isfile(file):
                shutil.move(file, moved_path)        
        if not os.path.exists('Validation'):
            os.mkdir('Validation')
        moved_path = "Validation"
        for file in dir_files[trainnum:]:
            #file_path = os.path.join(orgin_path, file)
            if os.path.isfile(file):
                shutil.move(file, moved_path)
        print("移动文件成功！")
        os.chdir('../')
    def test_background(self):
        pass
    def test_display_sample(self):
        pass
          
if __name__ == '__main__'  :
    test = testfunc()