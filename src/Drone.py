from IVirtualObject import VirtualObjectConfig
from Vector3D import Vector3D
from VirtualSwarmRobot import VirtualSwarmRobot

class Drone(VirtualSwarmRobot):
    def __init__(self, engine, name="", position=Vector3D(), orientation=Vector3D()):
        super().__init__(engine, name, position, orientation)
        self.config = VirtualObjectConfig(width=24, height=12, depth=24, tag="Drone")