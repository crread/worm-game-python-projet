from Worm import Worm


class Player:
    def __init__(self, numberWorm, HEIGHT, WIDTH, COLOR):
        super().__init__()
        self.worms = list(Worm(HEIGHT, WIDTH, COLOR) for x in range(0, numberWorm))
