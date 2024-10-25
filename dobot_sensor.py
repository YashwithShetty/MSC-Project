
import DobotAPI as dType
import time

# Load the Dobot API
api = dType.load()

# Connect to the Dobot
state = dType.ConnectDobot(api, "", 115200)
if state[0] != dType.DobotConnect.DobotConnect_NoError:
    print("Failed to connect to Dobot.")
    exit()

# Enable the infrared sensor on GP4
infraredPort = dType.InfraredPort.PORT_GP4  # This is the attribute for the infrared sensor port
dType.SetInfraredSensor(api, True, infraredPort)

# Conveyor settings
STEP_PER_CIRCLE = 360.0 / 1.8 * 5.0 * 16.0  # Microstep resolution
MM_PER_CIRCLE = 3.1415926535898 * 32.0      # Wheel circumference
speed_pulses = int(100.0 * STEP_PER_CIRCLE / MM_PER_CIRCLE)  # Convert 100 mm/s into pulses

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
        else:
            if not conveyor_running:
                print("Object Undetected. Starting conveyor.")
                dType.SetEMotorEx(api, 0, 1, speed_pulses, True)  # Start the conveyor
                conveyor_running = True
        time.sleep(1)  # Check the sensor every second
finally:
    # Ensure conveyor stops when script is stopped or exited
    dType.SetEMotorEx(api, 0, 0, 0, True)  # Stop the conveyor
    # Disconnect the Dobot
    dType.DisconnectDobot(api)
    print("Conveyor operation completed.")
s