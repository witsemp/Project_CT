from commands.moves import move_j
import numpy as np

def lower_to_pickup_wood(robot):
    start = [90.0, 90.0, 0.0, 0.0, 0.0, 0.0]
    end = [90.0, 180.0, -45.0, 0.0, 0.0, 0.0]
    path = move_j(robot, start, end)
    return path
def lift_with_wood(robot):
    start = [90.0, 180.0, -45.0, 0.0, 0.0, 0.0]
    end = [90.0, 90.0, 0.0, 0.0, 0.0, 0.0]
    path = move_j(robot, start, end)
    return path
def ride_to_drop(robot):
    start = [90.0, 90.0, 0.0, 0.0, 0.0, 0.0]
    end = [270.0, 90.0, 0.0, 0.0, 0.0, 0.0]
    path = move_j(robot, start, end)
    return path
def lower_to_place(robot):
    start = [270.0, 90.0, 0.0, 0.0, 0.0, 0.0]
    end = [270.0, 180.0, -45.0, 0.0, 0.0, 0.0]
    path = move_j(robot, start, end)
    return path
def lift_wo_wood(robot):
    start = [270.0, 180.0, -45.0, 0.0, 0.0, 0.0]
    end = [270.0, 90.0, 0.0, 0.0, 0.0, 0.0]
    path = move_j(robot, start, end)
    return path
def ride_back(robot):
    start = [270.0, 90.0, 0.0, 0.0, 0.0, 0.0]
    end = [90.0, 90.0, 0.0, 0.0, 0.0, 0.0]
    path = move_j(robot, start, end)
    return path
def visual(robot):
    positions = list()
    start = [90.0, 90.0, 0.0, 0.0, 0.0, 0.0]
    end = [90.0, 180.0, -45.0, 0.0, 0.0, 0.0]
    positions.append(move_j(robot, start, end))
    start = [90.0, 180.0, -45.0, 0.0, 0.0, 0.0]
    end = [90.0, 90.0, 0.0, 0.0, 0.0, 0.0]
    positions.append(move_j(robot, start, end))
    start = [90.0, 90.0, 0.0, 0.0, 0.0, 0.0]
    end = [270.0, 90.0, 0.0, 0.0, 0.0, 0.0]
    positions.append(move_j(robot, start, end))
    start = [270.0, 90.0, 0.0, 0.0, 0.0, 0.0]
    end = [270.0, 180.0, -45.0, 0.0, 0.0, 0.0]
    positions.append(move_j(robot, start, end))
    start = [270.0, 180.0, -45.0, 0.0, 0.0, 0.0]
    end = [270.0, 90.0, 0.0, 0.0, 0.0, 0.0]
    positions.append(move_j(robot, start, end))
    start = [270.0, 90.0, 0.0, 0.0, 0.0, 0.0]
    end = [90.0, 90.0, 0.0, 0.0, 0.0, 0.0]
    positions.append(move_j(robot, start, end))
    path = np.vstack(positions)
    robot.animate(stances=path, frame_rate=30, unit='deg')









