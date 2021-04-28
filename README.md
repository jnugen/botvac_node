# WIP

## (Neato) Botvac launch files

This repository contains ROS2 Foxy launch files for the Neato Botvac robots.

## Install on RPi4

Prerequisites:

    sudo apt install build-essential
    sudo apt install ros-foxy-xacro
    sudo apt install python3-rosdep2

You can check this out into your workspace as follows:

    cd <ws>/src
    git clone https://github.com/jnugen/botvac_node.git
    git clone https://github.com/jnugen/neato_robot.git
    git clone https://github.com/kobuki-base/cmd_vel_mux.git
    git clone https://github.com/kobuki-base/velocity_smoother.git
    git clone -b foxy-devel https://github.com/ros-planning/navigation2.git
    cd ..
    rosdep update
    rosdep install --from-paths src --ignore-src -r -y
    colcon build
    source install/setup.bash

## Launch on RPi4

    ros2 launch botvac_node botvac_base_only.launch.py

## Launch on PC

   ros2 launch nav2_bringup bringup_launch.py use_sim_time:=False autostart:=True map:=/home/camp/colcon_ws/src/navigation2/nav2_bringup/bringup/maps/map.yaml slam:=True

## Run RViz2 on PC

   launch nav2_bringup rviz_launch.py 

## Run Teleop on PC

    ros2 run teleop_twist_keyboard teleop_twist_keyboard


## Command to save map on PC

    ros2 run nav2_map_server map_saver_cli -f ~/colcon_ws/src/navigation2/nav2_bringup/bringup/maps/map --ros-args -p save_map_timeout:=5000


