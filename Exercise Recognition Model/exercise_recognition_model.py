from keras.models import *
from keras.layers import *

NUM_CLASSES = 3     # The number of exercises the model will classify
WINDOW_SIZE = 300

def createModel(n_filters=64, k_size=3):
    # model = Sequential()
    # # 100 filters, 100 kernal size, stride 1
    # model.add(Conv1D(100, 100, activation='relu', input_shape=(WINDOW_SIZE,6))) # Output window size - (kernal size - 1) -> when stride 1
    # model.add(Conv1D(100, 40, activation='relu'))
    # model.add(MaxPool1D(3))
    # model.add(Conv1D(160, 4, activation='relu')) 
    # # model.add(Flatten())
    # model.add(GlobalAveragePooling1D())
    # model.add(Dropout(0.5))
    # model.add(Dense(NUM_CLASSES, activation='softmax')) 

    model = Sequential()
    model.add(Conv1D(filters=n_filters, kernel_size=k_size, activation='relu', input_shape=(WINDOW_SIZE,6)))
    model.add(Conv1D(filters=n_filters, kernel_size=k_size, activation='relu'))
    model.add(Dropout(0.5))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Flatten())
    model.add(Dense(100, activation='relu'))
    model.add(Dense(NUM_CLASSES, activation='softmax'))
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    return model

