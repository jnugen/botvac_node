import os
import sys

import launch
import launch_ros.actions


def generate_launch_description():
    ld = launch.LaunchDescription([
        launch_ros.actions.Node(
            package = 'teleop_twist_joy',
            executable = 'teleop_node',
            name = 'teleop_joystick',
            parameters = [
                {'scale_angular': '1.5'},
                {'scale_linear': '0.5'},
                {'enable_button': '10'},
                {'axis_linear': '1'},
                {'axis_angular': '0'}
            ],
            remappings = [
                ('teleop_joystick/cmd_vel' 'raw_cmd_vel')
            ]
        ),
        launch_ros.actions.Node(
            package = 'joy',
            executable = 'joy_node',
            name = 'joystick',
            parameters = [
                {'autorepeat_rate': '4'}
            ]
        )
    ])
    return ld


if __name__ == '__main__':
    generate_launch_description()
