import argparse
import os
from ast import literal_eval

def findFiles(min_points, dry_run=True):
    '''
    Finds all files with less than min_points data points and prints them
    allowing the user to find garbage data files to be removed before training
    '''

    fileNames = []
    print("Listing files with less than {} data points:".format(min_points))
    # Open file for writing
    for exercise in os.listdir("data"):
        for rep_file in os.listdir("data/{}".format(exercise)):
            f = open("data/{}/{}".format(exercise,rep_file), "r")
            first_line = f.readline()
            data = literal_eval(first_line)
            f.close()
            if (len(data[0])< min_points):
                fileNames.append(rep_file)
                print("\t", rep_file)
                if (not dry_run):
                    os.remove("data/{}/{}".format(exercise,rep_file))
                    print("DELETED: data/{}/{}".format(exercise,rep_file))
        
    return fileNames

def main():
    parser = argparse.ArgumentParser(description='Show chart of exercise times')
    parser.add_argument('-e', '--exercise', dest='exercise', default='all',
                    help='The name of the exercise being performed - must match the folder name in data folder')
    parser.add_argument('-n', '--points', dest='min_points', default='20',
                    help='The number of data points a file must have less than to be listed')

    args = parser.parse_args()
    min_points = int(args.min_points)
    print("Find {} Files with less than {} data points".format(args.exercise, min_points))

    fileNames = findFiles(min_points) # Put a false as the second parameter to turn off dry run and permeanently delete files



main()
