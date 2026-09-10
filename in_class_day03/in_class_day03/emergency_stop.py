""" Investigate receiving a message using a callback function """
import rclpy
from rclpy.node import Node
from neato2_interfaces.msg import Bump
from geometry_msgs.msg import Twist, Vector3
class EmergencyStopNode(Node):
    """This is a message subscription node, which inherits from the rclpy Node class."""
    def __init__(self):
        """Initializes the EmergencyStopNode. No inputs."""
        super().__init__('touch_emergency_stop_node')
        self.bump_sub = self.create_subscription(Bump, 'bump', self.handle_bump_data, 10)
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.vel_loop)
        self.current_speed = Twist(linear=Vector3(x=0.2, y=0.0, z=0.0), angular=Vector3(x=0.0, y=0.0, z=0.0))
        print("Emergency stop node initted")

    def vel_loop(self):
        self.cmd_vel_pub.publish(self.current_speed)

    def handle_bump_data(self, msg: Bump):
        if any([bump_sensor > 0 for bump_sensor in [msg.left_front, msg.left_side, msg.right_front, msg.right_side]]):
            self.current_speed = Twist(linear=Vector3(x=0.0, y=0.0, z=0.0), angular=Vector3(x=0.0, y=0.0, z=0.0))
        else:
            self.current_speed = Twist(linear=Vector3(x=0.2, y=0.0, z=0.0), angular=Vector3(x=0.0, y=0.0, z=0.0))

def main(args=None):
    """Initializes a node, runs it, and cleans up after termination.
    Input: args(list) -- list of arguments to pass into rclpy. Default None.
    """
    rclpy.init(args=args)         # Initialize communication with ROS
    node = EmergencyStopNode()   # Create our Node
    rclpy.spin(node)              # Run the Node until ready to shutdown
    rclpy.shutdown()              # cleanup

if __name__ == '__main__':
    main()
