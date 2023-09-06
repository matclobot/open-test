import rclpy
import cv2
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import String
from sensor_msgs.msg import Image, CameraInfo
import pyrealsense2 as rs
from cv_bridge import CvBridge
#from rectangle_msg.msg import Rectangle
#import realsense2_camera_msgs as ,pipeline
import numpy as np
import time
import math
import geometry_msgs



class HelloworldSubscriber(Node):
   
    def __init__(self):
        
        super().__init__('hello_sub')
        qos_profile = QoSProfile(depth=10)
        self._bridge = CvBridge()
        #self.color_info = self.create_subscription(CameraInfo,'/camera/color/camera_info',self.color_camera_info,qos_profile)
        self.color_image = self.create_subscription(Image,'/camera/color/image_raw',self.color_camera_image,qos_profile)
        self.rectangle_data_pub = self.create_publisher(String,'/object_depth',qos_profile)
        self.depth_info = self.create_subscription(CameraInfo,'/camera/depth/camera_info',self.depth_camera_info,qos_profile)
        self.depth_image = self.create_subscription(Image,'/camera/depth/image_rect_raw',self.depth_camera_image,qos_profile)
        #self.rectangle_data = self.create_subscription(Rectangle,'/object_point',self.Point_AreaCallback,qos_profile)
        
        self.point_x = int(0)
        self.point_y = int(0)
        self.Rectangle_point = (100,160,100,160)
        self.Camera_Flag = False
        self.fov_vertical_rad = math.radians(79.5)
        self.fov_horizontal_rad = math.radians(127.2)

    def Point_AreaCallback(self,msg):
        
        self.Camera_Flag = True
       
    def depth_camera_image(self, msg):
        data_pub = String()

        #if self.Camera_Flag:
            
        self.depth_image_width =  self.camera_width
        self.depth_image_height = self.camera_height
        print(self.Rectangle_point)
        print("image size : ",self.depth_image_width,self.depth_image_height)
        center_x = int(self.Rectangle_point[0]+self.Rectangle_point[1])
        center_y = int(self.Rectangle_point[2]+self.Rectangle_point[3])
        self.point_x = center_x
        self.point_y = center_y
        print("center x : ", center_x)
        print("center y : ", center_y)
        depth_image = self._bridge.imgmsg_to_cv2(msg, "passthrough")
        depth_array = np.array(depth_image, dtype=np.float32)

        spatial_x = depth_array[center_x, center_y]
        
        spatial_width = 2.0 * spatial_x * math.tan(self.fov_horizontal_rad * 0.5)
        spatial_height = 2.0 * spatial_x * math.tan(self.fov_vertical_rad * 0.5)
        print("spatial_width : ",spatial_width)
        print("spatial_height : ",spatial_height)
        spatial_y = -1.0 * spatial_width * (center_x - self.depth_image_width / 2) / self.depth_image_width 
        spatial_z = -1.0 * spatial_height * (center_y - self.depth_image_height /2) / self.depth_image_height
        
        convert = np.array2string(spatial_x)
    
        print("x : " + str(spatial_x))
        print("y : " + str(spatial_y))
        print("z : " + str(spatial_z))
        data_pub.data = str(convert)
        print(type(data_pub),data_pub.data)
        self.rectangle_data_pub.publish(data_pub)
        self.Camera_Flag = False

           

    def color_camera_image(self, msg):
        
        #if self.Camera_Flag:
        image = self._bridge.imgmsg_to_cv2(msg,'bgr8')
        cv2.line(image,(self.point_x,self.point_x),(self.point_y,self.point_y),150,5)
        if image is None:
            print('image None')
        else:
            #OpenCV image color RGB -> BGR
            src_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            bgrLower = np.array([0,204,204])
            bgrUpper = np.array([210,255,255])
            bgrResult = self.bgrExtraction(image, bgrLower, bgrUpper)

            cv2.imshow('img_mask',bgrResult)
            #cv2.imshow('dst2',dst2)
            cv2.imshow('img',image)
            cv2.waitKey(33)

    def bgrExtraction(self,image,bgrLower,bgrUpper):
        img_mask = cv2.inRange(image, bgrLower,bgrUpper)
        result = cv2.bitwise_and(image, image, mask = img_mask)
        return result

    def depth_camera_info(self, msg):
        
        self.camera_width = msg.width
        self.camera_height = msg.height

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