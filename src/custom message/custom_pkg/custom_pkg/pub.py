import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import String
from my_msgs.msg import BboxMsg

class HelloworldPublisher(Node):

    def __init__(self):
        super().__init__('hello_pub')
        qos_profile = QoSProfile(depth=10)
        self.hello_pub = self.create_publisher(BboxMsg, 'hi', qos_profile)
        self.timer = self.create_timer(1, self.publish_helloworld_msg)
        self.count = 0

    def publish_helloworld_msg(self):
        msg = BboxMsg()
        msg.index = 1
        msg.cls = 1
        msg.minx = 1
        msg.maxy = 1
        #msg.data = 'Hello World: {0}'.format(self.count)
        self.hello_pub.publish(msg)
        #self.get_logger().info('published message: {0}'.format(msg.data))
        self.count += 1


def main(args=None):
    rclpy.init(args=args)
    node = HelloworldPublisher()    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard Interrupt (SIGINT)')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()