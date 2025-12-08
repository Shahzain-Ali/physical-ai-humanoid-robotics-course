#!/usr/bin/env python3

"""
Simple ROS 2 subscriber example for the Physical AI & Humanoid Robotics course.
This node subscribes to sensor data to demonstrate ROS 2 communication patterns.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class SensorSubscriber(Node):
    """
    A simple subscriber node that listens to sensor data.
    """
    def __init__(self):
        super().__init__('sensor_subscriber')
        self.subscription = self.create_subscription(
            String,
            'sensor_data',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)
    sensor_subscriber = SensorSubscriber()

    try:
        rclpy.spin(sensor_subscriber)
    except KeyboardInterrupt:
        pass
    finally:
        sensor_subscriber.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()