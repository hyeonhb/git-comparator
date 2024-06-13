import math
import pygame
import os
import time

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
        self.name=name

        self.view_mode = True # True : Top View,  False : Side View

        # resource 폴더 경로 구하기
        current_path = os.path.dirname(__file__)
        resource_path = os.path.join(current_path, os.pardir, 'resource')
        self.tag_images = {
            'Drone': self.load_image(resource_path, 'free-icon-camera-drone-5524149.png'),
            'RobotCar': self.load_image(resource_path, 'free-icon-camera-drone-5524149.png'),
        }

    def load_image(self, directory, fileName):
        image_path = os.path.join(directory, fileName)
        return pygame.transform.rotate(pygame.image.load(image_path), 90)

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

    def draw(self):
        for obj in self.engine.get_object_list():
            #obj list를 제대로 못가져 오는 문제 존재
            #왜 copy와 원본 리스트 간의 차이가 존재 하는지 확인이 필요함
            if not obj.config.tag in self.tag_images.keys():
                return

            # image 그리기
            image = self.tag_images[obj.config.tag]
            angle = math.degrees(obj.orientation.y)

            # position을 간단히 변수로 사용
            x = obj.position.x
            y = obj.position.y
            z = obj.position.z

            # y값에 따라 스케일 조정
            scale_factor = 1.0015 ** y

            if self.view_mode:  # Top view
                scale_x = (obj.config.width / image.get_width()) * scale_factor
                scale_y = (obj.config.depth / image.get_height()) * scale_factor
                scale = (scale_x + scale_y) / 2  # 평균 비율 사용
                image = pygame.transform.rotozoom(image, angle, scale)
                rect = image.get_rect(center=(x, z))
                pygame.draw.rect(self.screen, (0, 255, 0), rect, 1)
                self.screen.blit(image, rect.topleft)

                # 오브젝트의 좌표를 기준으로 Direction Line 그리기
                self.line_length = 20 * scale_factor
                x_axis_start = (x, z)
                x_axis_end = (x + self.line_length, z)
                y_axis_start = (x, z)
                y_axis_end = (x, z + self.line_length)
                center = (x, z)

                # 회전된 직선 그리기
                self.draw_rotated_line(self.screen, (255, 0, 0), x_axis_start, x_axis_end, -obj.orientation.y, center, 2)
                self.draw_rotated_line(self.screen, (0, 0, 255), y_axis_start, y_axis_end, -obj.orientation.y, center, 2)

            else:  # Side view
                scale_x = (obj.config.width / image.get_width())
                scale_y = (obj.config.height / image.get_height())
                scale = (scale_x + scale_y) / 2  # 평균 비율 사용
                image = pygame.transform.rotozoom(image, 0, scale)
                rect = image.get_rect(center=(x, self.screen_height - y))
                pygame.draw.rect(self.screen, (0, 255, 0), rect, 1)
                self.screen.blit(image, rect.topleft)

                # 오브젝트의 좌표를 기준으로 Direction Line 그리기
                self.line_length = 20
                x_axis_start = (x, self.screen_height - y)
                x_axis_end = (x + self.line_length, self.screen_height - y)
                y_axis_start = (x, self.screen_height - y)
                y_axis_end = (x, self.screen_height - y - self.line_length)
                center = (x, self.screen_height - y)

                # 회전된 직선 그리기
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
            #버튼 클릭 이벤트
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.switch_view_button.is_clicked(event.pos):
                    self.switch_view_button.click()
        
        #start_time = time.time()
        self.screen.fill((255, 255, 255))

        self.draw()
        self.switch_view_button.draw(self.screen)

        pygame.display.flip()
        #self.clock.tick(self.fps)
        #print(time.time() - start_time)

    def stop(self):
        self.running = False
        pygame.quit()
