# Module code: CMP-AMR-2021
# Autonomous Mobile Robotics Assessment1
# Name：Wenyi Ji
# Student ID: JIW18706130
# University of Lincoln

1.0	Brief Introduction:
This program is mainly used to escape the maze. The robot can move in the maze and try to find the exit. The robot can judge the running trajectory through the pictures returned by the sensor, to avoid hitting the wall and avoiding traps. The pixel of the trap is red, and the pixel of the exit is green. When the robot detects red, the linear velocity will become 0 and avoid the trap by changing the angular velocity. Once the robot detects the green exit, the programming will stop running. In addition, this program can record the obstacles the robot ever meets in movement.

2.0	System Explanation:
	How to start system:
	-At first, launch simulator: roslaunch uol_turtlebot_simulator simple.launch
	
	-In new terminal,run RViz: roslaunch uol_turtlebot_simulator turtlebot-rviz.launch

•	Explanation:
The main part of the program allows the robot to move in the maze, avoid traps and find an exit. There are three reading form which can return the distance of the robot to the obstacle forward, left, and right through the laser scanner. When the forward value is greater than 1, it means that there is no obstacle in front of the robot and the robot can move forward. When the forward value is equal to or less than 1, the robot will stop driving forward and determine the direction of the robot by comparing the left reading and the right reading between the robot and the obstacle. At the same time, when these readings are less than 0.75, it proves that there are obstacles near the robot, so the robot needs to adjust the form angle to avoid touching the obstacles.

The robot can detect traps and maze exits at the same time. To detect targets, the rgb camera and cv2 moment attributes allow the robot to use pixels to determine whether the target in front is a trap or an exit. When the robot detects red, it means that there is a trap ahead, and the robot will stop and rotate 180 degrees. When the robot detects green, it means that the front is an exit. The program has a class variable stop which is used to control the robot to stop driving. The default class variable is False. When the robot detects an exit, the class variable stop will be set to true and the program will end.

