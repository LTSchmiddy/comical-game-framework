# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 16:03:01 2015

@author: alex
"""
import GameStat
import pygame, os, math, random
import flipAnim

from dataManagers import counter

class InstEnemy(pygame.sprite.Sprite):
    def __init__ (self, pos, world, dimens=[64, 64]):
        super(InstEnemy, self).__init__()

        self.imgDir = "_IMAGES\Sprites\Enemies\Spectre"
        self.imgExt = ".png"
        self.imgDict = {}

        self.spawnerList = []

        self.typeMode = "Enemy"

        self.name = "Dark Shade"
        self.myIndex = 0

        self.pos = pos
        self.loadImages()

        self.image = pygame.Surface([125, 75]).convert_alpha()
        self.rect = pygame.Rect(pos, self.image.get_size())
        # self.image.fill([255, 255, 255])
        self.shouldDie = False
        self.shouldFire = True
        self.stats = {
            "health": GameStat.Stat(200, 0, 200),
            "attrSpeed": GameStat.Stat(4, 0, 100)
        }
        self.world = world

        self.showChargeCounter = counter.TickCounter(30, False, True)
        self.showChargeCounter.setTime(30)

        self.showHitCounter = counter.TickCounter(30, False, True)
        self.showHitCounter.setTime(30)

        self.rectOffset = [0, 0]

        # AI Data:
        self.radius = 300
        self.detectsPlayer = False
        self.playerSeenPos = [0, 0]
        self.attackDistance = 100

        self.shouldWander = True
        self.wanderCounter = counter.TickCounter(150, True, False)
        self.wanderCounter.setTime(140)
        self.wanderDir = [random.randint(-1, 1), random.randint(-1, 1)]


        # Motion Data:

        self.allowDown = True
        self.allowLeft = True
        self.allowRight = True
        self.allowUp = True

        self.direction = "r"

        self.momentum = [0, 0]
        self.CompoundMomentum = False
        self.playerLastPos = self.rect.topleft

        self.canFly = True

        self.xpReward = 0


    def setMyIndex(self):
        self.myIndex = self.world.Enemies.index(self)

    def runAI(self):
        if not self.CompoundMomentum:
            self.momentum[0] = 0
            if self.canFly:
                self.momentum[1] = 0

        self.resetCollision()
        self.checkForEnvCollisions()
        # self.rect.x = self.pos[0]
        # self.rect.y = self.pos[1]


    def say(self, text, time=120, offset=[0,0], size=16):

        self.world.wordbubbles.add(text, self.name + str(self.myIndex), self.rect, offset, size, time)



    def basicWanderAI(self):
        if self.wanderCounter.check():
            self.wanderDir = [random.randint(-1, 1), random.randint(-1, 1)]

        self.doMove(self.wanderDir)

    def preventOverlap(self):
        pass
        # for i in self.world.Enemies:
        #
        #     if pygame.sprite.collide_rect(self, i):
        #         if i.pos[0] < self.pos[0]:
        #             self.allowRight = False
        #             self.momentum[0] -= (self.rect.width + i.rect.width)
        #
        #         if i.pos[0] > self.pos[0]:
        #             # print "NO RIGHT"
        #             self.allowLeft = False
        #             self.momentum[0] += (self.rect.width + i.rect.width)
        #             # self.allowRight = False

    def basicChaseAI(self):
        self.checkForPlayer()
        if self.detectsPlayer:
            self.shouldWander = False
            self.moveTo([self.playerLastPos[0] - (self.rect.topleft[0] - self.pos[0]), self.playerLastPos[1]])
            if GameStat.getDist(self.pos, self.playerLastPos) > self.attackDistance:

                self.doAttack()


        else:
            if not self.shouldWander:
                self.moveTo(self.playerLastPos)

                if GameStat.getDist(self.playerLastPos, self.rect.topleft) < 256:
                    self.shouldWander = True
            else:
                self.basicWanderAI()
                # self.moveTo(self.playerLastPos)

    def getAngleTo(self, point):
        return math.atan2(point[1] - self.rect.topleft[1],
                   point[0] - self.rect.topleft[0])


    def checkForPlayer(self):
        self.detectsPlayer = False
        if pygame.sprite.collide_circle(self, self.world.mainPlayer):
            if self.world.ac.linecast(self.rect.center, self.world.mainPlayer.rect.center) == None:
                self.detectsPlayer = True
                self.playerLastPos = self.world.mainPlayer.pos[:]
                return True

        self.detectsPlayer = False
        return False


    def checkForEnvCollisions(self):
        for i in self.world.envObj:
            for j in i.Walls:
                if j.colliderect(self.rect):
                    self.handleEnvCollision(j)

    def doAttack(self):
        pass

    def takeHit(self, damage):
        self.stats["health"].modValue(damage)
        self.playerLastPos = self.world.mainPlayer.pos[:]
        self.shouldWander = False
        self.showHitCounter.reset()
        # print self.Health.getValue()
        if self.stats["health"].getValue() == 0:
            self.onDeath()

    def onDeath(self):
        if not self.shouldDie:
            self.shouldDie = True
            self.world.mainPlayer.level.rewardXP(self.xpReward)
            self.say("+" + str(self.xpReward) + " XP", 60, [0, 0], 22)

    def moveTo(self, target, buffer = None):
        if buffer == None:
            buffer = self.stats["attrSpeed"].getValue()


        if (target[0] - self.pos[0]) < -buffer:
            self.doMove([-1, 0])
        if (target[0] - self.pos[0]) > buffer:
            self.doMove([1, 0])
        if (target[1] - self.pos[1]) < -buffer:
            self.doMove([0, -1])
        if (target[1] - self.pos[1]) > buffer:
            self.doMove([0, 1])

    def doMove(self, direction):
        self.momentum[0] += direction[0] * self.stats["attrSpeed"].getValue()
        self.momentum[1] += direction[1] * self.stats["attrSpeed"].getValue()

    def resetCollision(self):
        self.allowDown = True
        self.allowLeft = True
        self.allowRight = True
        self.allowUp = True

    def handleEnvCollision(self, Rect):
        if Rect.direction == "up":
            self.allowDown = False
            if self.rect.bottom > Rect.top  and (self.momentum[1] >= 0):
                self.pos[1] = Rect.top - self.rect.height + 1 - self.rectOffset[1]

        if Rect.direction == "left":
            self.allowRight = False
            if self.rect.right < Rect.left:
                self.pos[0] = Rect.left - self.rect.width + 5 - self.rectOffset[0]

                # print "Left Hit \n ****"
        if Rect.direction == "right":
            self.allowLeft = False
            if self.rect.left > Rect.right:
                self.pos[0] = Rect.right + 5 - self.rectOffset[0]
                # print "Left Hit \n ****"

        if Rect.direction == "down":
            self.allowUp = False
            if self.rect.top > Rect.bottom:
                self.pos[1] = Rect.bottom + 5 - self.rectOffset[1]



    def updateMove(self):

        self.preventOverlap()
        if not self.canFly:
            if self.momentum[1] < 0:
                self.momentum[1] = 0

            if self.momentum[1] <= 20:
                self.momentum[1] += .5

        if self.allowDown == False and self.momentum[1] > 0:
            self.momentum[1] = 0
        if self.allowRight == False and self.momentum[0] > 0:
            # print "NO RIGHT"
            self.momentum[0] = 0
        if self.allowLeft == False and self.momentum[0] < 0:
            # print "NO RIGHT"
            self.momentum[0] = 0
        if self.allowUp == False and self.momentum[1] < 0:
            self.momentum[1] = 0

        # if self.inputTracker["shift"]:
        self.pos[0] += self.momentum[0]  # * (1 + self.inputTracker["shift"])
        self.pos[1] += self.momentum[1]
        self.rect.x = self.pos[0] + self.rectOffset[0]
        self.rect.y = self.pos[1] + self.rectOffset[1]

        if self.momentum[0] > 0:
            self.direction = "r"
        else:
            self.direction = "l"

    def loadImages(self):
        for i in os.listdir(self.imgDir):
            if i.endswith(self.imgExt):
                filePath = self.imgDir + "\\" + i
                imgName = i.split(self.imgExt)[0]
                imgIn = pygame.image.load(filePath)
                # print cModDict["itemID"]
                self.imgDict[imgName] = imgIn

    def sanitize(self):
        self.spawnerList = []
        del self.imgDict
        del self.image

    def reloadEnemy(self):
        self.imgDict = {}
        self.loadImages()
        self.image = pygame.Surface([125, 75]).convert_alpha()


    def updateDraw(self):
        super(InstEnemy, self).updateDraw()






# class EnemyManager:
#     def __init__(self):
#         self.entries = {}
#         self.defPath = "EngineControl/GamePlayObjects/Enemies"
#
#     def loadEnemyDefs(self):
#
#
#         for i in os.listdir(self.defPath):
#             enemyName = i.split(".enemy")[0]
#
#
#             toLoad = None
#             filePath = self.defPath + "/" + i
#             defFile = open(filePath, "r")
#             defStr = defFile.read() + "\ntoLoad = EnemyDef"
#             exec defStr
#
#             self.entries[enemyName] = toLoad
#
#     def __getitem__(self, i):
#         return self.entries[i]


defPath = "EngineControl/GamePlayObjects/Enemies"
classes = {}

defsStr = ""

for i in os.listdir(defPath):
    enemyName = i.split(".enemy")[0]


    toLoad = None
    filePath = defPath + "/" + i
    defFile = open(filePath, "r")
    defsStr = defsStr + defFile.read() + "\n\n"


exec defsStr