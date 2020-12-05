import os
import sys

import launch
import launch_ros.actions


def generate_launch_description():
    ld = launch.LaunchDescription([
        launch_ros.actions.Node(
            package = 'teleop_twist_keyboard',
            executable = 'teleop_twist_keyboard',
            name = 'teleop_keyboard',
            output = 'screen',
            #emulate_tty = 'True',
            #prefix = 'x-terminal-emulator -e /home/jnugen/bash-hacky',
            parameters = [
                #{'speed': '0.5'},
                #{'turn': '1.5'}
            ],
            remappings = [
                ('cmd_vel', 'raw_cmd_vel')
            ]
        )
    ])
    return ld

if __name__ == '__main__':
    generate_launch_description()
