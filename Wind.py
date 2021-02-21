import math
import random

from math import *


class Wind:
    def __init__(self):
        super().__init__()
        self.arrowWind = None
        self.wind = None
        self.init()

    def init(self):
        self.getNewWind()

    def getNewWind(self):
        velocity = random.randrange(0, 100, 1)
        angle = random.randrange(0, -360, -1)
        self.wind = {"x": int(velocity * cos(math.radians(angle))), "y": int(velocity * sin(math.radians(angle)))}
