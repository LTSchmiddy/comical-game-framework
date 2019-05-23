import os
import pygame


class Animation(object):
    def __init__(self, frameDelay, shouldLoop=True, frames = []):
        # Data Variables:

        self.frames = frames
        self.frameDelay = frameDelay
        self.shouldLoop = shouldLoop

        # Execution Variables:
        self.currentFrame = 0
        self.transitionCounter = 0

    def frameCount(self):
        return len(self.frames)

    def loadFramesFromFolder(self, folder, extension):
        self.frames = []
        for i in range(0, len(os.listdir(folder))):
            path = folder + "\\" + str(i + 1) + extension
            self.frames.append(pygame.image.load(path))

    def loadFramesFromTileRow(self, tiles, size, startPos, number):
        self.frames = []
        # tiles = TileScan.TileSet(file, size, True)

        for i in range(0, number):
            self.frames.append(tiles.getTile([startPos[0] + i, startPos[1]]))

    def duplicate(self):
        newFrames = []

        for i in self.frames:
            newFrames.append(i.copy())

        return Animation(self.frameDelay, self.shouldLoop, newFrames)



    def reset(self):
        self.currentFrame = 0
        self.transitionCounter = 0

    def getLastFrame(self):
        return self.frames[self.frameCount() - 1]

    def getFrame(self):
        if self.transitionCounter >= self.frameDelay:
            self.transitionCounter = 0
            self.currentFrame += 1

            if self.currentFrame >= self.frameCount():

                if not self.shouldLoop:
                    self.currentFrame = self.frameCount() - 1
                    return self.getLastFrame()
                else:
                    self.currentFrame = 0


        else:
            self.transitionCounter += 1

        return self.frames[self.currentFrame]







