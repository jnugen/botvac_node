# WIP

## (Neato) Botvac launch files

This repository contains ROS2 Foxy launch files for the Neato Botvac robots.
 
# Assumes Ubuntu 20.04 and ROS2 have been successfully installed

## Install on RPi4

Prerequisites:

    sudo apt install build-essential
    sudo apt install ros-foxy-xacro
    sudo apt install python3-rosdep2

You can check this out into your workspace as follows:

    cd <ws>/src
    git clone https://github.com/cpeavy2/botvac_node.git
    git clone https://github.com/cpeavy2/neato_robot.git
    git clone https://github.com/kobuki-base/cmd_vel_mux.git
    git clone https://github.com/kobuki-base/velocity_smoother.git
    git clone -b foxy-devel https://github.com/ros-planning/navigation2.git
    cd ..
    rosdep update
    rosdep install --from-paths src --ignore-src -r -y
    echo 'source ~/<ws>/install/setup.bash' >> ~/.bashrc   # sources setup.bash
    source ~/<ws>/install/setup.bash                       # sources setup.bash for current session
    colcon build
    

## Launch on RPi4

    ros2 launch botvac_node botvac_base_only.launch.py

## Launch on PC

   ros2 launch nav2_bringup bringup_launch.py use_sim_time:=False autostart:=True map:=/home/user/ws/src/navigation2/nav2_bringup/bringup/maps/map.yaml slam:=True
   
   Note: Load from directory on your workstation. Remove "slam:=True" to load saved map.

## Run RViz2 on PC

   ros2 launch nav2_bringup rviz_launch.py 

## Run Teleop on PC

    ros2 run teleop_twist_keyboard teleop_twist_keyboard
    
## Drive the robot around to create map

## Command to save map on PC

    ros2 run nav2_map_server map_saver_cli -f ~/<ws>/src/navigation2/nav2_bringup/bringup/maps/map --ros-args -p save_map_timeout:=5000
    
    Note: Save to directory on your workstation.
    
## To load in map and navigate: 

   ros2 launch nav2_bringup bringup_launch.py use_sim_time:=False autostart:=True map:=/home/user/ws/src/navigation2/nav2_bringup/bringup/maps/map.yaml
    
## Set the robot's pose. Select a target goal on the map and the robot will autonomously navigate there.
    
