import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Publisher(Node):
    def __init__(self):
        super().__init__('task02')
        self.get_logger().info("publisher started")

        self.declare_parameter('text', 'Hello, ROS2!')
        self.declare_parameter('topic_name', None)

        # Get parameters
        text = self.get_parameter('text').get_parameter_value().string_value
        self.get_logger().info(f'text is {text}')
        topic_name = self.get_parameter('topic_name').get_parameter_value().string_value
        self.get_logger().info(f'topic name is {topic_name}')

        self.publisher_ = self.create_publisher(String, topic_name, 10)

        # Set a timer to publish the message periodically
        self.timer = self.create_timer(1.0, self.publish_message)

        # Store the message to publish
        self.message = String()
        self.message.data = text

    def publish_message(self):
        self.publisher_.publish(self.message)


def main(args=None):
    rclpy.init(args=args)
    node = Publisher()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()