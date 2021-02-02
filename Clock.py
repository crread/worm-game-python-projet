from datetime import datetime


class Clock:
    def __init__(self, limitTimer):
        super().__init__()
        self.timer = datetime.now()
        self.limitTimer = limitTimer

    def resetTimer(self):
        self.timer = datetime.now()

    def getTimePassed(self):
        return int((datetime.now() - self.timer).total_seconds())

    def timePassedIsUnderLimit(self):
        if int((datetime.now() - self.timer).total_seconds()) < self.limitTimer:
            return True
        else:
            return False
