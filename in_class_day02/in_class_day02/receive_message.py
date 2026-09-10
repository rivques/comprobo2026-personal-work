""" Investigate receiving a message using a callback function """
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PointStamped

class ReceiveMessageNode(Node):
    """This is a message subscription node, which inherits from the rclpy Node class."""
    def __init__(self):
        """Initializes the ReceiveMessageNode. No inputs."""
        super().__init__('receive_message_node')
        self.sub = self.create_subscription(PointStamped, 'my_point', self.process_point, 10)

    def process_point(self, msg: PointStamped):
        print(msg.header)

def main(args=None):
    """Initializes a node, runs it, and cleans up after termination.
    Input: args(list) -- list of arguments to pass into rclpy. Default None.
    """
    rclpy.init(args=args)         # Initialize communication with ROS
    node = ReceiveMessageNode()   # Create our Node
    rclpy.spin(node)              # Run the Node until ready to shutdown
    rclpy.shutdown()              # cleanup

if __name__ == '__main__':
    main()
