import os
import sys

import launch
import launch_ros.actions
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    ld = launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(
            name='teleop_controler',
            default_value='logitech'
        ),
        launch.actions.DeclareLaunchArgument(
            name='input_cmd_vel_topic',
            default_value='/raw_cmd_vel'
        ),
        launch.actions.DeclareLaunchArgument(
            name='feedback_cmd_vel_topic',
            default_value='robot_cmd_vel'
        ),
        launch.actions.DeclareLaunchArgument(
            name='output_cmd_vel_topic',
            default_value='smoothed_cmd_vel'
        ),
        launch_ros.actions.Node(
            package='nodelet',
            executable='nodelet',
            name='cmd_vel_mux',
            parameters=[
                {
                    'robot_description': None
                },
                {
                    'yaml_cfg_file': get_package_share_directory('bv80bot_node') + '/param/mux.yaml'
                }
            ]
        ),
        launch_ros.actions.Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='laser_to_base',
            parameters=[
                {
                    'robot_description': None
                }
            ]
        ),
        launch_ros.actions.Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='raspicam_to_base',
            parameters=[
                {
                    'robot_description': None
                }
            ]
        ),
        launch_ros.actions.Node(
            package='neato_node',
            executable='neato.py',
            name='neato',
            output='screen',
            parameters=[
                {
                    'robot_description': None
                },
                {
                    'port': '/dev/ttyACM0'
                }
            ]
        ),
        launch_ros.actions.Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[
                {
                    'robot_description': None
                },
                {
                    'use_gui': 'False'
                }
            ]
        ),
        launch.actions.IncludeLaunchDescription(
            launch.launch_description_sources.PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory(
                    'bv80bot_node'), 'launch/include/$(arg teleop_controler)_teleop.launch.py')
            )
        ),
        launch.actions.IncludeLaunchDescription(
            launch.launch_description_sources.PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory(
                    'bv80bot_node'), 'launch/include/velocity_smoother.launch.py')
            ),
            launch_arguments={
                'input_cmd_vel_topic': launch.substitutions.LaunchConfiguration('input_cmd_vel_topic'),
                'feedback_cmd_vel_topic': launch.substitutions.LaunchConfiguration('feedback_cmd_vel_topic'),
                'output_cmd_vel_topic': launch.substitutions.LaunchConfiguration('output_cmd_vel_topic')
            }.items()
        )
    ])
    return ld


if __name__ == '__main__':
    generate_launch_description()
