import os
import sys

import launch
import launch_ros.actions
from launch.substitutions import LaunchConfiguration, Command
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    share_dir = get_package_share_directory('botvac_node')
    xacro_file = os.path.join(share_dir, 'urdf', 'neato.urdf.xacro')

    ld = launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(
            name = 'teleop_controller',
            default_value = 'keyboard'    # was xbox360
        ),
        launch.actions.DeclareLaunchArgument(
            name = 'input_cmd_vel_topic',
            default_value = 'raw_cmd_vel'
        ),
        launch.actions.DeclareLaunchArgument(
            name = 'feedback_cmd_vel_topic',
            default_value = 'robot_cmd_vel'
        ),
        launch.actions.DeclareLaunchArgument(
            name = 'output_cmd_vel_topic',
            default_value = 'smoothed_cmd_vel'
        ),
        launch_ros.actions.Node(
           package = 'cmd_vel_mux',
           executable = 'cmd_vel_mux_node',
           name = 'cmd_vel_mux',
           parameters = [
               os.path.join(share_dir, 'config', 'cmd_vel_mux_params.yaml')
           ]
        ),
        launch_ros.actions.Node(
           package = 'tf2_ros',
           executable = 'static_transform_publisher',
           name = 'laser_to_base',
           arguments = ['-0.090', '0.0', '0.037', '0', '0', '0', '1', 'base_link', 'base_laser_link'],
           parameters = [
           ]
        ),
        launch_ros.actions.Node(
            package = 'neato_node',
            executable = 'neato_node',
            name = 'neato_node',
            output = 'screen',
            parameters = [
                {'port': '/dev/ttyACM0'}
            ],
            remappings = [
                ('cmd_vel', 'robot_cmd_vel'),
                ('base_scan', 'scan')
            ],
            on_exit = launch.actions.Shutdown()
        ),
        launch_ros.actions.Node(
            package = 'robot_state_publisher',
            executable = 'robot_state_publisher',
            name = 'robot_state_publisher',
            output = 'screen',
            parameters = [
                {'robot_description': Command(['xacro', ' ', xacro_file])}
            ]
        ),
        # launch.actions.IncludeLaunchDescription(
        #     launch.launch_description_sources.PythonLaunchDescriptionSource(
        #         [ share_dir, '/launch/include/',
        #             LaunchConfiguration('teleop_controller'), '_teleop.launch.py' ]
        #     )
        # ),
        launch.actions.IncludeLaunchDescription(
            launch.launch_description_sources.PythonLaunchDescriptionSource(
                os.path.join(share_dir, 'launch', 'include', 'velocity_smoother.launch.py')
            ),
            launch_arguments = {
                'input_cmd_vel_topic': LaunchConfiguration('input_cmd_vel_topic'),
                'feedback_cmd_vel_topic': LaunchConfiguration('feedback_cmd_vel_topic'),
                'output_cmd_vel_topic': LaunchConfiguration('output_cmd_vel_topic')
            }.items()
        )
    ])
    return ld


if __name__ == '__main__':
    generate_launch_description()
