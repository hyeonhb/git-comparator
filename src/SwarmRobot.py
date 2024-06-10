from ISwarm import ISwarm
from Vector3D import Vector3D

class SwarmRobot(ISwarm):
    def __init__ (self, position=Vector3D(), orientation=Vector3D()):
        super().__init__(position, orientation)
        self.velocity = Vector3D()
        self.angular_velocity = Vector3D()

    def rotate(self, angular_velocity):
        self.angular_velocity = angular_velocity

    def move(self, velocity):
        self.velocity = velocity

    def stop(self):
        self.angular_velocity = Vector3D()
        self.velocity = Vector3D()