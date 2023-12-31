import numpy as np
import airsim
import os
import matplotlib.pyplot as plt
from PIL import Image

def seg_reid(client):
    object_names = client.simListSceneObjects()
    id = 0
    for ob in object_names:
        if ob.lower().startswith('light'):
            continue
        print(id, ob)
        client.simSetSegmentationObjectID(ob,  id % 255)
        id += 1

def read_pose_data(file_path='pose_data.txt'):
    poses = []
    with open(file_path, 'r') as file:
        for line in file:
            # Extracting numbers from each line and converting them to float
            pose = [float(value) for value in line.strip().split()]
            poses.append(pose)
    return poses

def delete_npy_files(folder='img'):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.npy') or file.endswith('.png'):
                file_path = os.path.join(root, file)
                os.remove(file_path)

def set_pose(client, pose):
    orientation = airsim.Quaternionr(pose[0], pose[1], pose[2], pose[3])
    position = airsim.Vector3r(pose[4], pose[5], pose[6])
    pose = airsim.Pose(position, orientation)
    client.simSetVehiclePose(pose, True)

def image_save(client, base_folder = 'img'):
    # Pause the simulation
    
    # Request various types of images
    responses = client.simGetImages([
        airsim.ImageRequest("front_left", airsim.ImageType.Scene, False, False),
        airsim.ImageRequest("front_left", airsim.ImageType.DepthPerspective, True),
        airsim.ImageRequest("front_left", airsim.ImageType.Segmentation, False, False),
        airsim.ImageRequest("front_left", airsim.ImageType.SurfaceNormals, False, False),
        airsim.ImageRequest("front_right", airsim.ImageType.Scene, False, False),
        airsim.ImageRequest("front_right", airsim.ImageType.DepthPerspective, True),
        airsim.ImageRequest("front_right", airsim.ImageType.Segmentation, True, False),
        airsim.ImageRequest("front_right", airsim.ImageType.SurfaceNormals, True, False)
        ])

    # Specify the base folder to save images
    
    folders = ['left_raw', 'left_depth_perspective', 'left_seg', 'left_surface_normals',
            'right_raw', 'right_depth_perspective', 'right_seg', 'right_surface_normals']

    # Ensure folders exist
    for folder in folders:
        path = os.path.join(base_folder, folder)
        if not os.path.exists(path):
            os.makedirs(path)
            
    timestamp = str(responses[0].time_stamp)
    # Process and save each response
    for i, response in enumerate(responses):
        
        camera = 'left' if i < 4 else 'right'

        if response.image_type == airsim.ImageType.Scene:
            folder = f"{camera}_raw"
        elif response.image_type == airsim.ImageType.DepthPerspective:
            folder = f"{camera}_depth_perspective"
        elif response.image_type == airsim.ImageType.Segmentation:
            folder = f"{camera}_seg"
        elif response.image_type == airsim.ImageType.SurfaceNormals:
            folder = f"{camera}_surface_normals"

        filename = os.path.join(base_folder, folder, f"{timestamp}")
        npy_filename = f"{filename}.npy"
        png_filename = f"{filename}.png"

        # Case 1: Pixels as floating-point values
        if response.pixels_as_float:
            print("Type %d, size %d" % (response.image_type, len(response.image_data_float)))
            img = np.array(response.image_data_float).reshape(response.height, response.width, -1)

        # Case 2: Pixels as uint8 values
        else:
            print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
            img = np.frombuffer(response.image_data_uint8, dtype=np.uint8).reshape(response.height, response.width, -1)

        
        img = np.flipud(img)
        img = np.fliplr(img)

        # Save the image using Matplotlib without showing it
        default_dpi = plt.rcParams['figure.dpi']
        plt.figure(figsize=(img.shape[1] / default_dpi, img.shape[0] / default_dpi),
                   dpi=default_dpi)
        if img.shape[2] == 1:
            plt.imshow(img, cmap='gray', aspect='auto')
        else:
            img = img[:, :, ::-1]
            plt.imshow(img, aspect='auto')

        np.save(npy_filename, img)
        plt.axis('off')
        plt.savefig(png_filename, bbox_inches='tight', pad_inches=0)
        plt.close()

def image_save_test(client, base_folder = 'img'):
    # Pause the simulation
    
    # Request various types of images
    responses = client.simGetImages([
        airsim.ImageRequest("front_left", airsim.ImageType.Scene, False, False),
        airsim.ImageRequest("front_right", airsim.ImageType.Scene, False, False),
        ])

    # Specify the base folder to save images
    
    folders = ['left_raw', 'right_raw']

    # Ensure folders exist
    for folder in folders:
        path = os.path.join(base_folder, folder)
        if not os.path.exists(path):
            os.makedirs(path)
            
    timestamp = str(responses[0].time_stamp)
    # Process and save each response
    for i, response in enumerate(responses):
        
        camera = 'left' if i < 1 else 'right'

        if response.image_type == airsim.ImageType.Scene:
            folder = f"{camera}_raw"

        filename = os.path.join(base_folder, folder, f"{timestamp}")
        png_filename = f"{filename}.png"
        npy_filename = f"{filename}.npy"
        # Case 1: Pixels as floating-point values
        if response.pixels_as_float:
            #print("Type %d, size %d" % (response.image_type, len(response.image_data_float)))
            img = np.array(response.image_data_float).reshape(response.height, response.width, -1)

        # Case 2: Pixels as uint8 values
        else:
            #print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
            img = np.frombuffer(response.image_data_uint8, dtype=np.uint8).reshape(response.height, response.width, -1)

        
        img = np.flipud(img)
        img = np.fliplr(img)

        # Save the image using Matplotlib without showing it
        default_dpi = plt.rcParams['figure.dpi']
        plt.figure(figsize=(img.shape[1] / default_dpi, img.shape[0] / default_dpi),
                   dpi=default_dpi)
        if img.shape[2] == 1:
            plt.imshow(img, cmap='gray', aspect='auto')
        else:
            img = img[:, :, ::-1]
            plt.imshow(img, aspect='auto')
        np.save(npy_filename, img)
        plt.axis('off')
        plt.savefig(png_filename, bbox_inches='tight', pad_inches=0)
        plt.close()
