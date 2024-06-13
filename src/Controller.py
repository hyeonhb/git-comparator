import tkinter as tk
from Drone import Drone
from RobotCar import RobotCar
from Swarm import Swarm
import time
from Vector3D import Vector3D

class VirtualRobotPanel:
    def __init__(self, root, robot):
        self.root = root
        self.robot = robot

        self.check=tk.BooleanVar()
        self.checkbox=tk.Checkbutton(self.root, text=self.robot.name, variable=self.check, command=self.toggle_status)
        self.checkbox.pack(anchor='w', side=tk.TOP)
        self.check.set(self.robot.enabled)

    def toggle_status(self):
        if self.check.get():
            self.robot.enable()
        else:
            self.robot.disable()

    def enable_self(self):
        self.robot.enable()
        self.check.set(self.robot.enabled)

    def disable_self(self):
        self.robot.disable()
        self.check.set(self.robot.enabled)

    def clear(self):
        self.checkbox.destroy()
        self.robot.disable()
        

class VirtualSwarmPanel:
    def __init__(self, root, swarm, engine):
        self.engine = engine
        self.root = root
        self.swarm = swarm

        self.tk_widgets = {}

        self.tk_widgets["frame"] = tk.Frame(self.root, bd=1, relief=tk.SOLID)

        self.tk_widgets["btn_frame"] = tk.Frame(self.tk_widgets["frame"])

        self.tk_widgets["drone_btn"] = tk.Button(self.tk_widgets["btn_frame"], text="Add Drone", command=self.add_new_drone)
        self.tk_widgets["rbcar_btn"] = tk.Button(self.tk_widgets["btn_frame"], text="Add RobotCar", command=self.add_new_rbcar)
        self.tk_widgets["clear_btn"] = tk.Button(self.tk_widgets["btn_frame"], text="Clear Robots", command=self.clear_robots)
        self.tk_widgets["enable_btn"] = tk.Button(self.tk_widgets["btn_frame"], text="Enable Robots", command=self.enable_robots)
        self.tk_widgets["disable_btn"] = tk.Button(self.tk_widgets["btn_frame"], text="Disable Robots", command=self.disable_robots)

        self.tk_widgets["drone_btn"].grid(row=0, column=0, sticky="nsew")
        self.tk_widgets["rbcar_btn"].grid(row=1, column=0, sticky="nsew")
        self.tk_widgets["clear_btn"].grid(row=0, column=1, rowspan=2, sticky="nsew")
        self.tk_widgets["enable_btn"].grid(row=2, column=0, columnspan=2, sticky="nsew")
        self.tk_widgets["disable_btn"].grid(row=3, column=0, columnspan=2, sticky="nsew")
        self.tk_widgets["btn_frame"].pack()

        self.robot_panel_list = []
        self.tk_widgets["robots_frame"] = tk.Frame(self.tk_widgets["frame"])
        self.tk_widgets["half_l_frame"] = tk.Frame(self.tk_widgets["robots_frame"])
        self.tk_widgets["half_r_frame"] = tk.Frame(self.tk_widgets["robots_frame"])

        for robot in self.swarm.get_robot_list():
            self.add_robot_control_panel(robot)

        self.tk_widgets["half_l_frame"].grid(row=0, column=0, sticky="nsew")
        self.tk_widgets["half_r_frame"].grid(row=0, column=1, sticky="nsew")
        self.tk_widgets["robots_frame"].pack()

        self.tk_widgets["frame"].pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def get_robot_frame(self):
        if len(self.robot_panel_list) % 2:
            return self.tk_widgets["half_r_frame"]
        else:
            return self.tk_widgets["half_l_frame"]

    def add_robot_to_swarm(self, robot):
        #Swarm에 로봇 추가
        self.swarm.add_robot(robot)
        self.add_robot_control_panel(robot)

    def add_robot_control_panel(self, robot):
        #새로운 로봇에 대한 Control Panel 생성
        self.robot_panel_list.append(VirtualRobotPanel(self.get_robot_frame(), robot))

    def add_new_drone(self):
        name = "Drone" + str(len(self.swarm.get_robot_list()))
        self.add_robot_to_swarm(Drone(self.engine, name))

    def add_new_rbcar(self):
        name = "RobotCar" + str(len(self.swarm.get_robot_list()))
        self.add_robot_to_swarm(RobotCar(self.engine, name))

    def enable_robots(self):
        for panel in self.robot_panel_list:
            panel.enable_self()

    def disable_robots(self):
        for panel in self.robot_panel_list:
            panel.disable_self()

    def clear_robots(self):
        #Swarm에 등록된 로봇 모두 remove
        for robot in self.swarm.get_robot_list():
            self.swarm.remove_robot(robot)

        #Robot control panel 모두 삭제
        for panel in self.robot_panel_list:
            panel.clear()
        self.robot_panel_list.clear()

    def clear(self):
        #Swarm에 등록된 Robot과 Control panel, widget 모두 삭제
        self.clear_robots()
        for widget in self.tk_widgets.values():
            widget.destroy()
        self.tk_widgets.clear()

