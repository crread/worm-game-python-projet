import sys
import pygame
import random

from math import *
from pygame.locals import *
from Landscape import Landscape
from Player import Player
from Projectile import Projectile
from Clock import Clock
from Worm import Worm


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
        self.actualPlayer = 0
        self.actualWorm = 0
        self.playingPlayer = None
        self.playingWorm = None
        self.clock = pygame.time.Clock()
        self.clockTurn = None
        self.shooting = False
        self.groundGroup = None

    # Init Functions

    def init(self):
        pygame.init()
        self.displayScreen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF,
                                                     vsync=1)
        self.BACKGROUND_IMAGE = pygame.image.load("assets/background_bluemoon.png").convert()
        pygame.display.set_caption(self.GAME_TITLE)
        self.WIDTH_SCREEN, self.HEIGHT_SCREEN = pygame.display.get_surface().get_size()
        self.projectile = Projectile(600, self.HEIGHT_SCREEN - 300, self.HEIGHT_SCREEN, self.WIDTH_SCREEN,
                                     self.displayScreen)
        self.projectile.initProjectile()
        self.font = {"classic": pygame.font.SysFont(None, 100),
                     "grenade": pygame.font.SysFont(None, 50)}

    def initGame(self):
        self.clockTurn = Clock(30)
        self.ground = Landscape()
        self.ground.initLandscape(self.WIDTH_SCREEN, self.HEIGHT_SCREEN)
        self.groundGroup = pygame.sprite.GroupSingle()
        self.groundGroup.add(self.ground.spriteLandScape)
        self.playerList = list(Player(self.numberWorms, self.HEIGHT_SCREEN, self.WIDTH_SCREEN,
                                      (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                                      self.displayScreen) for x in range(0, self.numberPlayers))

        self.sprites = pygame.sprite.Group()
        for player in range(len(self.playerList)):
            for worm in self.playerList[player].worms:
                self.sprites.add(worm)

        self.updateWormsPositions()

        self.projectile.updateInitPosition(self.playerList[self.actualPlayer].worms[self.actualWorm].x,
                                           self.playerList[self.actualPlayer].worms[self.actualWorm].y)

    # Important Functions

    def updateWormsPositions(self):
        for sprite in self.sprites:
            while len(pygame.sprite.spritecollide(sprite, self.groundGroup, False, pygame.sprite.collide_mask)) == 0:
                if sprite.y < self.HEIGHT_SCREEN + 50:
                    sprite.updatePositionForSetting()

    def changePlayerTurn(self):
        self.clockTurn.resetTimer()
        self.actualPlayer = self.actualPlayer + 1
        if self.actualPlayer > self.numberPlayers - 1:
            self.actualPlayer = 0
        if self.actualWorm > self.numberWorms - 1:
            self.actualWorm = self.actualWorm + 1
            self.actualWorm = 0
        self.projectile.wind.getNewWind()
        self.projectile.updateInitPosition(self.playerList[self.actualPlayer].worms[self.actualWorm].x,
                                           self.playerList[self.actualPlayer].worms[self.actualWorm].y)

    def distanceBetweenExplosionAndWorm(self):
        for sprite in self.sprites:
            if isinstance(sprite, Worm):
                if sqrt((abs(sprite.x) - abs(self.projectile.x)) ** 2 + (
                        abs(sprite.y) - abs(self.projectile.y)) ** 2) <= 100:
                    sprite.health -= self.projectile.sprites[self.projectile.typeProjectile].damage
        provisionalSpriteList = self.sprites
        self.sprites = [sprite for sprite in provisionalSpriteList if sprite.health > 0]

    def keyPressedEvents(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_q] and not self.shooting:
            self.playerList[self.actualPlayer].worms[self.actualWorm].moveWorm("left")
            self.projectile.updateInitPosition(self.playerList[self.actualPlayer].worms[self.actualWorm].x,
                                               self.playerList[self.actualPlayer].worms[self.actualWorm].y)
        if key[pygame.K_d] and not self.shooting:
            self.playerList[self.actualPlayer].worms[self.actualWorm].moveWorm("right")
            self.projectile.updateInitPosition(self.playerList[self.actualPlayer].worms[self.actualWorm].x,
                                               self.playerList[self.actualPlayer].worms[self.actualWorm].y)

    def keyDownEvents(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.showMenu = not self.showMenu
                if event.key == K_1 and not self.shooting:
                    self.shooting = True
                    self.projectile.initShoot("rocket")
                if event.key == K_2 and not self.shooting:
                    self.shooting = True
                    self.projectile.initShoot("grenade")

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if self.showMenu and self.gameStart:
                    if self.HEIGHT_SCREEN / 2 + self.font["classic"].size("EXIT")[
                        1] / 4 <= y <= self.HEIGHT_SCREEN / 2 + 100 + \
                            self.font["classic"].size("EXIT")[
                                1] / 4 and self.WIDTH_SCREEN / 2 - 300 <= x <= self.WIDTH_SCREEN / 2 + 300:
                        pygame.quit()
                        sys.exit()
                if not self.gameStart:
                    self.EventInputShowMenu(x, y)

    def inputEventListener(self):
        self.keyPressedEvents()
        self.keyDownEvents()

    def EventInputShowMenu(self, x, y):
        if self.HEIGHT_SCREEN / 2 - self.HEIGHT_SCREEN / 3 - self.font["classic"].size("2")[
            1] / 2 <= y <= self.HEIGHT_SCREEN / 2 - self.HEIGHT_SCREEN / 3 - self.font["classic"].size("2")[1] / 2 + \
                self.font["classic"].size("2")[1] * 2 and self.WIDTH_SCREEN / 2 + 300 - self.font["classic"].size("2")[
            0] / 2 <= x <= self.WIDTH_SCREEN / 2 + 300 + self.font["classic"].size("2")[0] * 2:
            self.numberPlayers = 2
        if self.HEIGHT_SCREEN / 2 - self.HEIGHT_SCREEN / 3 - self.font["classic"].size("3")[
            1] / 2 <= y <= self.HEIGHT_SCREEN / 2 - self.HEIGHT_SCREEN / 3 - self.font["classic"].size("3")[1] / 2 + \
                self.font["classic"].size("3")[1] * 2 and self.WIDTH_SCREEN / 2 + 450 - self.font["classic"].size("3")[
            0] / 2 <= x <= self.WIDTH_SCREEN / 2 + 450 + self.font["classic"].size("3")[0] * 2:
            self.numberPlayers = 3
        if self.HEIGHT_SCREEN / 2 - self.HEIGHT_SCREEN / 3 - self.font["classic"].size("4")[
            1] / 2 <= y <= self.HEIGHT_SCREEN / 2 - self.HEIGHT_SCREEN / 3 - self.font["classic"].size("4")[1] / 2 + \
                self.font["classic"].size("4")[1] * 2 and self.WIDTH_SCREEN / 2 + 600 - self.font["classic"].size("4")[
            0] / 2 <= x <= self.WIDTH_SCREEN / 2 + 600 + self.font["classic"].size("4")[0] * 2:
            self.numberPlayers = 4
        if self.HEIGHT_SCREEN / 3 - self.font["classic"].size("3")[1] / 2 <= y <= self.HEIGHT_SCREEN / 3 - \
                self.font["classic"].size("3")[
                    1] / 2 + self.font["classic"].size("3")[1] * 2 and self.WIDTH_SCREEN / 2 + 300 - \
                self.font["classic"].size("3")[
                    0] / 2 <= x <= self.WIDTH_SCREEN / 2 + 300 + self.font["classic"].size("3")[0]:
            self.numberWorms = 3
        if self.HEIGHT_SCREEN / 3 - self.font["classic"].size("4")[1] / 2 <= y <= self.HEIGHT_SCREEN / 3 - \
                self.font["classic"].size("4")[
                    1] / 2 + self.font["classic"].size("4")[1] * 2 and self.WIDTH_SCREEN / 2 + 450 - \
                self.font["classic"].size("4")[
                    0] <= x <= self.WIDTH_SCREEN / 2 + 450 + self.font["classic"].size("4")[0] / 2:
            self.numberWorms = 4
        if self.HEIGHT_SCREEN / 3 + self.HEIGHT_SCREEN / 6 - self.font["classic"].size("PLAY")[
            1] / 2 <= y <= self.HEIGHT_SCREEN / 3 + self.HEIGHT_SCREEN / 6 - self.font["classic"].size("PLAY")[1] / 2 + \
                self.font["classic"].size("PLAY")[0] and self.WIDTH_SCREEN / 2 - self.font["classic"].size("PLAY")[
            0] / 2 <= x <= self.WIDTH_SCREEN / 2 - self.font["classic"].size("PLAY")[0] / 2 + \
                self.font["classic"].size("PLAY")[0]:
            self.initGame()
            self.gameStart = True
        if self.HEIGHT_SCREEN / 3 + self.HEIGHT_SCREEN / 3 - self.font["classic"].size("EXIT")[
            1] / 2 <= y <= self.HEIGHT_SCREEN / 3 + self.HEIGHT_SCREEN / 3 - self.font["classic"].size("EXIT")[1] / 2 + \
                self.font["classic"].size("EXIT")[1] * 2 and self.WIDTH_SCREEN / 2 - self.font["classic"].size("EXIT")[
            0] / 2 <= x <= self.WIDTH_SCREEN / 2 - self.font["classic"].size("EXIT")[0] / 2 + \
                self.font["classic"].size("EXIT")[0]:
            pygame.quit()
            sys.exit()

    def displayFPS(self):
        self.draw_text_with_font(str(int(self.clock.get_fps())), (255, 255, 255), 0, 0, self.font["classic"])

    def draw_text(self, text, color, x, y, typeFont="classic"):
        textobj = self.font[typeFont].render(text, 10, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        self.displayScreen.blit(textobj, textrect)

    def draw_text_with_font(self, text, color, x, y, font):
        textobj = font.render(text, 10, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        self.displayScreen.blit(textobj, textrect)

    def draw_button(self, color, x, y, w, h):
        pygame.draw.rect(self.displayScreen, color, (x, y, w, h))

    def drawMenuInGame(self):
        self.draw_text("EXIT", (255, 255, 255), self.WIDTH_SCREEN / 2 - self.font["classic"].size("EXIT")[0] / 2,
                       self.HEIGHT_SCREEN / 2 + self.font["classic"].size("EXIT")[1] / 2)
        self.draw_text("MENU", (255, 255, 255), self.WIDTH_SCREEN / 2 - self.font["classic"].size("MENU")[0] / 2,
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
        # PLAY & EXIT
        self.draw_text("PLAY", (255, 255, 255), self.WIDTH_SCREEN / 2 - self.font["classic"].size("PLAY")[0] / 2,
                       self.HEIGHT_SCREEN / 3 + self.HEIGHT_SCREEN / 6)
        self.draw_text("EXIT", (255, 255, 255), self.WIDTH_SCREEN / 2 - self.font["classic"].size("EXIT")[0] / 2,
                       self.HEIGHT_SCREEN / 3 + self.HEIGHT_SCREEN / 3)

    def drawWormsLife(self):
        self.playingPlayer = self.playerList[self.actualPlayer]
        self.playingWorm = self.playingPlayer.worms[self.actualWorm]

        for sprite in self.sprites:
            if isinstance(sprite, Worm):
                self.draw_text_with_font(str(sprite.health), sprite.color, sprite.x - 10,
                                         sprite.y - 20, sprite.font)
        self.draw_text("Player " + str(self.actualPlayer + 1), (255, 255, 255), 0, 100)
        self.draw_text("Worm " + str(self.actualWorm + 1), (255, 255, 255), 0, 200)

        self.playingWorm.selected()

    def displaySecondsLeft(self):
        self.draw_text(str(self.clockTurn.limitTimer - self.clockTurn.getTimePassed()), (255, 255, 255),
                       self.WIDTH_SCREEN / 2, 100)

    def drawInGameLoop(self):
        self.displayScreen.blit(self.BACKGROUND_IMAGE, (0, 0))
        if self.gameStart:
            self.displayScreen.blit(self.ground.spriteLandScape.image, (0, (2 * self.HEIGHT_SCREEN / 3)))
            self.displayFPS()
            self.displaySecondsLeft()
            self.shooting = self.projectile.isShooting()
            if not self.shooting:
                self.projectile.trajectoryPreviewShoot()
            else:
                self.projectile.updateShootingProjectile(self.ground)
                self.shooting = self.projectile.isShooting()
                if self.shooting:
                    typeProjectile = self.projectile.typeProjectile
                    if typeProjectile == "grenade":
                        self.displayScreen.blit(self.projectile.sprites["grenade"].image,
                                                (self.projectile.x, self.projectile.y))
                        self.draw_text(
                            str(self.projectile.grenadeClock.limitTimer - self.projectile.grenadeClock.getTimePassed()),
                            (255, 255, 255), self.projectile.x - 10, self.projectile.y - 50, "grenade")
                    else:
                        self.displayScreen.blit(self.projectile.sprites["rocket"].surface,
                                                (self.projectile.x, self.projectile.y))
                else:
                    self.distanceBetweenExplosionAndWorm()
                    self.projectile.resetProjectile()
                    self.changePlayerTurn()
            self.updateWormsPositions()
            if self.showMenu:
                self.drawMenuInGame()
            self.drawWormsLife()
            for entity in self.sprites:
                self.displayScreen.blit(entity.surface, entity.rect)
        else:
            self.startMenu()

    def eventsInGameLoop(self):
        if self.gameStart:
            if not self.clockTurn.timePassedIsUnderLimit():
                self.changePlayerTurn()

    def gameLoop(self):
        while True:
            self.inputEventListener()
            self.eventsInGameLoop()
            self.drawInGameLoop()
            pygame.display.update()
            self.clock.tick(0)
