import serial
from time import sleep
# # uart = UART(3, 112500)
# uart = UART(3, 9600)
# uart.init(9600, bits=8, parity=None, stop=1) # init with given parameters

# print(uart.read(10))


ser = serial.Serial('COM3', 115200, timeout=0.05)

# ser.baudrate = 115200
# ser.port = 'COM3'

# print(ser)
# ser.open()
while True:
    data = (ser.readline(25).rstrip()).decode()
    try:
        data = eval('[' + data + ']')[0]
        print(data)
    except:
        pass