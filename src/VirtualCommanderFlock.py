import math
import random
from ICommander import ICommander
from IVirtualObject import IVirtualObject
from Vector3D import Vector3D

class VirtualCommanderFlock(ICommander, IVirtualObject):
    # Flocking params
    MAX_VELOCITY = 1.2
    PERCEPTION_RADIUS = 50
    SEPARATION_DISTANCE = 30

    def __init__(self, engine,
                 border_start=Vector3D(-500, -500, -500),
                 border_end=Vector3D(500, 500, 500),
                 border_pad=Vector3D(10, 10, 10)):
        IVirtualObject.__init__(self, engine, "Commander")
        ICommander.__init__(self)

        self.is_running = False
        self.border_pad = border_pad
        self.border_start = border_start - border_pad
        self.border_end = border_end + border_pad

    def commander_init(self):
        print("Init Commander")

        self.commander_stop()
        # 모든 Boid의 position을 랜덤 지정
        for swarm in self.swarm_list:
            for boid in swarm.get_robot_list():
                print(f"init {boid.name}")
                random_position = Vector3D(x=random.uniform(self.border_start.x, self.border_end.x),
                                            y=random.uniform(self.border_start.y, self.border_end.y),
                                            z=random.uniform(self.border_start.z, self.border_end.z))
                boid.set_postion(random_position)

        self.is_running = False

    def commander_start(self):
        print("Start Commander")

        # 모든 Boid의 velocity를 랜덤 지정
        for swarm in self.swarm_list:
            for boid in swarm.get_robot_list():
                print(f"start {boid.name}")
                random_velocity = Vector3D(x=random.uniform(-1, 1),
                                            y=random.uniform(-1, 1),
                                            z=random.uniform(-1, 1))
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
            for boid in swarm.get_robot_list():
                print(f"stop {boid.name}")
                boid.stop()

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
                    if distance < self.PERCEPTION_RADIUS:
                        neighbors_counter += 1

                        average_velocity += other.velocity
                        average_position += other.position

                    if distance < self.SEPARATION_DISTANCE:
                        diff = current_boid.position - other.position
                        diff = diff.scale_to_length(1 / max(distance, 0.00000001))

                        average_separation += diff

                if neighbors_counter > 0:
                    average_velocity /= neighbors_counter
                    average_position /= neighbors_counter
                    average_separation /= neighbors_counter

                next_velocity = current_boid.velocity
                next_velocity += average_velocity * 0.08
                next_velocity += average_position * 0.05
                next_velocity -= average_separation * 0.12
                next_velocity = next_velocity.scale_to_length(self.MAX_VELOCITY)

                # 실제 Boid 위치 셋업
                angle_radians = math.atan2(next_velocity.z, next_velocity.x)  # 라디안 단위의 각도
                current_boid.set_orientation(Vector3D(y=angle_radians))
                self.reflect_border(current_boid, next_velocity)
                current_boid.move(next_velocity * self.engine.tick)

    # border에 충돌할 경우 방향을 전환
    def reflect_border(self, boid, next_velocity):
        if boid.position.x < self.border_start.x or boid.position.x > self.border_end.x:
            next_velocity.x = -next_velocity.x
        if boid.position.y < self.border_start.y or boid.position.y > self.border_end.y:
            next_velocity.y = -next_velocity.y
        if boid.position.z < self.border_start.z or boid.position.z > self.border_end.z:
            next_velocity.z = -next_velocity.z