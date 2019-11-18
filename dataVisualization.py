import matplotlib.pyplot as plt
import argparse
import os
from ast import literal_eval
import matplotlib.ticker as ticker


def readAllFiles():
    num_points = []
    
    # Open file for writing
    for exercise in os.listdir("data"):
        # exercise points will hold the number of points in each file
        # for that exercise and the exercise name as the last value
        exercise_points = []
        for rep_file in os.listdir("data/{}".format(exercise)):
            f = open("data/{}/{}".format(exercise,rep_file), "r")
            # print("data/{}/{}".format(exercise,rep_file))
            first_line = f.readline()
            data = literal_eval(first_line)
            exercise_points.append(len(data[0]))
            f.close()
        print("{: >30}: {} data points".format(exercise, len(exercise_points)))
        exercise_points.append(exercise)
        num_points.append(exercise_points)
        

    return num_points


def readExerciseFiles(exercise):
    num_points = []
    rep_filenames = []

    # Open file for writing
    for rep_file in os.listdir("data/{}".format(exercise)):
        print(rep_file)
        f = open("data/{}/{}".format(exercise,rep_file), "r")
        first_line = f.readline()
        data = literal_eval(first_line)
        print(len(data[0]))
        num_points.append(len(data[0]))
        rep_filenames.append(rep_file)
        f.close()
    
    return num_points, rep_filenames


def createLineGraph(data, labels):
    plt.plot(data)
    plt.title('Number of data points per repetition')
    plt.ylabel('Number of data points')
    plt.xlabel('Rep number')
    plt.legend()
    plt.show()

# data is 2d array of exercise and data
def createMultiLineGraph(data):
    for i in range(len(data)):
        plt.plot(data[i][:-1], label = data[i][-1])
    plt.title('Number of data points per repetition per exercise')
    plt.ylabel('Number of data points')
    plt.xlabel('Rep number')
    plt.legend()
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Show chart of exercise times')
    parser.add_argument('-e', '--exercise', dest='exercise', default='all',
                    help='The name of the exercise being performed - must match the folder name in data folder')

    args = parser.parse_args()
    print(args.exercise)
    if (args.exercise == 'all'):
        num_points = readAllFiles()
        createMultiLineGraph(num_points)   
    else:
        num_points, labels = readExerciseFiles(args.exercise)    
        createLineGraph(num_points, labels)


main()