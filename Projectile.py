import math
import pygame
import sys

from math import *
from Wind import Wind
from Clock import Clock


class Projectile:
    def __init__(self, x, y, height, width, screen):
        super().__init__()
        self.x = None
        self.y = None
        self.grenadeClock = None
        self.typeProjectile = None
        self.wind = Wind()
        self.initX = x
        self.initY = y
        self.angle = -45
        self.v0 = 50
        self.time = 0
        self.HEIGHT_SCREEN = height
        self.WIDTH_SCREEN = width
        self.SCREEN = screen
        self.shooting = False
        self.rect = None
        self.surface = None
        self.group = None
        self.sprites = {}

    def initProjectile(self):
        self.sprites["grenade"] = pygame.sprite.Sprite()
        self.sprites["grenade"].image = pygame.image.load("assets/bombe.png").convert_alpha()
        self.sprites["grenade"].image = pygame.transform.scale(self.sprites["grenade"].image, (25, 25))
        self.sprites["grenade"].image.set_colorkey((0, 0, 0))
        self.sprites["grenade"].rect = self.sprites["grenade"].image.get_rect(center=(self.initX, self.initY))
        self.sprites["grenade"].mask = pygame.mask.from_surface(self.sprites["grenade"].image)
        self.sprites["grenade"].damage = 35

        self.sprites["rocket"] = pygame.sprite.Sprite()
        self.sprites["rocket"].surface = pygame.Surface((20, 20), pygame.SRCALPHA)
        self.sprites["rocket"].surface.fill((230, 60, 30))
        self.sprites["rocket"].rect = self.sprites["rocket"].surface.get_rect(center=(self.initX, self.initY))
        self.sprites["rocket"].mask = pygame.mask.from_surface(self.sprites["rocket"].surface)
        self.sprites["rocket"].damage = 50

        self.grenadeClock = Clock(4)
        self.group = pygame.sprite.GroupSingle()

    def initShoot(self, typeProjectile):
        self.typeProjectile = typeProjectile
        if self.typeProjectile == "grenade":
            self.grenadeClock.resetTimer()
        self.time = 0
        self.shooting = True

    def isShooting(self):
        print(self.shooting)
        return self.shooting

    def updateShootingProjectile(self, floorMask):
        if self.shooting:
            if self.typeProjectile == "rocket":
                self.shootRocket(floorMask)
            if self.typeProjectile == "grenade":
                self.shootGrenade(floorMask)

    def updateInitPosition(self, x, y):
        self.initX = x
        self.initY = y - 10

    def getTrajectory(self):
        g = -9.81
        resistanceCoef = 0.05
        initSpeed = {'V0': int(self.v0 * cos(self.angle)), 'W0': int(self.v0 * sin(self.angle))}
        initSpeed['V0'] = initSpeed['V0'] + 0.2 * self.wind.wind['x']
        initSpeed['W0'] = initSpeed['W0'] + 0.2 * self.wind.wind['y']
        dt = 0.1
        self.x = int(initSpeed['V0'] / resistanceCoef * (1 - math.exp(-resistanceCoef * self.time)) + self.initX)
        self.y = int((initSpeed['W0'] / resistanceCoef + g / pow(resistanceCoef, 2)) * (
                1 - math.exp(-resistanceCoef * self.time)) - (g * self.time) / resistanceCoef + self.initY)
        self.time = self.time + dt

    def trajectoryPreviewShoot(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        coef = 5
        if sqrt((abs(mouse_x) - abs(self.initX)) ** 2 + (abs(mouse_y) - abs(self.initY)) ** 2) / coef < 100:
            self.v0 = sqrt((abs(mouse_x) - abs(self.initX)) ** 2 + (abs(mouse_y) - abs(self.initY)) ** 2) / coef
        else:
            self.v0 = 100
        self.angle = -acos(((mouse_x - self.initX) * 100 + 0) / (
                sqrt((mouse_x - self.initX) ** 2 + (mouse_y - self.initY) ** 2) * (sqrt(100 ** 2 + 0 ** 2))))
        self.time = 0
        self.y = 0
        while self.y <= self.HEIGHT_SCREEN:
            self.getTrajectory()
            pygame.draw.circle(self.SCREEN, (230, 60, 30), (self.x, self.y), 3, 0)

    def shootRocket(self, ground):
        self.getTrajectory()
        self.sprites["rocket"].rect.x = self.x
        self.sprites["rocket"].rect.y = self.y
        self.sprites["rocket"].mask = pygame.mask.from_surface(self.sprites["rocket"].surface)
        self.group.add(ground.spriteLandScape)
        if pygame.sprite.spritecollide(self.sprites["rocket"], self.group, False, pygame.sprite.collide_mask):
            self.group.remove(ground.spriteLandScape)
            ground.updateMap([self.y, self.x, 50])
            self.shooting = False
        else:
            self.shooting = True

    def shootGrenade(self, ground):
        self.getTrajectory()
        self.sprites["grenade"].rect.x = self.x
        self.sprites["grenade"].rect.y = self.y
        self.sprites["grenade"].mask = pygame.mask.from_surface(self.sprites["grenade"].image)
        self.group.add(ground.spriteLandScape)
        if pygame.sprite.spritecollide(self.sprites["grenade"], self.group, False, pygame.sprite.collide_mask):
            self.group.remove(ground.spriteLandScape)
            ground.updateMap([self.y, self.x, 35])
            self.shooting = False
        else:
            self.shooting = True

    def resetProjectile(self):

        self.typeProjectile = None
        self.x = None
        self.y = None
        self.time = 0
