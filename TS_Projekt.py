from statemachine import StateMachine, State
from wood_gripper import WoodGripper
import time
wood_gripper = WoodGripper()
#n = input("Zakończ proces chwytaka (n)")
while(True):
    wood_gripper.process()
