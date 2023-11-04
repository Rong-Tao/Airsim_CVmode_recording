import airsim

# Connect to the AirSim simulator
client = airsim.CarClient()
client.confirmConnection()

# Get the pose of the CV agent
pose = client.simGetVehiclePose()

# Extract orientation and position data
orientation = pose.orientation
position = pose.position

# Format the data as 7 numbers per line: w, x, y, z, x_val, y_val, z_val
pose_data = f"{orientation.w_val} {orientation.x_val} {orientation.y_val} {orientation.z_val} {position.x_val} {position.y_val} {position.z_val}\n"

# Append the data to a text file
with open("pose_data.txt", "a") as file:
    file.write(pose_data)

print(pose_data)