class VirtualCommanderPanel:
    def __init__(self, root, commander, engine):
        self.engine = engine
        self.root = root
        self.commander = commander

        self.tk_widgets = {}

        self.tk_widgets["frame"] = tk.Frame(self.root, bd=1, relief=tk.SOLID)

        self.tk_widgets["btn_frame"] = tk.Frame(self.tk_widgets["frame"])

        self.tk_widgets["swarm_btn"] = tk.Button(self.tk_widgets["btn_frame"], text="Add Swarm", command=self.add_new_swarm)
        self.tk_widgets["clear_btn"] = tk.Button(self.tk_widgets["btn_frame"], text="Clear Swarms", command=self.clear_swarms)
        self.tk_widgets["init_btn"] = tk.Button(self.tk_widgets["btn_frame"], text="Init Commander", command=self.init_commander)
        self.tk_widgets["start_btn"] = tk.Button(self.tk_widgets["btn_frame"], text="Start Commander", command=self.start_commeder)
        self.tk_widgets["pause_btn"] = tk.Button(self.tk_widgets["btn_frame"], text="Pause Commander", command=self.puase_commander)
        self.tk_widgets["play_btn"] = tk.Button(self.tk_widgets["btn_frame"], text="Play Commander", command=self.play_commander)
        self.tk_widgets["stop_btn"] = tk.Button(self.tk_widgets["btn_frame"], text="Stop Commander", command=self.stop_commander)

        self.tk_widgets["init_btn"].grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.tk_widgets["start_btn"].grid(row=2, column=0, columnspan=2, sticky="nsew")
        self.tk_widgets["pause_btn"].grid(row=3, column=0, columnspan=2, sticky="nsew")
        self.tk_widgets["play_btn"].grid(row=4, column=0, columnspan=2, sticky="nsew")
        self.tk_widgets["stop_btn"].grid(row=5, column=0, columnspan=2, sticky="nsew")
        self.tk_widgets["swarm_btn"].grid(row=6, column=0, sticky="nsew")
        self.tk_widgets["clear_btn"].grid(row=6, column=1, sticky="nsew")

        self.tk_widgets["btn_frame"].pack()

        self.swarm_panel_list = []
        self.tk_widgets["swarms_frame"] = tk.Frame(self.tk_widgets["frame"])

        for swarm in self.commander.get_swarm_list():
            self.add_swarm_control_panel(swarm)

        self.tk_widgets["swarms_frame"].pack()

        self.tk_widgets["frame"].pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    def add_swarm_to_commander(self, swarm):
        self.commander.add_swarm(swarm)
        self.add_swarm_control_panel(swarm)

    def add_swarm_control_panel(self, swarm):
        #새로운 Swarm에 대한 Control Panel 생성
        self.swarm_panel_list.append(VirtualSwarmPanel(self.tk_widgets["swarms_frame"], swarm, self.engine))

    def add_new_swarm(self):
        self.add_swarm_to_commander(Swarm())

    def init_commander(self):
        self.commander.commander_init()

    def start_commeder(self):
        self.commander.commander_start()

    def puase_commander(self):
        self.commander.commander_pause()

    def play_commander(self):
        self.commander.commander_play()

    def stop_commander(self):
        self.commander.commander_stop()

    def clear_swarms(self):
        for swarm in self.commander.get_swarm_list():
            self.commander.remove_swarm(swarm)

        for panel in self.swarm_panel_list:
            panel.clear()
        self.swarm_panel_list.clear()

    def clear(self):
        self.clear_swarms()
        for widget in self.tk_widgets.values():
            widget.destroy()
        self.tk_widgets.clear()


class Controller:
    def __init__(self, engine, display, commander_list=[]):
        self.engine = engine
        self.display = display
        self.root = tk.Tk()
        self.root.title("Controller")
        self.commander_list = commander_list

        self.engine_frame = tk.Frame(self.root)
        self.pause_btn = tk.Button(self.engine_frame, text="Pause Engine", command=self.puase_engine)
        self.play_btn = tk.Button(self.engine_frame, text="Play Engine", command=self.play_engine)
        self.switch_btn = tk.Button(self.engine_frame, text="Switch view", command=self.switch_view)
        self.pause_btn.pack()
        self.play_btn.pack()
        self.switch_btn.pack()
        self.engine_frame.pack()

        self.commander_frame = tk.Frame(self.root)
        self.commander_panel_list = []
        for commander in self.commander_list:
            self.add_commander_control_panel(commander)
        self.commander_frame.pack()

    def start(self):
        self.tick_ms = int(1000 / self.display.fps)
        self.root.after(0, self.update)
        self.root.mainloop()

    def update(self):
        if self.display.running:
            start_time = time.time()
            self.display.update()
            elapsed_time = time.time() - start_time
            self.root.after(self.tick_ms - int(elapsed_time * 1000), self.update)

    def register_tk_update_cb(self, cb):
        self.tk_cb_list.append(cb)

    def add_commander(self, commander):
        self.commander_list.append(commander)
        self.add_commander_control_panel(commander)

    def remove_commander(self, commander):
        self.commander_list.remove(commander)
        self.remove_command_conrtol_panel(commander)

    def add_commander_control_panel(self, commander):
        self.commander_panel_list.append(VirtualCommanderPanel(self.commander_frame, commander, self.engine))

    def remove_command_conrtol_panel(self, commander):
        for panel in self.commander_panel_list:
            if panel.commander == commander:
                panel.clear()

    def puase_engine(self):
        self.engine.pause()

    def play_engine(self):
        self.engine.play()

    def switch_view(self):
        self.display.switch_view()