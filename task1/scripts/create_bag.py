import rclpy
# from rclpy.node import Node
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

# File Paths
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

# Load CSV
df = pd.read_csv(str(csv_file))

# Convert time (assume ms, convert to seconds)
df['time (us)'] = df['time (us)'] / 1000.0 

# Initialize ROS2 Bag Writer
writer = rosbag2_py.SequentialWriter()
storage_options = rosbag2_py.StorageOptions(uri=bag_file, storage_id="sqlite3")
converter_options = rosbag2_py.ConverterOptions(input_serialization_format="cdr", output_serialization_format="cdr")
writer.open(storage_options, converter_options)

# Create Topic
topic_info = rosbag2_py.TopicMetadata(
    name="/odometry",
    type="nav_msgs/msg/Odometry",
    serialization_format="cdr"
)
writer.create_topic(topic_info)

# Initialize ROS2 Node
rclpy.init()
node = rclpy.create_node('csv_to_rosbag')

for _, row in df.iterrows():
    msg = Odometry()
    
    # Set timestamp
    msg.header = Header()
    sec = int(row['time (us)'])
    nanosec = int((row['time (us)'] - sec) * 1e9)
    msg.header.stamp = Time(sec=sec, nanosec=nanosec)
    msg.header.frame_id = "odom"
    msg.child_frame_id = "base_link"
    
    # Pose (optional)
    msg.pose.pose = Pose()
    
    # Twist (velocity)
    msg.twist.twist = Twist()
    msg.twist.twist.linear.x = row['flowVelocityX[cm/s]'] / 100.0 
    msg.twist.twist.linear.y = row['secFlowVelocityX[cm/s]'] / 100.0
    # msg.twist.twist.angular.z = 0.0

    # Write to ROS 2 Bag
    timestamp_ns = node.get_clock().now().nanoseconds  # Get integer timestamp in nanoseconds
    # serialized_msg = rclpy.serialization.serialize_message(msg)  # Serialize Odometry message
    serialized_msg = serialize_message(msg)

    writer.write("/odometry", serialized_msg, timestamp_ns)  # Correct function call
    # writer.write("/odometry", node.get_clock().now().to_msg(), msg)

print(f"ROS 2 bag file created: {bag_file}")

# Shutdown Node
node.destroy_node()
rclpy.shutdown()
