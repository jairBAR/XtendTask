#!/usr/bin/env python3

import rclpy
from rclpy.serialization import serialize_message
import pandas as pd
import os
import shutil
import rosbag2_py
from builtin_interfaces.msg import Time
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist, Pose
from std_msgs.msg import Header
from ament_index_python.packages import get_package_share_directory

csv_file = os.path.join(
                get_package_share_directory('task1'),
                'assignment', 'velocity_sensors_data.csv'
            )

bag_file = os.path.join(
                get_package_share_directory('task1'),
                'assignment', 'sensor_data'
            )

if os.path.exists(bag_file):
    print(f"🗑️ Removing existing bag directory: {bag_file}")
    shutil.rmtree(bag_file)

df = pd.read_csv(str(csv_file))
df['time (us)'] = df['time (us)'] / 1000.0 

writer = rosbag2_py.SequentialWriter()
storage_options = rosbag2_py.StorageOptions(uri=bag_file, storage_id="sqlite3")
converter_options = rosbag2_py.ConverterOptions(input_serialization_format="cdr", output_serialization_format="cdr")
writer.open(storage_options, converter_options)

topic_info = rosbag2_py.TopicMetadata(
    name="/odometry",
    type="nav_msgs/msg/Odometry",
    serialization_format="cdr"
)
writer.create_topic(topic_info)

rclpy.init()
node = rclpy.create_node('csv_to_rosbag')

for _, row in df.iterrows():
    msg = Odometry()
    msg.header = Header()
    sec = int(row['time (us)'])
    nanosec = int((row['time (us)'] - sec) * 1e9)
    msg.header.stamp = Time(sec=sec, nanosec=nanosec)
    msg.header.frame_id = "odom"
    msg.child_frame_id = "base_link"
    msg.pose.pose = Pose()
    msg.twist.twist = Twist()
    msg.twist.twist.linear.x = row['flowVelocityX[cm/s]'] / 100.0 
    msg.twist.twist.linear.y = row['secFlowVelocityX[cm/s]'] / 100.0

    timestamp_ns = node.get_clock().now().nanoseconds
    serialized_msg = serialize_message(msg)

    writer.write("/odometry", serialized_msg, timestamp_ns)

print(f"ROS 2 bag file created: {bag_file}")

node.destroy_node()
rclpy.shutdown()
