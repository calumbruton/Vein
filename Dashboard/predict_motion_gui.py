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

WINDOW_SIZE = 150
COUNTER = 0


def predict(model, data, label_encoder):
    global COUNTER
    data = np.array(data)
    data = np.transpose(data)
    data = np.expand_dims(data, axis=0)
    pred_scores = model.predict(data)
    prediction = label_encoder.inverse_transform(np.argmax(pred_scores, axis=1))
    pred_scores = [round(x*100,1) for x in pred_scores.flatten()]
    print(pred_scores)
    print("{1}\n{0}\t{2}\n{1}".format(prediction, "-"*30, COUNTER))
    COUNTER += 1
    return prediction, pred_scores



def start_predictions_to_file():

    # Load a model
    model = load_model("../Exercise Recognition Model/99.7k2f2.h5")

    # Label encodings -- Manually update
    label_encoder = preprocessing.LabelEncoder()
    labels = ["Bicep Curls", "Dumbbell Row", "Lateral Raises"]
    label_encoder.fit(labels)

    print("Start")
    port="/dev/tty.HC-05-DevB"                          # Connect to my HC-05 BT Module
    bluetooth=serial.Serial(port, 115200)               # Start communications with the bluetooth unit
    print("Connected")
    bluetooth.flushInput()    
    
    # data is 6 dequeues of sensor data
    data = [collections.deque(WINDOW_SIZE*[0], WINDOW_SIZE) for _ in range(6)]
    prediction = ''

    timer = 0
    while(True):
        input_data=bluetooth.readline()   
        curr_data = input_data.decode().split(",")
        # Only if we receive all of the data use it
        if (len(curr_data) == 6):
            curr_data[5] = curr_data[5][:-2]                # Remove end of line stuff
            for i in range(6):
                data[i].append(curr_data[i])
        if timer % 50 == 0:
            prediction, conf_scores = predict(model, data, label_encoder)
            data_write = [list(x) for x in data]
        if timer % 10 == 0:
            f = open("shared_data.txt", "w")
            f.write('{}\n{}\n{}\n{}'.format(list(data_write), prediction, labels, conf_scores))
            f.close()
        timer+=1




if __name__ == "__main__":
    start_predictions_to_file()