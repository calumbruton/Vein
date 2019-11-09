import serial
import time

def readOnly():
    print("Start")
    port="/dev/tty.HC-05-DevB"                          # This will be different for various devices and on windows it will probably be a COM port.
    bluetooth=serial.Serial(port, 9600)                 # Start communications with the bluetooth unit
    print("Connected")
    bluetooth.flushInput()                              # This gives the bluetooth a little kick
    while(True):                               
        input_data=bluetooth.readline()                 # This reads the incoming data. In this particular example it will be the "Hello from Blue" line
        print(input_data.decode(), end='')              # These are bytes coming in so a decode is needed
    bluetooth.close()                                   # Otherwise the connection will remain open until a timeout which ties up the /dev/thingamabob
    print("Done")


readOnly()

