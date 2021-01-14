import random
import pygame


class Worm(pygame.sprite.Sprite):
    def __init__(self, WIDTH, HEIGHT):
        super().__init__()
        self.health = 100
        self.surface = pygame.Surface((30, 30))
        self.surface.fill((127, 0, 0))
        self.rectangle = self.surface.get_rect(center=(random.randint(0, 1920), 600-35))
