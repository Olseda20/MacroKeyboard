# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()


from machine import Pin, ADC, UART
import time 
import math
import ujson 
# import serial

uart = UART(1, 115200)                         # init with given baudrate
uart.init(115200, bits=8, parity=None, stop=1, txbuf=25) # init with given parameters

def toggle(max):
    lap = 0

    while (lap<max):
        p.value(1)
        d.value(1)
        time.sleep(1)
        p.value(0)
        d.value(0)
        time.sleep(1)
        lap += 1

if __name__ == "__main__":
    print('start')
    
    pot_max_val = 4095

    potPins = [34,35,32,33]
    potLen = len(potPins)
    pot = [0] * potLen
    potVal = pot

    # for i in range(potLen):
    #     pot[i] = ADC(Pin(potPins[i]))
    #     pot[i].atten(ADC.ATTN_11DB)

    swPins = [23,22,21,19,18,5,4,26,27,14]
    swLen = len(swPins)
    sw = [0] * swLen
    swVal = sw

    for i in range(swLen):
        sw[i] = Pin(swPins[i], Pin.IN, Pin.PULL_UP)

    while True:

        for i in range(potLen):
            pot = ADC(Pin(potPins[i]))
            pot.atten(ADC.ATTN_11DB)
            potVal[i] = round(pot.read()/pot_max_val,3) 
        print(potVal)

        for i in range(swLen):
            sw = Pin(swPins[i], Pin.IN, Pin.PULL_UP)
            swVal[i] = sw.value()
        print(swVal)

        # data = [pot1val, pot2val, pot3val, pot4val]
        # print(str(data))
        # print(sw1val)
        # uart.write(str(data))
        # uart.write('')
        # print(str(data))

        time.sleep(0.05)

        ##if significant change is recorded, update data script else continue looping


    # print('end')