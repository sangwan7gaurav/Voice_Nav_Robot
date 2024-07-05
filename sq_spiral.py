#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist

def path(pub,rate,var):
    trajectory = Twist()
    trajectory.linear.x = 1 + var
    pub.publish(trajectory)
    rate.sleep()
    trajectory.linear.x = 0.0
    pub.publish(trajectory)
    rate.sleep()
    trajectory.angular.z = 3.14159265358979323846/2
    pub.publish(trajectory)
    rate.sleep()
        
def sq_spiral():
    rospy.init_node("Circle", anonymous = True)
    sq_spiral_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(1)
    var = 0
    while not rospy.is_shutdown():
       path(sq_spiral_pub,rate,var)
       var += 0.25
        

if __name__ == '__main__':
    try:
        rospy.loginfo("Making a circle...")
        sq_spiral()
    except rospy.ROSInterruptException:
        pass
    