# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 15:16:21 2025

@author: peo0005
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

class TCSPC():
    def __init__(self,path):
        self.df_counts = pd.read_csv(path, skiprows=10, delimiter = '\t',header= None).dropna(axis=1)
        
        # find the time resolutions
        target_text = "#ns/channel"

        with open(path, 'r') as file:
            previous_line = None
            for line in file:
                # Check if the previous line matches the target text
                if previous_line and previous_line.strip() == target_text:
                    self.time_res =  np.fromstring(line.strip(), sep='\t')
                    break
                # Update the previous line
                previous_line = line
        

        self.df_time = pd.DataFrame(0, index=self.df_counts.index, columns=self.df_counts.columns)

        for i in range(len(self.df_counts.columns)):
            time = range(len(self.df_counts.index))*self.time_res[i]
            self.df_time[i] = time

    def plot(self,channel, bgchannel = None, xlim = None, smooth = None):
        #do bg subtraction if specified
        if bgchannel is None:
            ydata = self.df_counts[channel]
        else:
            ydata = self.df_counts[channel] - self.df_counts[bgchannel]
            

            
        plt.plot(self.df_time[channel],ydata)
        
        if smooth is not None:
            ydata_smooth = savgol_filter(ydata, window_length=smooth, polyorder=3)
            plt.plot(self.df_time[channel],ydata_smooth)
        if xlim is not None:
            plt.xlim(xlim)
        plt.xlabel('Time [ns]')

    def getData(self, channel, bgchannel = None, smooth = None):
        #do bg subtraction if specified
        if bgchannel is None:
            ydata = self.df_counts[channel]
        else:
            ydata = self.df_counts[channel] - self.df_counts[bgchannel]

        if smooth is not None:
            ydata_smooth = savgol_filter(ydata, window_length=smooth, polyorder=3)

        result_df = pd.DataFrame({'time': self.df_time[channel], 'counts': ydata_smooth})
        return result_df
        