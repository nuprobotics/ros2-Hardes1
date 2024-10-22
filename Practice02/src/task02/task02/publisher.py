import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Publisher(Node):
    def __init__(self):
        super().__init__('publisher')
        self.declare_parameter("topic_name", "")
        self.declare_parameter("text", "")

        self.topic_name_parameter = self.get_parameter("topic_name").get_parameter_value().string_value
        self.text_parameter = self.get_parameter("text").get_parameter_value().string_value


        self.publisher = self.create_publisher(String, self.topic_name_parameter, 1)
        self.timer = self.create_timer(1.0, self.publish_message)

    def publish_message(self):
        msg = String()
        msg.data = self.text_parameter
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = Publisher()
    rclpy.spin_once(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()