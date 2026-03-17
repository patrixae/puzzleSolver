#!/bin/bash
# Loosely based on https://gitlab.lrz.de/robotikss25/digitalization

set -e

source /opt/ros/${ROS_DISTRO}/setup.bash
echo "Sourced ROS2 ${ROS_DISTRO}"

colcon build

source /ros2_ws/install/setup.bash
echo "Sourced workspace"

exec "$@"
