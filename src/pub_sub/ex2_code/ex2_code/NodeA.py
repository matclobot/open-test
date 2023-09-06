import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import String

class NodeA(Node):
    def __init__(self):
        super().__init__('NodeA')
        qos_profile = QoSProfile(depth=10)
        self.pub = self.create_publisher(String, 'Pub_A',qos_profile)
        self.timer = self.create_timer(0.5,self.pub_timer)
        self.count = 0
    
    def pub_timer(self):
        msg = String()
        msg.data = 'NodeA respond: {0}'.format(self.count)
        self.pub.publish(msg)
        self.get_logger().info('Pub msg: {0}'.format(msg.data))
        self.count += 1

def main(args=None):
    rclpy.init(args=args)
    node = NodeA()
    try:
        rclpy.spin(node)
    except:
        node.get_looger().info('Keyboard Interrupt (SIGINT)')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
    