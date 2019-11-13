from keras.models import *
from keras.layers import *

NUM_CLASSES = 2     # The number of exercises the model will classify


def createModel():
    model = Sequential()
    # 100 filters, 10 kernal size, # stride 1
    model.add(Conv1D(100, 10, activation='relu', input_shape=(50,6)))
    model.add(Conv1D(100, 10, activation='relu'))
    model.add(MaxPool1D(3))
    model.add(Conv1D(160, 5, activation='relu'))
    # model.add(Flatten())
    model.add(GlobalAveragePooling1D())
    model.add(Dropout(0.5))
    model.add(Dense(NUM_CLASSES, activation='softmax')) 
    print(model.summary())
    return model
