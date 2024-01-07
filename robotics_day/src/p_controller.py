#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Pose
from tf.transformations import euler_from_quaternion
import math
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import numpy as np

pose_x = 0
pose_y = 0
pose_th = 0

def odom_callback(odom):

    global pose_x, pose_y, pose_th
    pose_x = odom.pose.pose.position.x
    pose_y = odom.pose.pose.position.y

    q = (
        odom.pose.pose.orientation.x,
        odom.pose.pose.orientation.y,
        odom.pose.pose.orientation.z,
        odom.pose.pose.orientation.w
    )
    roll, pitch, yaw = euler_from_quaternion(q)
    pose_th = yaw



if __name__ == '__main__':

    nodename = "p_controller"
    rospy.init_node(nodename)

    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    sub = rospy.Subscriber("/odom", Odometry, odom_callback, queue_size=10)    

    posen = [[1,1,math.radians(45)],[2,2,math.radians(45)],[3,3,math.radians(0)]]

   
    rate = rospy.Rate(10)

    twist_msg = Twist()

    i = 0
    Kp = 0.9
    ka = 1.3
    kb = -1.2

    while not rospy.is_shutdown():  
        
        
        distance_to_goal = math.sqrt(math.pow((posen[i][0] - pose_x), 2) + math.pow((posen[i][0] - pose_y), 2))

        alpha = math.atan2(posen[i][1] - pose_y, posen[i][0] - pose_x) - pose_th

        beta = posen[i][2] - alpha -pose_th

        if(alpha > math.pi):
    
            alpha = alpha - 2*math.pi

    
        if(alpha < - math.pi):
            alpha = alpha + 2*math.pi

        if(beta > math.pi):
    
            beta = beta - 2*math.pi

        if(beta < - math.pi):
            beta = beta + 2*math.pi

        if distance_to_goal < 0.01: #0.1
            
            twist_msg.linear.x = 0
            twist_msg.angular.z = 0
            pub.publish(twist_msg)
            i = i+1

            if i > 2:
                rospy.loginfo("Distance is smaller than 0.1. Shutting down the node.")
                rospy.signal_shutdown("Distance is smaller than 0.1")
        

        v = Kp*distance_to_goal
        w = ka*alpha + kb*beta

        if v > 0.2:
            v = 0.2
        if w < -1:
            w = -1
        if w > 1:
            w = 1

        twist_msg.linear.x = v  # Example linear velocity
        twist_msg.angular.z = w  # Example angular velocity
    
        # Publish the Twist message
        pub.publish(twist_msg)
        print("Twist message published!")
        print(twist_msg.linear.x)
        print(twist_msg.angular.z)
        rate.sleep()