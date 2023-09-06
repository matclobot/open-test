import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import String, UInt16
import time

class NodeB(Node):
    def __init__(self):
        super().__init__('NodeB')
        qos_profile = QoSProfile(depth=10)
        self.NodeB_sub = self.create_subscription(UInt16, 'send', self.data_sub, qos_profile)
        self.NodeB_pub = self.create_publisher(String, 'Receive', qos_profile)


    def data_sub(self,msg):
        msg_data = String()
        msg_data_int = UInt16()
        msg_data_int.data = msg.data

        if msg_data_int.data == 1:
            msg_data.data = 'OK'

        elif msg_data_int.data == 2:
            msg_data.data = 'NG'

        time.sleep(1)
        self.NodeB_pub.publish(msg_data)
        self.get_logger().info('Send msg: {0}'.format(msg_data.data))


def main(args = None):
    rclpy.init(args=args)
    node = NodeB()
    try:
        rclpy.spin(node)
    except:
        node.get_logger().info('keyboard Interrupt (SIGIT)')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()