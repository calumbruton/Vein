'''
Given the data in the data folder trains a 1D convolutional neural network
to predict the exercise the data corresponds to 

'''
import os
from ast import literal_eval
import numpy as np
import pandas as pd
import random
import keras
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

from model import *

# The size of the window (number of data points) used for classification
WINDOW_SIZE = 30
TEST_SET = 0.25

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
        data = np.transpose(data) # Reshape the data for 1D keras model

        clean_data.append(data)
        labels.append(label)

    clean_data = np.array(clean_data)
    labels = np.array(labels)

    # Randomly splits data and labels into test and training sets
    train_data, test_data, train_labels, test_labels = train_test_split(clean_data, labels, test_size=TEST_SET, random_state=40)

    return train_data, test_data, train_labels, test_labels, categories


def main():
    dataset = importData()
    train_data, test_data, train_labels, test_labels, labels = preprocess(dataset)

    labels = list(labels) # change labels from a set to list

    # Encode each of the labels of exercise to 0,1,2.. etc.
    label_encoder = preprocessing.LabelEncoder()
    label_encoder.fit(labels)
    train_labels = label_encoder.transform(train_labels)
    test_labels = label_encoder.transform(test_labels)

    print(train_data.shape)
    print(train_labels.shape)

    # Create and Compile the model
    model = createModel()
    model.compile(loss='sparse_categorical_crossentropy',
                optimizer='adam', metrics=['accuracy'])
        

    # Train the model
    model.fit(train_data, train_labels, batch_size=20, epochs=20, verbose=1)

    # Test the model
    test_loss, test_acc = model.evaluate(test_data, test_labels, verbose=2)
    print('\nTest accuracy: {0:.2f}%'.format(test_acc*100))

    # View the predictions
    predictions = model.predict(test_data)
    y_pred = np.argmax(predictions, axis=1)
    print(y_pred)
    print(test_labels)
    print("\nConfusion Matrix:\n", confusion_matrix(test_labels, y_pred))
    print("\nSummary:\n", pd.crosstab(test_labels, y_pred, rownames=['True'], colnames=['Predicted'], margins=True), sep="")

    # Change array vals from ints to their respective labels
    y_pred_names = label_encoder.inverse_transform(y_pred)
    test_label_names = label_encoder.inverse_transform(test_labels)

    # View predictions with their respective labels
    print("\nSummary With Labels:\n", pd.crosstab(test_label_names, y_pred_names, rownames=['True'], colnames=['Predicted'], margins=True), sep="")
    print("\nClassification report:\n", classification_report(test_label_names, y_pred_names))


main()


