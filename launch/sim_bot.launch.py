from ament_index_python.packages import get_package_share_path

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription

from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    urdf_package_path = get_package_share_path("urdf_demo")
    gazebo_package_path = get_package_share_path("gazebo_ros")
    robot_name_in_model = "bot"
    world_path = gazebo_package_path / "worlds/demo.world"

    # Pose where we want to spawn the robot
    spawn_x_val = "0.0"
    spawn_y_val = "0.0"
    spawn_z_val = "0.2"
    spawn_yaw_val = "0.00"

    # Declare the launch arguments
    gui_arg = DeclareLaunchArgument(
        name="gui",
        default_value="true",
        description="Set to false to run headless.",
    )

    server_arg = DeclareLaunchArgument(
        name="server",
        default_value="true",
        description="Set to false not to run gzserver.",
    )

    world_arg = DeclareLaunchArgument(
        name="world",
        default_value=str(world_path),
        description="Full path to the world model file to load",
    )

    # namespace_arg = DeclareLaunchArgument(
    #     name="namespace", default_value="", description="Top-level namespace"
    # )

    # use_namespace_arg = DeclareLaunchArgument(
    #     name="use_namespace",
    #     default_value="false",
    #     description="Whether to apply a namespace to the navigation stack",
    # )

    # head_arg = DeclareLaunchArgument(
    #     name="headless",
    #     default_value="False",
    #     description="Whether to execute gzclient",
    # )

    # use_sim_arg = DeclareLaunchArgument(
    #     name="use_sim",
    #     default_value="true",
    #     description="Whether to start the simulator",
    # )

    # sim_time_arg = DeclareLaunchArgument(
    #     name="use_sim_time",
    #     default_value="true",
    #     description="Use simulation (Gazebo) clock if true",
    # )

    # Launch urdf and rviz
    launch_rviz = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            str(urdf_package_path / "launch/view_bot.launch.py")
        ),
    )

    # Start Gazebo server
    launch_gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            str(gazebo_package_path / "launch/gzserver.launch.py")
        ),
        condition=IfCondition(LaunchConfiguration("server")),
        launch_arguments={"world": LaunchConfiguration("world")}.items(),
    )

    # Start Gazebo client
    launch_gazezbo_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            str(gazebo_package_path / "launch/gzclient.launch.py")
        ),
        condition=IfCondition(LaunchConfiguration("gui")),
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            str(gazebo_package_path / "launch/gazebo.launch.py"),
        )
    )

    # Launch the robot
    spawn_entity = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=[
            "-entity",
            robot_name_in_model,
            "-topic",
            "robot_description",
            "-x",
            spawn_x_val,
            "-y",
            spawn_y_val,
            "-z",
            spawn_z_val,
            "-Y",
            spawn_yaw_val,
        ],
        output="screen",
    )

    # Create the launch description and populate
    return LaunchDescription(
        [
            # namespace_arg,
            # use_namespace_arg,
            # simulator_arg,
            # sim_time_arg,
            gui_arg,
            server_arg,
            world_arg,
            launch_rviz,
            launch_gazebo_server,
            launch_gazezbo_client,
            # gazebo,
            spawn_entity,
        ]
    )
