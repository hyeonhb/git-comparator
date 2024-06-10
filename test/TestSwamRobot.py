import sys
import os
# src 디렉토리를 시스템 경로에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from VirtualSimEngine import VirtualSimEngine
from Drone import Drone
from Swarm import Swarm
import time
from Vector3D import Vector3D

if __name__ == '__main__':
    engine = VirtualSimEngine()
    swarm1 = Swarm()

    swarm1.add_robot(Drone(engine, "drone1"))
    #swarm1.add_robot(Drone(engine, "drone2"))
    #swarm1.add_robot(Drone(engine, "drone3"))

    engine.start()
    swarm1.move(Vector3D(1.0, 0, 0))
    time.sleep(3)

    engine.pause()
    time.sleep(1)

    engine.play()
    time.sleep(3)

    engine.stop()
    
