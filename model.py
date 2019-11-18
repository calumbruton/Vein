from keras.models import *
from keras.layers import *

NUM_CLASSES = 10     # The number of exercises the model will classify
WINDOW_SIZE = 30

def createModel():
    model = Sequential()
    # 100 filters, 10 kernal size, stride 1
    model.add(Conv1D(100, 10, activation='relu', input_shape=(WINDOW_SIZE,6))) # Output window size - (kernal size - 1) -> when stride 1
    model.add(Conv1D(100, 10, activation='relu'))
    model.add(MaxPool1D(3))
    model.add(Conv1D(160, 4, activation='relu')) 
    # model.add(Flatten())
    model.add(GlobalAveragePooling1D())
    model.add(Dropout(0.5))
    model.add(Dense(NUM_CLASSES, activation='softmax')) 
    print(model.summary())
    return model
