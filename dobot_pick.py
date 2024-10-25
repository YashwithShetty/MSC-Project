import DobotAPI as dType

# Load the Dobot API
api = dType.load()

# Connect to the Dobot
state = dType.ConnectDobot(api, "", 115200)
if state[0] != dType.DobotConnect.DobotConnect_NoError:
    print("Failed to connect to Dobot.")
    exit()

# Set velocity and acceleration
dType.SetPTPCommonParams(api, 100, 100)

# Define the Home and Pick Positions

home_position = [182.6247, -88.9444, 67.3457, -25.9676]   # [X, Y, Z, R]
pick_position = [207.9901, 2.4985, 24.1528, 0.6882]  # [X, Y, Z, R]
point1_position = [173.9806, -155.8300, 42.9136, -41.8500]  # [X, Y, Z, R]
point2_position = [148.1205, -180.0609, 41.8090, -50.5588]  # [X, Y, Z, R]
point3_position = [121.6288, -198.8924, 42.2298, -58.5529]  # [X, Y, Z, R]
point4_position = [93.4028, -213.6709, 41.9229, -66.3882]  # [X, Y, Z, R]


# Move to the home Position
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, *home_position)
dType.dSleep(2000)  # Wait for 2 seconds to ensure the Dobot reaches the pick position

# Move to the pick Position
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, *pick_position)
dType.dSleep(2000)  # Wait for 2 seconds to ensure the Dobot reaches the pick position

# Activate the suction cup to pick the object
dType.SetEndEffectorSuctionCup(api, True, True)
dType.dSleep(2000)

# Move to the home Position
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, *home_position)
dType.dSleep(2000)  # Wait for 2 seconds to ensure the Dobot reaches the pick position

# Move to the point1 Position
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, *point1_position)
dType.dSleep(2000)  # Wait for 2 seconds to ensure the Dobot reaches the pick position


# Activate the suction cup to pick the object
dType.SetEndEffectorSuctionCup(api, False, False)
dType.dSleep(2000) 

# Move to the home Position
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, *home_position)
dType.dSleep(2000)  # Wait for 2 seconds to ensure the Dobot reaches the pick position

# Move to the pick Position
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, *pick_position)
dType.dSleep(2000)  # Wait for 2 seconds to ensure the Dobot reaches the pick position

# Activate the suction cup to pick the object
dType.SetEndEffectorSuctionCup(api, True, True)
dType.dSleep(2000)

# Move to the home Position
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, *home_position)
dType.dSleep(2000)  # Wait for 2 seconds to ensure the Dobot reaches the pick position

# Move to the point2 Position
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, *point2_position)
dType.dSleep(2000)  # Wait for 2 seconds to ensure the Dobot reaches the pick position

# Activate the suction cup to pick the object
dType.SetEndEffectorSuctionCup(api, False, False)
dType.dSleep(2000) 

# Move to the home Position
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, *home_position)
dType.dSleep(2000)  # Wait for 2 seconds to ensure the Dobot reaches the pick position


# Move to the pick Position
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, *pick_position)
dType.dSleep(2000)  # Wait for 2 seconds to ensure the Dobot reaches the pick position

# Activate the suction cup to pick the object
dType.SetEndEffectorSuctionCup(api, True, True)
dType.dSleep(2000)

# Move to the home Position
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, *home_position)
dType.dSleep(2000)  # Wait for 2 seconds to ensure the Dobot reaches the pick position

# Move to the point3 Position
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, *point3_position)
dType.dSleep(2000)  # Wait for 2 seconds to ensure the Dobot reaches the pick position

# Activate the suction cup to pick the object
dType.SetEndEffectorSuctionCup(api, False, False)
dType.dSleep(2000) 

# Move to the home Position
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, *home_position)
dType.dSleep(2000)  # Wait for 2 seconds to ensure the Dobot reaches the pick position

# Move to the pick Position
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, *pick_position)
dType.dSleep(2000)  # Wait for 2 seconds to ensure the Dobot reaches the pick position

# Activate the suction cup to pick the object
dType.SetEndEffectorSuctionCup(api, True, True)
dType.dSleep(2000)

# Move to the home Position
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, *home_position)
dType.dSleep(2000)  # Wait for 2 seconds to ensure the Dobot reaches the pick position

# Move to the point4 Position
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, *point4_position)
dType.dSleep(2000)  # Wait for 2 seconds to ensure the Dobot reaches the pick position

# Activate the suction cup to pick the object
dType.SetEndEffectorSuctionCup(api, False, False)
dType.dSleep(2000) 

# Move to the home Position
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, *home_position)
dType.dSleep(2000)  # Wait for 2 seconds to ensure the Dobot reaches the pick position


# Disconnect the Dobot
dType.DisconnectDobot(api)
