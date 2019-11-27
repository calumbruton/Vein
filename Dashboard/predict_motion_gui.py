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
    predictions = model.predict(data)
    prediction = label_encoder.inverse_transform(np.argmax(predictions, axis=1))
    print("{1}\n{0}\t{2}\n{1}".format(prediction, "-"*30, COUNTER))
    COUNTER += 1
    return prediction



def start_predictions_to_file():

    # Load a model
    model = load_model("../Exercise Recognition Model/99.7k2f2.h5")

    # Label encodings -- Manually update
    label_encoder = preprocessing.LabelEncoder()
    label_encoder.fit(["Bicep Curls", "Dumbbell Row", "Lateral Raises"])

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
            # print("Yaw: {}\tPitch: {}\tRoll: {}\t\tXAccel: {}\tYAccel: {}\tZAccel: {}".format(curr_data[0],curr_data[1],curr_data[2],curr_data[3],curr_data[4],curr_data[5]))
            for i in range(6):
                data[i].append(curr_data[i])
        if timer % 50 == 0:
            prediction = predict(model, data, label_encoder)
            data_write = [list(x) for x in data]
            f = open("shared_data.txt", "w")
            f.write('{}\n{}'.format(list(data_write), prediction))
            f.close()
        timer+=1




if __name__ == "__main__":
    start_predictions_to_file()