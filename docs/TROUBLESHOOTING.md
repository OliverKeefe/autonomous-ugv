## Troubleshooting

- **`source ...: no such file or directory ... /*_local_setup_util_*.py`** —
  you sourced the workspace setup from the wrong directory. colcon setup scripts
  must be sourced **from the repo root** (where `install/` lives). A common
  accident: running `colcon build` while inside `src/` creates a second
  `src/build`, `src/install`, `src/log` tree; delete those and rebuild from root.

- **`invalid choice: 'launch'` from `ros2`** — only a minimal CLI set is
  sourced; re-source `/opt/ros/$ROS_DISTRO/setup.*` and install
  `ros-$ROS_DISTRO-ros-base` if still missing.

- **`CMake Error ... find_package(ament_cmake / nav_msgs)`** — ROS not sourced,
  or those packages not installed. `source /opt/ros/$ROS_DISTRO/setup.zsh`,
  and `rosdep install --from-paths src --ignore-src -y`.

- **Python `.venv` conflicts** — deactivate (`deactivate`) before `ros2`/`colcon`
  if you get import or `PYTHONPATH` oddities; ROS modules live in the system
  Python site-packages, not your virtualenv.