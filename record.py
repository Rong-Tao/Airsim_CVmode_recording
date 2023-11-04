import numpy as np
import airsim
import os
from record_lib import *
'''
client.simSetSegmentationObjectID("driveway[\w]*", 0, True)
id = 1
for ob in object_names:
    print(id, ob)
    if ob.lower().startswith("driveway"):
        continue
    else:
        client.simSetSegmentationObjectID(ob, 1 + id % 255)
        id += 1
'''
# Connect to the AirSim simulator
client = airsim.VehicleClient()
client.confirmConnection()
client.simPause(True)
folder = 'img'

delete_npy_files(folder)
poses = read_pose_data()

for pose in poses:
    set_pose(client, pose)
    image_save(client)