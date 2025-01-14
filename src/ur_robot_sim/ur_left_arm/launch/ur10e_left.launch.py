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

    
# ========== **GENERATE LAUNCH DESCRIPTION** ========== #
def generate_launch_description():
    
    #*****ADDING UR ROBOTS*****#
    # UR Robot Configuration
    ur_type = "ur10e"
    safety_limits = "true"
    safety_pos_margin = "0.15"
    safety_k_position = "20"
    # description_package = "ur_description"
    description_package = "ur_left_arm"
    description_file = "ur_left.urdf.xacro"
    tf_prefix = '""'
    sim_gazebo = "true"
    start_joint_controller = "true"
    
    # controllers_config_right = ""
    controllers_config_left = "/home/autolug_ws/src/ur_robot_sim/ur_left_arm/config/ur10e_left_controllers.yaml"
    

    # Robot Description Generation
    def generate_robot_description(robot_name, tf_prefix, controllers_config, namespace):
        return Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution([FindPackageShare(description_package), "urdf", description_file]),
            " ",
            "safety_limits:=", safety_limits,
            " ",
            "safety_pos_margin:=", safety_pos_margin,
            " ",
            "safety_k_position:=", safety_k_position,
            " ",
            "name:=", robot_name,
            " ",
            "ur_type:=", ur_type,
            " ",
            "tf_prefix:=", tf_prefix,
            " ",
            "sim_gazebo:=", sim_gazebo,
            " ",
            "simulation_controllers:=", controllers_config,
            " ",
            "namespace:=", namespace,
            " ",
            "start_joint_controller:=", "true",
            
        ]
    )
    
    robot_description_content_left = generate_robot_description("ur10e_left", "left", controllers_config_left, "ur10e_left")
    # robot_description_content_right = generate_robot_description("ur10e_right", "right", controllers_config_right, "ur10e_right")
    
    robot_description_left = {"robot_description": robot_description_content_left}
    # robot_description_right = {"robot_description": robot_description_content_right}
    
    
    robot_state_publisher_node_ur10e_left = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name='robot_state_publisher',
        # name='robot_state_publisher_ur10e_left',
        namespace='ur10e_left',
        output="both",
        parameters=[robot_description_left],
    )
    
    joint_state_broadcaster_spawner_left = Node(
        package="controller_manager",
        executable="spawner",
        namespace='ur10e_left',
        arguments=["joint_state_broadcaster", "--controller-manager", "/ur10e_left/controller_manager"],
    )

    # Spawn robot with a unique name to avoid "already exists" error
    spawn_robot_left = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=[
            "-entity", "ur10e_left",  # Changed entity name
            "-topic", "/ur10e_left/robot_description",  # Use robot_description topic instead of file
            "-x", "-0.5",
            "-y", "0.25",
            "-z", "0.741",
            "-Y", "0.0",
        ],
        output="screen",
    )

    # ***** RETURN LAUNCH DESCRIPTION ***** #
    return LaunchDescription([
        robot_state_publisher_node_ur10e_left,
        joint_state_broadcaster_spawner_left,
        spawn_robot_left,    
    ])