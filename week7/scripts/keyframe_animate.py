#!/usr/bin/python3
import rospy
from sensor_msgs.msg import JointState
import numpy as np
import tf2_ros






def keyframe_animation():
    rospy.init_node('keyframe_animation', anonymous=True)
    pub = rospy.Publisher('joint_states', JointState, queue_size = 10)
    rate = rospy.Rate(20)
    head_positions = np.linspace(-0.4, 0.4, 120)

    while not rospy.is_shutdown():

        joint_states = JointState()
        joint_states.header.stamp = rospy.get_rostime()
        joint_states.header.frame_id = "Torso"
        joint_states.name.append("HeadPitch")

        #animates headnod through array of positons
        for frame in head_positions:
            joint_states.position.append(frame)
            pub.publish(joint_states)

        rate.sleep()

if __name__ == '__main__':
    try:
        keyframe_animation()
    except rospy.ROSInterruptException:
        pass

