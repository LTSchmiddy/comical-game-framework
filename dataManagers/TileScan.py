import pygame, os

class TileSet:
    def __init__(self, imgPath, tileDimens, customPath=False):
        if not customPath:
            self.img = pygame.image.load("".join(["_IMAGES\\TileSets\\", imgPath])).convert_alpha()
            self.tileDimens = tileDimens
        else:
            self.img = pygame.image.load(imgPath).convert_alpha()
            self.tileDimens = tileDimens


    def getTile(self, pos, offset = [0, 0]):
        retVal = pygame.Surface(self.tileDimens)
        retVal = retVal.convert_alpha()
        for i in range(0, self.tileDimens[0]):
            for j in range(0, self.tileDimens[1]):
                setColor = self.img.get_at([self.tileDimens[0] * pos[0] + i + offset[0], self.tileDimens[1] * pos[1] + j + offset[1]])

                retVal.set_at([i, j], setColor)
        return retVal


# cave = TileSet("cave.png", [16, 16])
# sewer = TileSet("sewer_Large.png", [64, 64])