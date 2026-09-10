""" Investigate receiving a message using a callback function """
import numpy as np

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist, Vector3
class DistanceEmergencyStopNode(Node):
    """This is a message subscription node, which inherits from the rclpy Node class."""
    def __init__(self):
        """Initializes the EmergencyStopNode. No inputs."""
        super().__init__('distance_emergency_stop_node')
        self.bump_sub = self.create_subscription(LaserScan, 'stable_scan', self.handle_scan_data, 10)
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.vel_loop)
        self.current_speed = Twist(linear=Vector3(x=0.2, y=0.0, z=0.0), angular=Vector3(x=0.0, y=0.0, z=0.0))
        print("Distance mergency stop node initted")

    def vel_loop(self):
        self.cmd_vel_pub.publish(self.current_speed)

    ESTOP_DIST_THRESHOLD_M = 0.4
    def handle_scan_data(self, msg: LaserScan):
        range_violations = np.array(msg.ranges) < self.ESTOP_DIST_THRESHOLD_M # numpy clerverness - should be an 361-element array of bools
        # print(msg.ranges[0:5])
        # print(range_violations[0:5])
        if np.any(range_violations[0:30]) or np.any(range_violations[330:359]):
            self.current_speed = Twist(linear=Vector3(x=0.0, y=0.0, z=0.0), angular=Vector3(x=0.0, y=0.0, z=0.0))
            print(f"Stopping due to range violations at angles {np.flatnonzero(range_violations)}")
        else:
            self.current_speed = Twist(linear=Vector3(x=0.2, y=0.0, z=0.0), angular=Vector3(x=0.0, y=0.0, z=0.0))

def main(args=None):
    """Initializes a node, runs it, and cleans up after termination.
    Input: args(list) -- list of arguments to pass into rclpy. Default None.
    """
    rclpy.init(args=args)         # Initialize communication with ROS
    node = DistanceEmergencyStopNode()   # Create our Node
    rclpy.spin(node)              # Run the Node until ready to shutdown
    rclpy.shutdown()              # cleanup

if __name__ == '__main__':
    main()
