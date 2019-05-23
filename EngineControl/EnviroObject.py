import pygame
import random
import runpy
import flipAnim
import copy

from dataManagers import TileScan, audioMan

from dataManagers import contentPackages
contentHandler = contentPackages.mainHandler

envAudio = audioMan.SoundController()
envAudio.loadFromDir2("_AUDIO/FX/EnvObj", 1)
envAudio.prepSounds()


class Wall(pygame.Rect):
    def __init__(self, pos, dimens, direction):
        super(Wall, self).__init__(pos, dimens)

        self.direction = direction

#Game World Object Base:
class InstEnvObj(pygame.sprite.Sprite):
    def __init__(self, jsonArgs):
        global envAudio
        super(InstEnvObj, self).__init__()
        self.pklData = {"image":None}

        self.jsonArgs = jsonArgs
        self.audio = envAudio
        self.world = jsonArgs["world"]
        pos = jsonArgs["pos"]
        self.pos = pos

        self.typeMode = "Env"

        self.isChild = False
        self.hidden = False
        if "hidden" in self.jsonArgs:
            self.hidden = self.jsonArgs["hidden"]

        self.isFluid = False
        if "fluid" in self.jsonArgs:
            self.isFluid = self.jsonArgs["fluid"]

        dimens = [0, 0]
        if "dimens" in jsonArgs:
            dimens = jsonArgs["dimens"]
        self.dimens = dimens

        self.label = jsonArgs["label"]

        self.image = pygame.Surface(dimens)

        if "usePixelAlpha" in jsonArgs:
            if self.jsonArgs["usePixelAlpha"]:
                self.image = self.image.convert_alpha()


        if "alpha" in jsonArgs:
            self.image.set_alpha(jsonArgs["alpha"])
        self.dimens = dimens
        self.rect = pygame.Rect(pos, dimens)

        self.shouldDrawWalls = True
        if "drawWalls" in self.jsonArgs:
            self.shouldDrawWalls = self.jsonArgs["drawWalls"]


        if "color" in jsonArgs:
            self.color = jsonArgs["color"]
        else:
            self.color = [0, 0, 0]

        if "radius" in jsonArgs:
            self.radius = jsonArgs["radius"]

        self.setWalls(self.pos, self.dimens)

        self.isDrawn = False

        self.solid = True
        if "isSolid" in jsonArgs:
            self.solid = jsonArgs["isSolid"]


        self.layer = jsonArgs["layer"]

        if "CropB" in jsonArgs:
            self.cropBottomRect(jsonArgs["CropB"])

        self.name = ""
        if "name" in jsonArgs:
            self.name = jsonArgs["name"]

        if "radius" in jsonArgs:
            self.radius = jsonArgs["radius"]

        self.InterMod = None
        if "InteractMod" in jsonArgs:
            self.InterMod = contentHandler.loadInterMod(self, self.jsonArgs["InteractMod"])

    def setWalls(self, pos = None, dimens = None):

        if pos == None:
            pos = self.pos

        if dimens == None:
            dimens = self.dimens

        if self.jsonArgs["type"].endswith("Obj"):
            self.Walls = []
            if not "up" in self.jsonArgs["skipWall"]:
                self.Walls.append(Wall([pos[0] + 2, pos[1]], [dimens[0] - 4, 1], "up"))
            if not "left" in self.jsonArgs["skipWall"]:
                self.Walls.append(Wall([pos[0] - 5, pos[1] + 1], [1, dimens[1] - 1], "left"))
            if not "right" in self.jsonArgs["skipWall"]:
                self.Walls.append(Wall([pos[0] + dimens[0] + 5, pos[1] + 1], [1, dimens[1] - 1], "right"))
            if not "down" in self.jsonArgs["skipWall"]:
                self.Walls.append(Wall([pos[0] + 2, pos[1] + dimens[1]], [dimens[0] - 4, 1], "down"))

        elif self.jsonArgs["type"].endswith("Plat"):
            self.Walls = [
                Wall([pos[0] + 2, pos[1]], [dimens[0] - 4, 1], "up")
            ]
        else:
            self.Walls = []

    # def __setstate__(self, state):
    #     self.__dict__ = state
    #
    #     self.image = pygame.image.frombuffer(self.pklData["image"][str], self.pklData["image"]["dimens"], "RGBA")
    #     self.InterMod = None
    #     if "InteractMod" in self.jsonArgs:
    #         self.InterMod = \
    #         runpy.run_path("EngineControl\\GamePlayObjects\\InteractionModules\\" + jsonArgs["InteractMod"] + ".inter")[
    #             "InterMod"](self)
    #
    # def __getstate__(self):
    #     self.pklData["image"] = {
    #         "str": pygame.image.tostring(self.image, "RGBA"),
    #         "dimens": self.image.get_size()
    #     }
    #     del self.InterMod
    #     del self.image
    #     return self.__dict__

    def move(self, dir, movePlayer = True):
        self.rect.move_ip(dir)
        self.pos = [self.rect.topleft[0], self.rect.topleft[1]]

        # for i in self.Walls:
        if movePlayer and self.solid:
            if pygame.sprite.collide_rect(self.world.mainPlayer, self):
                self.world.mainPlayer.setPlayerPos(dir, True)


        self.setWalls(self.pos, self.dimens)

    def updateDraw(self):
        self.isDrawn = True
        # self.image.fill(self.color)

    def drawWalls(self, color = [0, 0, 0]):

        if not self.shouldDrawWalls:
            return

        if len(self.Walls) == 0:
            if color != [0, 0, 0]:
                newImg = pygame.Surface(self.rect.size)
                newImg.fill(color)
                newImg.set_alpha(75)
                self.image.blit(newImg, [0, 0])

        else:
            for i in self.Walls:
                if i.direction == "up":
                    pygame.draw.rect(self.image, color, pygame.Rect([0, 0], i.size), 10)

                elif i.direction == "left":
                    pygame.draw.rect(self.image, color, pygame.Rect([0, 0], i.size), 10)

                elif i.direction == "right":
                    pygame.draw.rect(self.image, color, pygame.Rect([self.image.get_width() - 1, 0], i.size), 10)

                elif i.direction == "down":
                    pygame.draw.rect(self.image, color, pygame.Rect([0, self.image.get_height() - 1], i.size), 10)



    def cropBottomRect(self, amount):
        self.Walls[3].move_ip(0, -amount)
        self.rect.height = self.rect.height - amount


