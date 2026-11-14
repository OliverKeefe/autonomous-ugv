import cv2

from typing import Tuple


def get_ubuntu_version():
    pass

def get_ros2_version():
    pass

def get_opencv_version() -> Tuple[int, int]:
    major, minor = (int(i) for i in cv2.__version__.split('.')[:2])
    return major, minor
