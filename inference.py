#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 14:43:38 2020

@author: c95hcw
"""
import time
import librosa
import numpy as np
import configparser


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()   
    return idx,array[idx]

#def segment_by_time(time_labels,i):
#    t1,c1 = find_nearest(time1[:],float(time_labels[i][0]))
#    t2,c2 = find_nearest(time1[:],float(time_labels[i][1]))
#    wav_name = time_labels[i][2]
#    save_wave_name = today_date + "/" + inference_file + "/" + wav_name + ".wav"    
#    librosa.output.write_wav(save_wave_name, wave_data[t1:t2], sr,norm=False)#.astype(np.int16)

def segment_by_time(time1,time_s,time_e,wav_n):
    t1,c1 = find_nearest(time1[:],float(time_s))
    t2,c2 = find_nearest(time1[:],float(time_e))
    wav_name = wav_n
    save_wave_name = today_date + "/" + inference_file + "/" + wav_name + ".wav"    
    librosa.output.write_wav(save_wave_name, wave_data[t1:t2], sr,norm=False)#.astype(np.int16)


samplerate = 16000
today_date=str(time.strftime("%Y_%m_%d", time.localtime()))

inference_file = "test"

wav_path = today_date + "/" + inference_file + "/record_original.wav"
timel_path = today_date + "/" + inference_file + "/record_original.txt"



f_txt = open(timel_path, "r")

string = f_txt.readlines()
f_txt.close()

time_start = []
time_end = []
wav_name=[]

for context in string:    
    strs=context.split("\n",1) # separet wave_name and label
    time_label=strs[0].split("\t",3) # clean labels的空白行   
    time_start.append(time_label[0]) # 
    time_end.append(time_label[1]) #  
    wav_name.append(time_label[2])

wave_data, sr = librosa.load(wav_path,samplerate) 
time1 = np.arange(0, len(wave_data)) * (1.0 / sr)

#map(lambda x,y,z : segment_by_time(time1,x,y,z),time_start,time_end,wav_name)

for i in  range(len(time_start)):
    time_s = time_start[i]
    time_e = time_end[i]
    wav_n = wav_name[i]
    segment_by_time(time1,time_s,time_e,wav_n)