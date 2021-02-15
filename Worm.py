import random
import pygame


class Worm(pygame.sprite.Sprite):
    def __init__(self, NUMBER, HEIGHT, WIDTH, COLOR, SCREEN):
        super().__init__()
        self.health = 100
        self.number = NUMBER
        self.x = random.randint(0, WIDTH)
        self.y = HEIGHT-800
        self.surface = pygame.Surface((20, 20))
        self.surface.fill(COLOR)
        self.rect = self.surface.get_rect(center=(self.x, self.y))
        self.displayScreen = SCREEN
        self.color = COLOR
        self.font = pygame.font.SysFont(None, 15)
        self.movingSpeed = 2
        self.mask = pygame.mask.from_surface(self.surface)

    def selected(self):
        self.draw_text("Worm " + str(self.number), self.color, self.x-20, self.y-30)

    def draw_text(self, text, color, x, y):
        textobj = self.font.render(text, 10, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        self.displayScreen.blit(textobj, textrect)

    def moveWorm(self, direction):
        if direction == "right":
            self.x = self.x + self.movingSpeed
        elif direction == "left":
            self.x = self.x - self.movingSpeed
        self.surface = pygame.Surface((20, 20))
        self.surface.fill(self.color)
        self.rect = self.surface.get_rect(center=(self.x, self.y))

    def updatePositionForSetting(self):
        self.y += 10
        self.rect.y = self.y
        self.mask = pygame.mask.from_surface(self.surface)

