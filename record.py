import numpy as np
import airsim
import os
from record_lib import *
from tqdm import tqdm
# Connect to the AirSim simulator
client = airsim.VehicleClient()
client.confirmConnection()

#seg_reid(client)

client.simPause(True)
folder = 'img'

delete_npy_files(folder)
poses = read_pose_data()

for pose in tqdm(poses):
    set_pose(client, pose)
    #image_save(client)
    image_save_test(client)