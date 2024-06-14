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

    border_start = Vector3D()
    border_end = Vector3D(display.screen_width, display.screen_height, display.screen_height)

    app = Controller(engine, display)
    app.add_commander(CommanderAnt(engine, border_start, border_end))
    app.add_commander(CommanderBird(engine, border_start, border_end))
    app.start()

    display.stop()
    engine.stop()