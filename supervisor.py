from statemachine import StateMachine, State
from robot_platform import RobotPlatform
from wood_gripper import WoodGripper
import time

class Supervisor(StateMachine):
    # Elements to supervise
    __robot_platform = RobotPlatform()
    __wood_gripper = WoodGripper()
    # List of states
    Idle = State("Supervisor is listening", initial = True)
    Pick_it_up = State("Command gripper to pick up wood")
    Ride_and_rotate_to_2 = State("Command robot to turn and platform to go to position 2")
    Drop_it_now = State("Command gripper to drop wood")
    Ride_and_rotate_to_1 = State("Command robot to turn and platform to go to position 1")

    # List of transitions
    pick_up_wood = Idle.to(Pick_it_up)
    ride_to_drop = Pick_it_up.to(Ride_and_rotate_to_2)
    drop_wood = Ride_and_rotate_to_2.to(Drop_it_now)
    ride_back = Drop_it_now.to(Ride_and_rotate_to_1)
    stop_cycle = Ride_and_rotate_to_1.to(Idle)

    # Processes definitions
    def on_pick_up_wood(self):
       print("Pick it up!!!")


    def on_ride_to_drop(self):
        print("Heading to a drop zone")


    def on_drop_wood(self):
        print("Drop this wood now!!!")


    def on_ride_back(self):
        print("Going back to start")


    def on_stop_cycle(self):
        print("End of work, give me paycheck")


    def test_cycle(self):
        while 1:
            key = input("Want to start cycle? y/n")
            if key == "y":
                self.on_pick_up_wood()
                break
            elif key == "n":
                print("Come back later \n zzzZZZ...")
                time.sleep(4)
            else:
                print("That's not answer to my question!!!")
                time.sleep(2)
        time.sleep(2)
        self.on_ride_to_drop()
        time.sleep(5)
        self.on_drop_wood()
        time.sleep(2)
        self.on_ride_back()
        time.sleep(5)
        self.on_stop_cycle()