# Game World Objects:





class InstColorObj(InstEnvObj):
    def __init__(self, jsonArgs):
        super(InstColorObj, self).__init__(jsonArgs)

    def updateDraw(self):
        self.image.fill(self.color)
        self.drawWalls()
        self.isDrawn = True



class InstColorBg(InstColorObj):
    def __init__(self, jsonArgs):
        super(InstColorBg, self).__init__(jsonArgs)
        self.Walls = []
        self.solid = False

class InstColorPlat(InstColorObj):
    def __init__(self, jsonArgs):
        super(InstColorPlat, self).__init__(jsonArgs)
        self.Walls = [Wall(self.pos, [self.dimens[0], 1], "up")]
        self.solid = False





class InstImageObj(InstEnvObj):
    def __init__(self, jsonArgs):
    # def __init__(self, pos, dimens, tile):
        super(InstImageObj, self).__init__(jsonArgs)

        if "tilePath" in jsonArgs:
            self.tile = TileScan.TileSet(jsonArgs["tilePath"], jsonArgs["tileSize"]).getTile(jsonArgs["tileCoord"])
        else:
            self.tile = contentHandler.loadImage(jsonArgs["imagePath"])

        self.tile = self.tile.convert_alpha()

    def updateDraw(self):
        self.isDrawn = True
        self.image.fill(self.color)
        i = 0
        j = 0

        for i in range(0, (self.image.get_width() / self.tile.get_width()) + 1):
            for j in range(0, (self.image.get_height() / self.tile.get_height()) + 1):
                self.image.blit(self.tile, [i * self.tile.get_width(), j * self.tile.get_height()])
                j += 1
            i += 1

        self.drawWalls()

