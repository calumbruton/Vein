import serial
import time
import keyboard 
import argparse
import os


def writeToFile(exercise, filenum, data):
    # Open file for writing
    f = open("data/{0}/{0}-{1}.txt".format(exercise,filenum), "w")
    f.write(str(data))  
    f.close()

def collectData(exercise, filenum):

    print("Start")
    port="/dev/tty.HC-05-DevB"                          # Connect to my HC-05 BT Module
    # port="/dev/tty.HC-05-DevB"                          # Connect to my HM-10 BTE Module
    bluetooth=serial.Serial(port, 115200)                 # Start communications with the bluetooth unit
    print("Connected")
    bluetooth.flushInput()                              # This gives the bluetooth a little kick

    # Viewing data and collecting data
    viewing = False
    collecting = False

    # yaw,pitch,roll,x_acc,y_acc,z_acc
    data = [[],[],[],[],[],[]]
    
    # Make a directory for the exercise data if it doesn't exist
    if not os.path.exists("data/{}".format(exercise)):
        os.makedirs("data/{}".format(exercise), mode=0o777)
        os.chmod("data/{}".format(exercise), mode=0o777)

    first = True    # Used to not save the first click of shift as it usually is longer
    sampling_rates = []

    try: 
        while(True):    
            # If q is pressed new rep
            if keyboard.is_pressed('shift'): 
                if first:
                    first = False
                    collecting = True
                    start_time = time.time()
                    print("\nStarting Collection\n")
                    time.sleep(0.15)    # Buffer to stop shift hold before next iteration

                else:
                    # Completed a rep save the data to a file
                    print("\nSave repitition\n")
                    end_time = time.time()
                    sampling_rates.append(len(data[0])/(end_time-start_time))
                    start_time = time.time()

                    time.sleep(0.15)

                    writeToFile(exercise, filenum, data)
                    data = [[],[],[],[],[],[]]
                    filenum+=1
            # If space is pressed and not intaking then start intaking else stop intaking
            elif keyboard.is_pressed('space'):
                viewing = not viewing
                time.sleep(0.3)
                if not viewing:
                    print("\nEND OF SET\n")
                    collecting = False
                    First = True
                    data = [[],[],[],[],[],[]]

            if viewing:
                input_data=bluetooth.readline()   
                curr_data = input_data.decode().split(",")
                # Only if we receive all of the data use it
                if (len(curr_data) == 6):
                    curr_data[5] = curr_data[5][:-2]                # Remove end of line stuff
                    print("Yaw: {}\tPitch: {}\tRoll: {}\t\tXAccel: {}\tYAccel: {}\tZAccel: {}".format(curr_data[0],curr_data[1],curr_data[2],curr_data[3],curr_data[4],curr_data[5]))
                    # print(curr_data, end='')
                    if collecting:
                        for i in range(6):
                            data[i].append(curr_data[i])

    # Gracefully exit on control C
    except KeyboardInterrupt:
        bluetooth.close()   
        print ("Sampling Rates: {} samples/second".format([round(x,2) for x in sampling_rates]))
        print("\n{0} Closed Bluetooth connection before exiting {0}\n".format("="*5))
        exit()


def main():
    parser = argparse.ArgumentParser(description='Receive data from IMU. Supply a num and ')
    parser.add_argument('filenum', metavar='N', type=int,
                    help='The starting number of the files to make for the exercise')
    parser.add_argument('-e', '--exercise', dest='exercise',
                    help='The name of the exercise being performed')

    args = parser.parse_args()
    print(args.exercise, args.filenum)

    collectData(args.exercise, args.filenum)


main()