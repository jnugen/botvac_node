import os
import sys

import launch
import launch_ros.actions


def generate_launch_description():
    ld = launch.LaunchDescription([
        launch_ros.actions.Node(
            package='gmapping',
            executable='slam_gmapping',
            name='SLAM',
            parameters=[
                {
                    'maxUrange': '5.0'
                },
                {
                    'maxRange': '4.8'
                },
                {
                    'xmin': '-50.0'
                },
                {
                    'ymin': '-50.0'
                },
                {
                    'xmax': '50.0'
                },
                {
                    'ymax': '50.0'
                }
            ]
        )
    ])
    return ld


if __name__ == '__main__':
    generate_launch_description()
