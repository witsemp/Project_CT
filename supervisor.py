from statemachine import StateMachine, State
from robot_platform import RobotPlatform
from wood_gripper import WoodGripper
import time
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from excercises import robot_visual
import robopy.base.model as robot

class Supervisor(StateMachine):

    __path = list()
    __model = robot.Puma560()
    __graph = nx.MultiDiGraph()
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

    # Flags for errors
    need_restart_gripper = False
    need_restart_robot_1 = False
    need_restart_robot_2 = False

    # Processes definitions
    def on_pick_up_wood(self):
        print("Pick it up!!!")
        self.__path.append(robot_visual.lower_to_pickup_wood(self.__model))
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
            self.__path.append(robot_visual.lift_with_wood(self.__model))

        else:
            self.__wood_gripper.gripper_error_handled()
            self.__robot_platform.gripper_error()


    def on_ride_to_drop(self):
        print("Heading to a drop zone")
        self.__path.append(robot_visual.ride_to_drop(self.__model))


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
        self.__path.clear()
        time.sleep(1)


    def on_restart_robot_1(self):
        print("Going idle because of robot failure")
        self.__robot_platform.endswitch_error_confirmed()
        self.__path.clear()
        time.sleep(1)


    def on_drop_wood(self):
        print("Drop this wood now!!!")
        self.__robot_platform.manipulator_lowered_to_place()
        self.__wood_gripper.position2_ready_to_place()
        self.__robot_platform.gripper_deactivated()
        self.__wood_gripper.pressure_deactivated()
        self.__path.append(robot_visual.lower_to_place(self.__model))
        while 1:
            n = input("Choose tray behavior: (a - tray hidden successfully, b - tray blocked while hiding): ")
            if (n == 'a'):
                self.__wood_gripper.tray_hidden()
                break
            if (n == 'b'):
                self.__wood_gripper.tray_blocked_hiding()
                self.__wood_gripper.tray_unlocked_hiding()
        self.__robot_platform.manipulator_lifted_wo_wood()
        self.__path.append(robot_visual.lift_wo_wood(self.__model))


    def on_ride_back(self):
        print("Going back to start")
        while 1:
            n = input("Platform at endswitch 1? (y/n/e): ")
            if n == "y":
                self.__robot_platform.rotated_endswitch_1()
                self.__path.append(robot_visual.ride_back(self.__model))
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
            self.__path.clear()
        else:
            print("End of work, give me my paycheck and close the visualisation screen after ending my moves if you want to start a new cycle!")
            path = np.vstack(self.__path)
            self.__model.animate(stances=path, frame_rate=30, unit='deg')
            self.__path.clear()
            time.sleep(1)


    def test_cycle(self):
        while 1:
            key = input("Want to start cycle? (y/n) ")
            if key == "y":
                self.pick_up_wood()
                break
            elif key == "n":
                print("Come back later \n zzzZZZ... ")
                time.sleep(4)
            else:
                print("That's not an answer to my question!!! ")
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
            key = input("Want to start cycle? (y/n) ")
            if key == "y":
                self.pick_up_wood()
                break
            elif key == "n":
                print("Come back later \n zzzZZZ... ")
                time.sleep(4)
            else:
                print("That's not an answer to my question!!! ")
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

    def build_supervisor_graph(self):
        nodes_supervisor = []
        edges_supervisor = []
        G = nx.MultiDiGraph()
        states = self.states
        for state in states:
            nodes_supervisor.append(state.value)
        transitions = self.transitions
        for transition in transitions:
            for dests in transition.destinations:
                edges_supervisor.append([transition.source.value, dests.value])
        print(nodes_supervisor)
        #print(edges_supervisor)
        G.add_nodes_from(nodes_supervisor)
        G.add_edges_from(edges_supervisor)
        self.__graph = G

    def draw_supervisor_graph(self):
        nx.planar_layout(self.__graph)
        nx.draw_circular(self.__graph, with_labels=True, font_weight='bold')
        print("List of self loops:" + str(list(nx.nodes_with_selfloops(self.__graph))))
        plt.show()

    def analyze_supervisor_graph(self, start_node, end_node):
        if start_node in self.__graph.nodes and end_node in self.__graph.nodes:
            if nx.has_path(self.__graph, start_node, end_node):
                print("Path between " + str(start_node) + " and " + str(end_node) + " exists")
                print("Path between " + str(start_node) + " and " + str(end_node) + " is: " + str(nx.shortest_path(self.__graph, start_node, end_node)))


            else:
                print("Path between nodes doesn't exist ")
        else:
            print("Invalid nodes provided ")








