import sys
import os
# src 디렉토리를 시스템 경로에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

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

    drone1 = Drone(engine, "Drone1")
    drone2 = Drone(engine, "Drone2", position=Vector3D(300, 0, 300))
    drone3 = Drone(engine, "Drone2", position=Vector3D(500, 0, 500))

    print(drone1.position)
    print(drone2.position)

    drone1.move(Vector3D(100.0, 0.0, 100.0))
    drone2.move(Vector3D(-50.0, 0.0, 100.0))

    drone3.rotate(Vector3D(0.0, - (math.pi), 0.0))

    swarm1 = Swarm()
    swarm1.add_robot(drone1)
    swarm1.add_robot(drone2)
    swarm1.add_robot(drone3)

    commander_ant = CommanderAnt(engine)
    commander_ant.add_swarm(swarm1)

    display = Display(engine, width=1024, height=768, name="SwamRobot Display")
    display.start()

    app = Controller(engine, display)
    app.add_commander(commander_ant)
    app.start()

    engine.stop()