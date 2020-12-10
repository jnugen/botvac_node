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
            default_value = 'keyboard'
        ),

        # launch the teleop controller
        #launch.actions.IncludeLaunchDescription(
            #launch.launch_description_sources.PythonLaunchDescriptionSource(
                #os.path.join(share_dir, 'launch', 'include',
                #    LaunchConfiguration('teleop_controller'), '_teleop.launch.py' ]
                #)
            #)
        #),

        # smooths inputs from cmd_vel_mux/input/teleop_raw to cmd_vel_mux/input/teleop
        launch.actions.IncludeLaunchDescription(
            launch.launch_description_sources.PythonLaunchDescriptionSource(
                os.path.join(share_dir, 'launch', 'include', 'velocity_smoother.launch.py')
            ),
            launch_arguments = {
                'input_cmd_vel_topic': 'raw_cmd_vel',
                'feedback_cmd_vel_topic': 'robot_cmd_vel',
                'output_cmd_vel_topic': 'smoothed_cmd_vel'
            }.items()
        ),

        # velocity commands multiplexer
        launch_ros.actions.Node(
           package = 'cmd_vel_mux',
           executable = 'cmd_vel_mux_node',
           name = 'cmd_vel_mux',
           parameters = [
               os.path.join(share_dir, 'config', 'cmd_vel_mux_params.yaml')
           ],
           remappings = [
               ('cmd_vel_mux/output', 'robot_cmd_vel'),
               ('cmd_vel_mux/input/nav', 'cmd_vel'),
               ('cmd_vel_mux/input/teleop', 'smoothed_cmd_vel')
           ]
        ),

        # create transform for laser (should be moved to the URDF)
        launch_ros.actions.Node(
           package = 'tf2_ros',
           executable = 'static_transform_publisher',
           name = 'laser_to_base',
           arguments = ['-0.090', '0.0', '0.037', '0', '0', '0', '1', 'base_link', 'base_laser_link'],
           parameters = [
           ]
        ),

        # launch the main base driver node
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

        # publish the robot state transforms
        launch_ros.actions.Node(
            package = 'robot_state_publisher',
            executable = 'robot_state_publisher',
            name = 'robot_state_publisher',
            output = 'screen',
            parameters = [
                {'robot_description': Command(['xacro', ' ', xacro_file])}
            ]
        ),
    ])
    return ld

if __name__ == '__main__':
    generate_launch_description()
