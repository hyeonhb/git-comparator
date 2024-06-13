import math
import pygame
import os
from Vector3D import Vector3D

class Button:
    def __init__(self, x, y, w, h, text, callback):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback
        self.font = pygame.font.Font(None, 36)
        self.color = (0, 0, 0)
        self.bg_color = (255, 255, 255)

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        text_surf = self.font.render(self.text, True, self.color)
        screen.blit(text_surf, (self.rect.x + (self.rect.width - text_surf.get_width()) // 2,
                                self.rect.y + (self.rect.height - text_surf.get_height()) // 2))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def click(self):
        self.callback()

class Display:
    def __init__(self, engine, width, height, fps=60, name=""):
        self.screen_width = width
        self.screen_height = height
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.running = False
        self.engine = engine
        self.name = name
        self.camera_position = Vector3D(0, 500, 1000)
        self.view_mode = True  # True: Top View, False: Side View
        self.previous_positions = {}
        self.image_cache = {}  # 이미지 캐시 추가
        # resource 폴더 경로 구하기
        current_path = os.path.dirname(__file__)
        resource_path = os.path.join(current_path, os.pardir, 'resource')
        self.tag_images = {
            'Drone': self.load_image(resource_path, 'drone_top_view.png', 'drone_side_view.png'),
            'RobotCar': self.load_image(resource_path, 'robotcar_top_view.png', 'robotcar_side_view.png')
        }

    def load_image(self, directory, top_view_file, side_view_file):
        top_view_image = pygame.transform.rotate(pygame.image.load(os.path.join(directory, top_view_file)), 90)
        side_view_image = pygame.image.load(os.path.join(directory, side_view_file))
        return {'top': top_view_image, 'side': side_view_image}

    def rotate_point(self, px, py, angle):
        new_x = px * math.cos(angle) - py * math.sin(angle)
        new_y = px * math.sin(angle) + py * math.cos(angle)
        return new_x, new_y

    def draw_rotated_line(self, screen, color, start_pos, end_pos, angle, center, width):
        rotated_start = self.rotate_point(start_pos[0] - center[0], start_pos[1] - center[1], angle)
        rotated_end = self.rotate_point(end_pos[0] - center[0], end_pos[1] - center[1], angle)

        rotated_start = (rotated_start[0] + center[0], rotated_start[1] + center[1])
        rotated_end = (rotated_end[0] + center[0], rotated_end[1] + center[1])

        pygame.draw.line(screen, color, rotated_start, rotated_end, width)

    def switch_view(self):
        self.view_mode = not self.view_mode

    def calculate_angel(self, dx, dz):
        angle = math.atan2(dz, dx)
        angle = math.degrees(angle)
        angle = (angle + 90) % 360
        return angle

    def calculate_perspective_scale(self, y):
        camera_y = self.camera_position.y
        distance = camera_y - y
        perspective_scale = camera_y / (distance + camera_y)
        return perspective_scale

    def draw(self):
        for obj in self.engine.get_object_list():
            if obj.config.tag not in self.tag_images:
                continue

            x = obj.position.x
            y = obj.position.y
            z = obj.position.z

            if obj not in self.previous_positions:
                self.previous_positions[obj] = Vector3D(x, y, z)

            dx = x - self.previous_positions[obj].x
            dz = z - self.previous_positions[obj].z

            self.previous_positions[obj] = Vector3D(x, y, z)

            # View mode와 이동 방향에 따라 각도와 반전 상태 결정
            if self.view_mode:  # Top view
                angle = self.calculate_angel(dx, dz)
                flip_image = False  # Top view에서는 반전 없음
                scale_factor = self.calculate_perspective_scale(y)
                if obj.config.tag == 'RobotCar':
                    scale_factor += 5
                elif obj.config.tag == 'Drone':
                    scale_factor += 0.4
            else:  # Side view
                angle = 0
                flip_image = dx > 0  # 오른쪽으로 이동할 때 이미지를 반전
                scale_factor = 3  # Side view에서는 고정된 scale factor 사용

            # 캐시 키에 view mode와 flip 상태 포함
            cache_key = (obj.config.tag, angle, scale_factor, self.view_mode, flip_image)
            if cache_key not in self.image_cache:
                image = self.tag_images[obj.config.tag]['top' if self.view_mode else 'side']
                scale_x = (obj.config.width / image.get_width()) * scale_factor
                scale_y = (obj.config.depth / image.get_height()) * scale_factor if self.view_mode else (obj.config.height / image.get_height()) * scale_factor
                scale = (scale_x + scale_y) / 2
                rotated_image = pygame.transform.rotozoom(image, angle if self.view_mode else 0, scale)
                if not self.view_mode and flip_image:
                    rotated_image = pygame.transform.flip(rotated_image, True, False)  # 이미지 좌우 반전
                self.image_cache[cache_key] = rotated_image
            else:
                rotated_image = self.image_cache[cache_key]

            rect = rotated_image.get_rect(center=(x, z) if self.view_mode else (x, self.screen_height - y))
            if not self.view_mode:
                y_offset = -20 if y == 0 else 0  # y가 0일 때 이미지를 약간 위로 이동
                rect = rotated_image.get_rect(center=(x, self.screen_height - y + y_offset))

            pygame.draw.rect(self.screen, (0, 255, 0), rect, 1)
            self.screen.blit(rotated_image, rect.topleft)

            self.draw_direction_lines(x, y, z, scale_factor, obj)

    def draw_direction_lines(self, x, y, z, scale_factor, obj):
        if self.view_mode:  # Top view
            self.line_length = 20 * scale_factor
            x_axis_start = (x, z)
            x_axis_end = (x + self.line_length, z)
            y_axis_start = (x, z)
            y_axis_end = (x, z + self.line_length)
            center = (x, z)
            self.draw_rotated_line(self.screen, (255, 0, 0), x_axis_start, x_axis_end, -obj.orientation.y, center, 2)
            self.draw_rotated_line(self.screen, (0, 0, 255), y_axis_start, y_axis_end, -obj.orientation.y, center, 2)
        else:  # Side view
            self.line_length = 20
            x_axis_start = (x, self.screen_height - y)
            x_axis_end = (x + self.line_length, self.screen_height - y)
            y_axis_start = (x, self.screen_height - y)
            y_axis_end = (x, self.screen_height - y - self.line_length)
            center = (x, self.screen_height - y)
            self.draw_rotated_line(self.screen, (255, 0, 0), x_axis_start, x_axis_end, 0, center, 2)
            self.draw_rotated_line(self.screen, (0, 0, 255), y_axis_start, y_axis_end, 0, center, 2)

    def start(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(self.name)
        self.switch_view_button = Button(50, 20, 100, 50, 'Switch View', self.switch_view)
        self.running = True

    def update(self):
        if not self.running:
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()
                return
            # 버튼 클릭 이벤트
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.switch_view_button.is_clicked(event.pos):
                    self.switch_view_button.click()

        # start_time = time.time()
        self.screen.fill((255, 255, 255))

        self.draw()
        self.switch_view_button.draw(self.screen)

        pygame.display.flip()
        # self.clock.tick(self.fps)
        # print(time.time() - start_time)

    def stop(self):
        self.running = False
        pygame.quit()
