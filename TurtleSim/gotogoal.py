#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

# Global variable for the turtle's pose
pose = Pose()

def pose_callback(data):
    global pose
    pose = data

def go_to_goal():
    # Initialize the ROS node
    rospy.init_node('go_to_goal_simple', anonymous=True)

    # Create a publisher to send velocity commands
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

    # Create a subscriber to get the turtle's pose
    rospy.Subscriber('/turtle1/pose', Pose, pose_callback)

    rate = rospy.Rate(10)  # 10 Hz

    # Set the goal position
    goal_x = 5.5
    goal_y = 5.5

    while not rospy.is_shutdown():
        # Calculate the distance to the goal
        distance = math.sqrt((goal_x - pose.x)**2 + (goal_y - pose.y)**2)

        # Create a Twist message
        vel_msg = Twist()

        # Move towards the goal
        if distance > 0.1:
            vel_msg.linear.x = 1.5
            vel_msg.angular.z = 4 * (math.atan2(goal_y - pose.y, goal_x - pose.x) - pose.theta)
        else:
            vel_msg.linear.x = 0
            vel_msg.angular.z = 0

        # Publish the velocity command
        velocity_publisher.publish(vel_msg)

        # Sleep to maintain the loop rate
        rate.sleep()

if __name__ == '__main__':
    try:
        go_to_goal()
    except rospy.ROSInterruptException:
        pass