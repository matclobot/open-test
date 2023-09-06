import yaml
from random import *
import rclpy
import os
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import String,Float32
from yami_msg.msg import Yamidata,Poirequest
from geometry_msgs.msg import Pose


class yaml_File(Node):

    def __init__(self):
        super().__init__('yaml_File')
        qos_profile = QoSProfile(depth=10)
        self.yaml_File_pub = self.create_publisher(Pose, 'yaml_Test', qos_profile)
        self.create_subscription(Poirequest, '/poi_request', self.on_sub_poi_request,qos_profile=qos_profile)
        #self.timer = self.create_timer(1, self.publish_yaml_msg)
        self.count = 0

        self._command_mapping = { '0' : self.create_poi,
                          '1' : self.read_poi,
                          '2' : self.update_poi,
                          '3' : self.delete_poi,
                          '4' : self.clear_poi,
                          '5' : self.create_default_poi
                        }
    
    def on_sub_poi_request(self, msg):
        self.choice_map(msg.mapname)
        command = msg.command
        poi_number = msg.number
        self._command_mapping[command](poi_number)

    def choice_map(self, map_name):
        #self.HOME_ROBOT_POI_INFO,
        try :
            self._map_file = os.path.join(map_name + '_poi.yaml')
        except : 
            f = open(self._map_file, "w")
            f.close()
            #log_msg = LogMsg()
            #log_msg.level     = 40 
            #log_msg.node_name = 'poi_manager'
            #log_msg.message   = 'cant read ' + str(map_name) + '_poi_yaml' 
            #self._log_pub.publish(log_msg)

    def create_poi(self, poi_number:str):
        poi_coordinate = self.read_yaml()
        pose   = {'position'   : {'x': random(), 
                                  'y': random(), 
                                  'z': random()},
                  'orientation': {'x': random(), 
                                  'y': random(), 
                                  'z': random(), 
                                  'w': random() },
                  'manipulator': {'x': random(),
                                  'y': random(),
                                  'z': random() }
        }
        poi_coordinate['POI'][poi_number] = pose

        self.dump_yaml(poi_coordinate)
        print ("create_OK")

    def create_default_poi(self, poi_number:str):
        print('######')
        info = {'POI': {}}
        self.dump_yaml(info)
        print('22')

        poi_coordinate = self.read_yaml()
        pose   = {'position'   : {'x': 0.0, 
                                  'y': 0.0, 
                                  'z': 0.0 },
                  'orientation': {'x': 0.0, 
                                  'y': 0.0, 
                                  'z': 0.0, 
                                  'w': 1.0 },
                  'manipulator': {'x': 0.0,
                                  'y': 0.0,
                                  'z': 0.0 }
        }

        poi_coordinate['POI']['Docking'] = pose
        self.dump_yaml(poi_coordinate)
        print('44')

        pose   = {'position'   : {'x': 0.5, 
                                  'y': 0.0, 
                                  'z': 0.0 },
                  'orientation': {'x': 0.0, 
                                  'y': 0.0, 
                                  'z': 0.0, 
                                  'w': 1.0 },
                  'manipulator': {'x': 0.0,
                                  'y': 0.0,
                                  'z': 0.0 }
        }
        
        poi_coordinate['POI']['Docking'] = pose
        self.dump_yaml(poi_coordinate)
        print('55')
        print ("default_create_OK")


    def update_poi(self, poi_number:str):

        poi_coordinate = self.read_yaml()
        if poi_coordinate['POI'].get(poi_number, None) is None :
            return 

        pose   = {'position'   : {'x': random(), 
                                  'y': random(), 
                                  'z': random()},
                  'orientation': {'x': random(), 
                                  'y': random(), 
                                  'z': random(), 
                                  'w': random() },
                  'manipulator': {'x': random(),
                                  'y': random(),
                                  'z': random() }
        }

        poi_coordinate['POI'][poi_number] =  pose
        self.dump_yaml(poi_coordinate)
        print ("Update_OK")

    def delete_poi(self, poi_number:str):
        poi_coordinate = self.read_yaml()
        if poi_coordinate['POI'].get(poi_number, None) is None :
            return 
        poi_coordinate['POI'].pop(poi_number)
        self.dump_yaml(poi_coordinate)
        print ("delete_OK")

    def clear_poi(self, poi_number:str):
        poi_coordinate = self.read_yaml()
        poi_coordinate['POI'].clear()
        self.dump_yaml(poi_coordinate)
        print ("clear_OK")

    def dump_yaml(self, info:dict):
        # self._overwrite_parameters(info)  
        #print(self._map_file)
        with open(self._map_file, 'w') as f:
            yaml.dump(info, f)

    def read_yaml(self):
        with open(self._map_file) as f:
            robot_info = yaml.full_load(f)
        if robot_info is None : 
            robot_info = {'POI': {}}
            return robot_info
        else : 
            return robot_info
        
        
    def read_poi(self, poi_number:str):
        pose_msg = Pose()
        poi_coordinate = self.read_yaml()
        pose_msg.position.x = poi_coordinate['POI'][poi_number]['position']['x']
        pose_msg.position.y = poi_coordinate['POI'][poi_number]['position']['y']
        pose_msg.position.z = poi_coordinate['POI'][poi_number]['position']['z']
        pose_msg.orientation.x = poi_coordinate['POI'][poi_number]['orientation']['x']
        pose_msg.orientation.y = poi_coordinate['POI'][poi_number]['orientation']['y']
        pose_msg.orientation.z = poi_coordinate['POI'][poi_number]['orientation']['z']
        pose_msg.orientation.w = poi_coordinate['POI'][poi_number]['orientation']['w']
        print(pose_msg)
        self.yaml_File_pub.publish(pose_msg)
        #print (data)
        print ("read_OK")


    #def publish_yaml_msg(self):
    #    msg = Yamidata()
    #    self.yaml_Write()
    #    self.yaml_Read()
    #    msg = self.yaml_data()
    #    #print (type(msg))
