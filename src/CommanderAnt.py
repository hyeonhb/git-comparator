import math
import random
from Vector3D import Vector3D
from VirtualCommanderFlock import VirtualCommanderFlock

class CommanderAnt(VirtualCommanderFlock):
    def __init__(self, engine, border_start, border_end, border_pad=Vector3D()):
        super().__init__(engine, border_start, border_end, border_pad, name="Commander Ant")

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

    def set_next_velocity(self):
        if self.is_running == False:
            return False
    def set_next_velocity(self):
        if not self.is_running:
            return False

        for swarm in self.swarm_list:
            next_values = []
            robot_list = swarm.get_robot_list()
            for current_boid in robot_list:
                neighbors_counter = 0
                close_counter = 0
                average_velocity = Vector3D()
                average_position = Vector3D()
                average_separation = Vector3D()

                for other in robot_list:
                    if other == current_boid:
                        continue

                    distance = self.get_distance_difference(current_boid, other)
                    if distance < self.PERCEPTION_RADIUS:
                        neighbors_counter += 1
                        average_velocity += other.velocity
                        average_position += other.position

                    if distance < self.SEPARATION_DISTANCE:
                        close_counter += 1
                        diff = current_boid.position - other.position
                        diff.y = 0.0
                        diff = diff.scale_to_length(1 / max(distance, 0.000001))
                        average_separation += diff

                if neighbors_counter > 0:
                    average_velocity /= neighbors_counter
                    average_position /= neighbors_counter
                if close_counter > 0:
                    average_separation /= close_counter

                delta_velocity = Vector3D()
                delta_velocity += average_velocity * 0.08
                delta_velocity += average_position * 0.05
                delta_velocity -= average_separation * 0.12

                next_velocity = current_boid.velocity + delta_velocity
                next_velocity.y = 0.0
                next_velocity = next_velocity.scale_to_length(self.MAX_VELOCITY)
                next_velocity *= self.engine.tick
                new_position = self.get_portal_posistion(current_boid)
                next_values.append((current_boid, next_velocity, new_position))

            for value in next_values:
                angle_radians = math.atan2(value[1].z, value[1].x)
                value[0].set_orientation(Vector3D(y=angle_radians))
                value[0].set_position(value[2])
                value[0].move(value[1])

    def get_distance_difference(self, current_boid, other):
        # 유클리디안 거리 (Euclidean Distance)
        # 거리차이 값에는 음수 개념이 없기 때문에 각 좌표 차이를 제곱해서 더해주고, 최종적으로는 제곱근 값을 리턴해준다.
        position_diff = (current_boid.position.x - other.position.x) ** 2 + (current_boid.position.z - other.position.z) ** 2
        return math.sqrt(position_diff)