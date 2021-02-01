import math
import pygame

from math import *
from Wind import Wind


class Projectile:
    def __init__(self, x, y, height, width, screen):
        super().__init__()
        self.wind = Wind()
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
        g = -9.81
        resistanceCoef = 0.05
        initSpeed = {'V0': int(self.v0 * cos(radians(self.angle))), 'W0': int(self.v0 * sin(radians(self.angle)))}
        initSpeed['V0'] = initSpeed['V0'] + 0.2 * self.wind.wind['x']
        initSpeed['W0'] = initSpeed['W0'] + 0.2 * self.wind.wind['y']
        dt = 0.1
        x = int(initSpeed['V0'] / resistanceCoef * (1 - math.exp(-resistanceCoef * self.time)) + initX)
        y = int((initSpeed['W0'] / resistanceCoef + g / pow(resistanceCoef, 2)) * (
                    1 - math.exp(-resistanceCoef * self.time)) - (g * self.time) / resistanceCoef + initY)
        self.time = self.time + dt
        return x, y

    # def projectileBounce(self):

    # Calculus for trajectory

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
