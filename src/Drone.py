from Vector3D import Vector3D
from VirtualSwarmRobot import VirtualSwarmRobot

class Drone(VirtualSwarmRobot):
    def __init__(self, engine, name="", position=Vector3D(), orientation=Vector3D()):
        super().__init__(engine, name, position, orientation)

    def update(self):
        print(f"Test Drone[{self.position}]")
        return super().update()