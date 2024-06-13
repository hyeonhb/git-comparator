import math
import pygame
import os
from Vector3D import Vector3D

class Display:
    def __init__(self, engine, width, height, fps=60, name=""):
        self.screen_width = width
        self.screen_height = height
        self.origin_x = self.screen_width / 2
        self.origin_y = self.screen_height / 2
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.running = False
        self.engine = engine
        self.name=name                
        self.camera_position = Vector3D(0, 0, self.screen_height)
        self.view_mode = True # True : Top View,  False : Side View

        # resource 폴더 경로 구하기
        current_path = os.path.dirname(__file__)
        resource_path = os.path.join(current_path, os.pardir, 'resource')
        self.tag_images = {
            'Drone': { "top":pygame.transform.rotate(self.load_nbit_image(resource_path, 'drone_top_view.png', 64), -90),
                        "side":self.load_nbit_image(resource_path,'drone_side_view.png', 64)},            
            'RobotCar': { "top":pygame.transform.rotate(self.load_nbit_image(resource_path, 'robotcar_top_view.png', 64), -90),
                            "side":self.load_nbit_image(resource_path,'robotcar_side_view.png', 64)}
        }

    def load_scaled_image(self, directory, file, scale_factor):
        image = pygame.image.load(os.path.join(directory, file))
        original_size = image.get_size()
        new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
        return pygame.transform.scale(image, new_size)

    def load_nbit_image(self, directory, file, n):
        image = pygame.image.load(os.path.join(directory, file))
        scale_factor = n / image.get_width()
        original_size = image.get_size()
        new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
        return pygame.transform.scale(image, new_size)
    
    def rotate_point(self, px, py, angle):
        new_x = px * math.cos(angle) - py * math.sin(angle)
        new_y = px * math.sin(angle) + py * math.cos(angle)
        return new_x, new_y

    def draw_rotated_line(self, screen, color, start_pos, end_pos, angle, center, width):
        rotated_start = self.rotate_point(start_pos[0] - center[0], start_pos[1] - center[1], -angle)
        rotated_end = self.rotate_point(end_pos[0] - center[0], end_pos[1] - center[1], -angle)
        
        rotated_start = (rotated_start[0] + center[0], rotated_start[1] + center[1])
        rotated_end = (rotated_end[0] + center[0], rotated_end[1] + center[1])

        pygame.draw.line(screen, color, rotated_start, rotated_end, width)

    def switch_view(self):
        self.view_mode = not self.view_mode

    def calculate_perspective_scale(self, x, camera):        
        distance = camera - x
        perspective_scale = camera / (distance + camera)
        return perspective_scale + 1

    def transform_y(self, y):
        return self.screen_height - y

    def draw(self):
        for obj in self.engine.get_object_list():
            if not obj.config.tag in self.tag_images.keys():
                continue            

            angle = math.degrees(obj.orientation.y)
            # 좌표계를 변환
            x = obj.position.x + self.origin_x
            y = obj.position.y + self.origin_y
            z = obj.position.z + self.origin_y

            if self.view_mode:  # Top view
                # y값에 따라 스케일 조정
                scale_factor = self.calculate_perspective_scale(y, self.camera_position.z)
                # image 그리기
                image = self.tag_images[obj.config.tag]['top']                
                scale_x = (obj.config.width / image.get_width())
                scale_y = (obj.config.depth / image.get_height())
                scale = (scale_x + scale_y) / 2  # 평균 비율 사용
                image = pygame.transform.rotozoom(image, angle, scale * scale_factor)
                rect = image.get_rect(center=(x, self.transform_y(z)))
                pygame.draw.rect(self.screen, (255, 255, 0), rect, 1)
                self.screen.blit(image, rect.topleft)

                # 오브젝트의 좌표를 기준으로 Direction Line 그리기
                self.line_length = 20 * scale_factor
                x_axis_start = (x, self.transform_y(z))
                x_axis_end = (x + self.line_length, self.transform_y(z))
                y_axis_start = (x, self.transform_y(z))
                y_axis_end = (x, self.transform_y(z + self.line_length))
                center = (x, self.transform_y(z))

                # 회전된 직선 그리기
                self.draw_rotated_line(self.screen, (255, 0, 0), x_axis_start, x_axis_end, obj.orientation.y, center, 2)
                self.draw_rotated_line(self.screen, (0, 0, 255), y_axis_start, y_axis_end, obj.orientation.y, center, 2)

            else:  # Side view
                # z값에 따라 스케일 조정
                scale_factor = self.calculate_perspective_scale(z, self.camera_position.z)
                # image 그리기
                image = self.tag_images[obj.config.tag]['side']                
                scale_x = (obj.config.width / image.get_width()) * scale_factor
                image = pygame.transform.rotozoom(image, 0, scale_x)

                rect = image.get_rect(center=(x, self.transform_y(y)))
                pygame.draw.rect(self.screen, (255, 255, 0), rect, 1)
                self.screen.blit(image, rect.topleft)

                # 오브젝트의 좌표를 기준으로 Direction Line 그리기
                self.line_length = 20 * scale_factor
                x_axis_start = (x, self.transform_y(y))
                x_axis_end = (x + self.line_length, self.transform_y(y))
                y_axis_start = (x, self.transform_y(y))
                y_axis_end = (x, self.transform_y(y + self.line_length))
                center = (x, self.transform_y(y))

                # 회전된 직선 그리기
                self.draw_rotated_line(self.screen, (255, 0, 0), x_axis_start, x_axis_end, 0, center, 2)
                self.draw_rotated_line(self.screen, (0, 255, 0), y_axis_start, y_axis_end, 0, center, 2)

    def start(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(self.name)
        self.running = True

    def update(self):
        if not self.running:
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()
                return            
        
        #start_time = time.time()
        self.screen.fill((255, 255, 255))

        self.draw()
        pygame.display.flip()
        #self.clock.tick(self.fps)
        #print(time.time() - start_time)

    def stop(self):
        self.running = False
        pygame.quit()
