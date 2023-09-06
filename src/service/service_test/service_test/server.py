from example_interfaces.srv import AddTwoInts
from service_pkg.srv import Test
import rclpy
from rclpy.node import Node


class MinimalService(Node):

    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(Test, 'add_two_ints', self.add_two_ints_callback)

    def add_two_ints_callback(self, request, response):
        response.sum= float(request.robot_number + request.scout_number)
        self.get_logger().info('Incoming request\na: %f b: %f' % (request.robot_number, request.scout_number))

        return response


def main(args=None):
    rclpy.init(args=args)

    minimal_service = MinimalService()

    rclpy.spin(minimal_service)

    rclpy.shutdown()


if __name__ == '__main__':
    main()