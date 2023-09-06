import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import String

class NodeB(Node):
    def __init__(self):
        
        super().__init__('NodeB')
        qos_profile = QoSProfile(depth=10)
        self.sub = self.create_subscription(String, 'Pub_A', self.sub_topic, qos_profile)
        self.pub_pubB = self.create_publisher(String,'Pub_B',qos_profile)

    def sub_topic(self,msg):
        pub_msg = String()
        pub_msg.data = msg.data
        self.pub_pubB.publish(pub_msg)
        self.get_logger().info('receive/Send msg: {0}'.format(msg.data))

def main(args=None):
    rclpy.init(args=args)
    node = NodeB()
    try:
        rclpy.spin(node)
    except:
        node.get_looger().info('Keyboard Interrupt (SIGINT)')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
    