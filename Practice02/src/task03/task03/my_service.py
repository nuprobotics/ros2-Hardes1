import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger


class MyService(Node):
    def __init__(self):
        super().__init__('my_service')
        self.declare_parameter('service_name', '/trigger_service')
        self.declare_parameter('default_string', 'No service available')

        self.service_name = self.get_parameter('service_name').get_parameter_value().string_value
        self.service_response = self.get_parameter('default_string').get_parameter_value().string_value
        self.stored_value = self.service_response

        self.client = self.create_client(Trigger, '/spgc/trigger')
        self.service = self.create_service(Trigger, self.service_name, self.service_callback)

        if not self.client.wait_for_service(timeout_sec=5.0):
            return

        request = Trigger.Request()
        future = self.client.call_async(request)
        future.add_done_callback(self.handle_trigger_response)

    def handle_trigger_response(self, future):
        try:
            response = future.result()
            if response.success:
                self.stored_value = response.message
        except Exception as e:
            self.get_logger().info(f'Response was unsuccessful {e}')

    def service_callback(self, _, response):
        response.success = True
        response.message = self.stored_value
        return response


def main(args=None):
    rclpy.init(args=args)
    node = MyService()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
