'''
Created by Calum Bruton
November 25 2019

Run to predict exercise in real time
'''
import keras
import serial
import collections
import numpy as np
from keras.models import *
from sklearn import preprocessing

RECOGNITION_WINDOW_SIZE = 150
REPETITION_WINDOW_SIZE = 30
COUNTER = 0


def predict_bicep_curl(rep_model, data):
    data = np.array(data)
    data = np.transpose(data)
    data = np.expand_dims(data, axis=0)
    pred_scores = rep_model.predict(data)
    is_rep = np.argmax(pred_scores, axis=1)
    return is_rep


def predict_exercise(recognition_model, data, label_encoder):
    global COUNTER
    data = np.array(data)
    data = np.transpose(data)
    data = np.expand_dims(data, axis=0)
    pred_scores = recognition_model.predict(data)
    prediction = label_encoder.inverse_transform(np.argmax(pred_scores, axis=1))
    pred_scores = [round(x*100,1) for x in pred_scores.flatten()]
    print(pred_scores)
    print("{1}\n{0}\t{2}\n{1}".format(prediction, "-"*30, COUNTER))
    COUNTER += 1
    return prediction, pred_scores



def start_predictions_to_file():

    # Load a model
    recognition_model = load_model("../Exercise Recognition Model/99.7k2f2.h5")
    bicep_curl_model = load_model("../Repetition Counter Model/94bicep-curl.h5")

    # Label encodings -- Manually update
    label_encoder = preprocessing.LabelEncoder()
    exercise_labels = ["Bicep Curls", "Dumbbell Row", "Lateral Raises"]
    label_encoder.fit(exercise_labels)

    print("Start")
    port="/dev/tty.HC-05-DevB"                          # Connect to my HC-05 BT Module
    bluetooth=serial.Serial(port, 115200)               # Start communications with the bluetooth unit
    print("Connected")
    bluetooth.flushInput()    
    
    # data is 6 dequeues of sensor data
    data = [collections.deque(RECOGNITION_WINDOW_SIZE*[0], RECOGNITION_WINDOW_SIZE) for _ in range(6)]
    rep_data = [collections.deque(REPETITION_WINDOW_SIZE*[0], REPETITION_WINDOW_SIZE) for _ in range(6)]
    current_exercise = ''
    bicep_curl_count = 0

    skip_rep_window = False # Used to skip a window after counting a rep
    timer = 0
    while(True):
        input_data=bluetooth.readline()   
        curr_data = input_data.decode().split(",")
        # Only if we receive all of the data use it
        if (len(curr_data) == 6):
            curr_data[5] = curr_data[5][:-2]                # Remove end of line stuff
            for i in range(6):
                data[i].append(curr_data[i])
                rep_data[i].append(curr_data[i])

        # Predict Excercise being performed
        if timer % 50 == 0:
            exercise_prediction, conf_scores = predict_exercise(recognition_model, data, label_encoder)
            # If the exercise has changed reset the repetition counter
            if exercise_prediction != current_exercise:
                bicep_curl_count = 0
            current_exercise = exercise_prediction
            data_write = [list(x) for x in data]

        if timer % 30 == 0:
            if (predict_bicep_curl(bicep_curl_model, rep_data)):
                if not skip_rep_window:
                    bicep_curl_count += 1
                    skip_window = True
                else: 
                    skip_rep_window = False  
            else:
                skip_rep_window = False    
            print("BICEP CURL COUNT: {}".format(bicep_curl_count))
        
        # Send data through to update the graphs 
        if timer % 15 == 0:
            f = open("dashboard_data.txt", "w")
            f.write('{}\n{}\n{}\n{}\n'.format(list(data_write), exercise_prediction, exercise_labels, conf_scores))
            f.write('{}'.format(bicep_curl_count))
            f.close()
        timer+=1




if __name__ == "__main__":
    start_predictions_to_file()