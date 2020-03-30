from statemachine import StateMachine, State
from wood_gripper import WoodGripper
from  robot_platform import RobotPlatform
import time
wood_gripper = WoodGripper()
robot_platform = RobotPlatform()
while True:
    n = input("Start new sequence? (y/n) ")
    if n == "y":
        #robot_platform.process()
        wood_gripper.process()
    if n == "n":
        break
