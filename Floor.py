import pygame


class Floor(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.surface = pygame.Surface((width, 20))
        self.surface.fill((255, 0, 0))
        self.rectangle = self.surface.get_rect(center=(width/2, height - 10))
