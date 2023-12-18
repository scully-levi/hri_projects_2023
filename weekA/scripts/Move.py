#!/usr/bin/python3

import ros_vosk
import rospy
from ros_vosk.msg import speech_recognition
from std_msgs.msg import String, Bool

def callback(data):
    temp = str(data)
    global user_answer_bool
    if "yes" in temp:
        print("yes")
        user_answer_bool= True
    else:
        print("no")
        user_answer_bool = False

if __name__ == '__main__':
    rospy.init_node('questions', anonymous=True)
    rate = rospy.Rate(1)
    sub = rospy.Subscriber('speech_recognition/final_result', String, callback)
    pub_tts = rospy.Publisher('tts/phrase', String, queue_size = 1)
    pub_move = rospy.Publisher('joint_states', JointState, queue_size = 10)

    user_answer_bool = None

    Qnum = 0
    rospy.sleep(1)
    for q in questions:
        print(q)
        pub.publish(q)
        response = ""
        while user_answer_bool == None:
            pass
        if user_answer_bool == True:
            response = yes_responses[Qnum]
        else:
            response = no_responses[Qnum]
        Qnum += 1
        pub.publish(response)
        user_answer_bool = None
        rospy.sleep(.5)
        pub.publish("My next question is")
    pub.publish("Thank you for your time")

