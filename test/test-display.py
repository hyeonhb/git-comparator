import os
import pygame as pg 
import random as rd
from abc import ABC, abstractmethod

#현재 작업 디렉토리를 스크립트 파일의 디렉토리로 변경
script_dir = os.path.dirname(__file__)
os.chdir(script_dir)

# 현재 작업 디렉토리 확인
# print("현재 작업 디렉토리", os.getcwd())

# pygame 초기화
pg.init()

# 디스플레이 설정
screen_width = 1024
screen_height = 768
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Swarm Display Test")

# FPS 설정
clock = pg.time.Clock()
FPS = 60

# 이미지 로드 
og_bee_image = pg.image.load('bee.png') # 출처: https://www.flaticon.com/free-icon/bee_809154?term=bee&page=1&position=2&origin=search&related_id=809154
og_ant_image = pg.image.load('ant.png') # 출처: https://www.flaticon.com/free-icon/ant_534859?term=ant&page=1&position=1&origin=search&related_id=534859
bee_image = pg.transform.scale(og_bee_image, (30, 30))
ant_image = pg.transform.scale(og_ant_image, (15, 15))

# 테스트 클래스 
class Vector3D:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

class IRobot(ABC):
    def __init__(self, pos, vx, vy):
        self.pos = pos
        self.vx = vx
        self.vy = vy

    def update_position(self, screen_width, screen_height):
        self.pos.x += self.vx
        self.pos.y += self.vy

        # 화면 경계에 도달하면 반대 방향으로 이동
        if self.pos.x <= 0 or self.pos.x >= screen_width - 50:
            self.vx = -self.vx
        if self.pos.y <= 0 or self.pos.y >= screen_height - 50:
            self.vy = -self.vy

class Drone(IRobot):
    pass
class RobotCar(IRobot):
    pass

class Swarm:    
    def __init__(self):
        self.swarm_robot_list = []

    def add_robot(self, robot):
        self.swarm_robot_list.append(robot)

class ICommander(ABC):
    def __init__(self):
        self.swarm_list = []

    def add_swarm(self, swarm):
        self.swarm_list.append(swarm)    
    
class CommanderBee(ICommander): 
    pass
class CommanderAnt(ICommander):    
    pass

class Controller:
    def __init__(self):
        self.commander_list = []
    
    def add_commander(self, commander):
        self.commander_list.append(commander)
    
    # commander 를 생성하고 Controller 에 등록함.
    def create_and_add_commander(self, commander_class, robot_class, num_swarms, num_robots):
        commander = commander_class()                
        for _ in range(num_swarms): # 무리의 수 
            swarm = Swarm()
            for _ in range(num_robots): # 로봇의 수
                pos, vx, vy = create_random_position_and_velocity(screen_width, screen_height)
                robot = robot_class(pos, vx, vy)
                swarm.add_robot(robot)
        commander.add_swarm(swarm)
        self.add_commander(commander)

    # 로봇 위치 업데이트 및 표시
    def draw_robots(self, screen, image_mapping):
        for commander in self.commander_list:
            for key, info in image_mapping.items():
                if isinstance(commander, info["commander_class"]):
                    for swarm in commander.swarm_list:
                        for robot in swarm.swarm_robot_list:
                            robot.update_position(screen_width, screen_height)
                            screen.blit(info["image"], (robot.pos.x, robot.pos.y))

    def get_robot_info(self):
        pass

# 랜덤한 위치와 속도를 생성함.
def create_random_position_and_velocity(screen_width, screen_height):
    x = rd.randint(0, screen_width - 50)
    y = rd.randint(0, screen_height - 50)
    vx = rd.choice([-1, 1]) * rd.randint(1, 5)
    vy = rd.choice([-1, 1]) * rd.randint(1, 5)
    return Vector3D(x, y, 0), vx, vy

controller = Controller()

# 매핑 딕셔너리 - commander, robot_class, image 를 설정함.
commander_info = {
    "bee": { "commander_class": CommanderBee, "robot_class": Drone, "image": bee_image},
    "ant": { "commander_class": CommanderAnt, "robot_class": RobotCar, "image": ant_image}
}

# commander 생성 및 추가
for info in commander_info.values():
    controller.create_and_add_commander(info["commander_class"], info["robot_class"], 1, 10)

# 메인 루프
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()            

    screen.fill((255, 255, 255))  # 흰색 배경

    # 로봇들 그리기
    controller.draw_robots(screen, commander_info)

    pg.display.flip()
    clock.tick(FPS)