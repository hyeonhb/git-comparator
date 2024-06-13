from Display import Display
from Drone import Drone
import math
from Vector3D import Vector3D
from VirtualSimEngine import VirtualSimEngine
from Controller import *
from Swarm import Swarm
from CommanderBird import CommanderBird
from CommanderAnt import CommanderAnt

if __name__ == '__main__':
    engine = VirtualSimEngine()
    engine.start()

    display = Display(engine, width=1024, height=768, name="SwamRobot Display")
    display.start()

    app = Controller(engine, display)
    app.add_commander(CommanderAnt(engine))
    app.add_commander(CommanderAnt(engine))
    app.start()

    display.stop()
    engine.stop()