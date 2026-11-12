#!/usr/bin/env python3
import traceback
from typing import Dict

from main_pkg.args import mode_argument
mode_argument()

import rclpy
import math

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from rclpy.qos import QoSProfile, ReliabilityPolicy
from sensor_msgs.msg import LaserScan

from main_pkg.marker_node import MarkerTracker

from pidc_pkg.pidc import PIDController

from utils.safety import clamp

mynode_ = None
pub_ = None
regions_ = {
    'left': 0,
    'right': 0,
    'front_left': 0,
    'front_right': 0,
    'front1': 0,
    'front2': 0,
}
twstmsg_ = None
count = 0
tracker_ = None  # Global tracker reference

def timer_callback():
    global pub_, twstmsg_
    if twstmsg_ is not None:
        pub_.publish(twstmsg_)

def clbk_laser(msg):
    global regions_, twstmsg_, count

    print("Data Points: ", len(msg.ranges))

    regions_ = {
        # 120 samples over 360 deg, index 0 = rear (-180 deg), 3 deg per index.
        # index i -> angle = -180 + 3*i degrees.
        'front': find_nearest(msg.ranges[58:62]),  # ~0 deg (straight ahead)
        'front_right': find_nearest(msg.ranges[43:51]),  # ~ -30 to -50 deg
        'front_left': find_nearest(msg.ranges[69:77]),  # ~ +30 to +50 deg
        'right': find_nearest(msg.ranges[29:32]),  # ~ -90 deg
        'left': find_nearest(msg.ranges[88:91]),  # ~ +90 deg
    }

    twstmsg_ = movement()

def find_nearest(list):
    f_list = filter(lambda item: item > 0.0, list)  # exclude zeros
    return min(min(f_list, default=10), 10)

#Basic movement method
def movement():
    global regions_, tracker_
    regions = regions_

    #print(tracker_.visionDebug()) # Debug camera print, similar to the LiDAR print below, to be used for the Camera functionality.

    print(f"[LiDAR]  Left: {regions['left']:.2f} | Front Left: {regions['front_left']:.2f} | Front: {regions['front']:.2f}\n| Front Right: {regions['front_right']:.2f} |Right: {regions['right']:.2f}\n")

    msg = Twist()

    #msg.linear.x = 0.2
    #msg.angular.z = really_basic_controller(regions)

    # Prevent collision
    if regions['front'] <= 0.5:
        msg.linear.x = 0.0
        msg.angular.z = -0.8 # TODO: if left closer than right, turn right et visa versa
    else:
        l_side = min(regions['left'], 2.0)
        r_side = min(regions['right'], 2.0)
        msg.angular.z = clamp(pid_steer_.control(0.0, r_side - l_side), -0.8, 0.8)
        msg.linear.x = clamp(pid_velocity_.control(regions['front'], 0.6), 0.0, 0.2)
    # really_basic_controller(r=regions)
    return msg

def really_basic_controller(r):
    """
      Temporary, just exists to prove the network connection
      to the physical robot actually works.
      """
    if r['front'] < 0.6:
        return -0.8
    if r['left'] < 0.4:
        return -0.5
    if r['right'] < 0.4:
        return 0.5
    if r['left'] < 0.4 and r['right'] < 0.4:
        return 0.0

    return 0.0

def stop():
    global mynode_
    msg = Twist()
    msg.angular.z = 0.0
    msg.linear.x = 0.0
    return msg

def main():
    global pub_, mynode_, tracker_, pid_steer_, pid_velocity_

    rclpy.init()
    mynode_ = rclpy.create_node('reading_laser')

    # PID Controller
    pid_steer_ = PIDController(kp=0.1, ki=0.4, kd=0.4, dt=0.2)
    pid_velocity_ = PIDController(kp=0.05, ki=0.2, kd=0.2, dt=0.2)

    # Initialise the vision tracker on the existing node
    tracker_ = MarkerTracker(mynode_)

    qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT)

    # publisher for twist velocity messages
    pub_ = mynode_.create_publisher(Twist, '/cmd_vel', 10)
    
    # subscribe to laser topic
    sub = mynode_.create_subscription(LaserScan, '/scan', clbk_laser, qos)

    timer_period = 0.2  # seconds
    timer = mynode_.create_timer(timer_period, timer_callback)

    #pid_ctrl = PIDController
    #pid_ctrl.control()

    # Run and handle interrupts
    try:
        rclpy.spin(mynode_)
    except Exception as e:
        print(e)
        traceback.print_exc()
        stop()  # stop the robot
    finally:
        mynode_.destroy_timer(timer)
        mynode_.destroy_node()


if __name__ == '__main__':
    main()
