import GameStat
import gameSettingsMaster
import math
import os
import pygame


# lvlFactor = 1.148698354997
# 1.148698354997 is the magic factor to get the needed additional XP to double every 5 levels.
# Will come in handy for implementation in "Exaggerated Mode".


class LevelHandler:
    # def __init__(self, inAlgorithm = "nextLevel = nextLevel * 1.148698354997"):
    def __init__(self, host, inAlgorithm = "nextLevel = nextLevel + 20"):
        self.level = GameStat.Stat(0, 0, 25, 0, 0, "", False)
        self.xp = GameStat.Stat(0, 0, float("inf"), 0, 0, "", False)
        self.xpToNextLevel = 100
        self.hasLeveledUp = 0

        self.host = host




        self.levelAlgorithm = inAlgorithm


    def rewardXP(self, amount):
        self.xp.modValue(amount)
        while self.shouldLevelUp():
            self.processLevelUp()

    def getLevel(self):
        return self.level.getValue()

    def getXP(self):
        return self.xp.getValue()

    def shouldLevelUp(self):
        if self.xp.getValue() >= self.xpToNextLevel:
            return True
        else:
            return False

    def processLevelUp(self):
        self.xp.setValue(self.xp.getValue() - self.xpToNextLevel)

        nextLevel = self.xpToNextLevel
        exec self.levelAlgorithm
        self.xpToNextLevel = nextLevel
        self.level.modValue(1)
        self.hasLeveledUp += 1

        self.host.loadAudio()
        self.host.audio.triggerSound("LevelUp")


    def checkIfLeveledUp(self):
        if self.hasLeveledUp > 0:
            self.hasLeveledUp -= 1
            return True
        return False



