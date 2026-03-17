#!/bin/bash
set -e
source /opt/ros/$ROS_DISTRO/setup.bash
source /ros2/install/setup.bash

MODE="$1"
shift || true

case "$MODE" in
  record)
    BAG_NAME="$1"
    shift || true

    if [ -z "$BAG_NAME" ]; then
      echo "Error: No bag name specified."
      exit 1
    fi

    if [ "$#" -eq 0 ]; then
      echo "Error: No topics specified to record."
      exit 1
    fi

    echo "Recording to bag: $BAG_NAME"
    echo "Topics: $@"

    BAG_PATH="/ros2/bags/$BAG_NAME"

    ros2 bag record -o "$BAG_PATH" "$@" &
    RECORD_PID=$!

    trap "echo 'Stopping recording...'; kill -2 $RECORD_PID; wait $RECORD_PID" SIGINT SIGTERM

    wait $RECORD_PID
    echo "Recording stopped."
    ;;

  play)
    if [ -z "$1" ]; then
      echo "Error: No bag specified."
      exit 1
    fi

    BAG_PATH="/ros2/bags/$1"

    echo "Playing bag: $1"
    exec ros2 bag play "$BAG_PATH"
    ;;

  *)
    echo "Usage:"
    echo "  docker run <image> record <bag_name> /topic1 /topic2 ..."
    echo "  docker run <image> play <bag_name>"
    exit 1
    ;;
esac
