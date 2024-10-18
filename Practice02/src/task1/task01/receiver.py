import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Receiver(Node):
    def __init__(self):
        super().__init__('receiver')
        self.a = -10
        self.subscription = self.create_subscription(
            String,
            '/spgc/sender',
            self.listener_callback, 1)

    def listener_callback(self, msg):
        self.get_logger().info('%s' % msg.data)

def main(args=None):
    rclpy.init(args=args)
    node = Receiver()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()