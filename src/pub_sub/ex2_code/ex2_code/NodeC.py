import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import String

class NodeC(Node):
    def __init__(self):
        super().__init__('NodeC')
        qos_profile = QoSProfile(depth=10)
        self.sub = self.create_subscription(String, 'Pub_B',self.sub_topic,qos_profile)
    def sub_topic(self,msg):
        sub_msg = String()
        sub_msg.data = msg.data 
        self.get_logger().info('Pub msg: {0}'.format(sub_msg.data))

def main(args=None):
    rclpy.init(args=args)
    node = NodeC()
    try:
        rclpy.spin(node)
    except:
        node.get_looger().info('Keyboard Interrupt (SIGINT)')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
    