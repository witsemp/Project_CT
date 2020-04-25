from statemachine import StateMachine, State
from wood_gripper import WoodGripper
from  robot_platform import RobotPlatform
from supervisor import Supervisor
import time

wood_gripper = WoodGripper()
robot_platform = RobotPlatform()
supervisor = Supervisor()
# S: message from supervisor
# G: message from wood gripper
# R: message from robot platform
while True:
    n = input("Start new sequence? (y/n) ")
    if n == "y":
        # robot_platform.process()
        # wood_gripper.process()
        #supervisor.test_cycle()
        supervisor.real_deal()
    if n == "n":
        break
