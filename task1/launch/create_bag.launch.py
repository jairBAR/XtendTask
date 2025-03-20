from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    return LaunchDescription([
        Node(
            package="task1",
            executable="create_bag.py",
            name="create_bag",
            output="screen",
        ),
    ])
