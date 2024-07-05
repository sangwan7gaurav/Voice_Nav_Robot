#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from math import pi

def move_continuous_circle():
    rospy.init_node('continuous_circle_turtle', anonymous=True)
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)  # 10hz

    while not rospy.is_shutdown():
        # Create a Twist message to send velocity commands
        vel_msg = Twist()

        # Set linear velocity to move forward
        vel_msg.linear.x = 1.0  # adjust as needed

        # Set angular velocity to make the turtle turn (to create a circle)
        vel_msg.angular.z = 1.0  # adjust as needed

        # Publish the velocity command
        pub.publish(vel_msg)

        # Sleep to maintain the specified rate
        rate.sleep()

if __name__ == '__main__':
    try:
        move_continuous_circle()
    except rospy.ROSInterruptException:
        pass


