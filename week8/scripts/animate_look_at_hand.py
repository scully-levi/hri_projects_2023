#!/usr/bin/python3
import math

import rospy
from sensor_msgs.msg import JointState
import numpy as np
import tf2_ros

def animate_look_at_hand():
    rospy.init_node('animate_look_at_hand', anonymous=True)
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

        #initalize array's of animated path pos for pitch and yaw
        pitch_path = np.linspace(current_pitch, goal_pitch_pos, 1200)
        yaw_path = np.linspace(current_yaw, goal_yaw_pos, 1200)

        #look through both arrays adjusting the head pitch and yaw pos incrementally until goal is reached
        for pitch_cord, yaw_cord in pitch_path,yaw_path:
            joint_states.position(goal_pitch_pos)
            joint_states.position(goal_yaw_pos)
            pub.publish(joint_states)

        rate.sleep()

if __name__ == '__main__':
    try:
        animate_look_at_hand()
    except rospy.ROSInterruptException:
        pass

