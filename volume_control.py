
from __future__ import print_function

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

from pycaw.pycaw import AudioUtilities


from pynput.keyboard import Key, Controller #https://pypi.org/project/pynput/



import serial
from time import sleep

from math import log, exp
ser = serial.Serial('COM3', 115200, timeout=0.05)


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


def main():
    prevPot = [0,0,0,0,0]
    Spotify_controller = AudioController('Spotify.exe')
    brave_controller = AudioController('brave.exe')
    discord_controller = AudioController('Discord.exe')
    csgo_controller = AudioController('csgo.exe')
    steam_controller = AudioController('steam.exe')

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

    master = cast(interface, POINTER(IAudioEndpointVolume))

    while True:
        try:
            data = (ser.readline(66).rstrip()).decode()
            # print(data)
            dataEval = eval('[' + data + ']')[0]
            
            #potentiometer and switch data
            pot, sw = dataEval
            # print(pot)

            for i in range(len(pot)):
                if pot[i] - 0.01 <= prevPot[i] <= pot[i] + 0.01:
                    pass
                else:
                    if pot[i] <= 0.005:
                        pot[i] == 0
                    if i == 0:
                        masterVal = -78*exp(-3.97*pot[i])+1.452
                        master.SetMasterVolumeLevel(masterVal, None)
                    elif i == 1:
                        print(pot[i])
                        brave_controller.set_volume(pot[i])
                        csgo_controller.set_volume(pot[i]) 
                    elif i == 2:
                        Spotify_controller.set_volume(pot[i])
                        pass
                    elif i == 3:
                        # discord_controller.set_volume(pot[i])  
                        steam_controller.set_volume(pot[i])
                        pass                    
                    elif i == 4:
                        pass
                    else:
                        pass
                    prevPot = pot

        except:
            pass



if __name__ == "__main__":
    main()