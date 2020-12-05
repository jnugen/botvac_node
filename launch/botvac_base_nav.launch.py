import os
import sys

import launch
import launch_ros.actions
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    ld = launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(
            name='map_name',
            default_value='map'
        ),
        launch.actions.IncludeLaunchDescription(
            launch.launch_description_sources.PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory(
                    'botvac_node'), 'launch', 'include', 'botvac_nav.launch.py')
            ),
            launch_arguments={
                'map_name': launch.substitutions.LaunchConfiguration('map_name')
            }.items()
        ),
        launch.actions.IncludeLaunchDescription(
            launch.launch_description_sources.PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory(
                    'botvac_node'), 'launch', 'include', 'botvac_base.launch.py')
            )
        )
    ])
    return ld


if __name__ == '__main__':
    generate_launch_description()
