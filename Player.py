from Worm import Worm


class Player:
    def __init__(self, numberWorm, HEIGHT, WIDTH):
        super().__init__()
        self.worms = list(Worm(HEIGHT, WIDTH) for x in range(0, numberWorm))
