#include "ros/ros.h"
#include "geometry_msgs/Twist.h"
#include <nav_msgs/Odometry.h>
#include <move_base_msgs/MoveBaseActionGoal.h>
#include <actionlib/client/simple_action_client.h>
#include <tf/transform_broadcaster.h>
#include <math.h>



// define a struct for the pose
struct pose
{
    //define poses variables
    double x;
    double y;
    double th;

};

class Regler
{
    public:

    Regler(double x,double y,double th)
    {
        //set some your desired pose, you should call the function drive from here
        p_soll.x = x;
        p_soll.y = y;
        p_soll.th = th; 
        drive();
    }


    private:
    ros::NodeHandle n;
    ros::Subscriber sub_odom;
    ros::Publisher pub_vel;

    //define message type for velocities
    geometry_msgs::Twist v_ros;

    //define variables for poses
    pose p_ist;
    pose p_soll;

    // define variable for distance
    double distance;
    
    //define variables for parameters
    double kP = 1.4;
    double ka = 1.8;
    double kb = -1.2;

    //define variables for angular velocities
    double alpha;
    double beta;

    void drive()
    {

    pub_vel = n.advertise<geometry_msgs::Twist>("cmd_vel",1000);
    sub_odom = n.subscribe("odom",10,&Regler::callback_odom, this);   

    ros::Rate r(10);

    while (ros::ok())
    {
        //define distance, alpha and beta
        distance = sqrt(pow(p_soll.x-p_ist.x, 2) + pow(p_soll.y-p_ist.y, 2));
        alpha = atan2(p_soll.y-p_ist.y, p_soll.x-p_ist.x) - p_ist.th;
        beta = p_soll.th - alpha - p_ist.th;

        //check the angles
        check_angles();

        //define the velocities
        v_ros.linear.x = kP*distance;
        v_ros.angular.z = ka* alpha+kb*beta;

        //check the velocities
        check_velocities();

        // set a tolerance for reaching the pose
        if (distance < 0.1)
            {
                ROS_INFO_STREAM("Pose reached!");
                v_ros.linear.x = 0;
                v_ros.angular.z = 0;
                pub_vel.publish(v_ros);
                ros::spinOnce();
                r.sleep();
                break;
            }
        
        //publish the velocities
        pub_vel.publish(v_ros);
        ros::spinOnce();
        r.sleep();
    }

    }

    void check_velocities()
    {
        // set some conditions for the velocities
        if (v_ros.linear.x > 0.2)
            v_ros.linear.x = 0.2;
        if (v_ros.angular.z < -1)
            v_ros.angular.z = -1;
        if (v_ros.angular.z > 1)
            v_ros.angular.z = 1;

    }

    void check_angles()
    {
        // set some conditions for alpha and beta
        if(alpha > -0.03 && alpha < 0.03)
        {
            alpha = 0;
        }
        if(beta > -0.03 && beta < 0.03)
        {
            beta = 0;
        }
        if(beta > M_PI)
        {
            beta = beta -2* M_PI;

        }
        if(beta < - M_PI)
        {
            beta = beta + 2* M_PI;

        }
        if(alpha >  M_PI)
        {
            alpha = alpha - 2* M_PI;

        }
        if(alpha < -  M_PI)
        {
            alpha = alpha + 2* M_PI;

        }

    }

    // http://docs.ros.org/en/noetic/api/nav_msgs/html/msg/Odometry.html

    void callback_odom(const nav_msgs::Odometry odom)
    {
    //hier code
    p_ist.x = odom.pose.pose.position.x;
    p_ist.y = odom.pose.pose.position.y;
    
     tf::Quaternion q(
        odom.pose.pose.orientation.x,
        odom.pose.pose.orientation.y,
        odom.pose.pose.orientation.z,
        odom.pose.pose.orientation.w);
    tf::Matrix3x3 m(q);	
    double roll, pitch, yaw;						
    m.getRPY(roll, pitch, yaw);

    //hier code
    p_ist.th = yaw;

    }


};


int main(int argc, char **argv)
{
    ros::init(argc, argv, "publisher");								
    Regler p1(1,1,M_PI/4);
    
    // wait for a little bit of time
    ros::Duration(2.0).sleep();

    Regler p2(2,2,M_PI/2);



    return 0;
}




                                    





