import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch.actions import ExecuteProcess, IncludeLaunchDescription, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.conditions import IfCondition, UnlessCondition
import xacro
import yaml
import tempfile
import time

# LOAD FILE:
def load_file(package_name, file_path):
    package_path = get_package_share_directory(package_name)
    absolute_file_path = os.path.join(package_path, file_path)
    try:
        with open(absolute_file_path, 'r') as file:
            return file.read()
    except EnvironmentError:
        # parent of IOError, OSError *and* WindowsError where available.
        return None

# LOAD YAML:
def load_yaml(package_name, file_path):
    package_path = get_package_share_directory(package_name)
    absolute_file_path = os.path.join(package_path, file_path)
    try:
        with open(absolute_file_path, 'r') as file:
            return yaml.safe_load(file)
    except EnvironmentError:
        # parent of IOError, OSError *and* WindowsError where available.
        return None
    
# ========== **GENERATE LAUNCH DESCRIPTION** ========== #
def generate_launch_description():
    
    # ***** GAZEBO ***** #   
    # DECLARE Gazebo WORLD file:
    conveyorbelt_gazebo = os.path.join(
        get_package_share_directory('conveyorbelt_gazebo'),
        'worlds',
        'conveyorbelt.world')
    # DECLARE Gazebo LAUNCH file:
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch'), '/gazebo.launch.py']),
                launch_arguments={'world': conveyorbelt_gazebo}.items(),
             )

    
    # #*****ADDING UR ROBOTS*****#
    # # UR Robot Configuration
    # ur_type = "ur10e"
    # safety_limits = "true"
    # safety_pos_margin = "0.15"
    # safety_k_position = "20"
    # # description_package = "ur_description"
    # description_package = "conveyorbelt_gazebo"
    # description_file = "ur.urdf.xacro"
    # tf_prefix = '""'
    # sim_gazebo = "true"
    # start_joint_controller = "true"
    
    # controllers_config_right = ""
    # controllers_config_left = ""
    

    # # Robot Description Generation
    # def generate_robot_description(robot_name, tf_prefix, controllers_config, namespace):
    #     return Command(
    #     [
    #         PathJoinSubstitution([FindExecutable(name="xacro")]),
    #         " ",
    #         PathJoinSubstitution([FindPackageShare(description_package), "urdf", description_file]),
    #         " ",
    #         "safety_limits:=", safety_limits,
    #         " ",
    #         "safety_pos_margin:=", safety_pos_margin,
    #         " ",
    #         "safety_k_position:=", safety_k_position,
    #         " ",
    #         "name:=", robot_name,
    #         " ",
    #         "ur_type:=", ur_type,
    #         " ",
    #         "tf_prefix:=", tf_prefix,
    #         " ",
    #         "sim_gazebo:=", sim_gazebo,
    #         " ",
    #         "simulation_controllers:=", controllers_config,
    #         " ",
    #         "namespace:=", namespace,
    #         " ",
    #         "start_joint_controller:=", "true",
            
    #     ]
    # )
    
    # robot_description_content_left = generate_robot_description("ur10e_left", "left", controllers_config_left, "ur10e_left")
    # robot_description_content_right = generate_robot_description("ur10e_right", "right", controllers_config_right, "ur10e_right")
    
    # robot_description_left = {"robot_description": robot_description_content_left}
    # robot_description_right = {"robot_description": robot_description_content_right}
    
    
    # robot_state_publisher_node_ur10e_left = Node(
    #     package="robot_state_publisher",
    #     executable="robot_state_publisher",
    #     name='robot_state_publisher',
    #     # name='robot_state_publisher_ur10e_left',
    #     namespace='ur10e_left',
    #     output="both",
    #     parameters=[robot_description_left],
    # )
    
    # robot_state_publisher_node_ur10e_right = Node(
    #     package="robot_state_publisher",
    #     executable="robot_state_publisher",
    #     name='robot_state_publisher',
    #     # name='robot_state_publisher_ur10e_right',
    #     namespace='ur10e_right',
    #     output="both",
    #     parameters=[robot_description_right],
    # )
    
    # # Nodes
    # # joint_state_publisher_node_ur10e_left = Node(
    # #     package="joint_state_publisher",
    # #     executable="joint_state_publisher",
    # #     name='joint_state_publisher',
    # #     # name='joint_state_publisher_ur10e_left',
    # #     namespace='ur10e_left'
    # # )
    
    # # joint_state_publisher_node_ur10e_right = Node(
    # #     package="joint_state_publisher",
    # #     executable="joint_state_publisher",
    # #     name='joint_state_publisher',
    # #     # name='joint_state_publisher_ur10e_right',
    # #     namespace='ur10e_right'
    # # )
    
    # joint_state_broadcaster_spawner_left = Node(
    #     package="controller_manager",
    #     executable="spawner",
    #     namespace='ur10e_left',
    #     arguments=["joint_state_broadcaster", "--controller-manager", "/ur10e_left/controller_manager"],
    # )
    
    # joint_state_broadcaster_spawner_right = Node(
    #     package="controller_manager",
    #     executable="spawner",
    #     namespace='ur10e_right',
    #     arguments=["joint_state_broadcaster", "--controller-manager", "/ur10e_right/controller_manager"],
    # )

    # # Spawn robot with a unique name to avoid "already exists" error
    # spawn_robot_left = Node(
    #     package="gazebo_ros",
    #     executable="spawn_entity.py",
    #     arguments=[
    #         "-entity", "ur10e_left",  # Changed entity name
    #         "-topic", "/ur10e_left/robot_description",  # Use robot_description topic instead of file
    #         "-x", "-0.5",
    #         "-y", "0.25",
    #         "-z", "0.741",
    #         "-Y", "0.0",
    #     ],
    #     output="screen",
    # )
    
    # spawn_robot_right = Node(
    #     package="gazebo_ros",
    #     executable="spawn_entity.py",
    #     arguments=[
    #         "-entity", "ur10e_right",  # Changed entity name
    #         "-topic", "/ur10e_right/robot_description",  # Use robot_description topic instead of file
    #         # "-topic", "/robot_description",  # Use robot_description topic instead of file
    #         "-x", "0.5",
    #         "-y", "0.25",
    #         "-z", "0.741",
    #         "-Y", "0.0",
    #     ],
    #     output="screen",
    # )


    # ***** RETURN LAUNCH DESCRIPTION ***** #
    return LaunchDescription([
        gazebo,
        # robot_state_publisher_node_ur10e_left,
        # robot_state_publisher_node_ur10e_right,
        # # joint_state_publisher_node_ur10e_left,
        # # joint_state_publisher_node_ur10e_right,
        # joint_state_broadcaster_spawner_left,
        # joint_state_broadcaster_spawner_right,
        # spawn_robot_left,
        # spawn_robot_right,        
    ])