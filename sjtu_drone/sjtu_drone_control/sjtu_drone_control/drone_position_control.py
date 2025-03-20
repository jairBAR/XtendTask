import rclpy
import math
import time
from sjtu_drone_control.drone_utils.drone_object import DroneObject

class DronePositionControl(DroneObject):
    def __init__(self):
        super().__init__('drone_position_control')

        self.takeOff()
        self.get_logger().info('Drone takeoff')
        time.sleep(3)
        self.posCtrl(True)
        self.get_logger().info('Position control mode set to True')
        self.move_drone_to_pose(0.0, 0.0, 6.0)
        time.sleep(3)
        i = 1
        while i<=10:
            self.move_drone_to_pose(50.0, 10.0, 5.0+i)
            time.sleep(5)
            self.move_drone_to_pose(-50.0, 10.0, 5.0+i)
            time.sleep(5)
            self.move_drone_to_pose(-50.0, -10.0, 5.0+i)
            time.sleep(5)
            self.move_drone_to_pose(50.0, -10.0, 5.0+i)
            time.sleep(5)
            i=i+1


    def move_drone_to_pose(self, x, y, z):
        super().moveTo(x, y, z)
        self.get_logger().info(f'Moving drone to pose: x={x}, y={y}, z={z}')


def main(args=None):
    rclpy.init(args=args)
    drone_position_control_node = DronePositionControl()
    rclpy.spin(drone_position_control_node)
    drone_position_control_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()