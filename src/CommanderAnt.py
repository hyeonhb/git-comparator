import math
import random
from Vector3D import Vector3D
from VirtualCommanderFlock import VirtualCommanderFlock

class CommanderAnt(VirtualCommanderFlock):
    def commander_start(self):
        print("Start Commander")

        # 모든 Boid의 velocity를 랜덤 지정
        for swarm in self.swarm_list:
            for boid in swarm.get_robot_list():
                print(f"start {boid.name}")
                random_velocity = Vector3D(x=random.uniform(-1, 1),
                                            z=random.uniform(-1, 1))
                boid.move(random_velocity)        
        self.is_running = True


    def get_distance_difference(self, current_boid, other):
        # 유클리디안 거리 (Euclidean Distance)
        # 거리차이 값에는 음수 개념이 없기 때문에 각 좌표 차이를 제곱해서 더해주고, 최종적으로는 제곱근 값을 리턴해준다.
        position_diff = (current_boid.position.x - other.position.x) ** 2 + (current_boid.position.z - other.position.z) ** 2
        return math.sqrt(position_diff)