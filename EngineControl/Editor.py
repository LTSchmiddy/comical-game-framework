import loadEnvMeta, json, os, copy, pygame, gameSettingsMaster

from dataManagers import counter



class WorldEditor:
    def __init__(self, world):
        self.world = world

        self.inEditorMode = False
        self.markerPosPlayer = True

        self.extEditorCmd = "npp\\bin\\notepad++.exe"
        self.tempJsonPath = "EngineControl\\TempFiles\\EditTemp.json"

        self.stepSize = 1

        self.selectedLabel = None

        self.holdDel = counter.TickCounter(30, False, False)


        self.useNoClip = False
        self.posNoClip = [0, 0]

        self.noEnemies = False

        self.ctrls = gameSettingsMaster.getSettingsDict()["Controls"]

        self.items = ItemEditor(self.world, self)

        self.currentObjBase = "BackWall1_Block"
        self.newObjJson = {
            "label": "SET_ME!!",
            "pos":[0, 0],
            "dimens":[5, 5],
            "useTemplate": "BackWall1",
            "layer": -1,
            "useMultPos": 32,
            "useMultDimens": 32
        }

        # self.newSlots = []

    def eventLoop(self, events):
        if pygame.K_KP_ENTER in events["kdown"]:
            self.inEditorMode = not self.inEditorMode
            # print "In Editor Mode:", self.inEditorMode
            # self.world.notif.notify("In Editor Mode: " + str(self.inEditorMode), 120)

            if not self.inEditorMode:
                self.clearSelected()

        if pygame.K_KP_PERIOD in events["kdown"]:
            self.useNoClip = not self.useNoClip
            self.posNoClip = self.world.mainPlayer.pos[:]
            self.world.mainPlayer.noClip = self.useNoClip

            self.world.mainPlayer.pos = self.posNoClip[:]
            self.world.mainPlayer.momentum = [0, 0]


        if self.useNoClip:
            if self.ctrls["Up"] in events["kheld"]:
                self.posNoClip[1] += -10

            if self.ctrls["Left"] in events["kheld"]:
                self.posNoClip[0] += -10

            if self.ctrls["Down"] in events["kheld"]:
                self.posNoClip[1] += 10

            if self.ctrls["Right"] in events["kheld"]:
                self.posNoClip[0] += 10

            self.world.mainPlayer.pos = self.posNoClip[:]
            self.world.mainPlayer.momentum = [0, 0]



        if pygame.K_END in events["kdown"]:
            self.noEnemies = not self.noEnemies
        if self.noEnemies:
            self.world.Enemies = []

        if self.inEditorMode:

            # if pygame.K_i in events["kdown"]:
            #     self.items.newItem("EXP1")


            if pygame.K_KP3 in events["kdown"]:
                self.editPlayerSpawn()

            if pygame.K_KP_MULTIPLY in events["kdown"]:
                self.world.loadFromWorldJson()

            if pygame.K_KP0 in events["kdown"]:
                self.saveEnv()

            if pygame.K_KP_PLUS in events["kdown"]:
                self.addNew()



            if pygame.K_PAGEDOWN in events["kdown"]:
                self.setObjBase("BackWall1_Block")
                self.world.notif.notify("Set Obj Base to BackWall1_Block")


            if pygame.K_PAGEUP in events["kdown"]:
                self.setObjBase("BasicImgObj")
                self.world.notif.notify("Set Obj Base to BasicImgObj")




            for i in ["health", "weapEnergy", "magic"]:
                self.world.mainPlayer.stats[i].setValue(self.world.mainPlayer.stats[i].getMax())

            highlight = self.world.getUnderMouse(False)
            if len(highlight) > 0:
                self.world.interactionMarker.setText(highlight[len(highlight) - 1], 200, [50, 150, 250])
                if not self.markerPosPlayer:
                    for i in self.world.envObj:
                        if i.label == highlight[len(highlight) - 1]:
                            self.world.interactionMarker.setPos(i.rect.topleft)
                            break
                else:
                    self.world.interactionMarker.setPos(self.world.mainPlayer.rect.topleft)
                self.world.interactionMarker.show = True

                if pygame.K_KP5 in events["kdown"]:
                    self.setSelected(highlight[len(highlight) - 1])


            if self.selectedLabel != None:
                if pygame.K_KP4 in events["kdown"]:
                    self.clearSelected()

                if pygame.K_KP_DIVIDE in events["kdown"]:
                    self.edit(self.selectedLabel)

                if pygame.K_KP_MINUS in events["kheld"]:
                    if self.holdDel.check():
                        self.delete(self.selectedLabel)
                        self.clearSelected()
                else:
                    self.holdDel.reset()

                if pygame.K_KP1 in events["kdown"]:
                    self.clone(self.selectedLabel)


                if pygame.K_UP in events["kdown"]:
                    self.move(self.selectedLabel, [0, -self.stepSize * 32])

                if pygame.K_LEFT in events["kdown"]:
                    self.move(self.selectedLabel, [-self.stepSize * 32, 0])

                if pygame.K_RIGHT in events["kdown"]:
                    self.move(self.selectedLabel, [self.stepSize * 32, 0])

                if pygame.K_DOWN in events["kdown"]:
                    self.move(self.selectedLabel, [0, self.stepSize * 32])


                if pygame.K_EQUALS in events["kdown"]:
                    self.toggleWall(self.selectedLabel, "up")
                    self.setSelected(self.selectedLabel)

                if pygame.K_LEFTBRACKET in events["kdown"]:
                    self.toggleWall(self.selectedLabel, "left")
                    self.setSelected(self.selectedLabel)

                if pygame.K_RIGHTBRACKET in events["kdown"]:
                    self.toggleWall(self.selectedLabel, "right")
                    self.setSelected(self.selectedLabel)

                if pygame.K_QUOTE in events["kdown"]:
                    self.toggleWall(self.selectedLabel, "down")
                    self.setSelected(self.selectedLabel)


                if pygame.K_KP7 in events["kdown"]:
                    self.resize(self.selectedLabel, [-self.stepSize, 0])
                    self.setSelected(self.selectedLabel)

                if pygame.K_KP8 in events["kdown"]:
                    self.resize(self.selectedLabel, [self.stepSize, 0])
                    self.setSelected(self.selectedLabel)

                if pygame.K_KP9 in events["kdown"]:
                    self.resize(self.selectedLabel, [0, -self.stepSize])
                    self.setSelected(self.selectedLabel)

                if pygame.K_KP6 in events["kdown"]:
                    self.resize(self.selectedLabel, [0, self.stepSize])
                    self.setSelected(self.selectedLabel)




    def setSelected(self, label):
        self.clearSelected()

        foundTarget = False
        for i in self.world.envObj:
            if i.label == label:
                self.selectedLabel = label
                foundTarget = True
                i.drawWalls([255, 255, 255])
                break

        if foundTarget:
            return
        else:
            self.world.notif.notify(label + ": No JSON data!!")
            return

    def clearSelected(self):
        if self.selectedLabel != None:
            for i in self.world.envObj:
                if i.label == self.selectedLabel:
                    i.updateDraw()
                    break
            self.selectedLabel = None

    def edit(self, label):
        jsonTable = self.world.worldJson["Objects"][label]

        writeOut = open(self.tempJsonPath, "w")
        json.dump(jsonTable, writeOut, sort_keys=True, indent = 4, separators = (',', ': '))
        writeOut.close()

        newJson = None

        while True:
            try:
                os.system(self.extEditorCmd + " " + self.tempJsonPath)
                writeIn = open(self.tempJsonPath, "r")
                newJson = json.load(writeIn)
                break
            except:
                print "Json Error: Try Again."
        self.world.worldJson["Objects"][label] = newJson
        writeOut.close()

        for i in self.world.envObj:
            if i.label == label:
                self.world.envObj.remove(i)
                break

        self.world.buildWorldObjects({label: copy.deepcopy(newJson)})
        self.world.sortEnvObj()


    def editPlayerSpawn(self):
        jsonTable = self.world.worldJson["PlayerSpawn"]

        writeOut = open(self.tempJsonPath, "w")
        json.dump(jsonTable, writeOut, sort_keys=True, indent=4, separators=(',', ': '))
        writeOut.close()

        os.system(self.extEditorCmd + " " + self.tempJsonPath)

        writeIn = open(self.tempJsonPath, "r")
        newJson = json.load(writeIn)
        self.world.worldJson["PlayerSpawn"] = copy.deepcopy(newJson)
        self.world.worldMeta["PlayerSpawn"] = copy.deepcopy(newJson)
        writeOut.close()

        self.world.loadPlayerSpawn()
        self.world.sortEnvObj()


    def clone(self, label):
        newJson = copy.deepcopy(self.world.worldJson["Objects"][label])
        newLabel = label

        while (newLabel in self.world.worldJson["Objects"]) or (label == newLabel):
            if not "^" in newLabel:
                newLabel = newLabel + "^-1"
            nblbList = newLabel.split("^")
            newLabel = "^".join([nblbList[0], str(int(nblbList[1]) + 1)])

        #
        # for i in self.world.envObj:
        #     if i.label == label:
        #         i.label = newLabel

        # print newLabel

        toLoad = {newLabel: newJson}
        self.world.worldJson["Objects"].update(copy.deepcopy(toLoad))
        # self.world.buildWorldObjects({newLabel: copy.deepcopy(self.world.worldJson["Objects"][newLabel])})
        self.world.buildWorldObjects(copy.deepcopy(toLoad))
        # self.world.loadFromWorldJson()
        self.world.sortEnvObj()

        self.setSelected(newLabel)

    def addNew(self):
        useX = self.world.mouseWorld[0] / 32
        useY = self.world.mouseWorld[1] / 32
        jsonTable = copy.deepcopy(self.newObjJson)

        jsonTable["pos"] = [useX, useY]

        writeOut = open(self.tempJsonPath, "w")
        json.dump(jsonTable, writeOut, sort_keys=True, indent=4, separators=(',', ': '))
        writeOut.close()

        newJsonTable = None

        while True:
            try:
                os.system(self.extEditorCmd + " " + self.tempJsonPath)
                writeIn = open(self.tempJsonPath, "r")
                newJsonTable = json.load(writeIn)
                break
            except ValueError:
                print "Json Error: Try Again."

        newLabel = newJsonTable["label"]

        while (newLabel in self.world.worldJson["Objects"]) or (newJsonTable["label"] == newLabel):
            if not "^" in newLabel:
                newLabel = newLabel + "^-1"
            nblbList = newLabel.split("^")
            newLabel = "^".join([nblbList[0], str(int(nblbList[1]) + 1)])

        newJsonTable["label"] = newLabel

        self.world.worldJson["Objects"].update({newJsonTable["label"]: newJsonTable})
        # print self.world.worldJson
        writeOut.close()

        self.world.buildWorldObjects({newJsonTable["label"]: copy.deepcopy(newJsonTable)})
        self.world.sortEnvObj()


    def setObjBase(self, fileName = "BackWall1_Block"):
        writeIn = open("EngineControl/LvlEdit/objBases/" + fileName + ".json", "r")
        self.newObjJson = json.load(writeIn)
        self.currentObjBase = fileName


    def getAllBases(self):
        retVal = []
        for i in os.listdir("EngineControl/LvlEdit/objBases"):
            retVal.append(i)

        return retVal

    def searchBases(self, searchTerm):
        retVal = []
        for i in os.listdir("EngineControl/LvlEdit/objBases"):
            if searchTerm in i:
                retVal.append(i)

        return retVal

    def delete(self, label):
        del self.world.worldJson["Objects"][label]
        for i in self.world.envObj:
            if i.label == label:
                self.world.envObj.remove(i)
                break

    def move(self, label, dir):
        # self.world.worldJson["Objects"][label]["pos"][0] += dir[0]
        # self.world.worldJson["Objects"][label]["pos"][1] += dir[1]

        for i in self.world.envObj:
            if i.label == label:
                i.move(dir)
                self.world.worldJson["Objects"][label]["pos"][0] = i.pos[0] / 32
                # self.world.worldJson["Objects"][label]["pos"][0] = i.pos[0] / self.world.worldMeta["Objects"][label]["useMultPos"]
                self.world.worldJson["Objects"][label]["pos"][1] = i.pos[1] / 32
                # self.world.worldJson["Objects"][label]["pos"][1] = i.pos[1] / self.world.worldMeta["Objects"][label]["useMultPos"]
                break



    def resize(self, label, dir):

        if "dimens" in self.world.worldJson["Objects"][label]:
            self.world.worldJson["Objects"][label]["dimens"][0] += dir[0]
            if self.world.worldJson["Objects"][label]["dimens"][0] < 1:
                self.world.worldJson["Objects"][label]["dimens"][0] = 1

            self.world.worldJson["Objects"][label]["dimens"][1] += dir[1]
            if self.world.worldJson["Objects"][label]["dimens"][1] < 1:
                self.world.worldJson["Objects"][label]["dimens"][1] = 1

            # print self.world.worldJson["Objects"][label]["dimens"]


            for i in self.world.envObj:
                if i.label == label:
                    self.world.envObj.remove(i)
                    break

            self.world.buildWorldObjects({label: copy.deepcopy(self.world.worldJson["Objects"][label])})
            self.world.sortEnvObj()

    def loadTestArea(self):
        self.world.triggerEnv([0, 0], "_TestArea", [100, 100])


    def toggleWall(self, label, side):
        if not "skipWall" in self.world.worldJson["Objects"][label]:
            self.world.worldJson["Objects"][label].update({"skipWall": []})

        if side in self.world.worldJson["Objects"][label]["skipWall"]:
            self.world.worldJson["Objects"][label]["skipWall"].remove(side)
        else:
            self.world.worldJson["Objects"][label]["skipWall"].append(side)

        self.world.worldMeta["Objects"][label]["skipWall"] = copy.deepcopy(self.world.worldJson["Objects"][label]["skipWall"])

        for i in self.world.envObj:
            if i.label == label:
                i.setWalls()
                i.drawWalls()
                break

        # self.world.buildWorldObjects({label: copy.deepcopy(self.world.worldJson["Objects"][label])})
        # self.world.sortEnvObj()

    def newEnv(self, grid, gridPos):
        newJson = {
            "Objects": {
                "Platform": {
                    "dimens": [
                        20,
                        5
                    ],
                    "layer": -10,
                    "pos": [
                        -10,
                        -5
                    ],
                    "useMultDimens": 32,
                    "useMultPos": 32,
                    "useTemplate": "BackWall1"
                },
            },
            "PlayerSpawn": {
                "Background Color": [
                    0,
                    0,
                    0
                ],
                "GameStart": [
                    0,
                    0
                ],
                "WorldEdge": {
                    "down": 2400,
                    "left": -2880,
                    "right": 2880,
                    "up": -2400
                }
            }
        }
        loadEnvMeta.saveEnvPath(loadEnvMeta.getEvlJsonPath(grid, gridPos), newJson)

    def getEnvPath(self):
        return loadEnvMeta.getEvlJsonPath(self.world.currentGrid, self.world.worldGridPos)

    def saveEnv(self):
        self.world.notif.notify("Env File Saved")
        loadEnvMeta.saveEnvPath(loadEnvMeta.getEvlJsonPath(self.world.currentGrid, self.world.worldGridPos), self.world.worldJson)


    def saveEnvAs(self, filePath):
        loadEnvMeta.saveEnv(filePath, self.world.worldJson)





