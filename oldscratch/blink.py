# ampy --port COM3 run blink.py

from machine import Pin, ADC, UART
import time 
import math
import ujson 

uart = UART(1, 115200)                         # init with given baudrate
uart.init(115200, bits=8, parity=None, stop=1) # init with given parameters

if __name__ == "__main__":
    
    pot_max_val = 4095

    pot1 = ADC(Pin(34))
    pot1.atten(ADC.ATTN_11DB)

    pot2 = ADC(Pin(35))
    pot2.atten(ADC.ATTN_11DB) 

    pot3 = ADC(Pin(32))
    pot3.atten(ADC.ATTN_11DB)

    pot4 = ADC(Pin(33))
    pot4.atten(ADC.ATTN_11DB)
    running = 0 


    while True:
        if running == 0:
            print('running')
            running = 1

        # read = pot.read()
        pot1val = pot1.read()/pot_max_val
        pot2val = pot2.read()/pot_max_val
        pot3val = pot3.read()/pot_max_val
        pot4val = pot4.read()/pot_max_val
        # print('pot1', pot1val)#, ,' pot2' , ,' pot3' , ,' pot4' , )

        data = {"Pot":[pot1val, pot2val, pot3val, pot4val]}
        uart.write('hello')
        # data = {"Pot":"yo"}

        # print('writing json')
        # d = ujson.dumps(data)
        # with open('pot_data.json', 'w') as f:
        #         f.write(d)
        #         f.close
        # print(data)

        time.sleep(0.05)

        ##if significant change is recorded, update data script else continue looping


    print('end')

'''

p = Pin(15, Pin.OUT)
d = Pin(2, Pin.OUT)
def toggle(max):
    lap = 0

    while (lap<max):
        p.value(1)
        # d.value(1)
        time.sleep(1)
        p.value(0)
        # d.value(0)
        time.sleep(1)
        lap += 1
    
# toggle(5)



# #digital read (connect to gnd and digi pin)
# switch = Pin(15, Pin.IN, Pin.PULL_UP)

# while True:
#     readswitch = switch.value()
#     print(readswitch)
#     time.sleep(0.01)'''