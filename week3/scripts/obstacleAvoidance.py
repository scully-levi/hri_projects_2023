#!/usr/bin/python3
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import math
import tf2_ros

robotSpace = 0.2


def sumOfEachQuarterOfArray(arr):
    size = len(arr)
    sizeOfQuarter = size // 4
    sums = []

    for i in range(4):
        startIndex = i * sizeOfQuarter
        endIndex = startIndex + sizeOfQuarter
        quarterSum = sum(arr[startIndex:endIndex])
        sums.append(quarterSum)

    return (sums.index(max(sums)))

def callback(data):
    closestValue = 20
    for value in data.ranges:
        if value < closestValue:
            closestValue = value
    #if closest scan is less than robot space, start turning towards clearest direction and slow down.
    if closestValue <= robotSpace:
        clearestDirection = sumOfEachQuarterOfArray(data.ranges)
        if clearestDirection == 0:
            move.angular.z = -0.5
        if clearestDirection == 1:
            move.angular.z = -1
        if clearestDirection == 2:
            move.angular.z = 0.5
        if clearestDirection == 3:
            move.angular.z = 1
        move.linear.x = 0.05
        pub.publish(move)


rospy.init_node('simple_obstacle_avoidance')
pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 1)
sub = rospy.Subscriber('/base_scan', LaserScan, callback)

rate = rospy.Rate(2)
move = Twist()

# spin() simply keeps python from exiting until this node is stopped
rospy.spin()



