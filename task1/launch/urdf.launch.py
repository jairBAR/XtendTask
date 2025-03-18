from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os
import xacro

def generate_launch_description():
    xacro_file_name = "sjtu_drone.urdf.xacro"
    xacro_file = os.path.join(
        get_package_share_directory("sjtu_drone_description"),
        "urdf", xacro_file_name
    )
    yaml_file_path = os.path.join(
        get_package_share_directory('sjtu_drone_bringup'),
        'config', 'drone.yaml'
    )
    robot_description_config = xacro.process_file(xacro_file, mappings={"params_path": yaml_file_path})
    robot_desc = robot_description_config.toxml()
    use_sim_time = LaunchConfiguration("use_sim_time", default="true")

    return LaunchDescription([
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            name="robot_state_publisher",
            # namespace=model_ns,
            output="screen",
            parameters=[{"use_sim_time": use_sim_time, "robot_description": robot_desc}],
            arguments=[robot_desc]
        ),

        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            # namespace=model_ns,
            output='screen',
        ),
        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            arguments=[
                "-d",
                os.path.join(
                    get_package_share_directory('task1'),
                    'config', 'rviz', 'drone.rviz'
                ),
            ],
            output="screen",
        ),
    ])
