from ICommander import ICommander
from IVirtualObject import IVirtualObject
import math
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

    def commander_start(self):
        print("Start Commander")
        self.is_running = True

    def commander_play(self):
        print("Play Commander")
        self.is_running = True

    def commander_pause(self):
        print("Pause Commander")
        self.is_running = False

    def commander_stop(self):
        print("Stop Commander")
        self.is_running = False

    def final(self):
        self.set_next_velocity()

    def set_next_velocity(self):
        if self.is_running == False:
            return False

        result = []

        for swarm in self.swarm_list:
            swram_velocity_list = []
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
                
                swram_velocity_list.append(next_velocity)

                # 실제 Boid 위치 셋업
                #current_boid.rotate(next_velocity)
                current_boid.move(next_velocity)
            
            result.append(swram_velocity_list)
        return result

    def get_distance_difference(self, current_boid, other):
        # 유클리디안 거리 (Euclidean Distance)
        # 거리차이 값에는 음수 개념이 없기 때문에 각 좌표 차이를 제곱해서 더해주고, 최종적으로는 제곱근 값을 리턴해준다.
        position_diff = (current_boid.position.x - other.position.x) ** 2 + (current_boid.position.z - other.position.z) ** 2
        return math.sqrt(position_diff)

