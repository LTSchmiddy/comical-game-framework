import pygame, os

class TickCounter:
    def __init__(self, ticks, shouldLoop=False, idleMode=True):
        self.ticks = ticks
        self.shouldLoop = shouldLoop
        self.idleMode = idleMode
        # Data Variables:
        self.current = -1

        self.currentState = self.idleMode


    def check(self):
        self.current += 1

        if self.current >= self.ticks:
            if self.shouldLoop:
                self.current = 0

            self.currentState = not self.idleMode
            return not self.idleMode


        self.currentState = self.idleMode
        return self.idleMode

    def getState(self):
        return self.currentState

    def reset(self):
        self.current = 0

    def setTime(self, ticks):
        self.ticks = ticks

    def getNow(self):
        return self.current









