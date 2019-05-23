import pygame, math, runpy, os, flipAnim, copy

from dataManagers import audioMan


from dataManagers import contentPackages
contentHandler = contentPackages.mainHandler


class InstProjectile(pygame.sprite.Sprite):
    def __init__(self, pos, angle, world):
        self.angle = angle
        self.pos = pos
        self.world = world

        self.mPi = math.pi

        self.projData = {}

        self.audio = self.world.projAudio

        # Defaults
        self.image = pygame.Surface([64, 64])
        self.rect = pygame.Rect(self.pos, self.image.get_size())
        self.shouldKill = False
        self.lifeTime = 150
        self.speed = 20

        self.multiplier = 3
        self.lifeSpan = 0
        # self.radius = 20
        self.friendly = True
        self.damage = 10
        self.startPos = pos
        self.drawAfter = 0

        self.useGravity = 0
        self.hitObj = None

        self.momentum = [0, 0]
        if type(self.angle) is list:
            self.momentum = [self.angle[0] * self.speed, self.angle[1] * self.speed]

        else:
            self.angleMomentum()
        # print angle

    def rotateImage(self, rotateAngle):
        self.image = pygame.transform.rotate(self.image, rotateAngle)


    def angleMomentum(self):
        self.momentum = [ self.speed * math.cos(self.angle), self.speed * math.sin(self.angle)]
    
    def updateMove(self):
        if self.useGravity:
            if self.momentum[1] <= 20:
                self.momentum[1] += 3
        self.rect.move_ip(self.momentum)

        self.lifeSpan += 1

    def onHit(self):
        self.shouldKill = True
        
    
    
    def updateDraw(self):
        # self.image.fill([255, 255, 255])
        pass

# Pulse Laser:

class ProjectileManager:
    def __init__(self):
        self.projDict = {}

        self.mPi = math.pi


        for i in os.listdir("EngineControl\\GamePlayObjects\\Projectiles"):

            if i.endswith(".proj"):
                dataIn = runpy.run_path("EngineControl\\GamePlayObjects\\Projectiles\\" + i)
                self.prepProjectile(dataIn)

        for i in contentHandler.packDict:
            for j in contentHandler.packDict[i].projDicts:
                # print "Hello"
                self.prepProjectile(contentHandler.packDict[i].projDicts[j])


    def prepProjectile(self, dataIn):

        if "loadImgOnStart" in dataIn:
            if dataIn["loadImgOnStart"]:
                frameList = []
                for i in dataIn["images"]:
                    newFrame = contentHandler.loadImage(i)
                    newFrame = newFrame.convert_alpha()
                    frameList.append(newFrame)

                if "animSpeed" in dataIn:
                    dataIn.update({"useAnimLoaded": flipAnim.Animation(dataIn["animSpeed"], True, frameList)})
                else:
                    dataIn.update({"useAnimLoaded": flipAnim.Animation(10, True, frameList)})


        self.projDict[dataIn["ID"]] = dataIn



    def __getattr__(self, item):
        return self.projDict[item]



class InstProjectileDesc(InstProjectile):
    def __init__(self, pos, angle, ref, world):
        super(InstProjectileDesc, self).__init__(pos, angle, world)
        self.refName = ref

        self.audio = None
        self.refDict = None
        self.onHitFunct = None
        self.onMoveFunct = None
        self.onDrawFunct = None
        self.anim = None
        self.image = None

        self.reloadProj()

        self.rect = pygame.Rect(self.pos, self.image.get_size())
        self.lifeTime = self.refDict["lifeTime"]
        self.speed = self.refDict["speed"]

        self.multiplier = self.refDict["multiplier"]
        self.lifeSpan = 0
        # self.radius = 20
        self.friendly = self.refDict["friendly"]
        self.damage = self.refDict["damage"]
        self.startPos = pos
        self.drawAfter = self.refDict["drawAfter"]
        self.energyUse = self.refDict["energyUse"]
        self.cooldown = self.refDict["cooldown"]

        if "useGravity" in self.refDict:
            self.useGravity = self.refDict["useGravity"]

        self.refDict["onLoad"](self)


        if type(self.angle) is list:
            self.momentum = [self.angle[0] * self.speed, self.angle[1] * self.speed]

        else:
            self.angleMomentum()

    def reloadProj(self):
        self.audio = self.world.projAudio
        self.refDict = self.world.projectiles.projDict[self.refName]
        self.onHitFunct = self.refDict["onHit"]
        self.onMoveFunct = self.refDict["onMove"]
        self.onDrawFunct = self.refDict["onDraw"]

        if "loadImgOnStart" in self.refDict:
            if self.refDict["loadImgOnStart"]:
                self.anim = self.refDict["useAnimLoaded"].duplicate()
            else:
                self.loadImg()
        else:
            self.loadImg()
        self.image = self.anim.frames[0]

    def loadImg(self):
        frameList = []
        for i in self.refDict["images"]:
            newFrame = contentHandler.loadImage(i)
            newFrame = newFrame.convert_alpha()
            frameList.append(newFrame)

        if "animSpeed" in self.refDict:
            self.anim = flipAnim.Animation(self.refDict["animSpeed"], True, frameList)
        else:
            self.anim = flipAnim.Animation(10, True, frameList)


    def sanitize(self):
        del self.refDict
        del self.onHitFunct
        del self.onMoveFunct
        del self.onDrawFunct
        del self.anim
        del self.image
        del self.audio


    def onHit(self, rectObj = None):
        self.hitObj = rectObj
        self.onHitFunct(self)


    def onHitPlayer(self, rectObj=None):
        self.hitObj = rectObj
        if "onHitPlayer" in self.refDict:
            self.refDict["onHitPlayer"](self)

        self.onHitFunct(self)



    def rotateImage(self, rotateAngle, useDegrees = True):
        if useDegrees:
            rotateAngle = math.degrees(rotateAngle)

        self.image = pygame.transform.rotate(self.image, rotateAngle)
        for i in range(0, len(self.anim.frames)):
            self.anim.frames[i] = pygame.transform.rotate(self.anim.frames[i], rotateAngle)


    def updateMove(self):
        self.onMoveFunct(self)
        if self.useGravity != 0:
            if self.momentum[1] <= 20:
                self.momentum[1] += self.useGravity
        self.rect.move_ip(self.momentum)
        self.lifeSpan += 1

    def updateDraw(self):
        self.onDrawFunct(self)
        self.image = self.anim.getFrame()



