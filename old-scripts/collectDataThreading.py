import serial
import time
import keyboard 
import argparse
import os
from threading import Thread


def writeToFile(exercise, filenum, data):
    # Open file for writing
    f = open("data/{0}/{0}-{1}.txt".format(exercise,filenum), "w")
    f.write(str(data))  
    f.close()


def keyboard_poller(exercise, filenum, data):
    first = True    # Used to not save the first click of shift as it usually is longer

    while (True):
        # If q is pressed new rep
        if keyboard.is_pressed('shift'): 
            if first:
                first = False
            else:
                # Completed a rep save the data to a file
                print("\nSave repitition -- {} DATA POINTS\n".format(len(data[0])))
                time.sleep(0.15)

                writeToFile(exercise, filenum, data)
                data = [[],[],[],[],[],[]]
                filenum+=1

    
def collectData(exercise, filenum, data):

    print("Start")
    port="/dev/tty.HC-05-DevB"                          # This will be different for various devices and on windows it will probably be a COM port.
    bluetooth=serial.Serial(port, 9600)                 # Start communications with the bluetooth unit
    print("Connected")
    bluetooth.flushInput()                              # This gives the bluetooth a little kick
    collecting = False


    # Make a directory for the exercise data if it doesn't exist
    if not os.path.exists("data/{}".format(exercise)):
        os.makedirs("data/{}".format(exercise), mode=0o777)

    try: 
        while(True):   
            # If space is pressed and not intaking then start intaking else stop intaking
            if keyboard.is_pressed('space'):
                collecting = not collecting
                time.sleep(0.3)
                if not collecting:
                    print("\nEND OF SET\n")
                    # Completed last rep save data to a file
                    # writeToFile(exercise, filenum, data)
                else:
                    print("\nSTART OF SET\n") 

            if collecting:
                # The data we actually store in Yaw,Pitch,Roll,XAccel,YAccel,ZAccel format
                input_data=bluetooth.readline()   
                curr_data = input_data.decode().split(",")
                # Only if we receive all of the data use it
                if (len(curr_data) == 6):
                    curr_data[5] = curr_data[5][:-2]                # Remove end of line stuff
                    print("Yaw: {}\tPitch: {}\tRoll: {}\t\tXAccel: {}\tYAccel: {}\tZAccel: {}".format(curr_data[0],curr_data[1],curr_data[2],curr_data[3],curr_data[4],curr_data[5]))
                    # print(curr_data, end='')
                    for i in range(6):
                        data[i].append(curr_data[i])

    finally:
        bluetooth.close()   
        print("\n{0} Closed Bluetooth connection before exiting {0}\n".format("="*5))



def main():
    parser = argparse.ArgumentParser(description='Receive data from IMU. Supply a num and ')
    parser.add_argument('filenum', metavar='N', type=int,
                    help='The starting number of the files to make for the exercise')
    parser.add_argument('-e', '--exercise', dest='exercise',
                    help='The name of the exercise being performed')

    args = parser.parse_args()
    print(args.exercise, args.filenum)

    # This data struct is shared between threads
    # yaw,pitch,roll,x_acc,y_acc,z_acc
    data = [[],[],[],[],[],[]]

    poller = Thread(target=collectData, args=(args.exercise, args.filenum, data))
    poller.start()
    print("HERE??")
    keyboard_poller(args.exercise, args.filenum, data)


main()