import pygame
import numpy
import matplotlib.pyplot as plt
from skimage import draw

from PIL import Image


class Landscape:
    def __init__(self):
        super().__init__()
        self.spriteLandScape = None
        self.spriteArrayLandScape = None
        self.mask = None
        self.rect = None
        self.height = None
        self.width = None

    def initLandscape(self, WIDTH, HEIGHT):
        self.width = WIDTH
        self.height = HEIGHT
        image = Image.open("assets/land.png")
        self.spriteArrayLandScape = numpy.array(image)
        self.spriteLandScape = pygame.sprite.Sprite()
        self.arrayToImage()

    def arrayToImage(self):
        newImage = Image.fromarray(self.spriteArrayLandScape, "RGB")
        mode = newImage.mode
        size = newImage.size
        data = newImage.tobytes()
        self.spriteLandScape.image = pygame.image.fromstring(data, size, mode).convert_alpha()
        self.spriteLandScape.image.set_colorkey((0, 0, 0))
        self.spriteLandScape.rect = self.spriteLandScape.image.get_rect(
            center=(self.width / 2, (2 * (self.height / 3)) + ((self.height / 3) / 2)))
        self.spriteLandScape.mask = pygame.mask.from_surface(self.spriteLandScape.image)

    def updateMap(self, zoneToDestroy):
        w, h = self.spriteLandScape.image.get_size()
        rr, cc = draw.disk(((h - (self.height - zoneToDestroy[0])) + 20, zoneToDestroy[1]), radius=zoneToDestroy[2], shape=self.spriteArrayLandScape.shape)
        self.spriteArrayLandScape[rr, cc] = 0
        self.arrayToImage()
