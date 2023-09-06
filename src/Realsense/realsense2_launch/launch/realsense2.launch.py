import launch.actions
import ament_index_python.packages

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import DeclareLaunchArgument

def generate_launch_description():
    
    ld =  LaunchDescription()
    #node 1
    realsense2_node = Node(
        package="realsense2_test", #package name
        executable="realsense2_node", #node name
        name="realsense2_node",       #display name
    )
    ld.add_action(realsense2_node)    #node name
    return ld    
    
    #node 2
    realsense2_msg_node = Node(
        package="realsense2_topic", #package name
        executable="realsense2_topic_node", #node name
        name="realsense2_topic_test",       #display name
    )
    ld.add_action(realsense2_msg_node)    #node name 
