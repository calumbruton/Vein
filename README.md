
# VEIN: A Wearable for the Lifter

Vein is a wearable device that uses an IMU and machine learning to count the number of repetitions performed of an exercise for a user and predict the exercise they are doing. Allowing the weight lifter to avoid the hassle of counting every rep and manually tracking their workouts.

- Orientation Note: Battery Opening to Hand

with arm extented:
- yaw = turning left and right
- roll = Up and down
- pitch = wrist turn

### Exercises Currently Supported
- Bicep Curl
- Lateral Raises
- Dumbbell Row

-------- Future ----
- Hammer Curl
- Front Raises
- Dumbbell Overhead Press
- Dumbbell Deadlift
- Dumbbell Press
- Dumbbell Lunge
- Bent Over Dumbbell Reverse Fly
- Dumbbell Row (hand)
- Pullup
- Bench Press
- Deadlift
- Squat
- Overhead press


## Start Dashboard

Start collecting and predicting motion:
```
cd Dashboard
python3 predict_motion_gui.py
```
In another terminal start the interface:
```
cd Dashboard
gunicorn --workers=3 --threads=3 app:server
```

<img width="1218" alt="Screen Shot 2019-11-27 at 5 05 18 AM" src="https://user-images.githubusercontent.com/12948431/69714017-9ad4c280-10d3-11ea-82e2-79bca345e5c5.png">


## Files
### collectData.py 
- Used to collect data for training
- run the script using the argument -e \<exercise name> and a positional argument \<N> for the file number of the exercise to start recording at
- Must be run as administrator for keyboard access
```
sudo python3 collectData.py -e bicep-curl 1
```
- Press spacebar to start viewing the data stream, press shift to start recording reps, and press shift at the end of each repition of the given exercise, press spacebar again to stop

### train_exercise_recognition_model.py
- Used to collect data for training
- run the script using the argument

### dataVisualization.py
- Used to preview the amount of time taken for each rep of a given exercise using matplotlib
- run the script with the flag -e \<exercise name> to show a specific exercise, it will also print out every repition file and the number of data points in it to the console
```
python3 dataVisualization.py -e bicep-curl
```
- run the script with no flag to show all excercises
```
python3 dataVisualization.py 
```

### visualizeImuData.py
- Used to view the data from the IMU (Intertial Measurement Unit). This include the Yaw, Pitch, Roll, X acceleration, Y acceleration, and Z acceleration for a given excercise over time.
- run the script with the flag -e \<exercise name> 
```
python3 visualizeImuData.py -e bicep-curl
```

<img width="600" alt="Screen Shot 2019-11-11 at 8 34 33 PM" src="https://user-images.githubusercontent.com/12948431/68634317-065b4500-04c3-11ea-99b7-808bec683ed5.png">


- To see an individual statistic with labels per rep use the -t \<N> flag where an N value of:
    - 1 = Yaw
    - 2 = Pitch
    - 3 = Roll
    - 4 = X Acceleration
    - 5 = Y Acceleration
    - 6 = Z Acceleration

```
python3 visualizeImuData.py -e bicep-curl -t 2
```

### findGarbageData.py
Helps find data with less than \<N> data points

```
python3 findGarbageData.py -n 20
```


### Exercise Recognition Model / train_exercise_recognition_model.py
- Used to train the keras model on the data collected
- Can load and see evaluation of an existing model using -l <filename>
```
python3 train_exercise_recognition_model.py
```

### Exercise Recognition Model / excercise_recognition_model.py
- This is where the code for the keras machine learning model is written


### Repetition Counter Model / train_repetition_model.py
- Used to train the keras model on the data collected with repetition markers
- Can load and see evaluation of an existing model using -l \<filename>
- -e \<excercise> flag must be set as this trains a repetition counting model for a single exercise
```
python3 train_repetition_model.py -e bicep-curl
```

### Repetition Counter Model / repetition_model.py
- This is where the code for the keras machine learning model is written for the repetition counting CNN



## Prototype Components
- Arduino Nano
- MPU 6050 IMU
- HC-05 Wireless Bluetooth Host Serial Transceiver Module 
- 9V Battery

<img width="400" alt="Vein Hardware" src="https://user-images.githubusercontent.com/12948431/68535026-b7b67b00-0309-11ea-9519-f89c0f019290.png">

## Machine Learning Model

TODO


## Requirements
```
pip3 install PyQt5 matplotlib numpy tensorflow sklearn pandas dash plotly
pip3 install keras==2.2.0
```

# Related Work

https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6387025/pdf/sensors-19-00714.pdf



