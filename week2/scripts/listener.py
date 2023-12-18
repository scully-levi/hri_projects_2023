#!/usr/bin/python3
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import math
import tf2_ros

robotSpace = 0.2

#this function divides sensor information into 4 quadrants and averages each quadrant
#the quadrant with the least average value has the clearest space, and the quadrant with the highest average has the most obstacles
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
    #obstacle avoidance
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
            #move towards person1
            trans = tfBuffer.lookup_transform('person1', 'base_footprint', rospy.Time(0))
            #get angle difference from robo to person1
            move.angular.z = 0.05 * math.atan2(trans.transform.translation.y, trans.transform.translation.x)
            #get distance from person1, this should make the robo slightly faster the farther away the robot is from person1
            move.linear.x = 0.2 * math.sqrt(trans.transform.translation.x ** 2 + trans.transform.translation.y ** 2)
            #if person one is less than 3 units away, slow down
            #don't scare the human
            if math.sqrt(trans.transform.translation.x ** 2 + trans.transform.translation.y ** 2) < 3:
                move.angular.z = 0.02 * math.atan2(trans.transform.translation.y, trans.transform.translation.x)
                move.linear.x = 0.05 * math.sqrt(trans.transform.translation.x ** 2 + trans.transform.translation.y ** 2)
            #if person1 is less than 2 units away, stop forward movement, and slow down rotational movement
            if math.sqrt(trans.transform.translation.x ** 2 + trans.transform.translation.y ** 2) < 2:
                move.angular.z = 0.01 * math.atan2(trans.transform.translation.y, trans.transform.translation.x)
                move.linear.x = 0.0
            pub.publish(move)
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            print('')

rospy.init_node('kill_all_humans')
pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 1)
sub = rospy.Subscriber('/base_scan', LaserScan, callback)

tfBuffer = tf2_ros.Buffer()
tf2listener = tf2_ros.TransformListener(tfBuffer)
rate = rospy.Rate(2)
move = Twist()

# spin() simply keeps python from exiting until this node is stopped
rospy.spin()



