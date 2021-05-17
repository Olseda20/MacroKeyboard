# # This file is executed on every boot (including wake-boot from deepsleep)
# #import esp
# #esp.osdebug(None)
# #import webrepl
# #webrepl.start()


# from machine import Pin, ADC, UART
# import time 
# import math
# import ujson 

# uart = UART(1, 115200)                                      # init with given baudrate
# uart.init(115200, bits=8, parity=None, stop=1, txbuf=66)    # init with given parameters

# def toggle(max):
#     lap = 0

#     while (lap<max):
#         p.value(1)
#         d.value(1)
#         time.sleep(1)
#         p.value(0)
#         d.value(0)
#         time.sleep(1)
#         lap += 1

# if __name__ == "__main__":
#     print('start')
    
#     pot_max_val = 4095

#     potPins = [34,35,32,33]
#     potLen = len(potPins)
#     pot = potVal = prevPotVal =[0] * potLen

#     swPins = [23,22,21,19,18,5,4,26,27,14]
#     swLen = len(swPins)
#     sw = swVal = prevSwVal = [0] * swLen


#     while True:
#         change = 0

#         #Process the Pot Data
#         for i in range(potLen):
#             pot = ADC(Pin(potPins[i]))
#             pot.atten(ADC.ATTN_11DB)
#             currPotVal = round(pot.read()/pot_max_val,3)
            
#             if currPotVal - 0.01 <= prevPotVal[i] <= currPotVal + 0.01:
#                 pass
#             else:
#                 change = 1
#                 if currPotVal < 0.01:
#                     potVal[i] == 0
#                 potVal[i] = currPotVal
#         # print(potVal)


#         #Process the Key Data
#         for i in range(swLen):
#             sw = Pin(swPins[i], Pin.IN, Pin.PULL_UP)
#             currSwVal = sw.value()
            
#             #finding the dropping edve (since it is active low)
#             if prevSwVal == 1 and currSwVal == 0: 
#                 change = 1
#                 # set the swVal aray to on only on dropping edge
#                 pass
        
            
#         # print(swVal)
        
#         ## process the switch data to out everytime a key is pressed
        
#         if change == 1:    
#             data = [list(potVal), list(swVal)]#'[' + str(potVal) + ',' + str(swVal) + ']'
#             # print(data)
#             uart.write(str(data))
#             uart.write('')

            
#             time.sleep(0.05)

#             prevPotVal = potVal
#             prevSwVal = swVal

#         ##if significant change is recorded, update data script else continue looping


#     # print('end')

# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()


from machine import Pin, ADC, UART
import time 
import math
import ujson 

uart = UART(1, 115200)                                      # init with given baudrate
uart.init(115200, bits=8, parity=None, stop=1, txbuf=66)    # init with given parameters

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
    pot = potVal = prevPotVal =[0] * potLen

    swPins = [23,22,21,19,18,5,4,26,27,14]
    swLen = len(swPins)
    sw = swVal = prevSwVal = [0] * swLen


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
                potVal[i] = currPotVal
        # print(potVal)


        #Process the Key Data
        for i in range(swLen):
            sw = Pin(swPins[i], Pin.IN, Pin.PULL_UP)
            currSwVal = sw.value()
            
            #finding the dropping edve (since it is active low)
            if prevSwVal == 1 and currSwVal == 0: 
                change = 1
                # set the swVal aray to on only on dropping edge
                pass
        
            
        # print(swVal)
        
        ## process the switch data to out everytime a key is pressed
        
        if change == 1:    
            data = [list(potVal), list(swVal)]#'[' + str(potVal) + ',' + str(swVal) + ']'
            print(data)
            uart.write(str(data))
            uart.write('')

            prevPotVal = potVal
            prevSwVal = swVal

        time.sleep(0.05)


    # print('end')