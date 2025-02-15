#!/usr/bin/python3

import ros_vosk
import rospy
from ros_vosk.msg import speech_recognition
from std_msgs.msg import String, Bool
from sensor_msgs.msg import JointState
import tf2_ros
import math

def callback(data):
    global user_answer
    user_answer = data
    temp = str(data)

    if "hand" in temp:
        look_at_hand_robo()
    else:
        pass

def look_at_hand_robo():
    rospy.init_node('look_at_hand_robo', anonymous=True)
    pub = rospy.Publisher('joint_states', JointState, queue_size=10)
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
        # total range of 4
        goal_yaw_pos = (desired_yaw_pos * 4) - 2

        joint_states.position(goal_pitch_pos)
        joint_states.position(goal_yaw_pos)
        pub.publish(joint_states)


if __name__ == '__main__':
    rospy.init_node('listener', anonymous=True)
    rate = rospy.Rate(60)
    sub = rospy.Subscriber('speech_recognition/final_result', String, callback)
    pub = rospy.Publisher('joint_states', JointState, queue_size = 10)
    user_answer = None
    user_answer_bool = False
    Qnum = 0
    while not rospy.is_shutdown():
        rospy.sleep(1)
        #waits for speech recognition, if it hears hand, robot will look at hand
        while user_answer == None:
            rospy.sleep(.01)

   # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
