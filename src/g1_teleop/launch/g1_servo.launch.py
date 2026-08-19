import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from moveit_configs_utils import MoveItConfigsBuilder

def generate_launch_description():
    # 1. LOADING ROBOT ANATOMY
    moveit_config = MoveItConfigsBuilder("g1_29dof_with_hand", package_name="g1_arm").to_moveit_configs()

    # 2. YAML PATH
    servo_yaml_path = os.path.join(
        get_package_share_directory('g1_teleop'),
        'config',
        'g1_servo.yaml'
    )

    # 3. SERVO START
    servo_node = Node(
        package='moveit_servo',
        executable='servo_node_main',
        name='servo_node',
        parameters=[
            moveit_config.to_dict(),
            servo_yaml_path          
        ],
        output='screen'
    )

    return LaunchDescription([servo_node])