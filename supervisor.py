from statemachine import StateMachine, State
from robot_platform import RobotPlatform
from wood_gripper import WoodGripper
import time
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

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
    restart_pressure = Pick_it_up.to(Idle)
    drop_wood = Ride_and_rotate_to_2.to(Drop_it_now)
    restart_robot_1 = Ride_and_rotate_to_2.to(Idle)
    ride_back = Drop_it_now.to(Ride_and_rotate_to_1)
    stop_cycle = Ride_and_rotate_to_1.to(Idle)

    # flags for errors
    need_restart_gripper = False
    need_restart_robot_1 = False
    need_restart_robot_2 = False

    # Processes definitions
    def on_pick_up_wood(self):
        print("Pick it up!!!")
        self.__robot_platform.wood_detected()
        self.__robot_platform.manipulator_lowered_to_pickup()
        self.__wood_gripper.position1_manipulator_lowered()
        while 1:
            n = input("Choose tray behavior: (a - tray extended correctly, b - tray blocked while extending): ")
            if n == 'a':
                self.__wood_gripper.tray_extended()
                break
            if n == 'b':
                self.__wood_gripper.tray_blocked_extending()
                self.__wood_gripper.tray_unlocked_extending()
        while 1:
            n = input("Pressure circuit status: (a - correct, b - fault): ")
            if n == "a":
                self.__wood_gripper.pressure_applied()
                break
            if n == "b":
                self.need_restart_gripper = True
                self.__wood_gripper.pressure_failure_1()
                break
        if not self.need_restart_gripper:
            self.__robot_platform.gripper_activated();
            self.__robot_platform.manipulator_lifted_w_wood()
        else:
            self.__wood_gripper.gripper_error_handled()
            self.__robot_platform.gripper_error()


    def on_ride_to_drop(self):
        print("Heading to a drop zone")
        while 1:
            n = input("Platform at endswitch 2? (y/n/e): ")
            if n == "y":
                self.__robot_platform.rotated_endswitch_2()
                break
            if n == "n":
                self.__robot_platform.endswitch2_no_confirmation()
            if n == "e":
                self.__robot_platform.endswitch2_error()
                self.__wood_gripper.robot_failure()
                self.need_restart_robot_1 = True
                break


    def on_restart_pressure(self):
        print("Going idle after pressure error")
        time.sleep(1)


    def on_restart_robot_1(self):
        print("Going idle because of robot failure")
        self.__robot_platform.endswitch_error_confirmed()
        time.sleep(1)


    def on_drop_wood(self):
        print("Drop this wood now!!!")
        self.__robot_platform.manipulator_lowered_to_place()
        self.__wood_gripper.position2_ready_to_place()
        self.__robot_platform.gripper_deactivated()
        self.__wood_gripper.pressure_deactivated()
        while 1:
            n = input("Choose tray behavior: (a - tray hidden successfully, b - tray blocked while hiding): ")
            if (n == 'a'):
                self.__wood_gripper.tray_hidden()
                break
            if (n == 'b'):
                self.__wood_gripper.tray_blocked_hiding()
                self.__wood_gripper.tray_unlocked_hiding()
        self.__robot_platform.manipulator_lifted_wo_wood()


    def on_ride_back(self):
        print("Going back to start")
        while 1:
            n = input("Platform at endswitch 1? (y/n/e): ")
            if n == "y":
                self.__robot_platform.rotated_endswitch_1()
                break
            if n == "n":
                self.__robot_platform.endswitch1_no_confirmation()
            if n == "e":
                self.__robot_platform.endswitch1_error()
                self.need_restart_robot_2 = True
                break
        time.sleep(1)


    def on_stop_cycle(self):
        if self.need_restart_robot_2:
            print("Going idle because of robot failure")
            self.__robot_platform.endswitch_error_confirmed()
        else:
            print("End of work, give me paycheck")
        time.sleep(1)


    def test_cycle(self):
        while 1:
            key = input("Want to start cycle? y/n")
            if key == "y":
                self.pick_up_wood()
                break
            elif key == "n":
                print("Come back later \n zzzZZZ...")
                time.sleep(4)
            else:
                print("That's not an answer to my question!!!")
                time.sleep(2)
        time.sleep(2)
        self.ride_to_drop()
        time.sleep(5)
        self.drop_wood()
        time.sleep(2)
        self.ride_back()
        time.sleep(5)
        self.stop_cycle()
    def real_deal(self):
        #reset flags
        self.need_restart_gripper = self.need_restart_robot_1 = self.need_restart_robot_2 = False
        # start cycle
        while 1:
            key = input("Want to start cycle? y/n")
            if key == "y":
                self.pick_up_wood()
                break
            elif key == "n":
                print("Come back later \n zzzZZZ...")
                time.sleep(4)
            else:
                print("That's not an answer to my question!!!")
                time.sleep(2)
        if self.need_restart_gripper:
            self.restart_pressure()
        else:
            self.ride_to_drop()
            if self.need_restart_robot_1:
                self.restart_robot_1()
            else:
                self.drop_wood()
                self.ride_back()
                self.stop_cycle()
    def draw_gripper_graph(self):
        nodes_gripper = []
        edges_gripper = []
        G = nx.DiGraph()
        states = self.__wood_gripper.states
        for state in states:
            nodes_gripper.append(state.value)
        transitions = self.__wood_gripper.transitions
        for transition in transitions:
            for dests in transition.destinations:
                edges_gripper.append([transition.source.value, dests.value])
        print(nodes_gripper)
        print(edges_gripper)
        G.add_nodes_from(nodes_gripper)
        G.add_edges_from(edges_gripper)
        nx.draw(G, with_labels=True, font_weight='bold')
        #plt.savefig("simple_path.png")
        plt.show()
    def draw_robot_graph(self):
        nodes_robot = []
        edges_robot = []
        G = nx.DiGraph()
        states = self.__robot_platform.states
        for state in states:
            nodes_robot.append(state.value)
        transitions = self.__robot_platform.transitions
        for transition in transitions:
            for dests in transition.destinations:
                edges_robot.append([transition.source.value, dests.value])
        print(nodes_robot)
        print(edges_robot)
        G.add_nodes_from(nodes_robot)
        G.add_edges_from(edges_robot)
        nx.draw(G, with_labels=True, font_weight='bold')
        #plt.savefig("simple_path.png")
        plt.show()
    def draw_supervisor_graph(self):
        nodes_supervisor = []
        edges_supervisor = []
        G = nx.DiGraph()
        states = self.states
        for state in states:
            nodes_supervisor.append(state.value)
        transitions = self.transitions
        for transition in transitions:
            for dests in transition.destinations:
                edges_supervisor.append([transition.source.value, dests.value])
        print(nodes_supervisor)
        print(edges_supervisor)
        G.add_nodes_from(nodes_supervisor)
        G.add_edges_from(edges_supervisor)
        nx.draw(G, with_labels=True, font_weight='bold')
        #plt.savefig("simple_path.png")
        plt.show()


