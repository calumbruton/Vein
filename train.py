'''
Given the data in the data folder trains a 1D convolutional neural network
to predict the exercise the data corresponds to 

'''
import os
from ast import literal_eval
import numpy as np
import random
import keras
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

from model import *

# The size of the window (number of data points) used for classification
WINDOW_SIZE = 50

def importData():
    dataset = []

    # Open file for reading data
    for exercise in os.listdir("data"):
        for rep_file in os.listdir("data/{}".format(exercise)):
            print(rep_file)
            f = open("data/{}/{}".format(exercise,rep_file), "r")
            first_line = f.readline()
            rep_data = literal_eval(first_line)
            dataset.append((rep_data, exercise))
            f.close()

    return dataset


def preprocess(dataset):
    clean_data = []
    labels = []
    categories = set()

    # dataset [i] is the ith rep
    # dataset[i][0] is the ith reps 6 arrays of imu data
    # dataset[i][1] is the excercise name label
    # dataset[i][0][n] is the ith reps nth set of data (Yaw, Pitch etc.)

    # For each rep data, tuple ([6 lists of imu data],label)
    for rep_data in dataset:
        label = rep_data[1]
        categories.add(label)

        # The window can only be X points, so 
        num_points = len(rep_data[0][0])
        if (num_points - WINDOW_SIZE < 0):
            print("WINDOW SIZE TOO LARGE")
            exit()
        start = random.randint(0,num_points-WINDOW_SIZE)
        end = start+WINDOW_SIZE
        # print("Range:", start, end)
        for i, imu_data in enumerate(rep_data[0]):
            rep_data[0][i] = imu_data[start:end]

        data = np.array(rep_data[0])
        # print("Before: ", data.shape)
        data = np.transpose(data) # Reshape the data for 1D keras model
        # print("After : ", data.shape)

        clean_data.append(data)
        labels.append(label)

    clean_data = np.array(clean_data)
    labels = np.array(labels)

    train_data, test_data, train_labels, test_labels = train_test_split(clean_data, labels, test_size=0.25, random_state=42)

    return train_data, test_data, train_labels, test_labels, categories


def main():
    dataset = importData()
    train_data, test_data, train_labels, test_labels, categories = preprocess(dataset)

    # Encode each of the categories of exercise to 0,1,2.. etc.
    label_encoder = preprocessing.LabelEncoder()
    label_encoder.fit(list(categories))
    train_labels = label_encoder.transform(train_labels)
    test_labels = label_encoder.transform(test_labels)

    print(train_data.shape)
    print(train_labels.shape)

    # Create and Compile the model
    model = createModel()
    model.compile(loss='sparse_categorical_crossentropy',
                optimizer='adam', metrics=['accuracy'])
        

    # Train the model
    model.fit(train_data, train_labels, batch_size=10, epochs=10, verbose=1)

    # Test the model
    test_loss, test_acc = model.evaluate(test_data, test_labels, verbose=2)
    print('\nTest accuracy:', test_acc)


main()


