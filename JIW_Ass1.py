#name:Wenyi Ji Student ID:JIW18706130
#Reference from some github about Autonomous Mobile Robotics
import rospy
import actionlib
import sys
import cv2
import math
import time
import numpy
import numpy as np
import cv_bridge
import cv_bridge
from math import radians
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import Image

class JIWAssignment:

    def __init__(self):
        #Converting ROS image to opencv image that python can understand
        self.bridge = cv_bridge.CvBridge() 
       
        #Publisher and subscribers present the sending and recieving data from robot
        rospy.loginfo("Publish")
        self.image_pub=rospy.Publisher('/mobile_base/commands/velocity',Twist, queue_size=1)
        rospy.loginfo("Subscriber")
        self.image_sub=rospy.Subscriber('/camera/rgb/image_raw',Image, self.image_callback)
        self.lasers=rospy.Subscriber('scan', LaserScan, callback=self.laserCall)
        

        #Setting the minimum distance from the wall
        self.miniDistance = 1.0
        #Set the robot turnning
        self.twist=Twist()
        #points on the map, robot will navigate to each point and then search for object (colour), once arrived at waypoint, flag will be set to True.
        self.red = False
        self.green=False
        #Setting colors to false, once found colours are set to be true
        self.found_red=False
        self.found_green=False
        #Initialize the angle 
        self.desiredAngle=0
        
        #Setting the distance between robot and obstacle
        self.front=1.0
        self.right=1.0
        self.left=1.0
        self.stop=False
        #Initialize first movement condition
        self.masks=[0,0]

    # This fuction is used to calculate the distance between robot and obstacle
    def laserCall(self,msg):
        #The range of laser
        Range = msg.ranges 
        #Return the minimum distance 
        self.distance=min(Range)
        self.front=msg.ranges[len(Range)/2]
        self.right=msg.ranges[0]
        self.left=msg.ranges[len(Range)-1]

        
        
    # This function is used to find the red obstacle and green exit
    def image_callback(self,msg):
        #Converting the image message to an opencv message that Python can understand
        image = self.bridge.imgmsg_to_cv2(msg,desired_encoding='bgr8')
        #Converting the color from RGB to HSV
        #hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        #Detecting colors
        lower=numpy.array([0,0,0])
    
        #Turn ranges into a mask
        redMask= cv2.inRange(image, lower, numpy.array((20, 20, 255)))
        greenMask= cv2.inRange(image, lower, numpy.array((20, 255, 20)))
        
        #Getting the dimensions of image
        h,w,d=image.shape

        #Selecting the boundry of what robot seeing
        screen_top=3*h/4
        screen_btm=screen_top +25

        #Setting the masks
        greenMask[0:screen_top, 0:w] = 0
        greenMask[screen_btm:h, 0:w] = 0
        redMask[0:screen_top, 0:w] = 0
        redMask[screen_btm:h, 0:w] = 0

        #Capturing moments of different  mask
        rMask=cv2.moments(redMask)
        gMask=cv2.moments(greenMask)
        #Previwing all mask in window and m00 is the contour
        self.masks=[rMask['m00'],gMask['m00']]


    #some sentence taken from github
    def robot_Move(self):
        r= rospy.Rate(5)
        rospy.loginfo("moving forward 0.2m/s")
        robot_move = Twist()
        
        #When robot moving 
        while(self.stop != True):
            #detecting red color
            while(self.masks[1]>2000000):
                print "Robot turning around", self.masks[1]
                for x in range(20):
                     # Linear volecity   
                    robot_move.linear.x=0.0
                     # Angular volecity
                    robot_move.angular.z=radians(45)
                    #Publish twist movement
                    self.image_pub.publish(robot_move)
                    r.sleep()

            #detecting green
            while(self.masks[0]>2000000):
                print "Exit finding", self.masks[0]
                for x in range(15):
                    robot_move.linear.x=0.3
                    robot_move.angular.z=0.0
                    #Publish twist movement
                    self.image_pub.publish(robot_move)
                    r.sleep()
                #Once the robot detect the green, stop programming
                self.stop()

            # counter is used to record the convers times
            counter=0
            #Distance between obstacle more than 1, robot keep moving
            if(self.front>=1):
                robot_move.linear.x=0.3
                robot_move.angular.z=-0.0
            # Robot meet a wall
            else:
                #When robot meet obstacle
                while(self.front<=1):
                    print "Turning count: ", counter
                    if(counter>12):
                        for x in range(20):
                            robot_move.linear.x=0.0
                            #Robot turn 180 degree
                            robot_move.angular.z=radians(45)
                            #Publish twist movement
                            self.image_pub.publish(robot_move)
                            r.sleep()

                        
                    if(self.left>=self.right):
                        robot_move.linear.x=0.0
                        robot_move.angular.z=radians(45)
                        counter=counter+1
                    else:
                        robot_move.linear.x=0.0
                        robot_move.angular.z=radians(45)
                        counter=counter+1
                    #Publish twist movement
                    self.image_pub.publish(robot_move)
                    r.sleep()
            #Determine the movement direction
            if(self.left<=0.75):
                #turnning right
                robot_move.linear.x=0.3
                robot_move.angular.z=-0.4

                #turnning left
                robot_move.linear.x=0.3
                robot_move.angular.z=0.4
            #Publish twist movement
            self.image_pub.publish(robot_move)
            r.sleep()

if __name__ == '__main__':
    rospy.init_node("JIWAssignment")
    mr = JIWAssignment()
    mr.robot_Move()



        

        



       
        

        
        
