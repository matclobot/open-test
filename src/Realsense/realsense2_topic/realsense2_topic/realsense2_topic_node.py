import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import String
from sensor_msgs.msg import Image, CameraInfo
import time



class HelloworldSubscriber(Node):
   
    def __init__(self):
        
        super().__init__('hello_sub')
        qos_profile = QoSProfile(depth=10)
        #self._bridge = CvBridge()
        #self.pipline = pipeline()
        #self.pc = PointCloud2()

        self.color_info = self.create_subscription(CameraInfo,'/camera/color/camera_info',self.color_camera_info,qos_profile)
        self.color_image = self.create_subscription(Image,'/camera/color/image_rect_raw',self.color_camera_image,qos_profile)
        self.depth_info = self.create_subscription(CameraInfo,'/camera/depth/camera_info',self.depth_camera_info,qos_profile)
        self.depth_image = self.create_subscription(Image,'/camera/depth/image_rect_raw',self.depth_camera_image,qos_profile)


        #self.fov_vertical_rad = math.radians(79.5)
        #self.fov_horizontal_rad = math.radians(127.2)
    def color_camera_info(self,msg):
        time.sleep(1)
        #print(msg)

    def color_camera_image(self,msg):
        time.sleep(1)
        #print("color image : ",msg)

    def depth_camera_image(self, msg):
        #cv2_img = CvBridge.imgmsg_to_cv2(msg,"bgr8")   
        time.sleep(1)
        #depth_image = np.array(msg.data, dtype=np.float32).reshape((848, 480))
        #depth_value = depth_image[848/2,480/2]
        
        
        #print("depth image : ",msg)
        
        
        #self.depth_image_width = msg.width
        #self.depth_image_height = msg.height
        #print(PointCloud2)
        #center_x = self.depth_image_width/2
        #center_y = self.depth_image_height/2
                    
        #depth_image = self._bridge.imgmsg_to_cv2(msg, "passthrough")
        #depth_array = np.array(depth_image, dtype=np.float32)

        #spatial_x = depth_array[center_x, center_y]

        #spatial_width = 2.0 * spatial_x * math.tan(self.fov_horizontal_rad * 0.5)
        #spatial_height = 2.0 * spatial_x * math.tan(self.fov_vertical_rad * 0.5)

        #spatial_y = -1.0 * spatial_width * (center_x - self.depth_image_width / 2) / self.depth_image_width 
        #spatial_z = -1.0 * spatial_height * (center_y - self.depth_image_height /2) / self.depth_image_height

        #center_coordinate = [center_x, center_y]

        #print("center_coordinate")
        #print(center_coordinate)
#
        #print("x : " + str(spatial_x))
        #print("y : " + str(spatial_y))
        #print("z : " + str(spatial_z))            


    def depth_camera_info(self, msg):
        time.sleep(1)
        
        camera_width = msg.width
        camera_height = msg.height
        print(msg.width, msg.height)

def main(args=None):
    rclpy.init(args=args)
    node = HelloworldSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard Interrupt (SIGINT)')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()