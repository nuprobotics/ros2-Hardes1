FROM ros:iron
ARG ROS_DISTRO=iron
WORKDIR workspace

COPY . .

SHELL [ "/bin/bash", "-c" ]

RUN apt update -y && apt install -y tmux
RUN rm /etc/ros/rosdep/sources.list.d/20-default.list
RUN rosdep init && rosdep update
RUN rosdep install -y --from-path ./Practice02/src --rosdistro=${ROS_DISTRO}
RUN source /opt/ros/${ROS_DISTRO}/setup.bash && colcon build
RUN chmod 700 /opt/ros/${ROS_DISTRO}/setup.bash

