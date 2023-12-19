#!/usr/bin/python3
import math

import rospy
from sensor_msgs.msg import JointState
import numpy as np
import tf2_ros

def look_at_hand_pointing():
    rospy.init_node('look_at_hand_pointing', anonymous=True)
    pub = rospy.Publisher('joint_states', JointState, queue_size = 10)
    rate = rospy.Rate(20)
    tfBuffer = tf2_ros.Buffer()
    while not rospy.is_shutdown():

        joint_states = JointState()
        joint_states.header.stamp = rospy.get_rostime()
        joint_states.header.frame_id = "Torso"
        joint_states.name.append("HeadPitch")
        joint_states.name.append("HeadYaw")
        hand = tfBuffer.lookup_transform('RThumb1', 'Head', rospy.Time(0))
        #should give 1 unit forward from hand and will now look there instead of the hand
        hand += (1,0,0)
        desired_yaw_angle = math.atan2(hand.transform.translation.y, hand.transform.translation.x)
        desired_pitch_angle = math.atan2(hand.transform.translation.z, hand.transform.translation.x)

        desired_pitch_pos = desired_pitch_angle / 180
        desired_yaw_pos = desired_yaw_angle / 180

        head_pitch_range = [-0.4, 0.4]
        # total range of 0.8
        goal_pitch_pos = (desired_pitch_pos * 0.8) - 0.4
        head_yaw_range = [-2, 2]
        #total range of 4
        goal_yaw_pos = (desired_yaw_pos * 4) - 2

        joint_states.position(goal_pitch_pos)
        joint_states.position(goal_yaw_pos)
        pub.publish(joint_states)

        rate.sleep()

if __name__ == '__main__':
    try:
        look_at_hand_pointing()
    except rospy.ROSInterruptException:
        pass

