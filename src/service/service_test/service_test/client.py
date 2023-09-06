import sys
from service_pkg.srv import Test
from example_interfaces.srv import AddTwoInts
import rclpy
from rclpy.node import Node
import random


class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(Test, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = Test.Request()

    def client_send(self):
        self.req.robot_number = float(random.randrange(1,4))
        self.req.scout_number = float(random.randrange(5,10))
        self.future = self.cli.call_async(self.req)





def main(args=None):
    rclpy.init(args=args)

    minimal_client = MinimalClientAsync()
    minimal_client.client_send()

    rclpy.spin_once(minimal_client)
    print(minimal_client.future.done())
    if minimal_client.future.done():
        
        try:
            response = minimal_client.future.result()
        except Exception as e:
            minimal_client.get_logger().info(
                'Service call failed %r' % (e,))
        else:
            minimal_client.get_logger().info(
                'Result of add_two_ints: for %f + %f = %f' %
                (minimal_client.req.robot_number, minimal_client.req.scout_number, response.sum))

    minimal_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()