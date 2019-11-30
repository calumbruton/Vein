from keras.models import *
from keras.layers import *

NUM_CLASSES = 2     # The number of exercises the model will classify
WINDOW_SIZE = 30

def createModel(n_filters=64, k_size=3):
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
