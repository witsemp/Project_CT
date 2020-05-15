from wood_gripper import WoodGripper
from robot_platform import RobotPlatform
from supervisor import Supervisor
import robopy.base.model as robot
from excercises import robot_visual
wood_gripper = WoodGripper()
robot_platform = RobotPlatform()
supervisor = Supervisor()
model = robot.Puma560()

while True:
    print("------------------------------")
    print("Choose action from menu below: ")
    print("------------------------------")
    print("Press 'a' to start a new cycle and visualize station at the end.  ")
    print("Press 'b' to show graphs of transitions between states.  ")
    print("Press 'c' to show only visualization of the whole cycle.  ")
    print("Press 'd' to show a path between 2 chosen states.  ")
    print("------------------------------")

    n = input("Action: ")
    if n == "a":
        supervisor.real_deal()
        
    elif n == "b":
        print("Choose graph to show: ")
        print("------------------------------")
        print("Press '1' to show the supervisor graph ")
        print("Press '2' to show the gripper  graph ")
        print("Press '3' to show the robot and the platform graph ")
        print("------------------------------")
        w = input("Action: ")
        if w == "1":
            supervisor.build_supervisor_graph()
            supervisor.draw_supervisor_graph()
        elif w == "2":
            wood_gripper.build_gripper_graph()
            wood_gripper.draw_gripper_graph()
        elif w == "3":
            robot_platform.build_robot_graph()
            robot_platform.draw_robot_graph()
            
    elif n == "c":
        robot_visual.visual(model)

    elif n == "d":
        print("Choose graph to analyze: ")
        print("------------------------------")
        print("Press '1' to analyze the supervisor graph ")
        print("Press '2' to analyze the gripper  graph ")
        print("Press '3' to analyze the robot and the platform graph ")
        print("------------------------------")
        w = input("Action: ")
        if w == "1":
            supervisor.build_supervisor_graph()
            x = input("Provide start node: ")
            y = input("Provide end node: ")
            supervisor.analyze_supervisor_graph(x, y)
        elif w == "2":
            wood_gripper.build_gripper_graph()
            x = input("Provide start node: ")
            y = input("Provide end node: ")
            wood_gripper.analyze_gripper_graph(x, y)
        elif w == "3":
            robot_platform.build_robot_graph()
            x = input("Provide start node: ")
            y = input("Provide end node: ")
            robot_platform.analyze_robot_graph(x, y)

