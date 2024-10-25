
from pathlib import Path

import tensorflow as tf
import DobotAPI as dType
import time
import cv2
import numpy as np
from copy import deepcopy as copy

# Conveyor CONSTS
STEP_PER_CIRCLE = 360.0 / 1.8 * 5.0 * 16.0  # Microstep resolution
MM_PER_CIRCLE = 3.1415926535898 * 32.0      # Wheel circumference
speed_pulses = int(100.0 * STEP_PER_CIRCLE / MM_PER_CIRCLE)  # Convert 100 mm/s into pulses
Z_OFFSET = 20

home_position = [182.6247, -88.9444, 67.3457, -25.9676]   # [X, Y, Z, R]
pick_position = [207.9901, 2.4985, 24.1528, 0.6882]  # [X, Y, Z, R]
point1_position = [173.9806, -155.8300, 42.9136, -41.8500]  # [X, Y, Z, R]
point2_position = [148.1205, -180.0609, 41.8090, -50.5588]  # [X, Y, Z, R]
point3_position = [121.6288, -198.8924, 42.2298, -58.5529]  # [X, Y, Z, R]
point4_position = [93.4028, -213.6709, 41.9229, -66.3882]  # [X, Y, Z, R]


# Define the labels
class_labels = ['unripe', 'partially_ripe', 'ripe', 'overripe']

model_filepath = Path(__file__).parent.joinpath('./models/banana_ripeness_classifier_finetuned.keras')
model = tf.keras.models.load_model(model_filepath)


def dobot_go(api, pos):
    # Move to the Approach Position
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, *pos)
    dType.dSleep(2000)  # Wait for 2 seconds to ensure the Dobot reaches the pick position

def dobot_control(api, location, suction:bool = True):
    approach = copy(location)
    approach[2] += Z_OFFSET

    # Move to the Approach Position
    dobot_go(api, approach)
    
    # Move to the pick Position
    dobot_go(api, location)

    # Activate the suction cup to pick the object
    dType.SetEndEffectorSuctionCup(api, suction, suction)
    dType.dSleep(500)

    # Move to the Approach Position
    dobot_go(api, approach)

def handle_camera():
    cap = cv2.VideoCapture(1)
    while True:
          # Try 0, 1, or higher if this doesn't work
        if not cap.isOpened():
            print("Error: Could not open camera.")
            return None
        ret, frame = cap.read()

        if not ret:
            print("Failed to grab frame")
            return None

        # Preprocess the image
        img = cv2.resize(frame, (224, 224))  # Resize to match the input shape of the model
        img_array = np.expand_dims(img, axis=0)  # Add batch dimension
        img_array = img_array / 255.0  # Normalize the image to [0, 1] range

        # Make predictions
        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions, axis=1)[0]

        # Get the label
        label = class_labels[predicted_class]
        #TODO check if no banana
        if label:
            break
        # Display the resulting frame
        # cv2.putText(frame, f'Predicted: {label}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        # cv2.imshow('Banana Ripeness Classification', frame)

    # Release the webcam and close windows
    cap.release()
    # cv2.destroyAllWindows()

    # Return the classification label
    return label

    

def main():
    # Load the Dobot API
    api = dType.load()

    # Connect to the Dobot
    state = dType.ConnectDobot(api, "", 115200)
    if state[0] != dType.DobotConnect.DobotConnect_NoError:
        print("Failed to connect to Dobot.")
        exit()


    # Enable the infrared sensor on GP4
    infraredPort = 2  # GP4 port is represented by 2 as per your system
    version = 1 # Assuming version 0 for this sensor
    dType.SetInfraredSensor(api, True, infraredPort, version)

    # Set velocity and acceleration
    dType.SetPTPCommonParams(api, 100, 100)

    # Move to the home Position
    dobot_go(api, home_position)
    try:
        conveyor_running = False
        while True:
            # Read the sensor value
            sensor_value = dType.GetInfraredSensor(api, infraredPort)[0]
            if sensor_value:
                if conveyor_running:
                    print("Object Detected! Stopping conveyor.")
                    dType.SetEMotorEx(api, 0, 0, 0, True)  # Stop the conveyor
                    conveyor_running = False

                    label = handle_camera()
                    print(label)
                    if not label:
                        raise('CAMERA FAILED')
                    dobot_control(api, pick_position ,suction=True)
                    
                    if label == class_labels[0]:
                        dobot_control(api,point1_position,suction=False)
                    elif label == class_labels[1]:
                        dobot_control(api,point2_position,suction=False)
                    elif label == class_labels[2]:
                        dobot_control(api,point3_position,suction=False)
                    elif label == class_labels[3]:
                        dobot_control(api,point4_position,suction=False)
                    dobot_go(api, home_position)
            else:
                if not conveyor_running:
                    print("Object Undetected. Starting conveyor.")
                    dType.SetEMotorEx(api, 0, 1, speed_pulses, True)  # Start the conveyor
                    conveyor_running = True
    finally:
        # Ensure conveyor stops when script is stopped or exited
        dType.SetEMotorEx(api, 0, 0, 0, True)  # Stop the conveyor
        
        # Move to the home Position
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, *home_position)
        dType.dSleep(2000)  # Wait for 2 seconds to ensure the Dobot reaches the pick position

        # Disconnect the Dobot
        dType.DisconnectDobot(api)

def close(api):
    dType.SetEMotorEx(api, 0, 0, 0, True)  # Stop the conveyor
        
    # Move to the home Position
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, *home_position)
    dType.dSleep(2000)  # Wait for 2 seconds to ensure the Dobot reaches the pick position

    # Disconnect the Dobot
    dType.DisconnectDobot(api)

if __name__ == '__main__':
    main()