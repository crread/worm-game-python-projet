import random
import pygame


class Worm(pygame.sprite.Sprite):
    def __init__(self, NUMBER, HEIGHT, WIDTH, COLOR, SCREEN):
        super().__init__()
        self.health = 100
        self.number = NUMBER
        self.x = random.randint(0, WIDTH)
        self.y = HEIGHT-40
        self.surface = pygame.Surface((20, 20))
        self.surface.fill(COLOR)
        self.rectangle = self.surface.get_rect(center=(self.x, self.y))
        self.displayScreen = SCREEN
        self.color = COLOR
        self.font = pygame.font.SysFont(None, 15)

    def select(self):
        self.draw_text("Worm " + str(self.number), self.color, self.x-20, self.y-30)

    def draw_text(self, text, color, x, y):
        textobj = self.font.render(text, 10, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        self.displayScreen.blit(textobj, textrect)

    def moveright(self):
        self.x = self.x - 5
        self.surface = pygame.Surface((20, 20))
        self.surface.fill(self.color)
        self.rectangle = self.surface.get_rect(center=(self.x, self.y))


    def moveleft(self):
        self.x = self.x + 5
        self.surface = pygame.Surface((20, 20))
        self.surface.fill(self.color)
        self.rectangle = self.surface.get_rect(center=(self.x, self.y))
