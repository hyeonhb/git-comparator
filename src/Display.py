import pygame
import time

class Display:
    def __init__(self, engine, width, height, fps=60, name=""):
        pygame.init()
        self.screen_width = width
        self.screen_height = height
        self.fps = fps
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(name)
        self.clock = pygame.time.Clock()
        self.running = True
        self.engine = engine

        self.tag_images = {
            'Drone': self.load_image('.\\resource\\free-icon-camera-drone-5524149.png'),
            'RobotCar': self.load_image('.\\resource\\free-icon-camera-drone-5524149.png'),
        }

    def load_image(self, image_path):
        return pygame.image.load(image_path)

    def start(self):
        try:
            while self.running:
                for event in pygame.event.get():
                    start_time = time.time()
                    if event.type == pygame.QUIT:
                        return
                self.screen.fill((255, 255, 255))

                object_list = self.engine.get_object_list()
                for object in object_list:
                    image = pygame.transform.scale(self.tag_images[object.config.tag], (object.config.width, object.config.depth))
                    self.screen.blit(image, (object.position.x, object.position.z))

                pygame.display.flip()
                self.clock.tick(self.fps)
                print(time.time() - start_time)
        finally:
            pygame.quit()

    def stop(self):
        self.running = False
