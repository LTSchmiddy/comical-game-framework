import pygame, EnviroObject, Player, Projectile, GameStat, math, Enemy, PickUpItems, envInteractObj, loadEnvMeta, metaQuery, Editor, Artifact, os, random, copy

from GamePlayObjects import EnemyTypes

from dataManagers import audioMan

class AdvancedChecker:
    def __init__(self, world):
        self.world = world

    def linecast(self, start, end, interval = 8, checkNonSolid = False, list = None):

        if list == None:
            list = self.world.envObj



        dist = GameStat.getDist(start, end)
        xDist = end[0] - start[0]
        yDist = end[1] - start[1]

        angle = math.atan2(yDist, xDist)

        # print math.degrees(angle)

        xInterval = (xDist / dist) * interval * 1.0
        yInterval = (yDist / dist) * interval * 1.0
        # print xInterval
        # print yInterval

        i = 0
        while (i * interval) <= dist:
            # print (i * interval), "vs.", dist
            checkPoint = [start[0] + (xInterval * i), start[1] + (yInterval * i)]

            # self.world.fireProjectile(checkPoint, 0, 0, "DebugParticle")

            for j in list:
                if j.solid:
                    if j.rect.collidepoint(checkPoint):
                        return j
            i += 1

        return None
