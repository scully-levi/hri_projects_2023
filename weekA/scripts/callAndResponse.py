#!/usr/bin/python3

import ros_vosk
import rospy
from ros_vosk.msg import speech_recognition
from std_msgs.msg import String, Bool

def callback_final(data1):
    print(data1)
    pub.publish(data1)

if __name__ == '__main__':
    rospy.init_node('call-reponse', anonymous=True)
    sub = rospy.Subscriber('speech_recognition/final_result', String, callback_final)
    pub = rospy.Publisher('tts/phrase', String ,queue_size = 10)

   # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()