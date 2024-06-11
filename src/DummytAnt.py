import random
import pygame

class DummyAnt:
    def __init__(self):
        self.position = pygame.Vector2(random.uniform(0, 1024), random.uniform(0, 768))
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))