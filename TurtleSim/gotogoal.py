#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
pose = Pose()

def pose_callback(data):
    global pose
    pose = data

def go_to_goal():
    rospy.init_node('go_to_goal_simple', anonymous=True)
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber('/turtle1/pose', Pose, pose_callback)

    rate = rospy.Rate(10)  # 10 Hz
    goal_x = 5.5
    goal_y = 5.5

    while not rospy.is_shutdown():
        distance = math.sqrt((goal_x - pose.x)**2 + (goal_y - pose.y)**2)

        vel_msg = Twist()

        if distance > 0.1:
            vel_msg.linear.x = 1.5
            vel_msg.angular.z = 4 * (math.atan2(goal_y - pose.y, goal_x - pose.x) - pose.theta)
        else:
            vel_msg.linear.x = 0
            vel_msg.angular.z = 0

        velocity_publisher.publish(vel_msg)

        rate.sleep()

if __name__ == '__main__':
    try:
        go_to_goal()
    except rospy.ROSInterruptException:
        pass
