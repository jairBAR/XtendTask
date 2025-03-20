FROM ros:humble-ros-base

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN apt-get update && apt-get install -y \
    sudo \
    git \
    build-essential \
    cmake \
    curl \
    gnupg2 \
    lsb-release \
    python3-colcon-common-extensions \
    python3-pip \
    wget \
    software-properties-common \
    ros-humble-robot-localization \
    ros-humble-gazebo-ros \
    ros-humble-gazebo-plugins \
    ros-humble-rviz2 \
    ros-humble-joy \
    ros-humble-cv-bridge \
    ros-humble-image-transport \
    ros-humble-map-msgs \
    ros-humble-resource-retriever \
    ros-humble-rviz-common \
    ros-humble-rviz-rendering \
    xterm \
    libboost-all-dev \
    qtbase5-dev \
    ros-humble-imu-tools \
    ros-humble-teleop-twist-keyboard \
    libqt5core5a \
    libqt5gui5 \
    libqt5opengl5 \
    libqt5widgets5 \
    ros-humble-ament-cmake-clang-format \
    ros-humble-joint-state-publisher \
    ros-humble-xacro \
    x11-apps \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install pandas

WORKDIR /workspace
RUN git clone -b master https://github.com/jairBAR/XtendTask.git src/XtendTask

RUN /bin/bash -c "source /opt/ros/humble/setup.bash && colcon build"

RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
RUN echo "source /workspace/install/setup.bash" >> ~/.bashrc

CMD ["/bin/bash"]
