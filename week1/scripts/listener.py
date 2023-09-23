#!/usr/bin/python3
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

robotSpace = 1

def callback(data):
    closestValue = 20 #highest value set for sensor reading is 10 so 20 will always be larger
    for value in data.ranges:
        if value < closestValue:
            closestValue = value

    rospy.loginfo(rospy.get_caller_id() + "Object distance: %s", closestValue)
    #if within 1 distance of object stop
    if closestValue <= robotSpace:
        move.linear.x = 0.0
        move.angular.z = 0.0

    else:
        move.linear.x = 0.5
        move.angular.z = 0.0

    pub.publish(move)

rospy.init_node('sub_pub')
pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 1)
sub = rospy.Subscriber('/base_scan', LaserScan, callback)
rate = rospy.Rate(2)
move = Twist()

# spin() simply keeps python from exiting until this node is stopped
rospy.spin()



