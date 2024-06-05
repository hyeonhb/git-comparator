import pygame
import threading
import time
from pyrr import Vector3

class VirtualRobotEngine:
    def __init__(self):
        self.running = False
        self.lock = threading.Lock()
        self.objects = []  # 등록된 객체 리스트

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()

    def run(self):
        while self.running:
            start_time = time.time()
            self.update_physics()
            elapsed_time = time.time() - start_time
            sleep_time = max(0, (1/60) - elapsed_time)
            time.sleep(sleep_time)

    def update_physics(self):
        with self.lock:
            for obj in self.objects:
                obj.update()
            print("Updating physics for all objects...")

    def register_object(self, obj):
        with self.lock:
            self.objects.append(obj)
            print(f"Registered object: {obj}")

    def get_objects(self):
        with self.lock:
            return self.objects.copy()

class VirtualRobot:
    def __init__(self, engine, name, position):
        self.name = name
        self.engine = engine
        self.engine.register_object(self)
        self.position = Vector3(position)  # 로봇의 초기 위치
        self.velocity = Vector3([0.0, 0.0, 0.0])  # 로봇의 초기 속도
        self.state = {}  # 로봇의 상태를 저장할 딕셔너리
        self.state['position'] = self.position

    def move(self, velocity):
        self.velocity = Vector3(velocity)

    def update(self):
        # 로봇의 상태 업데이트
        self.position += self.velocity * (1/60)  # 1/60초 동안의 이동
        print(f"Updating robot: {self.name}, Position: {self.position}")
        self.state['position'] = self.position
        

# Pygame 초기화
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# 시뮬레이션 엔진 생성 및 시작
engine = VirtualRobotEngine()
engine.start()

# 로봇 객체 생성 및 엔진에 등록
robot1 = VirtualRobot(engine, "Robot1", [-1.0, -1.0, -1.0])
robot2 = VirtualRobot(engine, "Robot2", [1.0, 1.0, 1.0])

robot2.move([1.0, 1.0, 1.0])

running = True
while running:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 물리 엔진 데이터 가져오기
    objects = engine.get_objects()

    # 화면 업데이트 (물리 엔진 데이터를 사용하여 화면에 그리기)
    screen.fill((0, 0, 0))  # 화면을 검은색으로 채우기

    # 예제: 로봇의 이름과 위치를 화면에 표시
    font = pygame.font.Font(None, 36)
    y = 50
    for obj in objects:
        position = obj.state['position']
        text = f"{obj.name} - Position: ({position.x:.2f}, {position.y:.2f}, {position.z:.2f})"
        position_text = font.render(text, True, (255, 255, 255))
        screen.blit(position_text, (50, y))
        y += 50

    pygame.display.flip()

    # 60 FPS로 유지
    clock.tick(60)

# Pygame 종료
pygame.quit()

# 시뮬레이션 엔진 종료
engine.stop()