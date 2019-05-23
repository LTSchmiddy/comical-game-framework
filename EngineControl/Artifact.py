import pygame, math, runpy, os, flipAnim
import pygame.gfxdraw

from dataManagers import counter

pygame.font.init()


class WordBubbleManager:
    def __init__(self, world):
        self.world = world

        self.wbDict = {}

    def add(self, text, tag, bindRect, offset=[0,0], size=16, time=120):
        if not self.wbDict.has_key(tag):
            self.wbDict.update({tag: []})

        self.wbDict[tag].append(WordBubble(self.world, text, bindRect, offset, size, time))


    def onUpdate(self):
        toRemove = []
        for i in self.wbDict:
            if len(self.wbDict[i]) == 0:
                toRemove.append(i)
                continue

            self.wbDict[i][0].onUpdate()

            if self.wbDict[i][0].shouldDie:
                del self.wbDict[i][0]

        if len(toRemove) > 0:
            for i in toRemove:
                del self.wbDict[i]


    def Draw(self):
        for i in self.wbDict:
            if len(self.wbDict[i]) > 0:
                self.world.retDrawOver.append([self.wbDict[i][0].image, self.wbDict[i][0].rect.topleft])

class WordBubble:
    def __init__(self, world, text, bindRect, offset=[0,0], size=16, time=120):
        self.shouldDie = False
        self.world = world
        self.text = text
        self.size = size
        self.time = time
        self.offset = offset
        self.bindRect = bindRect

        self.fontRend = pygame.font.Font("_IMAGES\\ComicSans.ttf", size)

        self.textSurf = self.fontRend.render(self.text, True, [0, 0, 0])

        self.ellipseRect = pygame.Rect([0, 0], [self.textSurf.get_width() * math.sqrt(2), self.textSurf.get_height() * math.sqrt(2)])

        self.image = pygame.Surface([self.ellipseRect.width, self.ellipseRect.height + 20])
        self.image = self.image.convert_alpha()
        self.rect = pygame.Rect([0, 0], self.image.get_size())

        self.image.fill([0, 0, 0, 0])

        pygame.draw.ellipse(self.image, [0, 0, 0], self.ellipseRect, 0)
        pygame.draw.ellipse(self.image, [255, 255, 255, 200], pygame.Rect([5, 5], [self.ellipseRect.width - 10, self.ellipseRect.height - 10]), 0)

        # for i in range(0, 15):
        #     pygame.gfxdraw.aaellipse(self.image, self.ellipseRect.centerx, self.ellipseRect.centery, (self.ellipseRect.width/2) - i, (self.ellipseRect.height/2) - i, [0, 0, 0])
        # pygame.gfxdraw.filled_ellipse(self.image, self.ellipseRect.centerx, self.ellipseRect.centery, self.ellipseRect.width/2, self.ellipseRect.height/2, [0, 0, 0])
        # pygame.draw.ellipse(self.image, [255, 255, 255, 200], pygame.Rect([5, 5], [self.ellipseRect.width - 10, self.ellipseRect.height - 10]), 0)

        self.image.blit(self.textSurf, [(self.ellipseRect.width - self.textSurf.get_width())/2, (self.ellipseRect.height - self.textSurf.get_height())/2])

        self.timer = counter.TickCounter(time, False, False)

    def onUpdate(self):
        self.shouldDie = self.timer.check()

        self.rect.bottomleft = self.bindRect.topright

    # def __setstate__(self, state):
    #
    #
    # def __getstate__(self):
    #     retVal = {
    #         "world": world,
    #         "text": text,
    #         "bindRect", bindRect, offset = [0, 0], size = 16, time = 120
    #     }



