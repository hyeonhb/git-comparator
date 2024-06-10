from IVirtualObject import VirtualObjectConfig
from Vector3D import Vector3D
from VirtualSwarmRobot import VirtualSwarmRobot

class RobotCar(VirtualSwarmRobot):
    def __init__(self, engine, name="RobotCar", position=Vector3D(), orientation=Vector3D()):
        super().__init__(engine, name, position, orientation)
        self.config = VirtualObjectConfig(width=10, height=3, depth=10, tag="RobotCar")

    def move(self, velocity):
        velocity.y = 0.0 #y축으로 이동할 수 없음(비행 X)
        return super().move(velocity)