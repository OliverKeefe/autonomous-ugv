# Autonomous Unmanned Ground Vehicle
A self-driving, autonomous unmanned ground vehicle controller, tested with Limo4.

## Getting started
This project requires a minimum of Ubuntu 24.04 and ROS2 Humble.

### Bash
```shell
cd ~/autonomous-ugv && source install/local_setup.bash
```

### Zsh
```shell
cd ~/autonomous-ugv && source install/local_setup.zsh
```

### Build
```shell
colcon build
```

### Launching Gazebo Simulator
```shell
ros2 launch limo_sim limo_world.launch.py
```

### Running a Simulation

> [!NOTE]
> `$ colcon build` is only required to be run upon code change. 

```shell
colcon build && ros2 run main_pkg main_node -mode simulation
```