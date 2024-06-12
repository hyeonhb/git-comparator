import random
import pygame

class DummyAnt:
    def __init__(self):
        self.position = pygame.Vector3(random.uniform(0, 1024), 0, random.uniform(0, 768))
        self.velocity = pygame.Vector3(random.uniform(-1, 1), 0, random.uniform(-1, 1))