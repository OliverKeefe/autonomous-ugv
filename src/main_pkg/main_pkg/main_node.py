#!/usr/bin/env python3
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

mynode_ = None
pub_ = None
regions_ = {
    'left': 0,
    'right': 0,
    'fLeft': 0,
    'fRight': 0,
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
        # LIDAR readings are anti-clockwise, starting at 0 on the right-most edge of the LiDAR FOV.
        'front': find_nearest(msg.ranges[120:122]),
        'right': find_nearest(msg.ranges[21:23]),
        'left':  find_nearest(msg.ranges[219:221]),
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

    print(f"[LiDAR]  Left: {regions['left']:.2f} | Front: {regions['front']:.2f} | Right: {regions['right']:.2f}\n")

    msg = Twist()

    msg.linear.x = 0.2
    msg.angular.z = really_basic_controller(regions)


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
    global pub_, mynode_, tracker_

    rclpy.init()
    mynode_ = rclpy.create_node('reading_laser')

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
        stop()  # stop the robot
    finally:
        mynode_.destroy_timer(timer)
        mynode_.destroy_node()


if __name__ == '__main__':
    main()