class InstImageBg(InstImageObj):
    def __init__(self, jsonArgs):
    # def __init__(self, pos, dimens, tile):
        super(InstImageBg, self).__init__(jsonArgs)

        self.solid = False
        self.Walls = []

class InstImagePlat(InstImageObj):
    def __init__(self, jsonArgs):
    # def __init__(self, pos, dimens, tile):
        super(InstImagePlat, self).__init__(jsonArgs)

        self.solid = False
        self.Walls = self.Walls = [Wall(self.pos, [self.dimens[0], 1], "up")]





class InstAnimImageObj(InstEnvObj):
    def __init__(self, jsonArgs):
    # def __init__(self, pos, dimens, tile):
        super(InstAnimImageObj, self).__init__(jsonArgs)

        self.anim = flipAnim.Animation(0, True)
        self.anim.loadFramesFromFolder(jsonArgs["animFolder"], jsonArgs["animExt"])
        self.tile = self.anim.frames[0]

        self.imgAnim = flipAnim.Animation(jsonArgs["animDelay"], True)

        self.isAnimDrawn = False

    def updateDraw(self):

        if not self.isAnimDrawn:
            i = 0
            j = 0

            for k in self.anim.frames:
                self.image = pygame.Surface(self.rect.size)
                self.image.fill(self.color)

                self.tile = k
                for i in range(0, (self.image.get_width() / self.tile.get_width()) + 1):
                    for j in range(0, (self.image.get_height() / self.tile.get_height()) + 1):
                        self.image.blit(self.tile, [i * self.tile.get_width(), j * self.tile.get_height()])
                        j += 1
                    i += 1
                self.drawWalls()
                self.imgAnim.frames.append(self.image)
            self.isAnimDrawn = True


        self.image = self.imgAnim.getFrame()





class InstAnimImageBg(InstAnimImageObj):
    def __init__(self, jsonArgs):
    # def __init__(self, pos, dimens, tile):
        super(InstAnimImageBg, self).__init__(jsonArgs)

        self.solid = False
        self.Walls = []

class InstAnimImagePlat(InstAnimImageObj):
    def __init__(self, jsonArgs):
    # def __init__(self, pos, dimens, tile):
        super(InstAnimImagePlat, self).__init__(jsonArgs)

        self.solid = False
        self.Walls = self.Walls = [Wall(self.pos, [self.dimens[0], 1], "up")]




class InstShuffleImageObj(InstEnvObj):
    def __init__(self, jsonArgs):
    # def __init__(self, pos, dimens, tile):
        super(InstShuffleImageObj, self).__init__(jsonArgs)
        self.tileList = []
        for i in range(0, len(self.tileList)):
            self.tileList[i] = self.tileList[i].convert_alpha()

        for i in jsonArgs["tiles"]:
            for j in range(0, i["weight"]):
                self.tileList.append(TileScan.TileSet(i["path"], i["size"]).getTile(i["coord"]))

        self.tile = random.choice(self.tileList)
        if "seed" in jsonArgs:
            self.seed = jsonArgs["seed"]
        else:
            newVal = 0
            for i in self.label:
                newVal += ord(i)
            self.seed = newVal / len (self.label)


    #
    def pickTile(self):
        self.tile = random.choice(self.tileList)

    def updateDraw(self):
        oldseed = random.seed
        random.seed(self.seed)
        self.isDrawn = True
        self.image.fill(self.color)
        i = 0
        j = 0

        for i in range(0, (self.image.get_width() / self.tile.get_width()) + 1):
            for j in range(0, (self.image.get_height() / self.tile.get_height()) + 1):
                self.tile = random.choice(self.tileList)
                self.image.blit(self.tile, [i * self.tile.get_width(), j * self.tile.get_height()])
                j += 1
            i += 1
        random.seed(oldseed)
        self.drawWalls()

