from IVirtualObject import VirtualObjectConfig
from Vector3D import Vector3D
from VirtualSwarmRobot import VirtualSwarmRobot

class RobotCar(VirtualSwarmRobot):
    def __init__(self, engine, name="RobotCar", position=Vector3D(), orientation=Vector3D()):
        super().__init__(engine, name, position, orientation)
        self.config = VirtualObjectConfig(width=24, height=12, depth=24, tag="RobotCar")

    def move(self, velocity):
        velocity.y = 0.0 #y축으로 이동할 수 없음(비행 X)
        return super().move(velocity)

    def set_position(self, position):
        position.y = 0.0 #y축 좌표를 지정할 수 없음(비행 x)
        return super().set_position(position)