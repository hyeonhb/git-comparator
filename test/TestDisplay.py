import sys
import os
# src 디렉토리를 시스템 경로에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from Display import Display
from Drone import Drone
from Vector3D import Vector3D
from VirtualSimEngine import VirtualSimEngine

if __name__ == '__main__':
    engine = VirtualSimEngine()
    engine.start()

    drone1 = Drone(engine, "Drone1")
    drone2 = Drone(engine, "Drone2", position=Vector3D(300, 0, 300))

    print(drone1.position)
    print(drone2.position)

    drone1.move(Vector3D(100.0, 0.0, 100.0))
    drone2.move(Vector3D(-50.0, 0.0, 100.0))

    display = Display(engine, width=1024, height=768, name="SwamRobot Display")
    display.start()

    engine.stop()