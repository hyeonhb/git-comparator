from ICommander import ICommander
from DummytAnt import DummyAnt
import math
import pygame

# Flocking params
MAX_VELOCITY = 1.2
PERCEPTION_RADIUS = 50
SEPARATION_DISTANCE = 30

class CommanderAnt(ICommander):
    def __init__(self, swarm_list):
        self.is_running = False
        self.swarm_list = [
            [DummyAnt(), DummyAnt(), DummyAnt(), DummyAnt()],
            [DummyAnt(), DummyAnt()],
            [DummyAnt(), DummyAnt(), DummyAnt(), DummyAnt(), DummyAnt(), DummyAnt(), DummyAnt()],
        ]

    def commander_start(self):
        self.is_running = True

    def commander_play(self):
        self.is_running = True

    def commander_pause(self):
        self.is_running = False

    def commander_stop(self):
        self.swarm_list = [] # swarm_list 초기화
        self.is_running = False

    def get_next_velocity_list(self):
        if self.is_running == False:
            return False

        result = []

        for swarm in self.swarm_list:
            swram_velocity_list = []
            for current_boid in swarm:
                for other in swarm:
                    if other == current_boid:
                        continue
                    
                    average_velocity = pygame.Vector2(0, 0)
                    average_position = pygame.Vector2(0, 0)
                    average_separation = pygame.Vector2(0, 0)
                    neighbors_counter = 0

                    distance = self.get_distance_difference(current_boid, other)
                    if distance < PERCEPTION_RADIUS:
                        neighbors_counter += 1

                        average_velocity += other.velocity
                        average_position += other.position

                    if distance < SEPARATION_DISTANCE:
                        diff = self.position - other.position
                        diff.scale_to_length(1 / distance)

                        average_separation += diff

                if neighbors_counter > 0:
                    average_velocity /= neighbors_counter
                    average_position /= neighbors_counter
                    average_separation /= neighbors_counter

                current_boid.velocity += average_velocity * 0.08
                current_boid.velocity += average_position * 0.05
                current_boid.velocity -= average_separation * 0.12
                current_boid.velocity.scale_to_length(MAX_VELOCITY)
                
                swram_velocity_list.append(current_boid.velocity)
            
            result.append(swram_velocity_list)
        return result

    def get_distance_difference(self, current_boid, other):
        # 유클리디안 거리 (Euclidean Distance)
        # 거리차이 값에는 음수 개념이 없기 때문에 각 좌표 차이를 제곱해서 더해주고, 최종적으로는 제곱근 값을 리턴해준다.
        position_diff = (current_boid.position[0] - other.position[0]) ** 2 + (current_boid.position[1] - other.position[1]) ** 2
        return math.sqrt(position_diff)

