import pygame

from pygame.locals import *
from math import *


class Projectile:
    def __init__(self, x, y, height, width, screen):
        super().__init__()
        self.x = x
        self.y = y
        self.angle = -45
        self.v0 = 50
        self.time = 0
        self.HEIGHT_SCREEN = height
        self.WIDTH_SCREEN = width
        self.SCREEN = screen
        self.shoot = False

    def updateInitPosition(self, x, y):
        self.x = x
        self.y = y

    def getTrajectory(self, initX, initY):
        g = 9.81
        vitesse = {'V0': int(self.v0 * cos(radians(self.angle))), 'W0': int(self.v0 * sin(radians(self.angle)))}
        dt = 0.1
        x = vitesse['V0'] * self.time + initX
        if self.shoot:
            print(int(vitesse['V0'] * self.time), int(vitesse['W0'] * self.time))
        y = 1 / 2 * g * pow(self.time, 2) + vitesse['W0'] * self.time + initY
        self.time = self.time + dt
        return x, y

    #def projectileBounce(self):



    def trajectoryPreviewShoot(self):
        positions = (0, 0)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        coef = 5
        self.v0 = sqrt((abs(mouse_x) - abs(self.x)) ** 2 + (abs(mouse_y) - abs(self.y)) ** 2) / coef
        pygame.draw.line(self.SCREEN, (0, 0, 0), (self.x, self.y), (mouse_x, mouse_y), 2)
        self.time = 0
        while positions[1] <= self.HEIGHT_SCREEN:
            positions = self.getTrajectory(self.x, self.y)
            pygame.draw.circle(self.SCREEN, (230, 60, 30), (positions[0], positions[1]), 3, 0)

    def shootRocket(self):
        self.shoot = True
        positions = self.getTrajectory(self.x, self.y)
        pygame.draw.circle(self.SCREEN, (230, 60, 30), (positions[0], positions[1]), 10, 0)
        if positions[1] >= self.HEIGHT_SCREEN:
            self.time = 0
            self.shoot = False
            return False
        return True
