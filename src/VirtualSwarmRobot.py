from IVirtualObject import IVirtualObject
from SwarmRobot import SwarmRobot

class VirtualSwarmRobot(IVirtualObject, SwarmRobot):
    def __init__(self, engine, name=""):
        super().__init__(engine, name)