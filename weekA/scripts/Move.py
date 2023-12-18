#!/usr/bin/python3

import ros_vosk
import rospy
from ros_vosk.msg import speech_recognition
from std_msgs.msg import String, Bool

def callback(data):
    user_answer = data
    temp = str(data)

    if "yes" in temp:
        #user_answer_bool = True
    else:
        #user_answer_bool = False


if __name__ == '__main__':
    rospy.init_node('listener', anonymous=True)
    rate = rospy.Rate(60)
    sub = rospy.Subscriber('speech_recognition/final_result', String, callback)
    pub = rospy.Publisher('tts/phrase', String, queue_size = 10)
    #I used Chat GPT to come up with yes/no questions and responses
    questions = ["Did you finish reading a book this week?",
                 "Have you ever tried bungee jumping?",
                 "Is your favorite season winter?",
                 "Did you attend a live concert this year?",
                 "Have you ever learned to play a musical instrument?"]
    yes_responses = ["That's impressive.",
                     "Wow that's Impressive!",
                     "Nice choice, I prefer the winter cold",
                     "That sounds like a blast!",
                     "It's a very impressive skill to have!"]
    no_responses = ["There's always next week.",
                    "That's okay, not everyone is into extreme activities.",
                    "Ew, as a robot I hate the summer heat",
                    "That's too bad, but theres always a chance to support your favorite artists in the future!",
                    "That's okay. It's never too late to learn!"]
    user_answer = None
    user_answer_bool = False
    Qnum = 0
    for q in questions:
        rospy.sleep(1)
        print(q)
        pub.publish(q)
        rospy.sleep(4)
        print('done')
        response = ""
        while user_answer == None:
            rospy.sleep(.01)
        if user_answer == True:
            response = yes_responses[Qnum]
        else:
            response = no_responses[Qnum]
        Qnum += 1
        pub.publish(response)

   # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
