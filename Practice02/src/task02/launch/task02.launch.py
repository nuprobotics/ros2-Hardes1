import os
from importlib.util import find_spec

from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    config = os.path.join(
        get_package_share_directory('task02'),
        'config',
        'task02.yaml'
    )

    return LaunchDescription([
        Node(
            package='task02',
            executable='publisher',
            name='publisher',
            output='screen',
            parameters=[config]
        ),
    ])