class InstShuffleImageBg(InstShuffleImageObj):
    def __init__(self, jsonArgs):
    # def __init__(self, pos, dimens, tile):
        super(InstShuffleImageBg, self).__init__(jsonArgs)

        self.solid = False
        self.Walls = []

class InstShuffleImagePlat(InstShuffleImageObj):
    def __init__(self, jsonArgs):
    # def __init__(self, pos, dimens, tile):
        super(InstShuffleImagePlat, self).__init__(jsonArgs)

        self.solid = False
        self.Walls = [Wall(self.pos, [self.dimens[0], 1], "up")]

#ImageGrid
class InstImageGridObj(InstEnvObj):
    def __init__(self, jsonArgs):
    # def __init__(self, pos, dimens, tile):
        super(InstImageGridObj, self).__init__(jsonArgs)
        self.tileGrid = jsonArgs["grid"]
        self.tileDict = {}
        self.tileSize = jsonArgs["tileSize"]

        pos = jsonArgs["pos"]
        dimens = [len(self.tileGrid[0]) * self.tileSize[0], len(self.tileGrid) * self.tileSize[1]]
        self.image = pygame.Surface(dimens).convert_alpha()
        self.rect = pygame.Rect(pos, dimens)



        for i in jsonArgs["images"]:
            if "tile" in jsonArgs["images"][i]:
                if "offset" in jsonArgs["images"][i]["tile"]:
                    self.tileDict[i] = TileScan.TileSet(jsonArgs["images"][i]["tile"]["path"], jsonArgs["images"][i]["tile"]["size"]).getTile(jsonArgs["images"][i]["tile"]["coord"], jsonArgs["images"][i]["tile"]["offset"])
                else:
                    self.tileDict[i] = TileScan.TileSet(jsonArgs["images"][i]["tile"]["path"], jsonArgs["images"][i]["tile"]["size"]).getTile(jsonArgs["images"][i]["tile"]["coord"])
            else:
                self.tileDict[i] = contentHandler.loadImage(jsonArgs["images"][i]["path"])
            self.tileDict[i] = self.tileDict[i].convert_alpha()

    def updateDraw(self):
        self.isDrawn = True
        if self.jsonArgs["shouldFill"]:
            self.image.fill(self.color)
        else:
            self.image.fill([0, 0, 0, 0])
        for y in range(0, len(self.tileGrid)):
            for x in range(0, len(self.tileGrid[y])):
                if not self.tileGrid[y][x] == "":
                    self.image.blit(self.tileDict[self.tileGrid[y][x]], [x * self.tileSize[0], y * self.tileSize[1]])

        # for i in self.Walls:
        #     pygame.draw.rect(self.image, pygame.Rect(self.rect.x))

        self.drawWalls()

class InstImageGridBg(InstImageGridObj):
    def __init__(self, jsonArgs):
    # def __init__(self, pos, dimens, tile):
        super(InstImageGridBg, self).__init__(jsonArgs)


        self.solid = False
        self.Walls = []

class InstImageGridPlat(InstImageGridObj):
    def __init__(self, jsonArgs):
    # def __init__(self, pos, dimens, tile):
        super(InstImageGridPlat, self).__init__(jsonArgs)

        self.solid = False
        self.Walls = [Wall(self.pos, [self.dimens[0], 1], "up")]



