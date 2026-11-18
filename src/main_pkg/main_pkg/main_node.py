#!/usr/bin/env python3
import time
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
target_yaw_ = None
last_scan_ = 0.0
yaw_ = 0.0
odometer_velocity_ = 0.0
turn_dir_ = 0.0

def sector_range():
    pass

def timer_callback():
    global pub_, twstmsg_
    if twstmsg_ is not None:
        pub_.publish(twstmsg_)

def clbk_odometer(msg):
    global yaw_, odometer_velocity_
    q = msg.pose.pose.orientation
    yaw_ = math.atan2(2.0 * (q.w * q.z + q.x * q.y),
                      1.0 - 2.0 * (q.y * q.y + q.z * q.z))
    odometer_velocity_ = abs(msg.twist.twist.linear.x)

def clbk_laser(msg):
    global regions_, twstmsg_, count, target_yaw_, last_scan_
    last_scan_ = time.monotonic()
    print("Data Points: ", len(msg.ranges))

    regions_ = {
        'front': find_nearest(msg.ranges[120:122]),
        'right': find_nearest(msg.ranges[21:23]),
        'left': find_nearest(msg.ranges[219:221]),
    }

    if target_yaw_ is None:
        target_yaw_ = yaw_

    twstmsg_ = movement()


def find_nearest(list):
    f_list = filter(lambda item: item > 0.0, list)  # exclude zeros
    return min(min(f_list, default=10), 10)

#Basic movement method
def movement():
    global regions_, tracker_, turn_dir_
    regions = regions_

    #print(tracker_.visionDebug()) # Debug camera print, similar to the LiDAR print below, to be used for the Camera functionality.

    print(f"[LiDAR]  Left: {regions['left']:.2f} | Front: {regions['front']:.2f}\n | Right: {regions['right']:.2f}\n")

    msg = Twist()

    if regions['front'] <= 0.5 or (turn_dir_ != 0.0 and regions['front'] < 0.8):
        if turn_dir_ == 0.0:  # decides once when entering.
            turn_dir_ = 1.0 if regions['left'] > regions['right'] else -1.0
            pid_steer_.reset()
            pid_velocity_.reset()
        msg.linear.x = 0.0
        msg.angular.z = 0.8 * turn_dir_
    else:
        turn_dir_ = 0.0
        l_side = min(regions['left'], 2.0)
        r_side = min(regions['right'], 2.0)
        msg.angular.z = clamp(pid_steer_.control(0.0, r_side - l_side), -0.5, 0.5)
        msg.linear.x = 0.15 # TODO: Re-add pid control to speed.
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
    pid_steer_ = PIDController(kp=0.3, ki=0.0, kd=0.8, out_limits=(-0.5, 0.5), dt=0.1)

    pid_velocity_ = PIDController(kp=0.2, ki=0.0, kd=0.0, out_limits=(0.0, 0.2),
                                  integral_limits=(-0.6, 0.6), dt=0.1)

    mynode_.create_subscription(Odometry, '/odom', clbk_odometer, 10)

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
