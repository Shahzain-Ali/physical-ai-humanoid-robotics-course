---
sidebar_position: 3
title: The Robotic Nervous System (ROS 2)
---

# The Robotic Nervous System (ROS 2)

## Learning Objectives

By the end of this module, you will be able to:
- Understand the architecture and components of ROS 2
- Create and manage ROS 2 nodes, topics, and services
- Implement communication patterns for robotic systems
- Use rclpy for Python-based robot control

## Introduction to ROS 2

Robot Operating System 2 (ROS 2) provides the framework for building robotic applications. Unlike traditional operating systems, ROS 2 is a collection of tools, libraries, and conventions that aim to simplify the task of creating complex and robust robot behavior across a wide variety of robot platforms.

### Key Concepts

- **Nodes**: Processes that perform computation
- **Topics**: Named buses over which nodes exchange messages
- **Services**: Synchronous request/response communication
- **Actions**: Asynchronous communication with feedback and goal preemption

## ROS 2 Architecture

ROS 2 uses a DDS (Data Distribution Service) implementation for communication between nodes. This provides:

- Real-time performance
- Scalability
- Device interoperability
- Security features

### DDS Implementations

Popular DDS implementations include:
- Fast DDS (default in ROS 2)
- Cyclone DDS
- RTI Connext DDS

## Creating Your First ROS 2 Node

Let's create a simple publisher node that publishes sensor data:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class SensorPublisher(Node):
    def __init__(self):
        super().__init__('sensor_publisher')
        self.publisher_ = self.create_publisher(String, 'sensor_data', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Sensor reading: {self.i}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    sensor_publisher = SensorPublisher()
    rclpy.spin(sensor_publisher)
    sensor_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Topics and Services

### Topics

Topics enable asynchronous communication between nodes using a publish/subscribe model:

- Publishers send messages to topics
- Subscribers receive messages from topics
- Multiple publishers and subscribers can use the same topic
- Communication is loosely coupled

### Services

Services provide synchronous request/response communication:

- One client sends a request
- One server processes the request and sends a response
- Communication is tightly coupled
- Useful for operations that require a response

## Practical Exercise: ROS 2 Navigation

Create a simple navigation system that:
1. Publishes sensor data
2. Subscribes to sensor data
3. Processes the data to make navigation decisions
4. Publishes movement commands

## References

[1] ROS 2 Documentation. (2023). Retrieved from https://docs.ros.org/en/rolling/
[2] Lütkebohle, I., et al. (2022). ROS 2: Towards a Standardized Middleware for Robotics. IEEE Robotics & Automation Magazine.