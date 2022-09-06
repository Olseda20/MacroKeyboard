
from __future__ import print_function

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

from pycaw.pycaw import AudioUtilities


from pynput.keyboard import Key, Controller #https://pypi.org/project/pynput/

import serial
from time import sleep, time

from math import log, exp

from serial.serialwin32 import Serial
ser = serial.Serial('COM3', 115200, timeout=None)

class AudioController(object):
    def __init__(self, process_name):
        self.process_name = process_name
        self.volume = self.process_volume()

    def mute(self):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                interface.SetMute(1, None)
                print(self.process_name, 'has been muted.')  # debug

    def unmute(self):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                interface.SetMute(0, None)
                print(self.process_name, 'has been unmuted.')  # debug

    def process_volume(self):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                # print('Volume:', interface.GetMasterVolume())  # debug
                return interface.GetMasterVolume()

    def set_volume(self, decibels):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                # only set volume in the range 0.0 to 1.0
                self.volume = min(1.0, max(0.0, decibels))
                interface.SetMasterVolume(self.volume, None)
                # print('Volume set to', self.volume)  # debug

    # def decrease_volume(self, decibels):
    #     sessions = AudioUtilities.GetAllSessions()
    #     for session in sessions:
    #         interface = session.SimpleAudioVolume
    #         if session.Process and session.Process.name() == self.process_name:
    #             # 0.0 is the min value, reduce by decibels
    #             self.volume = max(0.0, self.volume-decibels)
    #             interface.SetMasterVolume(self.volume, None)
    #             print('Volume reduced to', self.volume)  # debug

    # def increase_volume(self, decibels):
    #     sessions = AudioUtilities.GetAllSessions()
    #     for session in sessions:
    #         interface = session.SimpleAudioVolume
    #         if session.Process and session.Process.name() == self.process_name:
    #             # 1.0 is the max value, raise by decibels
    #             self.volume = min(1.0, self.volume+decibels)
    #             interface.SetMasterVolume(self.volume, None)
    #             print('Volume raised to', self.volume)  # debug

def initiateAudioController():
    controller = []

    chan1_1, chan1_2 = 'brave','Twitch'
    chan2_1, chan2_2 = 'Spotify',''
    chan3_1, chan3_2 = 'Discord',''
    chan4_1, chan4_2 = 'csgo',''

    #channel 0 reserved for master volume
    #could be some kind of for loop for a list in a to create the individual channels
    
    #channel 1 (browser?)
    controller.append(AudioController(chan1_1 + '.exe'))
    controller.append(AudioController(chan1_2 + '.exe'))
    #channel 2 (multimedia spotify netflix..)
    controller.append(AudioController(chan2_1 + '.exe'))
    controller.append(AudioController(chan2_2 + '.exe'))

    #channel 3 
    controller.append(AudioController(chan3_1 + '.exe'))
    controller.append(AudioController(chan3_2 + '.exe'))

    #channel 4 (for games)
    controller.append(AudioController(chan4_1 + '.exe'))
    controller.append(AudioController(chan4_2 + '.exe'))

    return controller

def main():
    controller = initiateAudioController()

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

    master = cast(interface, POINTER(IAudioEndpointVolume))

    swPrev = []

    print('start')
    while True:
        try:

            #waiting for serial data
            data = (ser.readline().rstrip()).decode()
            dataEval = eval('[' + data + ']')[0]
            print(dataEval)
            #potentiometer and switch data
            pot, sw = dataEval
            # print(pot)

            for i in range(len(pot)):
                if i == 0:
                    masterVal = -78*exp(-3.97*pot[i])+1.452
                    master.SetMasterVolumeLevel(masterVal, None)
                elif i == 1:
                    #general media, brave, twitch? 
                    controller[0].set_volume(pot[i])
                    controller[1].set_volume(pot[i]) 
                elif i == 2:
                    #Spotify channel other media? (netflix?) 
                    controller[2].set_volume(pot[i])
                    controller[3].set_volume(pot[i])
                elif i == 3:
                    #Discord channel
                    controller[4].set_volume(pot[i])
                    controller[5].set_volume(pot[i])
                    pass                    
                elif i == 4:
                    #gaming channel
                    controller[6].set_volume(pot[i])
                    controller[7].set_volume(pot[i])
                    pass
                else:
                    pass
            
            # if time_check = 0:
            #     sw_time_now = time()
            # for i in range(len(sw)):
                #process only a keypress per time period?
                # time_recieved_data 
                # if sw == swPrev: 
                    
                #     time_recieved_data > 1s:
                # if 
                #     sw[0] = 
                
                #in time period set keypress to activate certain macros, probably 

            #     pass
            # swPrev = sw

        except:
            pass



if __name__ == "__main__":
    main()