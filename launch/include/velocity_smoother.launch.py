import os
import sys

import launch
import launch_ros.actions
from ament_index_python.packages import get_package_share_directory

import yaml


pkg_name = 'velocity_smoother'
node_name = 'teleop_velocity_smoother'

config_file = 'velocity_smoother_params.yaml'

input_cmd_vel_topic = 'raw_cmd_vel'
feedback_cmd_vel_topic = 'robot_cmd_vel'
feedback_odom_topic = 'odom'
output_cmd_vel_topic = 'smoothed_cmd_vel'

def generate_launch_description():
    share_dir = get_package_share_directory(pkg_name)

    params_file = os.path.join(share_dir, 'config', config_file)
    with open(params_file, 'r') as f:
        params = yaml.safe_load(f)[pkg_name]

    ld = launch.LaunchDescription([
        launch_ros.actions.Node(
            package = pkg_name,
            executable = pkg_name,
            name = node_name,
            output = 'both',
            parameters = [params],
            remappings = [
                (node_name + '/input', input_cmd_vel_topic),
                (node_name + '/feedback/cmd_vel', feedback_cmd_vel_topic),
                (node_name + '/feedback/odometry', feedback_odom_topic),
                (node_name + '/smoothed', output_cmd_vel_topic)
            ]
        )
    ])
    return ld


if __name__ == '__main__':
    generate_launch_description()
