from statemachine import StateMachine, State
from wood_gripper import WoodGripper
from  robot_platform import RobotPlatform
import time
wood_gripper = WoodGripper()
robot_platform = RobotPlatform()
while(True):
    #wood_gripper.process()
    robot_platform.process()
