from Worm import Worm


class Player:
    def __init__(self, numberWorm):
        super().__init__()
        self.worms = list(Worm() for x in range(0, numberWorm))
