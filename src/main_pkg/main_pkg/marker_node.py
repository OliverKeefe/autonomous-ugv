#!/usr/bin/env python3

import math
import cv2
import numpy as np

from cv_bridge import CvBridge
from sensor_msgs.msg import CameraInfo, Image
from rclpy.qos import QoSProfile, ReliabilityPolicy
from utils.versions import get_opencv_version

class MarkerTracker:
    def __init__(self, node):
        self.node = node
        self.marker_size = 0.10  # Target marker: 100mm x 100mm ArUco (DICT_4X4_50)
        self.bridge = CvBridge()

        # Camera Details (Retrieved from /camera_info)
        self.fx = None
        self.cx = None
        self.image_width = None
        self.has_camera_info = False

        # Latest marker tracking data
        self.marker_found = False
        self.distance = None  # Metres
        self.angle = None     # Radians (positive = right, negative = left)

        self.dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

        # `DetectorParameters_create()` is deprecated in versions exceeding 4.7
        cv2_major, cv2_minor = get_opencv_version()

        if (cv2_major, cv2_minor) >= (4, 7):
            self.parameters = cv2.aruco.DetectorParameters()
        else:
            self.parameters = cv2.aruco.DetectorParameters_create()

        self.detector = cv2.aruco.ArucoDetector(self.dictionary, self.parameters)

        qos_best_effort = QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT)

        # Subscriptions
        self.sub_cam_info = self.node.create_subscription(CameraInfo, '/camera/color/camera_info', self._camera_info_callback, qos_best_effort)
        self.sub_cam_image = self.node.create_subscription(Image, '/camera/color/image_raw', self._image_callback, qos_best_effort)

    def _camera_info_callback(self, msg: CameraInfo):
        # Extract parameters: K = [fx, 0, cx, 0, fy, cy, 0, 0, 1]
        self.fx = msg.k[0]
        self.cx = msg.k[2]
        self.image_width = msg.width
        self.has_camera_info = True

    def _image_callback(self, msg: Image):
        if self.has_camera_info == False:
            return

        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='rgb8')
        except Exception as e:
            print(f"CVBridge conversion error: {e}")
            return

        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = cv2.aruco.detectMarkers(gray, self.dictionary, parameters=self.parameters)

        if ids is None or len(corners) == 0:
            self.marker_found = False
            self.distance = None
            self.angle = None
            return

        # Always select the first detected marker
        centre_x, centre_y, px_width = self.measure_marker(corners[0])

        dist, ang = self.calculate_pose(centre_x, centre_y, px_width)
        self.marker_found = True
        self.distance = dist
        self.angle = ang

    @staticmethod
    def measure_marker(marker_corners):
        c = marker_corners[0]

        centre_x = float(c[:, 0].mean())
        centre_y = float(c[:, 1].mean())

        top_edge = np.linalg.norm(c[0] - c[1])
        bottom_edge = np.linalg.norm(c[3] - c[2])
        px_width = float((top_edge + bottom_edge) / 2.0)

        return centre_x, centre_y, px_width

    def calculate_pose(self, centre_x, centre_y, px_width):
        """
        Task - Calculate distance and angle from pixel measurements
    
        Available Variables:
          - self.fx          : Camera focal length in pixels (fx)
          - self.cx          : Optical centre x-coordinate in pixels (cx)
          - self.image_width : Total frame width in pixels (W)
          - self.marker_size : Real marker width in metres (S = 0.10 m)
    
        Inputs:
          - centre_x, centre_y : Marker centre position in image pixels
          - px_width           : Average apparent marker width in pixels
    
        Camera Model Equations:
          1) px_width = marker_size * fx / distance   --> solve for distance (metres)
          2) tan(theta) = (centre_x - cx) / fx        --> solve for angle theta (radians)
        """

        distance = 0.0
        angle = 0.0
    
        return float(distance), float(angle)

    def visionDebug(self):
        if ((self.distance == 0.0) and (self.angle == 0.0)):
            return(f"[Vision] Distance & Angle = 0.0, check calculate_pose()!")

        elif self.marker_found:
            return(f"[Vision] Marker @ Distance: {self.distance:.2f}m | Angle: {math.degrees(self.angle):.1f} deg")    
             
        else:
            return("[Vision] Target Marker not Detected")