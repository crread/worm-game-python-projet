import sys
import pygame
import random

from Floor import Floor
from pygame.locals import *
from Player import Player


class Game:
    def __init__(self):
        super().__init__()
        self.ground = None
        self.displayScreen = None
        self.WIDTH_SCREEN = None
        self.HEIGHT_SCREEN = None
        self.displayScreen = None
        self.playerList = None
        self.font = None
        self.sprites = None
        self.showMenu = False
        self.GAME_TITLE = "worms fangame"
        self.NUMBER_WORMS = 3
        self.BACKGROUND_IMAGE = pygame.image.load("assets/background_bluemoon.png")
        self.fps = pygame.time.Clock()

    def keyboardEventListener(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_a:
                    self.showMenu = not self.showMenu

    def mouseEventListener(self):
        pass

    def initGame(self):
        pygame.init()
        self.displayScreen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption(self.GAME_TITLE)
        self.WIDTH_SCREEN, self.HEIGHT_SCREEN = pygame.display.get_surface().get_size()
        self.ground = Floor(self.WIDTH_SCREEN, self.HEIGHT_SCREEN)
        self.playerList = {f'player{x + 1}': Player(self.NUMBER_WORMS, self.WIDTH_SCREEN, self.HEIGHT_SCREEN,
                                                    (random.randint(0, 255), random.randint(0, 255),
                                                     random.randint(0, 255))) for x in range(0, 2)}
        self.font = pygame.font.SysFont(None, 100)
        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.ground)
        for player in self.playerList:
            for worm in self.playerList[player].worms:
                self.sprites.add(worm)

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, 10, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def gameLoop(self):
        while True:
            self.displayScreen.blit(self.BACKGROUND_IMAGE, (0, 0))
            self.keyboardEventListener()
            self.mouseEventListener()
            if self.showMenu:
                self.draw_text("OPTIONS", self.font, (255, 255, 255), self.displayScreen, self.WIDTH_SCREEN / 2 - 170, self.HEIGHT_SCREEN / 2 - 300)
            for entity in self.sprites:
                self.displayScreen.blit(entity.surface, entity.rectangle)
            pygame.display.update()
