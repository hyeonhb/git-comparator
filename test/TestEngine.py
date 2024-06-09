import sys
import os
# src 디렉토리를 시스템 경로에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import time
from VirtualSwarmRobot import VirtualSwarmRobot
from VirtualSimEngine import VirtualSimEngine

class TestRobot(VirtualSwarmRobot):
    def __init__(self, engine, name=""):
        super().__init__(engine, name)

    def update(self):
        print(f"Test calling update[{self.name}]")

if __name__ == '__main__':
    engine = VirtualSimEngine()
    robot1 = TestRobot(engine, "robot1")
    robot2 = TestRobot(engine, "robot2")

    engine.start()

    robot1.start()
    time.sleep(3)
    robot1.stop()

    time.sleep(2)

    robot2.start()
    time.sleep(1)
    engine.pause()
    time.sleep(3)
    engine.play()
    time.sleep(1)
    robot2.stop()

    engine.stop()