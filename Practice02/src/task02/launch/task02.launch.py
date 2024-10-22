import os
from importlib.util import find_spec

from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node

def generate_launch_description():
    config = os.path.join(
        get_package_share_directory('task02'),
        'config',
        'task02.yaml'
    )

    text_arg = DeclareLaunchArgument(
        'text',
        default_value='Hello, ROS2!',
        description='Text to publish'
    )

    return LaunchDescription([
        text_arg,
        Node(
            package='task02',
            executable='publisher',
            name='publisher',
            output='screen',
            parameters=[config]
        ),
    ])