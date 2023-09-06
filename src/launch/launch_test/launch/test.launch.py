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
    pub_node = Node(
        package="launch_test", #package name
        executable="pub_node", #node name
        name="pub_node",       #display name
    )
    ld.add_action(pub_node)    #node name
    return ld
    
    #node 2
    sub_node = Node(
        package="launch_test", #package name
        executable="sub_node", #node name
        name="sub_node",       #display name
    )
    ld.add_action(sub_node)    #node name 
    return ld