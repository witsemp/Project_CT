from statemachine import StateMachine, State
from wood_gripper import WoodGripper
from  robot_platform import RobotPlatform
from supervisor import Supervisor
import time

wood_gripper = WoodGripper()
robot_platform = RobotPlatform()
supervisor = Supervisor()

while True:
    n = input("Start new sequence? (y/n) ")
    if n == "y":
        # robot_platform.process()
        # wood_gripper.process()
        #supervisor.test_cycle()
        #supervisor.real_deal()
        supervisor.draw_robot_graph()
        supervisor.draw_gripper_graph()
        supervisor.draw_supervisor_graph()
    if n == "n":
        break
