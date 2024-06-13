# 측면 디스플레이 테스트용

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
from CommanderAnt import CommanderAnt
from CommanderBird import CommanderBird

if __name__ == '__main__':
    engine = VirtualSimEngine()
    engine.start()

    drone1 = Drone(engine, "Drone1")
    drone2 = Drone(engine, "Drone2", position=Vector3D(300, 0, 300))
    drone3 = Drone(engine, "Drone3", position=Vector3D(500, 0, 500))
    drone4 = Drone(engine, "Drone4", position=Vector3D(600, 0, 200))
    drone5 = Drone(engine, "Drone5", position=Vector3D(500, 760, 500))

    print(drone1.position)
    print(drone2.position)

    drone1.move(Vector3D(100.0, 0.0, 100.0))
    drone2.move(Vector3D(-50.0, 0.0, 100.0))

    drone3.rotate(Vector3D(0.0, - (math.pi), 0.0))
    drone4.move(Vector3D(0.0, 5.0, 0.0))
    drone5.move(Vector3D(0.0, -5.0, 0.0))

    swarm1 = Swarm()
    swarm1.add_robot(drone1)
    swarm1.add_robot(drone2)
    swarm1.add_robot(drone3)
    swarm1.add_robot(drone4)
    swarm1.add_robot(drone5)

    commander_bird = CommanderBird(engine)
    commander_bird.add_swarm(swarm1)
    
    robotcar1 = RobotCar(engine, "Robotcar1")
    robotcar2 = RobotCar(engine, "Robotcar2", position=Vector3D(300, 0, 300))
    robotcar3 = RobotCar(engine, "Robotcar3", position=Vector3D(300, 0, 300))

    robotcar1.move(Vector3D(100, 0, 100))
    robotcar2.move(Vector3D(-100, 0, -100))

    swarm2 = Swarm()
    swarm2.add_robot(robotcar1)
    swarm2.add_robot(robotcar2)
    swarm2.add_robot(robotcar3)

    commander_ant = CommanderAnt(engine)
    commander_ant.add_swarm(swarm2)

    display = Display(engine, width=1024, height=768, name="SwamRobot Display")
    display.start()

    app = Controller(engine, display)
    app.add_commander(commander_bird)
    app.add_commander(commander_ant)
    app.start()

    engine.stop()