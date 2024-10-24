import os
from math import trunc

from rclpy.node import Node
import rclpy
from sensor_msgs.msg import CompressedImage
from std_srvs.srv import Trigger


class ImageReceiver(Node):
    def __init__(self):
        super().__init__('image_receiver')
        self.declare_parameter('topic_name', 'unknown_topic')

        self.topic_name_parameter = self.get_parameter("topic_name").get_parameter_value().string_value
        self.subscription = self.create_subscription(
            CompressedImage,
            self.topic_name_parameter,
            self.image_save_callback,
            10)

        self.output_path = 'folder_with_images'

        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        self.image_counter = 0
        self.stop_saving = False

        self.service = self.create_service(
            Trigger,
            '/hardes1/stop',
            self.service_callback
        )

    def image_save_callback(self, msg):
        if not self.stop_saving:
            image_path = os.path.join(self.output_path, f'image_{self.image_counter}.jpg')
            try:
                with open(image_path, 'wb') as f:
                    f.write(msg.data)
                self.get_logger().info(f'Image {self.image_counter} saved to {image_path}')
                self.image_counter += 1
            except Exception as e:
                self.get_logger().info("saving failed")

    def service_callback(self, _, response):
        self.stop_saving = True
        self.get_logger().info("Image saving has been stopped.")
        response.success = True
        response.message = ''
        return response


def main(args=None):
    rclpy.init(args=args)
    node = ImageReceiver()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