class ItemEditor:
    def __init__(self, world, mainEditor):
        self.world = world
        self.mainEditor = mainEditor

#
#
#
#         self.newItemText = """
# itemID = "**ID**"
# desc = "New Item Description"
# name = "New Item"
# value = 30
# equip = None
#
# consumeOnUse = True
#
# imagePath = "_IMAGES\\Sprites\\Items\\Telepathy Book\\TelepathyBook.png"
#
#
# def onItemUse(world, item=None):
#     pass
#
#
# def onItemEquip(world, item=None):
#     pass
#
#
# def onItemRemove(world, item=None):
#     pass
#
#         """
#
#
#     def newItem(self, newItemID):
#
#         writeText = newItemID.join(self.newItemText.split("**ID**"))
#
#         newItemFName = newItemID + ".item"
#         newItemPath = "EngineControl\\GamePlayObjects\\Items\\" + newItemFName
#
#         newItemFile = open(newItemPath, "w")
#
#         newItemFile.write(writeText)
#         newItemFile.close()
#
#         while True:
#             try:
#                 os.system(self.mainEditor.extEditorCmd + " " + newItemPath)
#                 self.world.items.loadNewItem(newItemFName)
#
#                 break
#             except ValueError:
#                 print "Error In Item File: Try Again."
#
#
#




