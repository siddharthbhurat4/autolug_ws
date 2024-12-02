FROM osrf/ros:humble-desktop-full
ARG USERNAME=USERNAME
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN apt-get update \
    && apt-get install -y ros-humble-rviz2 \
    ros-humble-realsense2-description \
    ros-humble-gazebo-ros-pkgs \
    ros-humble-ur-description \
    ros-humble-ur-moveit-config \
    ros-humble-ur-robot-driver \
    ros-humble-gazebo-ros2-control \
    ros-humble-ros2-controllers \
    ros-humble-moveit \
    ros-humble-robotiq-description
# echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
# source ~/.bashrc
# Delete user if it exists in container (e.g Ubuntu Noble: ubuntu)
RUN if id -u $USER_UID ; then userdel `id -un $USER_UID` ; fi

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    #
    # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3-pip
ENV SHELL /bin/bash

# ********************************************************
# * Anything else you want to do like clean up goes here *
# ********************************************************

# [Optional] Set the default user. Omit if you want to keep the default as root.
USER $USERNAME
CMD ["/bin/bash"]
