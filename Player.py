from Worm import Worm


class Player:
    def __init__(self, numberWorm, HEIGHT, WIDTH, COLOR, SCREEN):
        super().__init__()
        self.worms = list(Worm(x, HEIGHT, WIDTH, COLOR, SCREEN) for x in range(0, numberWorm))
        self.wormTarget = 0
