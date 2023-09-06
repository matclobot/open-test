import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import String, UInt16
import time
#global check
class NodeA(Node):

    def __init__(self):
        super().__init__('NodeA')
        qos_profile = QoSProfile(depth=10)
        self.NodeA_sub = self.create_subscription(String,'Receive',self.data_sub,qos_profile)
        self.NodeA_pub = self.create_publisher(UInt16,'send',qos_profile)

        data_msg_int = UInt16()
        data_msg_int.data = 1
        self.NodeA_pub.publish(data_msg_int)

        

    def data_sub(self,msg):
        data_msg = String()
        data_msg_int = UInt16()
        data_msg.data = msg.data
        
        if msg.data == 'OK':
            data_msg_int.data = 2
            
        elif msg.data == 'NG':
            data_msg_int.data = 1

        time.sleep(1)
        self.get_logger().info('Send msg: {0}'.format(data_msg_int.data))
        self.NodeA_pub.publish(data_msg_int)




def main(args = None):
    rclpy.init(args=args)
    node = NodeA()
    try:
        rclpy.spin(node)
    except:
        node.get_logger().info('keyboard Interrupt (SIGIT)')
    finally:
        node.destroy_node()
        rclpy.shutdown()
        
if __name__ == '__main__':
    main()
