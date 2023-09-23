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
    else:
        try:
            trans = tfBuffer.lookup_transform('person1', 'base_footprint', rospy.Time(0))
            move.angular.z = 0.05 * math.atan2(trans.transform.translation.y, trans.transform.translation.x)
            move.linear.x = 0.2 * math.sqrt(trans.transform.translation.x ** 2 + trans.transform.translation.y ** 2)
            if math.sqrt(trans.transform.translation.x ** 2 + trans.transform.translation.y ** 2) < 3:
                move.angular.z = 0.02 * math.atan2(trans.transform.translation.y, trans.transform.translation.x)
                move.linear.x = 0.05 * math.sqrt(trans.transform.translation.x ** 2 + trans.transform.translation.y ** 2)

            if math.sqrt(trans.transform.translation.x ** 2 + trans.transform.translation.y ** 2) < 2:
                move.angular.z = 0.01 * math.atan2(trans.transform.translation.y, trans.transform.translation.x)
                move.linear.x = 0.0
            pub.publish(move)
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            print('')

rospy.init_node('sub_pub')
pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 1)
sub = rospy.Subscriber('/base_scan', LaserScan, callback)

tfBuffer = tf2_ros.Buffer()
tf2listener = tf2_ros.TransformListener(tfBuffer)
rate = rospy.Rate(2)
move = Twist()

# spin() simply keeps python from exiting until this node is stopped
rospy.spin()



