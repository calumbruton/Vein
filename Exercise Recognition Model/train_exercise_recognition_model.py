'''
Given the data in the data folder trains a 1D convolutional neural network
to predict the exercise the data corresponds to 

'''
import os
import argparse
from ast import literal_eval
import numpy as np
import pandas as pd
import random
import keras
from collections import Counter
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import StratifiedKFold
from numpy import mean
from numpy import std

from exercise_recognition_model import *

WINDOW_SIZE = 300       # The size of the window (number of data points) used for classification
TEST_SET = 0.25         # 25% Test Set
RANDOM_SEED = 40        # Seed Value to Split Train and Test Set
OVERLAP = 0.5           # 50% Window Overlap

def importData():
    dataset = []

    # Open file for reading data
    for exercise in os.listdir("../data"):
        for set_file in os.listdir("../data/{}".format(exercise)):
            print(set_file)
            f = open("../data/{}/{}".format(exercise,set_file), "r")
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

    # For each set data, a tuple ([6 lists of imu data],label)
    for set_data in dataset:
        label = set_data[1]
        categories.add(label)

        # The window can only be X points, so 
        num_points = len(set_data[0][0])
        if (num_points - WINDOW_SIZE < 0):
            print("WINDOW SIZE TOO LARGE")
            exit()

        # Make multiple partitions of data from the same set of reps
        # partitions = (num_points-window)/increment
        start = 0
        increment = int(WINDOW_SIZE * OVERLAP)
        while start+WINDOW_SIZE < num_points:
            end = start+WINDOW_SIZE
            # print("Range:", start, end)
            # imu_data is one of the arrays of data collected, roll, pitch, etc.
            new_data = []
            for i, imu_data in enumerate(set_data[0]):
                new_data.append(imu_data[start:end])

            data = np.array(new_data)
            data = np.transpose(data) # Reshape the data for 1D keras model

            clean_data.append(data)
            labels.append(label)
            start += increment

    clean_data = np.array(clean_data)
    labels = np.array(labels)

    # Randomly splits data and labels into test and training sets
    train_data, test_data, train_labels, test_labels = train_test_split(clean_data, labels, test_size=TEST_SET, random_state=RANDOM_SEED)

    return train_data, test_data, train_labels, test_labels, categories


# params is an array of arrays in order of: filter sizes, kernal sizes
def test_all_params(train_data, test_data, train_labels, test_labels, params, repeats=10):
    # test each parameter
    all_scores = list()
    for n_filters in params[0]:
        filter_scores = list()
        for kernal_size in params[1]:
            print("\n Testing Filters: {} Kernal Size: {}".format(n_filters, kernal_size))
            # repeat experiment
            kernal_scores = list()
            for r in range(repeats):
                model = createModel(n_filters,kernal_size) 
                model.fit(train_data, train_labels, batch_size=32, epochs=10, verbose=0)
                test_loss, score = model.evaluate(test_data, test_labels, verbose=0)
                score = score * 100.0
                print(">> Filters: {} Kernal Size: {} Iteration #{} Accuracy: {}".format(n_filters, kernal_size, r+1, score))
                kernal_scores.append(score)
            filter_scores.append(kernal_scores)
        all_scores.append(filter_scores)
    # summarize results
    summarize_all_results(all_scores, params)


# summarize all results
def summarize_all_results(scores, params):
    # summarize mean and standard deviation
    for n in range(len(params[0])):
        for k in range(len(params[1])):
            m, s = mean(scores[n][k]), std(scores[n][k])
            print("Filters: {} Kernal Size: {} -- Mean Score: {:.3f} Std Dev: {:.3f}".format(params[0][n], params[1][n], m, s))


def main():
    parser = argparse.ArgumentParser(description='Create 1D CNN and Evaluate Results')
    parser.add_argument('-t', '--test', dest='test', default=False, action='store_true',
                    help='Run tests on different parameters')
    args = parser.parse_args()
    
    dataset = importData()
    train_data, test_data, train_labels, test_labels, labels = preprocess(dataset)

    print("{1}\nTraining set record distribution: \n{0}\n{1}".format(Counter(train_labels), "-"*100))
    print("{1}\nTest set record distribution: \n{0}\n{1}".format(Counter(test_labels), "-"*100))

    labels = list(labels) # change labels from a set to list

    # Encode each of the labels of exercise to 0,1,2.. etc.
    label_encoder = preprocessing.LabelEncoder()
    label_encoder.fit(labels)
    train_labels = label_encoder.transform(train_labels)
    test_labels = label_encoder.transform(test_labels)

    print(train_data.shape)
    print(train_labels.shape)

    # Test different parameters
    if(args.test):
        filter_sizes = [2,3,4,8,16,32,64]
        kernal_sizes = [2,3,4,6,8]
        params = [filter_sizes, kernal_sizes]
        test_all_params(train_data, test_data, train_labels, test_labels, params)

    # Create and Compile the model
    model = createModel(n_filters=2, k_size=2)
    print(model.summary())

    # Train the model using k-fold cross validation - one split acts as validation
    kfold = StratifiedKFold(n_splits=6, shuffle=True, random_state=RANDOM_SEED)

    # train and validation will be indices of values of each set, stratified to balance the number of each class
    for train, validation in kfold.split(train_data, train_labels):
        print (Counter(train_labels[train]))
        model.fit(train_data[train], train_labels[train], validation_data=(train_data[validation], train_labels[validation]), batch_size=32, epochs=10, verbose=1)

    # Test the model
    test_loss, test_acc = model.evaluate(test_data, test_labels, verbose=2)
    print('\nTEST ACCURACY: {0:.2f}%\n'.format(test_acc*100))

    # View the predictions
    predictions = model.predict(test_data)
    y_pred = np.argmax(predictions, axis=1)
    print("Prediction Array:\n", y_pred)
    print("Test Label Array:\n", test_labels)
    print("\nConfusion Matrix:\n", confusion_matrix(test_labels, y_pred))
    print("\nSummary:\n", pd.crosstab(test_labels, y_pred, rownames=['True'], colnames=['Predicted'], margins=True), sep="")

    # Change array vals from ints to their respective labels
    y_pred_names = label_encoder.inverse_transform(y_pred)
    test_label_names = label_encoder.inverse_transform(test_labels)

    # View predictions with their respective labels
    print("\nSummary With Labels:\n", pd.crosstab(test_label_names, y_pred_names, rownames=['True'], colnames=['Predicted'], margins=True), sep="")
    print("\nClassification report:\n", classification_report(test_label_names, y_pred_names))


main()


