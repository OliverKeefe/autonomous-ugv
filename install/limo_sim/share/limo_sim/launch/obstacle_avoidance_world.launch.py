import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    AppendEnvironmentVariable,
    SetEnvironmentVariable
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    # Package configuration
    package_name = 'limo_sim'
    robot_name_in_model = 'limo'

    sdf_file_path = 'urdf/limo_four_diff.sdf'
    world_file_path = 'worlds/obstacle_avoidance_world.world'
    models_dir_path = 'models'

    # Robot spawn pose
    spawn_x_val = '0'
    spawn_y_val = '0'
    spawn_z_val = '0.0'
    spawn_yaw_val = '1.57'

    # Package paths
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    pkg_share = get_package_share_directory(package_name)

    default_sdf_model_path = os.path.join(pkg_share, sdf_file_path)
    world_path = os.path.join(pkg_share, world_file_path)

    bridge_params = os.path.join(
        pkg_share,
        'params',
        'limo_coding_bridge.yaml'
    )

    gazebo_config = os.path.join(
        pkg_share,
        'params',
        'gazebo2.config'
    )

    # Gazebo resource paths
    robot_model_base_path = os.path.dirname(pkg_share)
    world_models_path = os.path.join(pkg_share, models_dir_path)

    rmw_implementation = SetEnvironmentVariable(
        name="RMW_IMPLEMENTATION",
        value="rmw_fastrtps_cpp"
    )

    set_gazebo_resource_path = AppendEnvironmentVariable(
        'GZ_SIM_RESOURCE_PATH',
        robot_model_base_path + ':' + world_models_path
    )

    # Launch configurations
    use_sim_time = LaunchConfiguration(
        'use_sim_time',
        default='true'
    )

    world = LaunchConfiguration('world')

    # Launch arguments
    declare_use_sim_time = DeclareLaunchArgument(
        name='use_sim_time',
        default_value='true',
        description='Use simulation clock'
    )

    declare_world = DeclareLaunchArgument(
        name='world',
        default_value=world_path,
        description='World file'
    )

    # Load robot SDF
    with open(default_sdf_model_path, 'r') as sdf_file:
        robot_desc = sdf_file.read()

    # Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[
            {
                'robot_description': robot_desc,
                'use_sim_time': use_sim_time
            }
        ],
        output='screen'
    )

    # Gazebo launch
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                pkg_ros_gz_sim,
                'launch',
                'gz_sim.launch.py'
            )
        ),
        launch_arguments={
            'gz_args':
                f'-r -v4 --gui-config {gazebo_config} {world_path}',
            'on_exit_shutdown': 'true'
        }.items()
    )

    # ROS Gazebo bridge
    gazebo_ros_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '--ros-args',
            '-p',
            f'config_file:={bridge_params}',
        ],
        output='screen'
    )

    # Spawn robot
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', robot_name_in_model,
            '-topic', 'robot_description',
            '-x', spawn_x_val,
            '-y', spawn_y_val,
            '-z', spawn_z_val,
            '-Y', spawn_yaw_val
        ],
        output='screen'
    )

    ld = LaunchDescription()

    ld.add_action(set_gazebo_resource_path)
    ld.add_action(rmw_implementation)

    ld.add_action(declare_use_sim_time)
    ld.add_action(declare_world)

    ld.add_action(gazebo)
    ld.add_action(spawn_entity)
    ld.add_action(robot_state_publisher)
    ld.add_action(gazebo_ros_bridge)


    return ld