#
    #    #self.msg.data = 'yaml_File: {0}'.format(str(msg))
    #    
#
    #def yaml_Write(self):
    #    ori_data_w = random()
    #    ori_data_x = random()
    #    ori_data_y = random()
    #    ori_data_z = random()
    #    pos_data_w = random()
    #    pos_data_x = random()
    #    pos_data_y = random()
    #    pos_data_z = random()
    #    self.pos_number = randint(0,5)
#
    #    data = {'POI':{str(self.pos_number):{'orientation':{'w':ori_data_w,'x':ori_data_x,'y':ori_data_y,'z':ori_data_z},'position':{'w':pos_data_w,'x':pos_data_x,'y':pos_data_y,'z':pos_data_z}}}}
    #    
    #    with open('1675752859695TVb_poi.yaml', 'w') as file:
    #       yaml.dump(data, file, default_flow_style=False)
#
#
    #def yaml_Read(self):
    #    with open('1675752859695TVb_poi.yaml')as f:
    #        self.data = yaml.load(f)
    #                # 데이터 확인
    #    #print(self.data)
#
#
    #def yaml_data(self):
    #    Yami_data = Yamidata()
    #    #test = self.data['POI'][str(self.pos_number)]['orientation']['w']
    #    Yami_data.poi_number = str(self.pos_number)
    #    Yami_data.ori_w = str(self.data['POI'][str(self.pos_number)]['orientation']['w'])
    #    Yami_data.ori_x = str(self.data['POI'][str(self.pos_number)]['orientation']['x'])
    #    Yami_data.ori_y = str(self.data['POI'][str(self.pos_number)]['orientation']['y'])
    #    Yami_data.ori_z = str(self.data['POI'][str(self.pos_number)]['orientation']['z'])
    #    Yami_data.pos_w = str(self.data['POI'][str(self.pos_number)]['position']['w'])
    #    Yami_data.pos_x = str(self.data['POI'][str(self.pos_number)]['position']['x'])
    #    Yami_data.pos_y = str(self.data['POI'][str(self.pos_number)]['position']['y'])
    #    Yami_data.pos_z = str(self.data['POI'][str(self.pos_number)]['position']['z'])
    #    print (Yami_data)
    #    self.yaml_File_pub.publish(Yami_data)
    #    return Yami_data



def main(args=None):
    rclpy.init(args=args)
    node = yaml_File()    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard Interrupt (SIGINT)')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

