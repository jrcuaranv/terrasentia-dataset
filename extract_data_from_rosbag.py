"""
Script to extract data from rosbag files in the Terrasentia dataset
It is necessary to build fpn_msgs first in the catkin_ws
adapted from: https://cvg.cit.tum.de/data/datasets/rgbd-dataset/tools

"""
import argparse
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import cv2
from cv_bridge import CvBridge, CvBridgeError
import rospy
import rosbag
from sensor_msgs.msg import Image
import math 
cv_bridge = CvBridge()

def latlong2xyz(lat, lon, lat0, lon0): 
    # WGS84 ellipsoid constants:
    a = 6378137
    b = 6356752.3142
    e = math.sqrt(1-b**2/a**2)

    #east and north in meters
    east = a*math.cos(math.radians(lat0))*math.radians(lon-lon0)/math.pow(1-e**2*(math.sin(math.radians(lat0)))**2,0.5)
    north = a*(1 - e**2)*math.radians(lat-lat0)/math.pow(1-e**2*(math.sin(math.radians(lat0)))**2,1.5)
    return east, north # ENU (east, north, up) x and y coordinates in a reference frame with the origin in lat0, lon0
    #return north, east # NED (north, east, down) x and y coordinates in a reference frame with the origin in lat0, lon0

    
bag_file = "/media/jose/SSD1G/slam_dataset/ts_2022_06_09_13h16m39s_one_row.bag"
out_dir   = "/media/jose/SSD1G/slam_dataset/data_test"

left_cam_topic = "/terrasentia/zed2/zed_node/left/image_rect_color/compressed"
right_cam_topic = "/terrasentia/zed2/zed_node/right/image_rect_color/compressed"
deph_topic = "/terrasentia/zed2/zed_node/depth/depth_registered"
odom_topic = "/terrasentia/zed2/zed_node/odom"
gps_topic = "/terrasentia/full_gps"

# Add topics to extract
topics_list = [deph_topic, odom_topic, gps_topic, left_cam_topic] #right_cam_topic,


out_left_imgs_dir = os.path.join(out_dir, "left_imgs")
out_right_imgs_dir = os.path.join(out_dir, "right_imgs")
out_dep_dir = os.path.join(out_dir, "depth")
if not os.path.isdir(out_left_imgs_dir):
    os.makedirs(out_left_imgs_dir)
if not os.path.isdir(out_right_imgs_dir):
    os.makedirs(out_right_imgs_dir)
if not os.path.isdir(out_dep_dir):
    os.makedirs(out_dep_dir)

if not os.path.exists(bag_file):
    print("couldn't find bag file. check path")
    sys.exit(-1)

bag = rosbag.Bag(bag_file)
topics = bag.get_type_and_topic_info()[1].keys()

left_imgs_file = open(os.path.join(out_dir, 'left_imgs.txt'), 'w')
right_imgs_file = open(os.path.join(out_dir, 'right_imgs.txt'), 'w')
dep_file = open(os.path.join(out_dir, 'depth.txt'), 'w')
odom_file = open(os.path.join(out_dir, 'zed_odom.txt'), 'w')
gps_file = open(os.path.join(out_dir, 'gps.txt'), 'w')


for topic, msg, t in bag.read_messages(topics=topics_list):
    fn = format(((rospy.rostime.Time.to_nsec(t)/1e9) - 0), '.6f')
    print('timestamp', fn)
    if topic==left_cam_topic:
        np_arr = np.frombuffer(msg.data, np.uint8)
        cvimg = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        out_fn = os.path.join(out_left_imgs_dir, fn + '.png')
        left_imgs_file.write(fn + ' ' + 'rgb/' + fn + '.png' + '\n')
        cv2.imwrite(out_fn, cvimg)

    if topic==right_cam_topic:
        np_arr = np.frombuffer(msg.data, np.uint8)
        cvimg = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        out_fn = os.path.join(out_right_imgs_dir, fn + '.png')
        right_imgs_file.write(fn + ' ' + 'rgb/' + fn + '.png' + '\n')
        cv2.imwrite(out_fn, cvimg)
    
    
    if topic==deph_topic:
        cvimg = cv_bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
        cvimg = (1000*cvimg).astype(np.uint16) # depth will be in [mm]
        out_fn = os.path.join(out_dep_dir, fn + '.png')
        dep_file.write(fn + ' ' + 'depth/' + fn + '.png' + '\n')
        cv2.imwrite(out_fn, cvimg)
    
    if topic==odom_topic:
        odom_position = msg.pose.pose.position
        odom_orientation = msg.pose.pose.orientation
        # odom in TUM format: timestamp, x, y, z, qx, qy, qz, qw
        odom_file.write(fn + " " + str(odom_position.x) + " " + str(odom_position.y) + " " + str(odom_position.z) + " ")
        odom_file.write(str(odom_orientation.x) + " " + str(odom_orientation.y) + " " + str(odom_orientation.z) + " " + str(odom_orientation.w) + "\n")
    
    if topic == gps_topic:
        latitude = msg.latitude
        longitude = msg.longitude
        
        z_gps = msg.altitude
        # origin near the cornfield
        lat0 = 40.072126519
        long0 = -88.20951076
        x_gps, y_gps = latlong2xyz(latitude, longitude, lat0, long0) # in ENU (east, north, up)
        
        # gps in TUM format: timestamp, x, y, z, qx, qy, qz, qw
        gps_file.write(str(t.secs) +"." + str(t.nsecs).zfill(9)+ ' ' + str(x_gps) + ' ' + str(y_gps) + ' ' + str(z_gps) + ' 0.0 0.0 0.0 1.0\n')
            


left_imgs_file.close()
right_imgs_file.close()
dep_file.close()
odom_file.close()
gps_file.close()
bag.close()

# plot gps tracks
gps_data = np.loadtxt(out_dir + '/gps.txt')
plt.figure(1)
plt.plot(gps_data[:,1],gps_data[:,2])
plt.xlabel('x')
plt.ylabel('y')
plt.title('GPS tracks')
plt.show()