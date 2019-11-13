import matplotlib
import matplotlib.pyplot as plt
import argparse
import os
import numpy as np
from ast import literal_eval
import matplotlib.ticker as ticker
plt.switch_backend('Qt4Agg')

def readExerciseFiles(exercise):
    '''
    Read the data from all the repition files in the given directory
    '''
    
    imu_data = [[],[],[],[],[],[]]
    rep_filenames = []

    # Open file for reading data
    for rep_file in os.listdir("data/{}".format(exercise)):
        print(rep_file)
        f = open("data/{}/{}".format(exercise,rep_file), "r")
        first_line = f.readline()
        rep_data = literal_eval(first_line)
        for i in range(6):
            imu_data[i].append(rep_data[i])
        rep_filenames.append(rep_file)
        f.close()
    
    return imu_data, rep_filenames


def removeOutliers(data, m):
    '''Given a dataset remove any data m standard deviations from the mean'''
    np_arr = np.asarray(data)
    before = len(np_arr)
    np_arr = np_arr[abs(np_arr - np.mean(np_arr)) < m * np.std(np_arr)]
    after = len(np_arr)
    if (before-after > 0): print("Outliers removed {}".format(before-after))
    return np_arr

# data is 2d array of exercise and data
def createMultiLineGraph(imu_data, title, labels):
    
    plt.figure(title)
    # For each type of data from the IMU (YPR, XYZ acc)
    for t in range(6):  
        # New figure for each data type
        # f1 = plt.figure(t+1)
        plt.subplot(2,3,t+1)
        # For each reptition plot the data
        for set_num in range(len(imu_data[t])):
            imu_data[t][set_num] = [float(i) for i in imu_data[t][set_num]]
            # Remove outliers
            clean_data = removeOutliers(imu_data[t][set_num], 2.5)
            plt.plot(clean_data, label = labels[set_num])
        setTitleAndAxiNames(t)

    # plt.legend()
    plt.tight_layout()

    # Maximize the chart window
    figM = plt.get_current_fig_manager()
    figM.window.showMaximized()
    
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Show chart of exercise times')
    parser.add_argument('-e', '--exercise', dest='exercise', required=True,
                    help='The name of the exercise being performed - must match the folder name in data folder')
    parser.add_argument('-t', '--type', dest='type', type=int,
                    help='Given a value 1 to 6 displays only the data for the exercise corresponding to 1 = Yaw etc. for YPR, XYZ accel')

    args = parser.parse_args()
    print("View IMU data for {}".format(args.exercise))
    plt.switch_backend('Qt5Agg')

    imu_data, rep_filenames = readExerciseFiles(args.exercise)   
    if (args.type): 
        showSpecific(imu_data, args.type, rep_filenames)
    else: 
        createMultiLineGraph(imu_data, args.exercise, rep_filenames)


def showSpecific(imu_data, t, labels):
    '''
    Given an integer 1 to 6 shows the data corresponding to
    YPR, XYZ Acc = 123, 456
    '''
    type_data = imu_data[t-1]   # Get the imu_data for the specific attribute
    for num, rep_data in enumerate(type_data):
        rep_data = [float(i) for i in rep_data]
        plt.plot(rep_data, label = labels[num])
    setTitleAndAxiNames(t-1)
    plt.tight_layout()
    plt.legend()
    plt.show()
    
def setTitleAndAxiNames(t):
    '''
    Given an integer t sets the title and axi names of the plot
    0 = Yaw
    1 = Pitch
    2 = Roll
    3 = X Acceleration
    4 = Y Acceleration
    5 = Z Acceleration
    '''
    # Yaw
    if (t == 0):
        plt.title('Yaw vs Time')
        plt.ylabel('Yaw (degrees/131sec)')
        plt.xlabel('Time')
        plt.yticks(np.arange(-180,180,40))
    # Pitch
    if (t == 1):
        plt.title('Pitch vs Time')
        plt.ylabel('Pitch (degrees/131sec)')
        plt.xlabel('Time')
        plt.yticks(np.arange(-180,180,40))
    # Roll
    if (t == 2):
        plt.title('Roll vs Time')
        plt.ylabel('Roll (degrees/131sec)')
        plt.xlabel('Time')
        plt.yticks(np.arange(-180,180,40))
    # X Acceleration
    if (t == 3):
        plt.title('X Acceleration vs Time')
        plt.ylabel('X Acceleration (m/16384 $s^2$)')
        plt.xlabel('Time')
    # Y Acceleration
    if (t == 4):
        plt.title('Y Acceleration vs Time')
        plt.ylabel('Y Acceleration (m/16384 $s^2$)')
        plt.xlabel('Time')
    # Z Acceleration
    if (t == 5):
        plt.title('Z Acceleration vs Time')
        plt.ylabel('Z Acceleration (m/16384 $s^2$)')
        plt.xlabel('Time')

main()