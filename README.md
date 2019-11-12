
# VEIN: A Wearable for the Lifter

Vein is a wearable device that uses an IMU and machine learning to count the number of repetitions performed of an exercise for a user and predict the exercise they are doing. Allowing the weight lifter to avoid the hassle of counting every rep and manually tracking their workouts.

### Exercises Currently Supported
- Bicep Curl
- Lateral Raises
- Front Raises
- Pullup
- Bench Press
- Deadlift
- Squat
- Overhead press

## Files
### collectData.py 
- Used to collect data for training
- run the script using the argument -e \<exercise name> and a positional argument \<N> for the file number of the exercise to start recording at
- Must be run as administrator for keyboard access
```
sudo python3 collectData.py 1 -e bicep-curl
```

### dataVisualization.py
- Used to preview the amount of time taken for each rep of a given exercise using matplotlib
- run the script with the flag -e \<exercise name> to show a specific exercise
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


## Prototype Components
- Arduino Nano
- MPU 6050 IMU
- HC-05 Wireless Bluetooth Host Serial Transceiver Module 
- 9V Battery

<img width="400" alt="Vein Hardware" src="https://user-images.githubusercontent.com/12948431/68535026-b7b67b00-0309-11ea-9519-f89c0f019290.png">

## System Design





## Requirements
```
pip3 install PyQt5 matplotlib numpy tensorflow
pip3 install keras==2.2.0
```
