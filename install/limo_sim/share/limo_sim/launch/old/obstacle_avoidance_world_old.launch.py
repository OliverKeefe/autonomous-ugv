import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, AppendEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

  # Constants for paths to different files and folders
  package_name = 'limo_sim'
  robot_name_in_model = 'limo_sim'
  sdf_file_path = 'urdf/limo_four_diff.sdf'
  world_file_path = 'worlds/obstacle_avoidance_world.world'
  models_dir_path = 'models' # Directory for world models

  # Pose where we want to spawn the robot
  spawn_x_val = '0'
  spawn_y_val = '0'
  spawn_z_val = '0.0'
  spawn_yaw_val = '1.57'

  ############ You do not need to change anything below this line #############

  # Set the path to different files and folders.
  pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
  pkg_share = get_package_share_directory(package_name)

  default_sdf_model_path = os.path.join(pkg_share, sdf_file_path)
  world_path = os.path.join(pkg_share, world_file_path)
  bridge_params = os.path.join(pkg_share, 'params', 'limo_coding_bridge.yaml')
  gazebo_config = os.path.join(pkg_share, 'params', 'gazebo2.config')

  # Set up the environment variable for Gazebo models
  robot_model_base_path = os.path.dirname(pkg_share)
  world_models_path = os.path.join(pkg_share, models_dir_path)
  set_gazebo_resource_path = AppendEnvironmentVariable(
          'GZ_SIM_RESOURCE_PATH',
          robot_model_base_path + ':' + world_models_path)

  # Launch configuration variables specific to simulation
  use_sim_time = LaunchConfiguration('use_sim_time', default='true')
  urdf_model = LaunchConfiguration('urdf_model')
  world = LaunchConfiguration('world')

  # Declare the launch arguments
  declare_use_sim_time_cmd = DeclareLaunchArgument(
    name='use_sim_time',
    default_value='True',
    description='Use simulation (Gazebo) clock if true')

  declare_sdf_model_path_cmd = DeclareLaunchArgument(
    name='urdf_model',
    default_value=default_sdf_model_path,
    description='Absolute path to robot sdf file')

  declare_world_cmd = DeclareLaunchArgument(
    name='world',
    default_value=world_path,
    description='Full path to the world model file to load')

  with open(default_sdf_model_path, 'r') as sdfRead:
    robot_desc = sdfRead.read()

  # Subscribe to the joint states of the robot, and publish the 3D pose of each link.
  start_robot_state_publisher_cmd = Node(
    package='robot_state_publisher',
    executable='robot_state_publisher',
    parameters=[{'robot_description': robot_desc ,'use_sim_time': use_sim_time}]
    )

  # Start Gazebo server
  start_gazebo_server_cmd = IncludeLaunchDescription(
    PythonLaunchDescriptionSource(
        os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
    ),
    launch_arguments={'gz_args': ['-r -s -v4 ', world], 'on_exit_shutdown': 'true'}.items()
)

  # Start Gazebo client
  start_gazebo_client_cmd = IncludeLaunchDescription(
    PythonLaunchDescriptionSource(
        os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
    ),
    launch_arguments={'gz_args': ['-g --gui-config ', gazebo_config]}.items()
)

  #ROS Gazebo Bridging
  start_gazebo_ros_bridge_cmd = Node(
    package='ros_gz_bridge',
    executable='parameter_bridge',
    arguments=[
        '--ros-args',
        '-p',
        f'config_file:={bridge_params}',
    ],
    output='screen',
  )

  # Launch the robot
  spawn_entity_cmd = Node(
    package='ros_gz_sim',
    executable='create',
    arguments=['-name', robot_name_in_model,
                '-topic', 'robot_description',
                    '-x', spawn_x_val,
                    '-y', spawn_y_val,
                    '-z', spawn_z_val,
                    '-Y', spawn_yaw_val],
                    output='screen')

  # Create the launch description and populate
  ld = LaunchDescription()

  # Add the corrected environment variable action
  ld.add_action(set_gazebo_resource_path)

  # Declare the launch options
  ld.add_action(declare_use_sim_time_cmd)
  ld.add_action(declare_sdf_model_path_cmd)
  ld.add_action(declare_world_cmd)

  # Add any actions
  ld.add_action(start_gazebo_server_cmd)
  ld.add_action(start_gazebo_client_cmd)
  ld.add_action(spawn_entity_cmd)
  ld.add_action(start_robot_state_publisher_cmd)
  ld.add_action(start_gazebo_ros_bridge_cmd)

  return ld
