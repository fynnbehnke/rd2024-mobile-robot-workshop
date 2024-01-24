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
    
    # siehe Bildschirm, um die Roboterpose zu setzen



    q = (
        odom.pose.pose.orientation.x,
        odom.pose.pose.orientation.y,
        odom.pose.pose.orientation.z,
        odom.pose.pose.orientation.w
    )

    roll, pitch, yaw = euler_from_quaternion(q)




if __name__ == '__main__':

    nodename = "p_controller"
    rospy.init_node(nodename)

    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    sub = rospy.Subscriber("/odom", Odometry, odom_callback, queue_size=10)    

    # posen = [[1,1,math.radians(45)],[2,2,math.radians(45)],[3,3,math.radians(0)]] posen definieren

   
    rate = rospy.Rate(10)

    twist_msg = Twist() 

    i = 0

    # Kp = 0.1
    # ka = 0.2
    # kb = -0.3 Parameter selbstständig definieren

    while not rospy.is_shutdown():  
        
    # berechne den Abstand zwischen Roboterpose und Zielpose     
    
    
    # berechne alpha (winkel zum Ziel)

    # berechne beta (Endorientierung)

        if(alpha > math.pi):
    
            alpha = alpha - 2*math.pi

    
        if(alpha < - math.pi):
            alpha = alpha + 2*math.pi

        if(beta > math.pi):
    
            beta = beta - 2*math.pi

        if(beta < - math.pi):
            beta = beta + 2*math.pi


        # setze einen Toleranzwert, P-Regler hat immer eine Abweichung !!
            
        

        if distance_to_goal < tolerance: #0.1
            
            twist_msg.linear.x = 0
            twist_msg.angular.z = 0
            pub.publish(twist_msg)
            
            i = i+1

            if i > len(posen)-1: 
                
                rospy.signal_shutdown("") # system wird gekillt, schreibe einen vernünftigen Kommentar
        

        # linear velocity berechne
        # angular velocity
    


        # setze Beschränkungen der Geschwindigkeiten 

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
        

        rate.sleep()