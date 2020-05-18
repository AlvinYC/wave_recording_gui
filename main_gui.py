from tkinter import Tk, Label, Button
import wave
import time
import numpy as np
import pyaudio
import  tkinter as tk
import PIL  #,Image 
from PIL import ImageTk 
import datetime
import threading
import os
import glob
import re


class NCSISTGUI:
    def __init__(self, master):
        self.master = master
        self.row_image1 = PIL.Image.open("./image/micro3.png").resize((150,150),PIL.Image.ANTIALIAS)
        self.row_image2 = PIL.Image.open("./image/pause3.png").resize((150,150),PIL.Image.ANTIALIAS)
        self.reco_im = ImageTk.PhotoImage(self.row_image1)  
        self.stop_im = ImageTk.PhotoImage(self.row_image2)  
        # buttom timing parameter
        self.start_time = ''  # Begin when streaming start
        self.BOS_time = ''  # Begin of Speech time
        self.EOS_time = ''  # End of Speech time
        self.click = 0
        # recording parameter
        self.stream = None
        self.frames= []
        self.pa = pyaudio.PyAudio()
        self.recording_format = pyaudio.paInt16
        self.recording_chunk = 3024
        self.recording_sample_rate = 16000
        self.recording_channel = 1
        # output file name parameter
        self.date_folder_name=str(time.strftime("%Y_%m_%d", time.localtime()))
        self.recoder='alvin'
        self.save_wave_name = ''
        self.save_label_name = ''
        self.save_label_content = ''

        master.title(" NCSIST Meeting Record")

        self.label = Label(master, text="This is our first GUI!")
        self.label.pack()
        self.button_start =Button(master,image=self.reco_im, command=self.press_button_play)
        self.button_start.pack(side="left")
        self.button_stop = Button(master,image=self.stop_im, command=self.press_button_stop)
        self.button_stop.pack(side="right")

        self.wave_name_generate()
        my_thread = threading.Thread(target=self.start_record)
        my_thread.setDaemon(True)#守護執行緒      
        my_thread.start()

    def wave_name_generate(self):
        # date dir generate
        if not os.path.isdir(self.date_folder_name):
            os.mkdir(self.date_folder_name)
        # author dir generate
        record_folder = self.date_folder_name + "/" +self. recoder 
        if not os.path.isdir(record_folder ):
            os.mkdir(record_folder)

        # output file: full path for wave and label name
        self.save_wave_name = record_folder + "/" + "record_original.wav"
        self.save_label_name = record_folder + "/" + "record_original.txt"

    def press_button_play(self):
        self.BOS_time = datetime.datetime.now() # 獲取當前時間
        BOS_duration = (self.BOS_time - self.start_time).total_seconds()
        print('\tpress_time = ' + str(BOS_duration))
        self.save_label_content += str(BOS_duration)  + '\t'
        self.swith_button_status('play')

    def press_button_stop(self):
        self.EOS_time = datetime.datetime.now() # 獲取當前時間
        EOS_duration = (self.EOS_time - self.start_time).total_seconds()
        print('---- stop time = ' + str(self.EOS_time))
        self.save_label_content += str(EOS_duration) + '\tsepaker\n'
        print("已錄時間： ", EOS_duration)    
        self.swith_button_status('stop')   
            
    def swith_button_status(self,trigger):
        # dobule click check mechanism
        if  (trigger=='play' and str(self.button_start['state']) == 'disabled'): return
        if  (trigger=='stop' and str(self.button_stop['state']) == 'disabled'): return

        if trigger=='stop':
            self.button_stop.config(state = 'disabled')
            self.button_start.config(state = 'active')
        else:
            self.button_start.config(state = 'disabled')
            self.button_stop.config(state = 'active')
        self.master.update

    def on_closing(self):
        
        wf = wave.open(self.save_wave_name, 'wb')
        wf.setnchannels(self.recording_channel)
        wf.setsampwidth(2)
        wf.setframerate(self.recording_sample_rate)
        print('after sample rate = ' + str(wf.getframerate()))
        wf.writeframes(np.array(self.frames).tostring())
        wf.close()  
        
        f1 = open(self.save_label_name, 'w', encoding='utf-8')
        f1.write(self.save_label_content)
        f1.close()
        print("Saved")      

        #self.stream.stop_stream()
        #self.stream.close()
        #self.pa.terminate()   
        self.master.destroy()

    def start_record(self):
        print("* recording")
        self.stream = self.pa.open(format=self.recording_format, 
                                                        channels=self.recording_channel, 
                                                        rate=self.recording_sample_rate, 
                                                        input=True,
                                                        frames_per_buffer=self.recording_chunk)
        self.stream.start_stream()
        self.start_time = datetime.datetime.now()
        while True:
            data = self.stream.read(self.recording_chunk, exception_on_overflow = False)
            self.frames.append(data)
    
    def greet(self):
        print("Greetings!")

if __name__== "__main__":
    root = Tk()
    my_gui = NCSISTGUI(root)
    root.protocol("WM_DELETE_WINDOW", my_gui.on_closing)
    root.mainloop()