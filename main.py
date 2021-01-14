import sys
import pygame

from pygame.locals import *
from Player import Player
from Floor import Floor

if __name__ == '__main__':

    GAME_TITLE = "worms fangame"
    WIDTH_SCREEN = 450
    HEIGHT_SCREEN = 600
    NUMBER_WORMS = 3

    pygame.init()
    displayScreen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
    pygame.display.set_caption(GAME_TITLE)

    playerList = [(f'player{x + 1}', Player(NUMBER_WORMS)) for x in range(0, 2)]
    ground = Floor(WIDTH_SCREEN, HEIGHT_SCREEN)

    sprites = pygame.sprite.Group()
    sprites.add(ground)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        for entity in sprites:
            displayScreen.blit(entity.surface, entity.rectangle)

        pygame.display.update()
