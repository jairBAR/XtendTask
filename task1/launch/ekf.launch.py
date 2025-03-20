
import os
import pathlib
import launch_ros.actions
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, TimerAction, IncludeLaunchDescription, ExecuteProcess
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory


def get_pkg_path(pkg_name, *args):
    return str(pathlib.Path(get_package_share_directory(pkg_name), *args))


def include_launch_wo_args(path):
    return IncludeLaunchDescription(
        PythonLaunchDescriptionSource(get_pkg_path('task1', "launch", path))
    )

def include_launch_with_args(path, args):
    return IncludeLaunchDescription(
        PythonLaunchDescriptionSource(get_pkg_path('task1', "task1", path)),
        launch_arguments=args
    )

def generate_launch_description():
    config_file = os.path.join(get_package_share_directory("task1"), 'config', 'ekf_drone.yaml')
    bag_file_path = os.path.join(get_package_share_directory("task1"), 'assignment', 'sensor_data')

    return LaunchDescription([

        include_launch_wo_args("urdf.launch.py"),

        DeclareLaunchArgument(
            'config',
            default_value=config_file,
            description='Path to our YAML configuration file'
        ),

        TimerAction(
            period=1.0,  # delay in seconds
            actions=[launch_ros.actions.Node(
                package='robot_localization',
                executable='ekf_node',
                name='ekf_se_odom',
                output='screen',
                parameters=[LaunchConfiguration('config')],
            )]),
        
        TimerAction(
            period=2.0,  # delay in seconds
            actions=[ExecuteProcess(
                cmd=["ros2", "bag", "play", bag_file_path],
                output="screen"
            )]
        ),
    ])


if __name__ == '__main__':
    generate_launch_description()
