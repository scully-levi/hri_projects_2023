#!/usr/bin/python3
import rospy
from sensor_msgs.msg import JointState
import math
import tf2_ros


def keyframe_animation():
    rospy.init_node('keyframe_animation', anonymous=True)
    pub = rospy.Publisher('joint_states', JointState, queue_size = 10)
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():

        joint_states = JointState()
        joint_states.header.stamp = rospy.get_rostime()
        joint_states.header.frame_id = "Torso"
        joint_states.name.append("HeadYaw")
        joint_states.name.append("HeadPitch")

        joint_states.position.append(0.17)
        joint_states.position.append(-0.39)

        pub.publish(joint_states)
        rate.sleep()

if __name__ == '__main__':
    try:
        keyframe_animation()
    except rospy.ROSInterruptException:
        pass

