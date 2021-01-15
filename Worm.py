import random
import pygame


class Worm(pygame.sprite.Sprite):
    def __init__(self, WIDTH, HEIGHT, COLOR):
        super().__init__()
        self.health = 100
        self.surface = pygame.Surface((20, 20))
        self.surface.fill(COLOR)
        self.rectangle = self.surface.get_rect(center=(random.randint(0, WIDTH), HEIGHT-40))
