import math
import random
from ICommander import ICommander
from IVirtualObject import IVirtualObject
from Vector3D import Vector3D

class VirtualCommanderFlock(ICommander, IVirtualObject):
    # Flocking params
    MAX_VELOCITY = 1.2
    PERCEPTION_RADIUS = 60
    SEPARATION_DISTANCE = 35
    PAD_DISTNACE = 40

    def __init__(self, engine,
                 border_start=Vector3D(-500, -500, -500),
                 border_end=Vector3D(500, 500, 500),
                 border_pad=Vector3D()):
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
                boid.set_position(random_position)

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
        pass

    # border에 충돌할 경우 방향을 전환
    def reflect_border(self, boid, next_velocity):

        #if boid.position.x <= self.border_start.x or boid.position.x >= self.border_end.x:
        #    next_velocity.x = -next_velocity.x
        #if boid.position.y <= self.border_start.y or boid.position.y >= self.border_end.y:
        #    next_velocity.y = -next_velocity.y
        #if boid.position.z <= self.border_start.z or boid.position.z >= self.border_end.z:
        #    next_velocity.z = -next_velocity.z

        min_x = min(boid.position.x - self.border_start.x, self.border_end.x - boid.position.x)
        min_y = min(boid.position.y - self.border_start.y, self.border_end.y - boid.position.y)
        min_z = min(boid.position.z - self.border_start.z, self.border_end.z - boid.position.z)

        if min_x < self.PAD_DISTNACE:
            next_velocity.x += (self.PAD_DISTNACE - min_x) / self.PAD_DISTNACE * (1 if boid.position.x < (self.border_start.x + self.border_end.x) / 2 else -1)
        if min_y < self.PAD_DISTNACE:
            next_velocity.y += (self.PAD_DISTNACE - min_y) / self.PAD_DISTNACE * (1 if boid.position.y < (self.border_start.y + self.border_end.y) / 2 else -1)
        if min_z < self.PAD_DISTNACE:
            next_velocity.z += (self.PAD_DISTNACE - min_z) / self.PAD_DISTNACE * (1 if boid.position.z < (self.border_start.z + self.border_end.z) / 2 else -1)

        return next_velocity

    def get_portal_posistion(self, boid):
        position = Vector3D() + boid.position
        if position.x < self.border_start.x:
            position.x = self.border_end.x
        elif position.x > self.border_end.x:
            position.x = self.border_start.x

        if position.y < self.border_start.y:
            position.y = self.border_end.y
        elif position.y > self.border_end.y:
            position.y = self.border_start.y

        if position.z < self.border_start.z:
            position.z = self.border_end.z
        elif position.z > self.border_end.z:
            position.z = self.border_start.z

        return position