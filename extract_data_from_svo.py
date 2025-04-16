"""
Extracting data from svo files in Terrasentia dataset
Requires ZED SDK (version older than 4.1. Tested with ZED SDK 3.7.2)
"""
import pyzed.sl as sl
import cv2
import os
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt

def extract_data_from_single_svo(svo_input_path, output_folder, skip=1, resize_shape=None):
    print("Extracting frames and poses from:", svo_input_path)
    # File to store absolute poses
    os.makedirs(output_folder, exist_ok=True)
    
    pose_file_path = os.path.join(output_folder, "poses.txt")
    pose_file = open(pose_file_path, 'w')
    left_subfolder = os.path.join(output_folder, "left")
    right_subfolder = os.path.join(output_folder, "right")
    os.makedirs(left_subfolder, exist_ok=True)
    os.makedirs(right_subfolder, exist_ok=True)

    # Initialize ZED camera
    zed = sl.Camera()

    # Set configuration parameters
    init_params = sl.InitParameters()
    init_params.set_from_svo_file(svo_input_path)  # Use the SVO file as input
    init_params.svo_real_time_mode = False  # Process as fast as possible (not in real-time)
    # Enable positional tracking
    init_params.coordinate_units = sl.UNIT.METER  # Set units to meters
    # init_params.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Z_UP  # Define coordinate system
    init_params.coordinate_system = sl.COORDINATE_SYSTEM.IMAGE  # x right, y down, z forward

    # Open the SVO file
    if zed.open(init_params) != sl.ERROR_CODE.SUCCESS:
        print("Error opening SVO file!")
        exit(1)

    # Enable positional tracking
    tracking_params = sl.PositionalTrackingParameters()
    # tracking_params.enable_imu_fusion = False  # Disable IMU fusion (for visual only tracking)
    zed.enable_positional_tracking(tracking_params)

    # Runtime parameters
    runtime_params = sl.RuntimeParameters()

    # Image and pose containers
    left_image = sl.Mat()
    right_image = sl.Mat()
    pose = sl.Pose()  # To store camera pose
    frame_count = 0
    saved_frames_count = 0

   
    while True:
        # Grab the next frame
        if zed.grab(runtime_params) == sl.ERROR_CODE.SUCCESS:
            if frame_count % skip == 0:
                # Retrieve the left RGB image
                zed.retrieve_image(left_image, sl.VIEW.LEFT)  # Get left image in RGB format
                zed.retrieve_image(right_image, sl.VIEW.RIGHT)
                left_rgb = left_image.get_data()  # Convert to numpy array (height, width, 4)
                right_rgb = right_image.get_data()  # Convert to numpy array (height, width, 4)
                # Remove alpha channel (last dimension)
                left_rgb = left_rgb[:, :, :3]
                right_rgb = right_rgb[:, :, :3]
                # # resize image
                if resize_shape is not None:
                    left_rgb = cv2.resize(left_rgb, resize_shape, interpolation=cv2.INTER_LINEAR)
                    right_rgb = cv2.resize(right_rgb, resize_shape, interpolation=cv2.INTER_LINEAR)
                # Retrieve LEFT camera pose
                tracking_state = zed.get_position(pose, sl.REFERENCE_FRAME.WORLD)
                # print(tracking_state)
                if (tracking_state == sl.POSITIONAL_TRACKING_STATE.OK) or (tracking_state == sl.POSITIONAL_TRACKING_STATE.SEARCHING):
                    # Get translation (x, y, z)
                    translation = pose.get_translation().get()
                    # Get orientation as quaternion (qx, qy, qz, qw)
                    quaternion = pose.get_orientation().get()
                    # Write pose to file in format: x y z qx qy qz qw
                    pose_line = f"{translation[0]} {translation[1]} {translation[2]} {quaternion[0]} {quaternion[1]} {quaternion[2]} {quaternion[3]}\n"
                    pose_file.write(pose_line)
                    
                    left_output_path = os.path.join(left_subfolder, f"left_frame_{saved_frames_count:06d}.png")
                    right_output_path = os.path.join(right_subfolder, f"right_frame_{saved_frames_count:06d}.png")
                    cv2.imwrite(left_output_path, left_rgb)
                    cv2.imwrite(right_output_path, right_rgb)
                    pose_line = "{:.6f} {:.6f} {:.6f} {:.6f} {:.6f} {:.6f} {:.6f}\n".format(
                                translation[0], translation[1], translation[2],
                                quaternion[0], quaternion[1], quaternion[2], quaternion[3])
                    pose_file.write(pose_line)
                    saved_frames_count += 1
                    
                else:
                    print(f"Warning: Pose not available for frame {saved_frames_count}")
            frame_count += 1

        else:
            print("Frames extracted:", saved_frames_count)
            break  # No more frames

    pose_file.close()
    zed.disable_positional_tracking()
    zed.close()

def plot_trajectories(poses_path, output_dir):

    poses = np.loadtxt(poses_path)
    x = poses[:, 0]
    y = poses[:, 1]
    z = poses[:, 2]

    deltax = np.diff(x)
    deltay = np.diff(y)
    deltaz = np.diff(z)
    deltaxyz = np.sqrt(deltax**2 + deltay**2 + deltaz**2)
    cumdist = np.cumsum(deltaxyz) # total traveled distance
    print(cumdist.shape)
    print("Total traveled distance:",cumdist[-1])
    plt.figure(1)
    plt.plot(x, z, 'ro')
    plt.title('Camera trajectory')
    plt.xlabel('X')
    plt.ylabel('Z')
    plt.axis('equal')
    plt.grid()
    #saving figure
    file_prefix = poses_path.split('/')[-2]
    file_name = file_prefix + '_traj_length_' + str(int(cumdist[-1])).zfill(5) +  "m.png"
    file_path = os.path.join(output_dir, file_name)
    plt.savefig(file_path)
    plt.clf()  # Clears figure

########### Main script ###########    
svo_folder_path = Path("/media/jose/SSD1G/datasets/terrasentia_data") # folder containing svo files. They can be in subfolders as well
output_dir = '/media/jose/SSD1G/datasets/terrasentia_data/images_v3'
skip = 5 # Number of images to skip (for downsampling)
# Resize images to this shape (width, height). Set to None if no resizing is needed. Original size is 1280x720
resize_shape = (832, 468) 

intrinsics = np.array([527.20909706, 527.20909706, 627.52751277, 341.21312068]) #fx, fy, cx, cy for (1280x720) resolution
if resize_shape is not None:
    # Calculate new intrinsics for the resized image
    scale_x = resize_shape[0] / 1280
    scale_y = resize_shape[1] / 720
    intrinsics[0] *= scale_x  # fx
    intrinsics[1] *= scale_y  # fy
    intrinsics[2] *= scale_x  # cx
    intrinsics[3] *= scale_y  # cy
    print("New intrinsics:", intrinsics)


files_count = 0
for file_path in svo_folder_path.rglob("*.svo"):
    try:
        print(f"Processing Number {files_count}_{file_path}")
        file_name = file_path.name.split('.svo')[0]
        output_subdir = os.path.join(output_dir, file_name)
        os.makedirs(output_subdir, exist_ok=True)
        extract_data_from_single_svo(str(file_path), output_subdir, skip=skip)
        files_count += 1
        plot_trajectories(os.path.join(output_subdir, "poses.txt"), output_dir)
    except Exception as e:
        print("Error processing", file_path, ":", str(e))

print("New intrinsics:", intrinsics)