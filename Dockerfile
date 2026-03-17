# Loosely based on https://gitlab.lrz.de/robotikss25/digitalization

ARG ROS_DISTRO=jazzy

FROM ros:${ROS_DISTRO}
ENV ROS_DISTRO=${ROS_DISTRO}

WORKDIR /ros2

# install overlay dependencies
COPY robotikss25/robotik_interfaces/package.xml /ros2/robotik_interfaces/package.xml
COPY package.xml /ros2/src/package.xml
RUN . /opt/ros/${ROS_DISTRO}/setup.sh \
  && apt-get update -y \
  && apt-get install -y python3-pip \
  && rosdep install --from-paths src --from-path robotik_interfaces --ignore-src --rosdistro ${ROS_DISTRO} -y \
  && rm -rf /var/lib/apt/lists/*
RUN pip install --break-system-packages frechetdist==0.6 torch==2.7.0

# build overlay source
COPY robotikss25/robotik_interfaces/ /ros2/robotik_interfaces
COPY setup.cfg /ros2/src
COPY setup.py /ros2/src
COPY solution.launch /ros2/src/solution.launch
COPY resource/ /ros2/src/resource
COPY puzzle_solver/ /ros2/src/puzzle_solver
RUN . /opt/ros/$ROS_DISTRO/setup.sh \
    && colcon build

# source entrypoint setup
RUN sed --in-place --expression \
      '$isource "/ros2/install/setup.bash"' \
      /ros_entrypoint.sh

ENV ROS_DOMAIN_ID=0

CMD ["ros2", "launch", "puzzle_solver", "solution.launch"]
