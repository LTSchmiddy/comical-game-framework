import pygame, AdvancedChecks, EnviroObject, Player, Projectile, math, Enemy, PickUpItems, envInteractObj, loadEnvMeta, metaQuery, Editor, Artifact, os, random, copy, questMan

from GamePlayObjects import EnemyTypes

from dataManagers import audioMan

__all__ = ['Artifact', 'Editor','Enemy', 'envInteractObj', 'EnviroObject',  'flipAnim', 'GameStat',  'loadEnvMeta', 'metaQuery', 'PickUpItems', 'Player',  'Projectile', "questMan"]


# for i in os.listdir("EngineControl"):
#     if i != "__init__.py" and ".py" in i and not (i in __all__):
#         __all__.append(i.split(".")[0])
#
# print __all__





class Environment:
    def __init__(self, width, height, panel, grid = "_OverWorld", gridPos = [0, 0]):
        self.version = 1.0
        self.panel = panel
        self.ac = AdvancedChecks.AdvancedChecker(self)

        self.editor = Editor.WorldEditor(self)

        # self.worldEdgeLeft = -90 * 32
        # self.worldEdgeRight = 105 * 32
        # self.worldEdgeUp = -60 * 32
        # self.worldEdgeDown = 75 * 32

        self.worldEdgeLeft = -float("inf")
        self.worldEdgeRight = float("inf")
        self.worldEdgeUp = -float("inf")
        self.worldEdgeDown = float("inf")


        # self.random = random

        self.retDrawUnder = []
        self.retDrawOver = []
        self.retDraw = []
        self.permenData = metaQuery.metaArchive(self)


        self.items = PickUpItems.ItemManager(self)
        self.projectiles = Projectile.ProjectileManager()

        self.projAudio = audioMan.SoundController()
        self.projAudio.loadFromDir2("_AUDIO/FX/Projectiles", 1)
        self.projAudio.prepSounds()

        self.worldMeta = {}
        self.worldJson = {}
        self.size = [width, height]

        self.defineWorldObj()

        self.envObj = []

        self.envProj = []

        # self.envInterObj = []
        self.interactionMarker = envInteractObj.InteractionMarker(self)
        self.interactionMarker.setText("TESTING!!")


        # self.envInterObj = []
        self.envInterObj = [PickUpItems.InstPickup([400, 40], "SMG1", self)]

        self.envLocalTransitionObj = {}

        #Data Pertaining To Level Files

        # self.currentGrid = "_Amberdale"
        self.currentGrid = grid
        # self.worldGridPos = [0, 0]
        self.worldGridPos = gridPos

        self.currentLevel = loadEnvMeta.getEvlJsonPath(self.currentGrid, self.worldGridPos)

        self.frameSize = [0, 0]

        self.nextLevel = None
        self.nextDestination = None
        

        # self.Panel = pygame.Surface (self.size)
        # self.backgroundColor = [25, 25, 25]
        self.backgroundColor = [25, 25, 25]
        self.mouseWorld = [0, 0]

        self.triggerEnv([0, 0], grid, gridPos)
        self.reloadEvl()
        # self.mainPlayer = Player.InstPlayer([0, 0], self)
        self.mainPlayer = Player.InstPlayer(self.worldMeta["PlayerSpawn"]["GameStart"], self)



        self.Enemies = []
        # self.Enemies = [Enemy.classes["VoidStalker"]([0, 0], self)]
        self.enemiesToSpawn = []

        self.wordbubbles = Artifact.WordBubbleManager(self)

        # self.backgroundImage = pygame.Surface([1920, 1080])
        # # self.backgroundImage.fill(self.backgroundColor)
        # self.backgroundImage.fill([0, 0, 0])
        # self.backgroundImage.blit(pygame.image.load("_IMAGES/WorldBackgrounds/OverWorld/BgImage1.png"), [0, 0])

        self.Quests = questMan.QuestManager(self)

        self.wasFocused = False

        self.waitToReRender = True

        self.updateInvUI = False
        self.notif = None
        self.dialog = None
        self.flipbook = None
        self.steamApi = None
        self.debugLog = None
        self.audio = None
        self.saveMan = None
        self.storeMan = None
        self.contentPackageManager = None

        self.newPos = None


    def loadContentPacks(self):
        self.items.loadFromContPacks()


    def logicStep (self, offsetWorld):
        self.Enemies.extend(self.enemiesToSpawn)
        for i in self.enemiesToSpawn:
            i.setMyIndex()

        self.enemiesToSpawn = []


        # if self.wasFocused == False and pygame.mouse.get_focused():
        #     self.reloadEvl()


        if self.nextDestination != None:
            self.loadNextEnviroment(self.nextDestination)
            self.nextDestination = None

        if self.nextLevel != None:
            self.mainPlayer.setPlayerPos(self.nextLevel[0])
            self.loadEnv(self.nextLevel[0], self.nextLevel[1], self.nextLevel[2])
            self.nextLevel = None


        self.wasFocused = pygame.mouse.get_focused()
        
        self.mouseWorld = [-offsetWorld[0] + pygame.mouse.get_pos()[0], -offsetWorld[1] + pygame.mouse.get_pos()[1]]
        
        self.mainPlayer.bgTasks()

        # Enemy AI

        for i in self.envObj:
            if i.InterMod != None:
                i.InterMod.onAIUpdate()

            if i.rect.colliderect(self.mainPlayer.rect):
                if i.InterMod != None:
                    i.InterMod.onCollision()
                if i.isFluid:
                    self.mainPlayer.inFluid = True

            # if i.rect.colliderect(self.mainPlayer.rect):
            for j in i.Walls:
                if j.colliderect(self.mainPlayer.rect):
                    self.mainPlayer.handleEnvCollision(j)


        for i in self.Enemies:
            i.runAI()

            if i.shouldDie:
                self.Enemies.remove(i)


        for i in self.envInterObj:
            i.runAI()
            if i.rect.colliderect(self.mainPlayer):
                if i.tag == "Pickup":
                    if not self.mainPlayer.useOnHit:
                        i.onPickup()
                    else:
                        i.onUse()
                else:
                    i.onInteract()




            if i.shouldDie:
                self.envInterObj.remove(i)


        # Transition Tiles


        # Handle Projectiles
        for i in self.envProj:
            try:
                for j in range (0, i.multiplier):
                    
                    if i.lifeSpan > i.lifeTime:
                        i.shouldKill = True
                    else:   
                        for j in self.envObj:
                            if j.solid:
                                if i.rect.colliderect(j) and i.lifeSpan > 0:
                                    i.onHit(j)
                                
                        if i.rect.colliderect(self.mainPlayer) and i.friendly == False:
                            self.mainPlayer.takeHit(-i.damage)
                            i.onHitPlayer(self.mainPlayer)
                        for k in self.Enemies:
                            if i.rect.colliderect(k) and i.friendly == True:
                                k.takeHit(-i.damage)
                                i.onHit(k)
                    
                    if i.shouldKill == False:
                        i.updateMove()
            except ValueError:
                pass
            if i.shouldKill:
                i.onHit()
                self.envProj.remove(i)

        self.wordbubbles.onUpdate()
          
        
    def runEvents(self, events, PlayerOCL):

        fireAngle = math.atan2(self.mouseWorld[1] - self.mainPlayer.pos[1] - self.mainPlayer.dimens[1] / 2,self.mouseWorld[0] - self.mainPlayer.pos[0] - self.mainPlayer.dimens[0] / 2)
        # fireAngle = math.atan2(pygame.mouse.get_pos()[1] - self.frameSize[1] / 2 - self.mainPlayer.dimens[1] / 2, pygame.mouse.get_pos()[0] - self.frameSize[0] / 2 - self.mainPlayer.dimens[0] / 2)
        self.mainPlayer.runEvents(events, PlayerOCL, self.mouseWorld, fireAngle)
        
        if self.editor != None:
            self.editor.eventLoop(events)


    def fireProjectile(self, origin, angle, acc, projectile):
        angleAdj = 0
        if acc != 0:
            angleAdj = math.radians(random.randint(-acc, acc))
        self.envProj.append(Projectile.InstProjectileDesc(origin, angle + angleAdj, projectile, self))




    def spawnEnemy(self, enemyName, position):
        newEnemy = Enemy.classes[enemyName](position, self)
        self.enemiesToSpawn.append(newEnemy)

        return newEnemy

    def preDraw(self):

        if self.newPos != None:
            # print "MOVING!"
            self.mainPlayer.pos = self.newPos[:]
        self.newPos = None


        if self.mainPlayer.pos[0] < self.worldEdgeLeft:
            self.mainPlayer.pos[0] = self.worldEdgeLeft

        if self.mainPlayer.pos[0] + self.mainPlayer.rect.width > self.worldEdgeRight:
            self.mainPlayer.pos[0] = self.worldEdgeRight - self.mainPlayer.rect.width

        if self.mainPlayer.pos[1] < self.worldEdgeUp:
            self.mainPlayer.pos[1] = self.worldEdgeUp

        if self.mainPlayer.pos[1] + self.mainPlayer.rect.height > self.worldEdgeDown:
            self.mainPlayer.pos[1] = self.worldEdgeDown - self.mainPlayer.rect.height


    def Draw(self, frameSize):

        self.preDraw()
        #Draw Background
        self.retDrawUnder = []
        self.retDrawOver = []
        self.retDraw = []


        # self.Panel.fill(self.backgroundColor)
        self.frameSize = frameSize
        #Draw Player
        

        for i in self.Enemies:
            i.updateDraw()
            self.retDraw.append([i.image, [i.pos[0], i.pos[1]]])

            # pygame.draw.line(self.Panel, [0, 0, 255], self.mainPlayer.rect.center, self.mouseWorld, 20)
            # pygame.draw.circle (self.Panel, [0, 0, 255], [int(self.mouseWorld[0]), int(self.mouseWorld[1])], 30, 0)
        for i in self.envObj:
            if not i.isDrawn:
                i.updateDraw()

            if not i.hidden:
                if i.layer <= 0:
                    self.retDrawUnder.append([i.image, [i.rect.x, i.rect.y]])
                else:
                    self.retDrawOver.append([i.image, [i.rect.x, i.rect.y]])

        # for i in self.envLocalTransitionObj:
        #     self.envLocalTransitionObj[i].updateDraw()
        #     self.retDrawUnder.append([self.envLocalTransitionObj[i].image, [ self.envLocalTransitionObj[i].rect.x,  self.envLocalTransitionObj[i].rect.y]])


        for i in self.envInterObj:
            i.updateDraw()
            self.retDraw.append([i.image, [i.rect.x, i.rect.y]])



        self.mainPlayer.updateDraw(frameSize[0]/2, frameSize[1]/2)
        self.retDraw.append([self.mainPlayer.imgArmBottom, [self.mainPlayer.pos[0] + self.mainPlayer.offsetBottomArm[0] , self.mainPlayer.pos[1]  + self.mainPlayer.offsetBottomArm[1]]])
        self.retDraw.append([self.mainPlayer.imgBody, [self.mainPlayer.pos[0] + self.mainPlayer.offsetBody[0], self.mainPlayer.pos[1]  + self.mainPlayer.offsetBody[1]]])
        self.retDraw.append([self.mainPlayer.imgLegs, [self.mainPlayer.pos[0] + self.mainPlayer.offsetLegs[0] , self.mainPlayer.pos[1]  + self.mainPlayer.offsetLegs[1]]])
        self.retDraw.append([self.mainPlayer.imgArmTop, [self.mainPlayer.pos[0] + self.mainPlayer.offsetTopArm[0] , self.mainPlayer.pos[1] + self.mainPlayer.offsetTopArm[1]]])

        for i in self.envProj:
            i.updateDraw()
            # pygame.draw.circle(self.Panel, [0, 0, 255], [i.rect.x, i.rect.y], 20, 0)
            if i.lifeSpan >= i.drawAfter:
                self.retDraw.append([i.image, [i.rect.x, i.rect.y]])



        # Draw Interaction Label:
        if self.interactionMarker.show and self.interactionMarker.text != "":
            self.retDrawOver.append([self.interactionMarker.image, [self.interactionMarker.rect.x, self.interactionMarker.rect.y]])


        self.wordbubbles.Draw()











    # ***************************************************************************

    # World Loading Methods:
    def defineWorldObj(self):
        self.envObjTypes = loadEnvMeta.objectTable()
        self.enemyObjTypes = loadEnvMeta.enemyTable()

    def triggerEnv(self, playerPos, grid = None, gridPos = None):
        self.nextLevel = [playerPos, grid, gridPos]



    def loadEnv(self, playerPos, grid = None, gridPos = None):
        self.clearRendering()

        self.Enemies = []
        self.envInterObj = []
        self.envProj = []
        self.envObj = []


        if grid != None:
            self.currentGrid = grid

        if gridPos != None:
            self.worldGridPos = gridPos


        self.currentLevel = loadEnvMeta.getEvlJsonPath(self.currentGrid, self.worldGridPos)
        self.worldJson = loadEnvMeta.loadEnv(self.currentLevel)
        self.worldMeta = {}
        self.loadFromWorldJson(playerPos)


    def loadFromWorldJson(self, playerPos = None, doClear = True):
        self.worldMeta = copy.deepcopy(self.worldJson)
        if doClear:
            self.envObj = []

        self.loadPlayerSpawn()

        self.backgroundColor = self.worldMeta["PlayerSpawn"]["Background Color"]

        if "WorldEdge" in self.worldMeta["PlayerSpawn"]:
            if "left" in self.worldMeta["PlayerSpawn"]["WorldEdge"]:
                self.worldEdgeLeft = self.worldMeta["PlayerSpawn"]["WorldEdge"]["left"]

            else:
                self.worldEdgeLeft = -float("inf")

            if "right" in self.worldMeta["PlayerSpawn"]["WorldEdge"]:
                self.worldEdgeRight = self.worldMeta["PlayerSpawn"]["WorldEdge"]["right"]
            else:
                self.worldEdgeRight = float("inf")

            if "up" in self.worldMeta["PlayerSpawn"]["WorldEdge"]:
                self.worldEdgeUp = self.worldMeta["PlayerSpawn"]["WorldEdge"]["up"]
            else:
                self.worldEdgeUp = -float("inf")

            if "down" in self.worldMeta["PlayerSpawn"]["WorldEdge"]:
                self.worldEdgeDown = self.worldMeta["PlayerSpawn"]["WorldEdge"]["down"]


            else:
                self.worldEdgeDown = float("inf")

        else:
            self.worldEdgeLeft = -float("inf")
            self.worldEdgeRight = float("inf")
            self.worldEdgeUp = -float("inf")
            self.worldEdgeDown = float("inf")


        self.buildWorldObjects(self.worldMeta["Objects"], [0, 0])
        # self.sortEnvObjEXP()
        self.sortEnvObj()

        if playerPos != None:
            self.mainPlayer.setPlayerPos(playerPos)



    def readLvlJson(self, filePath = None):
        self.clearRendering()

        # newEnemies = []
        self.currentLevel = loadEnvMeta.getEvlJsonPath(self.currentGrid, self.worldGridPos)
        self.worldJson = loadEnvMeta.loadEnv(self.currentLevel)
        self.worldMeta = copy.deepcopy(self.worldJson)
        self.loadPlayerSpawn()

        self.envObj = []
        self.buildWorldObjects(self.worldMeta["Objects"], [0, 0])
        # self.sortEnvObjEXP()
        self.sortEnvObj()

    def loadPlayerSpawn(self):
        self.backgroundColor = self.worldMeta["PlayerSpawn"]["Background Color"]

        if "WorldEdge" in self.worldMeta["PlayerSpawn"]:
            if "left" in self.worldMeta["PlayerSpawn"]["WorldEdge"]:
                self.worldEdgeLeft = self.worldMeta["PlayerSpawn"]["WorldEdge"]["left"]
            else:
                self.worldEdgeLeft = -float("inf")

            if "right" in self.worldMeta["PlayerSpawn"]["WorldEdge"]:
                self.worldEdgeRight = self.worldMeta["PlayerSpawn"]["WorldEdge"]["right"]
            else:
                self.worldEdgeRight = float("inf")

            if "up" in self.worldMeta["PlayerSpawn"]["WorldEdge"]:
                self.worldEdgeUp = self.worldMeta["PlayerSpawn"]["WorldEdge"]["up"]
            else:
                self.worldEdgeUp = -float("inf")

            if "down" in self.worldMeta["PlayerSpawn"]["WorldEdge"]:
                self.worldEdgeDown = self.worldMeta["PlayerSpawn"]["WorldEdge"]["down"]
            else:
                self.worldEdgeDown = float("inf")

        else:
            self.worldEdgeLeft = -float("inf")
            self.worldEdgeRight = float("inf")
            self.worldEdgeUp = -float("inf")
            self.worldEdgeDown = float("inf")


    
    def buildWorldObjects(self, dict, offset = [0, 0], isChild = False):

        newEnvObj = []

        for i in dict:
            dict[i]["label"] = i
            dict[i]["world"] = self
            # Loading from Templates


            if not "skipWall" in dict[i]:
                dict[i]["skipWall"] = []

            if not "shouldFill" in dict[i]:
                dict[i]["shouldFill"] = False

            if "useTemplateFile" in dict[i] or "useTemplate" in dict[i]:
                # templateFile = dict[i]["useTemplateFile"]

                if not "useTemplateFile" in dict[i]:
                    dict[i]["useTemplateFile"] = "WorldTemplates.json"

                if not "useTemplate" in dict[i]:
                    dict[i]["useTemplate"] = "__main__"

                templateMeta = loadEnvMeta.loadTemplate("Objects", dict[i]["useTemplate"], dict[i]["useTemplateFile"])
                for j in templateMeta:

                    if not j in dict[i]:
                        dict[i][j] = templateMeta[j]




            if not "PopUp" in dict[i]:
                dict[i]["PopUp"] = ""

            if not "pos" in dict[i]:
                dict[i]["pos"] = [0, 0]
            # if not "use64Xpos" in dict[i]:
            #     dict[i]["use64Xpos"] = True
            #
            # if dict[i]["use64Xpos"]:
            #     dict[i]["pos"][0] = dict[i]["pos"][0] * 32
            #     dict[i]["pos"][1] = dict[i]["pos"][1] * 32
            #

            if not "useMultPos" in dict[i]:
                dict[i]["useMultPos"] = 32

            dict[i]["pos"][0] = dict[i]["pos"][0] * dict[i]["useMultPos"]
            dict[i]["pos"][1] = dict[i]["pos"][1] * dict[i]["useMultPos"]

            # if not "use64Xdimens" in dict[i]:
            #     dict[i]["use64Xdimens"] = False
            #
            # if dict[i]["use64Xdimens"]:
            #     dict[i]["dimens"][0] = dict[i]["dimens"][0] * 32
            #     dict[i]["dimens"][1] = dict[i]["dimens"][1] * 32

            if not "useMultDimens" in dict[i]:
                dict[i]["useMultDimens"] = 1

            if "useMultDimens" in dict[i] and "dimens" in dict[i]:
                dict[i]["dimens"][0] = dict[i]["dimens"][0] * dict[i]["useMultDimens"]
                dict[i]["dimens"][1] = dict[i]["dimens"][1] * dict[i]["useMultDimens"]

            dict[i]["pos"][0] += offset[0]
            dict[i]["pos"][1] += offset[1]

            newCreatedObj = self.envObjTypes[dict[i]["type"]](dict[i])
            newCreatedObj.isChild = isChild
            newEnvObj.append(newCreatedObj)

            if "Children" in dict[i]:
                # print "Found a Child in", i
                self.buildWorldObjects(dict[i]["Children"], dict[i]["pos"], True)

        self.envObj.extend(newEnvObj)

    def sortEnvObj(self):
        newEnvObj = self.envObj[:]
        self.envObj = []
        while len(newEnvObj) > 0:
            AddObj = newEnvObj[0]
            for i in newEnvObj:
                if i.layer < AddObj.layer:
                    AddObj = i
            self.envObj.append(AddObj)
            newEnvObj.remove(AddObj)

    def sortEnvObjEXP(self, array = None):
        less = []
        equal = []
        greater = []

        if array == None:
            array = self.envObj[:]

        if len(array) > 1:
            pivot = array[0].layer
            for x in array:
                if x.layer < pivot:
                    less.append(x)
                if x.layer == pivot:
                    equal.append(x)
                if x.layer > pivot:
                    greater.append(x)
            # Don't forget to return something!
            return self.sortEnvObjEXP(less) + equal + self.sortEnvObjEXP(greater)  # Just use the + operator to join lists
        # Note that you want equal ^^^^^ not pivot
        else:  # You need to hande the part at the end of the recursion - when you only have one element in your array, just return the array.
            self.envObj = array
            return array

    def triggerNextEnviroment(self, dest):
        self.nextDestination = dest


    def loadNextEnviroment(self, destination):
        if destination == "UP":
            self.worldGridPos[1] -= 1
        if destination == "DOWN":
            self.worldGridPos[1] += 1
        if destination == "RIGHT":
            self.worldGridPos[0] += 1
        if destination == "LEFT":
            self.worldGridPos[0] -= 1

        self.currentLevel = loadEnvMeta.getEvlJsonPath(self.currentGrid, self.worldGridPos)
        self.readLvlJson(self.currentLevel)

        if destination == "UP":
            self.newPos = [self.envLocalTransitionObj["DOWN"].rect.x + 25, self.envLocalTransitionObj["DOWN"].rect.y]
        if destination == "DOWN":
            self.newPos = [self.envLocalTransitionObj["UP"].rect.x + 25, self.envLocalTransitionObj["UP"].rect.y - 50]
        if destination == "RIGHT":
            self.newPos = [self.envLocalTransitionObj["LEFT"].rect.x, self.envLocalTransitionObj["LEFT"].rect.y]
        if destination == "LEFT":
            self.newPos = [self.envLocalTransitionObj["RIGHT"].rect.x, self.envLocalTransitionObj["RIGHT"].rect.y]






    def reloadEvl(self):


        self.readLvlJson(self.currentLevel)
        # self.Panel = pygame.Surface (self.size)

    def clearRendering(self):
        self.retDrawUnder = []
        self.retDrawOver = []
        self.retDraw = []


    def canSave(self):
        # if len(self.Enemies) == 0:
        #     return True
        # return False

        return True

    def sanitizeForPickling(self):
        self.envObj = []
        self.Enemies = []
        # self.envProj = []

        for i in self.envInterObj:
            i.sanitize()

        for i in self.envProj:
            i.sanitize()

        for i in self.Enemies:
            i.sanitize()

        self.clearRendering()
        self.envLocalTransitionObj = {}
        del self.ac
        del self.interactionMarker
        del self.items
        del self.projectiles
        del self.steamApi
        del self.audio
        del self.projAudio
        del self.panel
        del self.wordbubbles
        del self.saveMan
        del self.dialog
        del self.editor
        del self.storeMan
        del self.contentPackageManager
        # del self.random
        self.mainPlayer.sanitizeForPickling()

    def reloadGame(self):
        self.ac = AdvancedChecks.AdvancedChecker(self)
        self.items = PickUpItems.ItemManager(self)
        self.projectiles = Projectile.ProjectileManager()
        #UpdatePlayer:
        # newPlayer = Player.InstPlayer([0, 0], self)
        # newPlayer.__dict__.update(self.mainPlayer.__dict__)
        # self.mainPlayer = newPlayer

        self.mainPlayer.reload()
        # self.mainPlayer.loadImages()
        # self.mainPlayer.loadAudio()





        for i in self.envInterObj:
            i.loadImages()
        # for i in self.envLocalTransitionObj:
        #     self.envLocalTransitionObj[i].loadImages()
        #
        self.steamApi = None
        self.audio = None
        self.panel = None
        self.saveMan = None
        self.dialog = None
        self.storeMan = None
        self.contentPackageManager = None


        self.editor = Editor.WorldEditor(self)

        self.projAudio = audioMan.SoundController()
        self.projAudio.loadFromDir2("_AUDIO/FX/Projectiles", 1)
        self.projAudio.prepSounds()

        self.reloadEvl()
        for i in self.envProj:
            i.reloadProj()

        for i in self.Enemies:
            i.reloadEnemy()

        # self.random = random
        self.wordbubbles = Artifact.WordBubbleManager(self)
        self.interactionMarker = envInteractObj.InteractionMarker(self)

    def getUnderMouse(self, includeChildren = True):
        retVal = []

        for i in self.envObj:
            if includeChildren:
                if i.rect.collidepoint(self.mouseWorld):
                    retVal.append(i.label)
            else:
                if i.rect.collidepoint(self.mouseWorld) and not i.isChild:
                    retVal.append(i.label)

        return retVal





    def versionUpdate(self):
        pass