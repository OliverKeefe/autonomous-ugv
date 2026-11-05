<h1 align="center">Autonomous Unmanned Ground Vehicle</h1>

<div align="center">

<img src="https://img.shields.io/badge/ROS_2-22314E.svg?style=flat-square&logo=ros&logoColor=white" alt="ROS 2">
<img src="https://img.shields.io/badge/C%2B%2B_17-00599C.svg?style=flat-square&logo=cplusplus&logoColor=white" alt="C++">
<img src="https://img.shields.io/badge/Python_3.12-3776AB.svg?style=flat-square&logo=python&logoColor=white" alt="Python 3.12">
<img src="https://img.shields.io/badge/OpenCV-5C3EE8.svg?style=flat-square&logo=opencv&logoColor=white" alt="OpenCV">
<img src="https://img.shields.io/badge/CUDA-76B900.svg?style=flat-square&logo=nvidia&logoColor=white" alt="NVIDIA Jetson Orin Nano">

</div>

## 🤖 Overview
A ROS 2-based autonomous navigation system for Robotic Unmanned Ground Vehicles (UGVs), built and tested on the **AgileX Robotics Limo 4 Pro** platform and simulated in Gazebo / MuJoCo. The project provides implementations of traditional control theory, computer vision (OpenCV) and RL-based navigation. Additionally, support for high-level instructions given by humans in natural language are to be implemented.

## 🛣️ Feature Roadmap

- [x] Implement PID Controller
- [x] Add LiDAR in Gazebo sim
- [ ] Implement Fuzzy Logic Controller
- [ ] Implement Computer Vision and Camera Drivers
- [ ] Implement Reinforcement Learning / Goal-Oriented Navigation
- [ ] Implement Obstacle Avoidance
- [ ] Implement Natural Language Instruction

## ⚙️ Getting Started

### Dependencies 
#### Ubuntu 26.04+

**ROS2 Lyrical Luth**

Set the locale.

```shell
locale  # check for UTF-8
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
locale  # verify settings
```

Enable required repositories
```shell
sudo apt install software-properties-common
sudo add-apt-repository universe
```

Install ROS apt source repositories
```shell
sudo apt update && sudo apt install curl -y
export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F'"' '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
sudo dpkg -i /tmp/ros2-apt-source.deb
```

Install Development Tools
```shell
sudo apt update && sudo apt install ros-dev-tools
```

Install ROS
```shell
sudo apt update && sudo apt upgrade -y \
sudo apt install ros-lyrical-desktop \ 
sudo apt install ros-lyrical-ros-base \
```

**Gazebo Sim - Jetty**
Install Pre-reqs
```shell
sudo apt-get update
sudo apt-get install curl lsb-release gnupg
```

Install Sim
```shell
sudo curl https://packages.osrfoundation.org/gazebo.gpg --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] https://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null
sudo apt-get update
sudo apt-get install gz-jetty
```

#### Ubuntu 24.04 LTS

The machines in the robotics lab used for field-testing run **Ubuntu 24.04 with ROS 2 Humble**. Naturally, the project must build and
run on both. When adding dependencies, always add them to `package.xml` and install
them for the *distro that machine uses* (`ros-lyrical-*` for Ubuntu 26.04+ devices, `ros-humble-*` in
the lab).

The lab machines are pre-provisioned, so in most cases:

```shell
sudo apt update
sudo apt install python3-rosdep colcon
rosdep update
rosdep install --from-paths src --ignore-src -y
```

If a fresh lab install is needed instead:

```shell
sudo apt install ros-humble-desktop ros-humble-ros-gz gazebo
```

(`ros_gz` on Humble pairs with the Gazebo *Fortress* release; on Lyrical it
pairs with the newer Gazebo; both are handled by the same `ros_gz` APIs used in
this repo's launch files.)

## 🛠️ Building and Running

Run colcon **from the repository root** (`autonomous-ugv/`), never from inside
`src/`. **An FYI To Myself** Sourcing must also happen from the repo root :

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
```shell
colcon build && ros2 run main_pkg main_node -mode simulation
```

> [!TIP]
> `colcon build` is only required to be run upon code change. 


🔬 **Check setup wasn't botched**

```shell
ros2 pkg prefix limo_sim   # should print path under this repo's install/
ros2 launch limo_sim limo_world.launch.py
```