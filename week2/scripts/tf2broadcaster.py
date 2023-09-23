#!/usr/bin/python3
import rospy
from people_msgs.msg import PositionMeasurementArray
import geometry_msgs.msg
import tf_conversions
import tf2_ros

def callback(data):
    #print(len(data.people))
    for person in data.people:
        print(person.pos)
        br = tf2_ros.TransformBroadcaster()
        t = geometry_msgs.msg.TransformStamped()

        t.header.stamp = rospy.Time.now()
        t.header.frame_id = "base_footprint"
        t.child_frame_id = "person1"
        t.transform.translation.x = person.pos.x
        t.transform.translation.y = person.pos.y
        t.transform.translation.z = person.pos.z
        q = tf_conversions.transformations.quaternion_from_euler(0, 0, 0)
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]

        print(person.reliability)
        if person.reliability > 2:
            br.sendTransform(t)


rospy.init_node('KillAllHumans')
sub = rospy.Subscriber('/people_tracker_measurements', PositionMeasurementArray, callback)
rate = rospy.Rate(2)

rospy.spin()