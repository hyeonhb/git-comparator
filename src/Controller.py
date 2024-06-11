from tkinter import *
import tkinter as tk
from Drone import Drone
from RobotCar import RobotCar

class VirtualRobotPanel:
    def __init__(self, root, robot):
        self.root = root
        self.robot = robot

        self.check=BooleanVar()
        self.checkbox=Checkbutton(self.root, text=self.robot.name, variable=self.check, command=self.toggle_status)
        self.checkbox.pack()
        self.check.set(self.robot.enabled)

    def toggle_status(self):
        if self.check.get():
            self.robot.enable()
        else:
            self.robot.disable()

    def clear(self):
        self.checkbox.destroy()

class VirtualSwarmPanel:
    def __init__(self, root, swarm, engine):
        self.engine = engine
        self.root = root
        self.swarm = swarm
        self.button_frame = tk.Frame(self.root)
        self.robot_frame = tk.Frame(self.root)
        self.robot_panel_list = []

        self.drone_button = tk.Button(self.button_frame, text="Add Drone", command=self.add_drone)
        self.rbcar_button = tk.Button(self.button_frame, text="Add RobotCar", command=self.add_rbcar)
        self.clear_button = tk.Button(self.button_frame, text="Clear Swarm", command=self.clear_robots)

        self.drone_button.grid(row=0, column=0)
        self.rbcar_button.grid(row=0, column=1)
        self.clear_button.grid(row=1, column=0, columnspan=2)
        self.button_frame.pack()

        for robot in self.swarm.get_robot_list():
            self.robot_panel_list.append(VirtualRobotPanel(self.robot_frame, robot))

        self.robot_frame.pack()

    def add_robot_to_swarm(self, robot):
        self.swarm.add_robot(robot)
        self.robot_panel_list.append(VirtualRobotPanel(self.robot_frame, robot))

    def add_drone(self):
        name = "Drone" + str(len(self.swarm.get_robot_list()))
        self.add_robot_to_swarm(Drone(self.engine, name))

    def add_rbcar(self):
        name = "RobotCar" + str(len(self.swarm.get_robot_list()))
        self.add_robot_to_swarm(RobotCar(self.engine, name))

    def clear_robots(self):
        for robot in self.swarm.get_robot_list():
            self.swarm.remove_robot(robot)
        for panel in self.robot_panel_list:
            panel.clear()

class CommenderPanel:
    def __init__(self, root, commender, engine):
        pass

class Controller:
    def __init__(self, commander_list):
        self.root = tk.Tk()
        self.root.title("Controller")

        self.commander_list = commander_list

    def add_commander(self, commander):
        self.commander_list.append(commander)

    def remove_commander(self, commander):
        self.commander_list.remove(commander)
