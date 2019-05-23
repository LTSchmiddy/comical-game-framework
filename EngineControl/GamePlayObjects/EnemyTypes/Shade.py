import os
import pygame

from EngineControl import Enemy as Enemy


class Tier1(Enemy.InstEnemy):
    def __init__ (self, pos, world):
        super(Tier1, self).__init__(pos, world)

        self.imgDir = "_IMAGES\Sprites\Enemies\Shade"
        self.imgExt = ".png"
        self.imgDict = {}

        self.loadImages()

        self.image = self.imgDict["Shade1Right"]

        self.radius = 600



        # self.radius = 350
        # self.image.fill([255, 255, 255])


    def loadImages(self):
        for i in os.listdir(self.imgDir):
            if i.endswith(self.imgExt):
                filePath = self.imgDir + "\\" + i
                imgName = i.split(self.imgExt)[0]
                imgIn = pygame.image.load(filePath)
                # print cModDict["itemID"]
                self.imgDict[imgName] = imgIn
        # print self.imgDict

    def runAI(self):
        super(Tier1, self).runAI()
        self.basicChaseAI()

        self.updateMove()




    def updateDraw(self):
        pass

        # def takeHit(self, damage):
        #     self.stats["health"].modValue(damage)
        #     # print self.Health.getValue()
        #     if self.stats["health"].getValue() == 0:
        #         self.onDeath()
        #
        # def onDeath(self):
        #     self.shouldDie = True