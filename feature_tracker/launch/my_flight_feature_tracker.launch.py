from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node


def generate_launch_description():
    config_pkg_path = get_package_share_directory('config_pkg')

    config_file_arg = DeclareLaunchArgument(
        'config_file',
        default_value='config/my_flight_data/my_flight_config.yaml',
        description='Config file relative to config_pkg share directory'
    )
    config_path = PathJoinSubstitution([config_pkg_path, LaunchConfiguration('config_file')])

    vins_path = PathJoinSubstitution([
        config_pkg_path,
        'config/../'
    ])

    feature_tracker_node = Node(
        package='feature_tracker',
        executable='feature_tracker',
        name='feature_tracker',
        namespace='feature_tracker',
        output='screen',
        parameters=[{
            'config_file': config_path,
            'vins_folder': vins_path
        }]
    )

    rviz_config_path = PathJoinSubstitution([
        config_pkg_path,
        'config/vins_euroc_rviz.rviz'
    ])

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_path],
        output='screen'
    )

    return LaunchDescription([
        config_file_arg,
        LogInfo(msg=['[my_flight feature tracker] config path: ', config_path]),
        feature_tracker_node,
        rviz_node
    ])
