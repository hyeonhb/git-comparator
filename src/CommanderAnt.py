import math
import random
from ICommander import ICommander
from IVirtualObject import IVirtualObject
from Vector3D import Vector3D

# Flocking params
MAX_VELOCITY = 1.2
PERCEPTION_RADIUS = 50
SEPARATION_DISTANCE = 30

class CommanderAnt(ICommander, IVirtualObject):
    def __init__(self, engine, swarm_list=[]):
        IVirtualObject.__init__(self, engine, "Commander")
        ICommander.__init__(self, swarm_list)

        self.is_running = False

    def commander_init(self):
        print("Init Commander")

        # 모든 Boid의 position을 랜덤 지정
        for swarm in self.swarm_list:
            for boid in swarm:
                random_position = Vector3D(random.uniform(0, 1024), 0, random.uniform(0, 768))
                boid.set_postion(random_position)

        self.is_running = False

    def commander_start(self):
        print("Start Commander")

        # 모든 Boid의 velocity를 랜덤 지정
        for swarm in self.swarm_list:
            for boid in swarm:
                random_velocity = Vector3D(random.uniform(-1, 1), 0, random.uniform(-1, 1))
                boid.move(random_velocity)

        self.is_running = True

    def commander_play(self):
        print("Play Commander")
        self.is_running = True

    def commander_pause(self):
        print("Pause Commander")
        self.is_running = False

    def commander_stop(self):
        print("Stop Commander")

        # 모든 Boid를 정지
        for swarm in self.swarm_list:
            for boid in swarm:
                stop_velocity = Vector3D(0, 0, 0)
                boid.move(stop_velocity)

        self.is_running = False

    def final(self):
        self.set_next_velocity()

    def set_next_velocity(self):
        if self.is_running == False:
            return False

        for swarm in self.swarm_list:
            robot_list = swarm.get_robot_list()
            for current_boid in robot_list:
                for other in robot_list:
                    if other == current_boid:
                        continue
                    
                    average_velocity = Vector3D()
                    average_position = Vector3D()
                    average_separation = Vector3D()
                    neighbors_counter = 0

                    distance = self.get_distance_difference(current_boid, other)
                    if distance < PERCEPTION_RADIUS:
                        neighbors_counter += 1

                        average_velocity += other.velocity
                        average_position += other.position

                    if distance < SEPARATION_DISTANCE:
                        diff = current_boid.position - other.position
                        diff.scale_to_length(1 / distance)

                        average_separation += diff

                if neighbors_counter > 0:
                    average_velocity /= neighbors_counter
                    average_position /= neighbors_counter
                    average_separation /= neighbors_counter

                next_velocity = current_boid.velocity
                next_velocity += average_velocity * 0.08
                next_velocity += average_position * 0.05
                next_velocity -= average_separation * 0.12
                next_velocity.scale_to_length(MAX_VELOCITY)

                # 실제 Boid 위치 셋업
                current_boid.set_orientation(next_velocity)
                current_boid.move(next_velocity)

                self.correct_position(current_boid, next_velocity)

    def get_distance_difference(self, current_boid, other):
        # 유클리디안 거리 (Euclidean Distance)
        # 거리차이 값에는 음수 개념이 없기 때문에 각 좌표 차이를 제곱해서 더해주고, 최종적으로는 제곱근 값을 리턴해준다.
        position_diff = (current_boid.position.x - other.position.x) ** 2 + (current_boid.position.z - other.position.z) ** 2
        return math.sqrt(position_diff)
    
    # 화면밖으로 나갈 경우, 반대편에서 등장하도록 포지션 보정
    def correct_position(boid, next_velocity):
        BOID_SIZE = 90
        next_position = boid.position + next_velocity

        if next_position.x < 0:
            boid.position.x = 1024 - BOID_SIZE
        if next_position.z < 0:
            boid.position.z = 768 - BOID_SIZE
        if next_position.x > 1024:
            boid.position.x = BOID_SIZE
        if next_position.z > 768:
            boid.position.z = BOID_SIZE
