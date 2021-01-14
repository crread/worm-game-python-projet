import sys
import pygame

from pygame.locals import *
from Player import Player
from Floor import Floor

if __name__ == '__main__':

    GAME_TITLE = "worms fangame"
    NUMBER_WORMS = 3

    pygame.init()
    displayScreen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH_SCREEN, HEIGHT_SCREEN = pygame.display.get_surface().get_size()
    pygame.display.set_caption(GAME_TITLE)

    BACKGROUND_IMAGE = pygame.image.load("assets/background_bluemoon.png")

    playerList = {f'player{x + 1}': Player(NUMBER_WORMS, WIDTH_SCREEN, HEIGHT_SCREEN) for x in range(0, 2)}
    ground = Floor(WIDTH_SCREEN, HEIGHT_SCREEN)

    sprites = pygame.sprite.Group()
    sprites.add(ground)
    print(playerList["player1"])

    for player in playerList:
        for worm in playerList[player].worms:
            sprites.add(worm)

    while True:

        displayScreen.blit(BACKGROUND_IMAGE, (0, 0))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        for entity in sprites:
            displayScreen.blit(entity.surface, entity.rectangle)

        pygame.display.update()
