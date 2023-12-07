#!/usr/bin/python3
import rospy
from sensor_msgs.msg import JointState
import math
import tf2_ros

rospy.init_node('keyframe_animation')
pub = rospy.Publisher('/HeadYaw', Twist, queue_size = 1)
rate = rospy.Rate(10)
while not rospy.is_shutdown():

    xVel = 0.25
    yVel = 0.25

    HeadYaw =

# spin() simply keeps python from exiting until this node is stopped
rospy.spin()
