# **Xtend Home Assignement** 
by Yair Barzilay

* Clone this repo and checkout master.
> git clone -b master https://github.com/jairBAR/XtendTask.git

* In each of the task's folders you will find a video you can play which will showcase the results. 
* However, If you'd like to launch everything on your own, you can either use docker, or if you have ros-humble on ubuntu22, you can simply build the project yourself.

---	

### Using Docker
* Run the script that's in the repo:
> cd XtendTask

> ./docker_up.sh

* Then, once the docker image is built you should find yourself inside the container, so just follow the instructions for Task 1 and 2 in the next section...

### Building in a workspace
* Make sure you have the following dependencies installed:
```
sudo apt-get update && sudo apt-get install -y \
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
    libglib2.0-0
```


* Then simply build your ros2 workspace as you would on any given monday.

---
## Launching the Tasks

### Task 1
* This is a single node state estimator (EKF) which produces the robot's base_link position within a world fixed frame called odom.
* You first need to create a ros2bag of the sensor data which was originaly supplied as a spreadsheet:
> ros2 launch task1 create_bag.launch.py

* Once the ros2bag is created, run the launch file:
> ros2 launch task1 ekf.launch.py

### Task 2
* This is a physical world simulation of a drone flying autonomously in a square route moving upwards in a spiral-like fashion.
* Kindly note, that the Gazebo world might take a few minutes to load depending on your computer's available resources.
> ros2 launch task2 drone_sim.launch.py 

---

# The assignment

## Task 1 - Sensor Fusion
* The supplied data was given in a spreadsheet format with one time column hinting at a 'us' time unit and two sensor readings in units of cm/s.
* I assumed the data of the columns is orthogonoal and therefor independant for each one. In other words, I assumed the first column to be velocity measured in the X axis and the second column to be velocity measured in the Y axis.
* There was no additional information about the data, neither was there any ground truth or at least a specific scenario told in-order to assume the validity of the solution. Meaning I could not assume some sort of pattern to emerge such as driving in a sine wave configration or flying in a circular motion, etc...
* The task stated that some "sensors may have errors in certain scenarios" which i assumed was a hint towards using a Kalman Filter since Kalman filters are specifically designed to account for sensor measurement errors via covariances, when they are given or at least computed in some manner.
* On ther hand, the task stated that "the data from each sensor is good enough" therefor I did not feel obliged to provide the missing covariances myself and since the EKF implementation I was using did not require it either, it was indeed redundant to create.
* The task called for the algorithm to be real-time and efficient as possible. Kalaman filters are often used in flight controllers for state estmation purposes which are generally required for control loop closures (specifically RPY). However velocity sensors output data which is typically used to estimate positional (XYZ) data which is usually utlizied in higher level control, sometimes also reffered to as outer loop control.
* Since the supplied data was that of velocity sensors and not say a gyroscope I opted to utilize a very well-known and highly utilized package called 'robot_localization' which implements two types of state estimators for omnidirectional bodies.
* To achieve this, I saved the spreadsheet into CSV format and then collected the contents of each column (transforming the cm/s to m/s) into a ros2 bag with a 'nav_msgs/msg/Odometry' topic called /odometry specifying the frame id to be 'odom' and the child frame to be 'base_link'.
* According to [REP105](https://ros.org/reps/rep-0105.html) of ROS when the state estimation has unbounded drift, as would be the case when using only diffrential data (velocities), the convention is to use a world fixed frame called 'odom'.
* Thus, the odom state estimator was set up to recieve one topic called 'odometry' and only utilize its Vx and Vy components. This can be easily seen via the configuration file:

![image](https://github.com/user-attachments/assets/de6a8554-838a-4d79-b113-28e6b6beb98f)

* The results were as expected for such a simple and data-sparesed scenario. I was able to estimate a position but I have no clue as to its validity, as stated above, since there is no ground truth or at least a specific scenario told such as 'driving in a sine wave configration' or 'flying in a circular motion'.

In the following picture you can see the input Vx data (green) vs the output data (red) of the state estmation node for the same dimension (Vx):

![image](https://github.com/user-attachments/assets/918643eb-9be1-4440-a2fa-2912fd4dbd7a)
![image](https://github.com/user-attachments/assets/322dbee9-714e-4682-b3fc-ed6eff1f48e1)

In the following picture is an XY plot of the position estimation (the sum product of the EKF):
![image](https://github.com/user-attachments/assets/70ff899c-59d8-415f-a791-d9d47e537db4)


## Task 2 - Gazebo Simulation
* The task specified using ROS (1 or 2) simulate a robot flying/driving in a clustered environment. You may choose your sensors, and/or use gazebo data for the position estimation. The movement should mainly be autonomous.
* A quick google search turned up [stju_drone](https://github.com/NovoG93/sjtu_drone) an open sourced (although GPL licensed) package for simulating a drone flying in some world scene.
* Addimatedly, I had to apply a minor fix to their drone control python script to make it work (they have an import error). However the simulation works.
* As can be seen, this simulates a drone flying around autnomously in a rising sqaure configuration (helix-like).
* The simulated drone has 4 sensors:
1) Camera front
2) Camera bottom
3) IMU
4) GPS
* The cameras can be seen in RVIZ and the trajectory (tracklet) is being drawn in light blue.
  
![task2](https://github.com/user-attachments/assets/a37168b0-3e44-4ae2-83cd-f0e259fefb47)



