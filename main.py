# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

from machine import Pin, ADC, UART
import time 
import math

uart = UART(1, 115200)                                      # init with given baudrate
uart.init(115200, bits=8, parity=None, stop=1, txbuf=66)    # init with given parameters

if __name__ == "__main__":
    print('start')
    
    pot_max_val = 4095

    potPins = [34,36,32,33,39]
    potLen = len(potPins)
    pot = potVal = prevPotVal =[0] * potLen

    swPins = [23,21,18,4,27,22,19,5,26,14]
    swLen = len(swPins)
    sw = swVal = prevSwVal = swSend = [0] * swLen


    while True:
        change = 0
        #Process the Pot Data
        for i in range(potLen):
            pot = ADC(Pin(potPins[i]))
            pot.atten(ADC.ATTN_11DB)
            currPotVal = round(pot.read()/pot_max_val,3)
            
            if currPotVal - 0.01 <= prevPotVal[i] <= currPotVal + 0.01:
                pass
            else:
                change = 1
                if currPotVal < 0.01:
                    potVal[i] == 0
                if currPotVal < 0.988:
                    potVal[i] == 1
                potVal[i] = currPotVal

        # Process the Key Data
        swSend = [0] * swLen
        for i in range(swLen):
            # print('sw'+str(swVal))
            sw[i] = Pin(swPins[i], Pin.IN, Pin.PULL_UP)
            swVal[i] = sw[i].value()
            if swVal[i] != 1:
                swVal[i] = 1
            else :
                swVal[i] = 0
            
            #sends data only when key is pressed
            if swVal[i] == 1 and prevSwVal[i] == 0:
                change = 1
                swSend[i] = 1  

        ## process the switch data to out everytime a key is pressed 
        if change == 1:    
            data = [list(potVal), list(swSend)]
            print(data)
            uart.write('')

        prevSwVal = swSend
        prevPotVal = potVal

        time.sleep(0.05)


    # print('end')