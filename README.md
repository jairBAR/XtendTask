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
> sudo apt install ros-humble-gazebo-ros ros-humble-gazebo-plugins ros-humble-joy ros-humble-teleop-twist-joy ros-humble-imu-tools ros-humble-robot-localization

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
* Kindly note, that the Gazebo world might take a few minutes to load depending on your computer's resources.
> ros2 launch task2 drone_sim.launch.py 