class InstSingleImageObj(InstEnvObj):
    def __init__(self, jsonArgs):
    # def __init__(self, pos, dimens, tile):
        super(InstSingleImageObj, self).__init__(jsonArgs)
        pos = jsonArgs["pos"]


        self.label = jsonArgs["label"]

        self.anim = None
        if "tilePath" in jsonArgs:
            self.image = self.tile = TileScan.TileSet(jsonArgs["tilePath"], jsonArgs["tileSize"]).getTile(jsonArgs["tileCoord"])
        elif "animFolder" in jsonArgs:
            self.anim = flipAnim.Animation(jsonArgs["animDelay"], True)
            self.anim.loadFramesFromFolder(jsonArgs["animFolder"], jsonArgs["animExt"])
            self.image = self.anim.getFrame()
        else:
            self.image = contentHandler.loadImage(jsonArgs["imagePath"])
        self.imageOriginal = self.image.convert_alpha()
        self.image = self.image.convert_alpha()

        dimens = [self.image.get_width(), self.image.get_height()]
        self.dimens = dimens
        self.rect = pygame.Rect(pos, dimens)

        # self.Walls = [
        #     Wall(pos, [dimens[0], 1], "up"),
        #     Wall([pos[0], pos[1] + 1], [1, dimens[1] - 1], "left"),
        #     Wall([pos[0] + dimens[0] - 1, pos[1] + 1], [1, dimens[1] - 1], "right"),
        #     Wall([pos[0] + 1, pos[1] + dimens[1]], [dimens[0] - 2, 1], "down")
        # ]

        self.setWalls(self.pos, self.dimens)
        self.isDrawn = False
        self.solid = True

        self.layer = jsonArgs["layer"]



        self.InterMod = None
        if "InteractMod" in jsonArgs:
            self.InterMod = runpy.run_path("EngineControl\\GamePlayObjects\\InteractionModules\\" + jsonArgs["InteractMod"] + ".inter")["InterMod"](self)

        if "CropB" in jsonArgs:
            self.cropBottomRect(jsonArgs["CropB"])

    def drawWalls(self, color = [0, 0, 0]):

        if not self.shouldDrawWalls:
            return


        # if self.anim != None:
            # self.image = copy.deepcopy(self.imageOriginal)
        if len(self.Walls) == 0:
            pass

        else:
            for i in self.Walls:
                if i.direction == "up":
                    pygame.draw.rect(self.image, color, pygame.Rect([0, 0], i.size), 10)

                elif i.direction == "left":
                    pygame.draw.rect(self.image, color, pygame.Rect([0, 0], i.size), 10)

                elif i.direction == "right":
                    pygame.draw.rect(self.image, color, pygame.Rect([self.image.get_width() - 1, 0], i.size), 10)

                elif i.direction == "down":
                    pygame.draw.rect(self.image, color, pygame.Rect([0, self.image.get_height() - 1], i.size), 10)

    def updateDraw(self):

        if self.anim != None:
            self.image = self.anim.getFrame()

            if "alpha" in self.jsonArgs:
                self.image.set_alpha(self.jsonArgs["alpha"])
        else:
            self.drawWalls()
            self.isDrawn = True



class InstSingleImageBg(InstSingleImageObj):
    def __init__(self, jsonArgs):
        # def __init__(self, pos, dimens, tile):
        super(InstSingleImageBg, self).__init__(jsonArgs)

        self.solid = False
        self.Walls = []

class InstSingleImagePlat(InstSingleImageObj):
    def __init__(self, jsonArgs):
        # def __init__(self, pos, dimens, tile):
        super(InstSingleImagePlat, self).__init__(jsonArgs)

        self.solid = False
        self.Walls = [Wall(self.pos, [self.dimens[0], 1], "up")]

# class InstPlatform(pygame.sprite.Sprite):
#     def __init__(self, pos, dimens, color):
#         self.image = pygame.Surface(dimens)
#         self.rect = pygame.Rect(pos, dimens)
#         self.Walls = [Wall(pos, [dimens[0], 1], "up")]
#         self.color = color
#
#         self.isDrawn = False
#
#
#     def updateDraw(self):
#         self.isDrawn = True