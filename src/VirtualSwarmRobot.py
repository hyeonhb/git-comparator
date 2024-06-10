from IVirtualObject import IVirtualObject
import math
from SwarmRobot import SwarmRobot
import time
import threading
from Vector3D import Vector3D

class VirtualSwarmRobot(IVirtualObject, SwarmRobot):
    def __init__(self, engine, name="", position=Vector3D(), orientation=Vector3D()):
        IVirtualObject.__init__(self, engine, name)
        SwarmRobot.__init__(self, position, orientation)
        self.lock = threading.Lock()

    def rotate(self, angular_velocity):
        with self.lock:
            super().rotate(angular_velocity)

    def move(self, velocity):
        with self.lock:
            super().move(velocity)

    def stop(self):
        with self.lock:
            super().stop()

    def update_orientation(self):
        with self.lock:
            if self.angular_velocity != 0.0:
                self.orientation = self.orientation + (self.angular_velocity * self.engine.delta_time)
                self.orientation = self.orientation % (2 * math.pi) #방향은 2PI의 주기를 가짐

    def update_position(self):
        with self.lock:
            if self.velocity != 0.0:
                self.position = self.position + (self.velocity * self.engine.delta_time)

    def update(self):
        self.update_orientation()
        self.update_position()