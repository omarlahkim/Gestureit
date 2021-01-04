from threading import Timer
import time


class ResettableTimer(object):
    def __init__(self, interval, function):
        self.interval = interval
        self.function = function
        self.timer = Timer(self.interval, self.function)
        self.count = 0

    def start(self):
        self.timer.start()

    def reset(self):
        self.timer.cancel()
        self.count = 0
        self.timer = Timer(self.interval, self.function)
        self.timer.start()

    def execute(self):
        self.count +=1
        self.function()


