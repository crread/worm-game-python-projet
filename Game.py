import sys
import pygame
import random

from math import *

from Floor import Floor
from pygame.locals import *
from Player import Player
from Projectile import Projectile


class Game:
    def __init__(self):
        super().__init__()
        self.ground = None
        self.BACKGROUND_IMAGE = None
        self.displayScreen = None
        self.WIDTH_SCREEN = None
        self.HEIGHT_SCREEN = None
        self.displayScreen = None
        self.playerList = None
        self.font = None
        self.sprites = None
        self.projectile = None
        self.showMenu = False
        self.gameStart = False
        self.GAME_TITLE = "worms fangame"
        self.numberPlayers = 2
        self.numberWorms = 3
        self.clock = pygame.time.Clock()
        self.shooting = False

    def init(self):
        pygame.init()
        self.displayScreen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.BACKGROUND_IMAGE = pygame.image.load("assets/background_bluemoon.png").convert()

        pygame.display.set_caption(self.GAME_TITLE)
        self.WIDTH_SCREEN, self.HEIGHT_SCREEN = pygame.display.get_surface().get_size()
        self.projectile = Projectile(600, self.HEIGHT_SCREEN - 300, self.HEIGHT_SCREEN, self.WIDTH_SCREEN,
                                     self.displayScreen)
        self.font = pygame.font.SysFont(None, 100)

    def initGame(self):
        self.ground = Floor(self.WIDTH_SCREEN, self.HEIGHT_SCREEN)
        self.playerList = {f'player{x + 1}': Player(self.numberWorms, self.WIDTH_SCREEN, self.HEIGHT_SCREEN,
                                                    (random.randint(0, 255), random.randint(0, 255),
                                                     random.randint(0, 255))) for x in range(0, self.numberPlayers)}

        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.ground)
        for player in self.playerList:
            for worm in self.playerList[player].worms:
                self.sprites.add(worm)

    def inputEventListener(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.showMenu = not self.showMenu
                if event.key == K_SPACE and not self.shooting:
                    self.shooting = True
                    self.projectile.time = 0
                if event.key == K_p:
                    self.projectile.wind.getNewWind()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if self.showMenu and self.gameStart:
                    if self.HEIGHT_SCREEN / 2 + self.font.size("EXIT")[1] / 4 <= y <= self.HEIGHT_SCREEN / 2 + 100 + \
                            self.font.size("EXIT")[
                                1] / 4 and self.WIDTH_SCREEN / 2 - 300 <= x <= self.WIDTH_SCREEN / 2 + 300:
                        pygame.quit()
                        sys.exit()
                if not self.gameStart:
                    self.EventInputShowMenu(x, y)

    def EventInputShowMenu(self, x, y):
        if self.HEIGHT_SCREEN / 2 - self.HEIGHT_SCREEN / 3 - self.font.size("2")[
            1] / 2 <= y <= self.HEIGHT_SCREEN / 2 - self.HEIGHT_SCREEN / 3 - self.font.size("2")[1] / 2 + \
                self.font.size("2")[1] * 2 and self.WIDTH_SCREEN / 2 + 300 - self.font.size("2")[
            0] / 2 <= x <= self.WIDTH_SCREEN / 2 + 300 + self.font.size("2")[0] * 2:
            self.numberPlayers = 2
        if self.HEIGHT_SCREEN / 2 - self.HEIGHT_SCREEN / 3 - self.font.size("3")[
            1] / 2 <= y <= self.HEIGHT_SCREEN / 2 - self.HEIGHT_SCREEN / 3 - self.font.size("3")[1] / 2 + \
                self.font.size("3")[1] * 2 and self.WIDTH_SCREEN / 2 + 450 - self.font.size("3")[
            0] / 2 <= x <= self.WIDTH_SCREEN / 2 + 450 + self.font.size("3")[0] * 2:
            self.numberPlayers = 3
        if self.HEIGHT_SCREEN / 2 - self.HEIGHT_SCREEN / 3 - self.font.size("4")[
            1] / 2 <= y <= self.HEIGHT_SCREEN / 2 - self.HEIGHT_SCREEN / 3 - self.font.size("4")[1] / 2 + \
                self.font.size("4")[1] * 2 and self.WIDTH_SCREEN / 2 + 600 - self.font.size("4")[
            0] / 2 <= x <= self.WIDTH_SCREEN / 2 + 600 + self.font.size("4")[0] * 2:
            self.numberPlayers = 4
        if self.HEIGHT_SCREEN / 3 - self.font.size("3")[1] / 2 <= y <= self.HEIGHT_SCREEN / 3 - self.font.size("3")[
            1] / 2 + self.font.size("3")[1] * 2 and self.WIDTH_SCREEN / 2 + 300 - self.font.size("3")[
            0] / 2 <= x <= self.WIDTH_SCREEN / 2 + 300 + self.font.size("3")[0]:
            self.numberWorms = 3
        if self.HEIGHT_SCREEN / 3 - self.font.size("4")[1] / 2 <= y <= self.HEIGHT_SCREEN / 3 - self.font.size("4")[
            1] / 2 + self.font.size("4")[1] * 2 and self.WIDTH_SCREEN / 2 + 450 - self.font.size("4")[
            0] <= x <= self.WIDTH_SCREEN / 2 + 450 + self.font.size("4")[0] / 2:
            self.numberWorms = 4
        # if self.HEIGHT_SCREEN / 2 + self.font.size("5")[1] / 4 <= y <= self.HEIGHT_SCREEN / 2 + 100 + self.font.size("5")[1] / 4 and self.WIDTH_SCREEN / 2 - 300 <= x <= self.WIDTH_SCREEN / 2 + 300:
        # if self.HEIGHT_SCREEN / 2 + self.font.size("6")[1] / 4 <= y <= self.HEIGHT_SCREEN / 2 + 100 + self.font.size("6")[1] / 4 and self.WIDTH_SCREEN / 2 - 300 <= x <= self.WIDTH_SCREEN / 2 + 300:
        if self.HEIGHT_SCREEN / 3 + self.HEIGHT_SCREEN / 6 - self.font.size("PLAY")[
            1] / 2 <= y <= self.HEIGHT_SCREEN / 3 + self.HEIGHT_SCREEN / 6 - self.font.size("PLAY")[1] / 2 + \
                self.font.size("PLAY")[0] and self.WIDTH_SCREEN / 2 - self.font.size("PLAY")[
            0] / 2 <= x <= self.WIDTH_SCREEN / 2 - self.font.size("PLAY")[0] / 2 + self.font.size("PLAY")[0]:
            self.initGame()
            self.gameStart = True
        if self.HEIGHT_SCREEN / 3 + self.HEIGHT_SCREEN / 3 - self.font.size("EXIT")[
            1] / 2 <= y <= self.HEIGHT_SCREEN / 3 + self.HEIGHT_SCREEN / 3 - self.font.size("EXIT")[1] / 2 + \
                self.font.size("EXIT")[1] * 2 and self.WIDTH_SCREEN / 2 - self.font.size("EXIT")[
            0] / 2 <= x <= self.WIDTH_SCREEN / 2 - self.font.size("EXIT")[0] / 2 + self.font.size("EXIT")[0]:
            pygame.quit()
            sys.exit()

    def displayFPS(self):
        self.draw_text(str(int(self.clock.get_fps())), (255, 255, 255), 0, 0)

    def draw_text(self, text, color, x, y):
        textobj = self.font.render(text, 10, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        self.displayScreen.blit(textobj, textrect)

    def draw_button(self, color, x, y, w, h):
        pygame.draw.rect(self.displayScreen, color, (x, y, w, h))

    # !TODO refaire les widgets avec pygame-menu

    def drawMenuInGame(self):
        self.draw_text("EXIT", (255, 255, 255), self.WIDTH_SCREEN / 2 - self.font.size("EXIT")[0] / 2,
                       self.HEIGHT_SCREEN / 2 + self.font.size("EXIT")[1] / 2)
        self.draw_text("MENU", (255, 255, 255), self.WIDTH_SCREEN / 2 - self.font.size("MENU")[0] / 2,
                       self.HEIGHT_SCREEN / 2 - 350)

    def startMenu(self):
        # SELECT PLAYERS
        self.draw_text(f"NUMBER OF PLAYERS : {self.numberPlayers}", (255, 255, 255),
                       self.WIDTH_SCREEN / 2 - self.WIDTH_SCREEN / 3,
                       self.HEIGHT_SCREEN / 2 - self.HEIGHT_SCREEN / 3)
        self.draw_text("2", (255, 255, 255), self.WIDTH_SCREEN / 2 + 300,
                       self.HEIGHT_SCREEN / 2 - self.HEIGHT_SCREEN / 3)
        self.draw_text("3", (255, 255, 255), self.WIDTH_SCREEN / 2 + 450,
                       self.HEIGHT_SCREEN / 2 - self.HEIGHT_SCREEN / 3)
        self.draw_text("4", (255, 255, 255), self.WIDTH_SCREEN / 2 + 600,
                       self.HEIGHT_SCREEN / 2 - self.HEIGHT_SCREEN / 3)
        # SELECT NUMBER OF WORMS
        self.draw_text(f"NUMBER OF WORMS : {self.numberWorms}", (255, 255, 255),
                       self.WIDTH_SCREEN / 2 - self.WIDTH_SCREEN / 3,
                       self.HEIGHT_SCREEN / 3)
        self.draw_text("3", (255, 255, 255), self.WIDTH_SCREEN / 2 + 300,
                       self.HEIGHT_SCREEN / 3)
        self.draw_text("4", (255, 255, 255), self.WIDTH_SCREEN / 2 + 425,
                       self.HEIGHT_SCREEN / 3)
        self.draw_button((0, 0, 0), self.WIDTH_SCREEN / 2 + 550 - self.font.size("5")[0] / 2,
                         self.HEIGHT_SCREEN / 3 - self.font.size("5")[1] / 2, self.font.size("5")[0] * 2,
                         self.font.size("5")[1] * 2)
        self.draw_text("5", (255, 255, 255), self.WIDTH_SCREEN / 2 + 550,
                       self.HEIGHT_SCREEN / 3)
        self.draw_button((0, 0, 0), self.WIDTH_SCREEN / 2 + 675 - self.font.size("6")[0] / 2,
                         self.HEIGHT_SCREEN / 3 - self.font.size("6")[1] / 2, self.font.size("6")[0] * 2,
                         self.font.size("6")[1] * 2)
        self.draw_text("6", (255, 255, 255), self.WIDTH_SCREEN / 2 + 675,
                       self.HEIGHT_SCREEN / 3)
        # PLAY & EXIT
        self.draw_text("PLAY", (255, 255, 255), self.WIDTH_SCREEN / 2 - self.font.size("PLAY")[0] / 2,
                       self.HEIGHT_SCREEN / 3 + self.HEIGHT_SCREEN / 6)
        self.draw_text("EXIT", (255, 255, 255), self.WIDTH_SCREEN / 2 - self.font.size("EXIT")[0] / 2,
                       self.HEIGHT_SCREEN / 3 + self.HEIGHT_SCREEN / 3)

    def drawPointTestAngleCalcul(self):
        pygame.draw.circle(self.displayScreen, (0, 0, 0), (700, 700), 3, 0)  # origine
        pygame.draw.circle(self.displayScreen, (0, 0, 0), (1000, 1000), 3, 0)  # vecteur A
        pygame.draw.circle(self.displayScreen, (0, 0, 0), (1000, 500), 3, 0)  # vecteur B

        # Calcul de l'angle

        vectorA = (3, 3)
        vectorB = (3, -2)

        sqrtVectorA = (sqrt(vectorA[0] ** 2 + vectorA[1] ** 2))
        sqrtVectorB = (sqrt(vectorB[0] ** 2 + vectorB[1] ** 2))

        sumVectors = vectorA[0] * vectorA[1] + vectorB[0] * vectorB[1]

        angle = sumVectors / sqrtVectorA * sqrtVectorB
        print(angle)

    def gameLoop(self):
        while True:
            self.displayScreen.blit(self.BACKGROUND_IMAGE, (0, 0))
            self.inputEventListener()
            self.displayFPS()
            if self.gameStart:
                if not self.shooting:
                    self.projectile.trajectoryPreviewShoot()
                else:
                    self.shooting = self.projectile.shootRocket()
                if self.showMenu:
                    self.drawMenuInGame()
                for entity in self.sprites:
                    self.displayScreen.blit(entity.surface, entity.rectangle)
            else:
                self.startMenu()
            pygame.display.update()
            self.clock.tick(60)
