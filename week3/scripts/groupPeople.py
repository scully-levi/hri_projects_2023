#!/usr/bin/python3
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import math
import tf2_ros
from people_msgs.msg import PositionMeasurementArray

def circleCheck():
    pass

def lineCheck():
    pass

peopleGroups = []
def callback(data):
    global peopleGroups
    distanceToGroup = 2
    for index, person in enumerate(data.people):
        index2 = index + 1
        tempList = [person]
        for index2, nextPerson in enumerate(data.people):
            if math.dist(person.pos, nextPerson.pos) < distanceToGroup:
                tempList.append(nextPerson)
        peopleGroups.append(tempList)

    print(peopleGroups)

rospy.init_node('groupDetection')
sub = rospy.Subscriber('/people_tracker_measurements', PositionMeasurementArray, callback)


rate = rospy.Rate(2)
move = Twist()

# spin() simply keeps python from exiting until this node is stopped
rospy.spin()



