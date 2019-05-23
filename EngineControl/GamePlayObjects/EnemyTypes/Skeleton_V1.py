import pygame

from EngineControl import Enemy as Enemy
from EngineControl import GameStat as GameStat
from EngineControl import flipAnim as flipAnim
from dataManagers import TileScan


class Skeleton(Enemy.InstEnemy):
    def __init__ (self, pos, world):

        self.tileSet = TileScan.TileSet("_IMAGES\\Sprites\\Enemies\\Skeleton1\\MAINSkeletonTileSheet.png", [64, 64], True)
        self.image = self.tileSet.getTile([0, 0])
        self.rect = pygame.Rect(pos, self.image.get_size())
        self.radius = 350
        # self.image.fill([255, 255, 255])
        self.shouldDie = False
        self.shouldFire = True
        self.stats = {
            "health": GameStat.Stat(20, 0, 20)
        }
        self.walkUpAnim = flipAnim.Animation(5)
        self.walkUpAnim.loadFramesFromTileRow(self.tileSet,[64, 64], [1, 8], 8)
        self.world = world


    def runAI(self):
        pass

    def takeHit(self, damage):
        self.stats["health"].modValue(damage)
        # print self.Health.getValue()
        if self.stats["health"].getValue() == 0:
            self.onDeath()

    def onDeath(self):
        self.shouldDie = True


    def updateDraw(self):
        self.image = self.walkUpAnim.getFrame()