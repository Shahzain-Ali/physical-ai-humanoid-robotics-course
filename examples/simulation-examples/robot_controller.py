"""
Simple robot controller example for the Physical AI & Humanoid Robotics course.
This demonstrates basic robot control concepts that could be applied in simulation environments.
"""

import math
import time
from enum import Enum


class RobotState(Enum):
    """
    Possible states for the robot.
    """
    IDLE = "idle"
    MOVING = "moving"
    MANIPULATING = "manipulating"
    ERROR = "error"


class SimpleRobotController:
    """
    A simple robot controller that demonstrates basic control concepts.
    This could be adapted for use in Gazebo, Unity, or other simulation environments.
    """

    def __init__(self):
        self.state = RobotState.IDLE
        self.position = [0.0, 0.0, 0.0]  # x, y, z
        self.orientation = [0.0, 0.0, 0.0, 1.0]  # quaternion (x, y, z, w)
        self.joint_positions = [0.0] * 6  # 6 DOF for simple robot arm
        self.velocity = [0.0, 0.0, 0.0]
        self.is_simulated = True

    def move_to_position(self, target_position, speed=0.1):
        """
        Move the robot to a target position.
        """
        self.state = RobotState.MOVING
        print(f"Moving to position: {target_position} at speed {speed}")

        # Calculate distance to target
        dx = target_position[0] - self.position[0]
        dy = target_position[1] - self.position[1]
        dz = target_position[2] - self.position[2]
        distance = math.sqrt(dx*dx + dy*dy + dz*dz)

        # Simple linear interpolation
        steps = int(distance / speed) + 1
        for i in range(steps):
            progress = i / steps
            self.position[0] = self.position[0] + dx * progress
            self.position[1] = self.position[1] + dy * progress
            self.position[2] = self.position[2] + dz * progress

            # Update velocity
            self.velocity[0] = dx / steps if steps > 0 else 0
            self.velocity[1] = dy / steps if steps > 0 else 0
            self.velocity[2] = dz / steps if steps > 0 else 0

            # Simulate processing time
            if self.is_simulated:
                time.sleep(0.01)  # Short delay to simulate real-time processing

        print(f"Reached target position: {self.position}")
        self.state = RobotState.IDLE
        return True

    def rotate_to_orientation(self, target_orientation):
        """
        Rotate the robot to a target orientation.
        """
        print(f"Rotating to orientation: {target_orientation}")
        self.orientation = target_orientation
        return True

    def move_joint_to_position(self, joint_index, target_angle):
        """
        Move a specific joint to a target angle.
        """
        if 0 <= joint_index < len(self.joint_positions):
            print(f"Moving joint {joint_index} to angle {target_angle}")
            self.joint_positions[joint_index] = target_angle
            return True
        else:
            print(f"Invalid joint index: {joint_index}")
            return False

    def get_robot_state(self):
        """
        Get the current state of the robot.
        """
        return {
            "position": self.position,
            "orientation": self.orientation,
            "joint_positions": self.joint_positions,
            "velocity": self.velocity,
            "state": self.state.value
        }

    def execute_trajectory(self, waypoints):
        """
        Execute a trajectory defined by a series of waypoints.
        """
        print(f"Executing trajectory with {len(waypoints)} waypoints")
        for i, waypoint in enumerate(waypoints):
            print(f"Moving to waypoint {i+1}/{len(waypoints)}: {waypoint}")
            success = self.move_to_position(waypoint["position"])
            if "orientation" in waypoint:
                self.rotate_to_orientation(waypoint["orientation"])
            if not success:
                print(f"Failed to reach waypoint {i+1}")
                self.state = RobotState.ERROR
                return False

        print("Trajectory completed successfully")
        return True


def main():
    """
    Example usage of the robot controller.
    """
    controller = SimpleRobotController()

    # Print initial state
    print("Initial robot state:")
    print(controller.get_robot_state())

    # Move to a position
    controller.move_to_position([1.0, 0.5, 0.0])
    print(f"Current state after move: {controller.get_robot_state()}")

    # Execute a simple trajectory
    waypoints = [
        {"position": [1.0, 0.5, 0.0]},
        {"position": [1.5, 1.0, 0.2]},
        {"position": [2.0, 0.0, 0.1]},
    ]

    controller.execute_trajectory(waypoints)
    print(f"Final state: {controller.get_robot_state()}")


if __name__ == "__main__":
    main()