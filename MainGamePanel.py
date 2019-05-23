# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 16:03:01 2015

@author: alex
"""

import pygame, os, EngineControl, pickle, copy
pygame.init()
pygame.font.init()


class GUI:
    def __init__(self, rect, pos, jsonArgs = None):
        self.postWorld = True
        self.surfaceDrawn = True
        self.show = True
        self.pos = pos
        self.dimens = rect
        self.Panel = pygame.Surface(self.dimens)
        self.fillColor = [75, 75, 75]
        self.backgroundColor = [75, 75, 75]



        self.offsetWorld = [0, 0]
        self.World = EngineControl.Environment(2000, 1000, self.Panel, "_MenuArea", [100, 100])
        self.World.editor = None

        self.fontRend = pygame.font.Font(None, 40)

        # self.saveMan = None
        self.savePath = "gameSaves\save1.cgs"





    def get_hostvar(self, var):
        self.hostvar = var
        # self.saveMan = self.hostvar["saveM"]


        if self.hostvar["Game Env"] != None:
            self.World = self.hostvar["Game Env"]
        self.World.notif = self.hostvar["Game Notif"]
        self.World.dialog = self.hostvar["dialogM"]
        self.World.flipbook = self.hostvar["flipbookM"]
        self.World.debugLog = self.hostvar["debugLogging"]

        self.World.steamApi = self.hostvar["steamAPI"]
        self.World.audio = self.hostvar["masterAudio"]
        self.World.saveMan = self.hostvar["saveM"]
        self.World.storeMan = self.hostvar["storeManager"]
        self.World.contentPackageManager = self.hostvar["ContentPackageManager"]



 
    def send_hostvar(self):
        self.hostvar["Game Notif"] = self.World.notif
        self.hostvar["Game Env"] = self.World
        self.hostvar["flipbookM"] = self.World.flipbook
        self.hostvar["steamAPI"] = self.World.steamApi
        self.hostvar["debugLogging"] = self.World.debugLog
        self.hostvar["masterAudio"] = self.World.audio
        self.hostvar["saveM"] = self.World.saveMan
        self.hostvar["storeManager"] = self.World.storeMan
        self.hostvar["ContentPackageManager"] = self.World.contentPackageManager


        return self.hostvar
            
    def bg_tasks(self):
        self.savePath = self.hostvar["saveM"].savePath

        if self.hostvar["saveM"].getSaveTrigger():
            self.saveGame()

        if self.hostvar["saveM"].getLoadTrigger():
            self.loadGame()

        if self.hostvar["saveM"].getNewTrigger():
            self.newGame()

        if self.hostvar["DebugStart"]:
            self.show = True
        if not self.show:
            return
        # if self.postWorld:
        #     self.hostvar["Game Env"] = self.World
        #     self.postWorld = False

        self.surfaceDrawn = False

        self.hostvar["Player Health"] = self.World.mainPlayer.stats["health"].getValue()
        self.hostvar["Player Health Max"] = self.World.mainPlayer.stats["health"].getMax()
        self.hostvar["Player Weapon Energy"] = self.World.mainPlayer.stats["weapEnergy"].getValue()
        self.hostvar["Player Weapon Energy Max"] = self.World.mainPlayer.stats["weapEnergy"].getMax()
        self.hostvar["Player Magic"] = self.World.mainPlayer.stats["magic"].getValue()
        self.hostvar["Player Magic Max"] = self.World.mainPlayer.stats["magic"].getMax()

        self.hostvar["Player Weapon Name"] = self.World.mainPlayer.projectileWeapName[self.World.mainPlayer.projectileIndex]

        if self.hostvar["Game Paused"] and self.hostvar["DebugStart"]:
            return

        self.World.logicStep(self.offsetWorld)

        self.offsetWorld = [0 + (self.dimens[0]/2) - self.World.mainPlayer.pos[0], 0 + (self.dimens[1]/2) - self.World.mainPlayer.pos[1]]


        if self.offsetWorld[0] > -self.World.worldEdgeLeft:
            self.offsetWorld[0] = -self.World.worldEdgeLeft

        if self.offsetWorld[0] - self.dimens[0] < -self.World.worldEdgeRight:
            self.offsetWorld[0] = -self.World.worldEdgeRight + self.dimens[0]

        if self.offsetWorld[1] > -self.World.worldEdgeUp:
            self.offsetWorld[1] = -self.World.worldEdgeUp

        if self.offsetWorld[1] - self.dimens[1] < -self.World.worldEdgeDown:
            self.offsetWorld[1] = -self.World.worldEdgeDown + self.dimens[1]





        
        

        self.surfaceDrawn = True


        
        # print "whiter"

    def event_loop(self, events):



        if not self.show:
            return
        self.surfaceDrawn = False

        if self.hostvar["Game Paused"] and self.hostvar["DebugStart"]:
            return


        if pygame.K_F5 in events["kdown"]:
            # self.hostvar["Game Notif"].notify("Saving Game...", 180)

            self.saveGame()

        if pygame.K_F7 in events["kdown"]:
            self.loadGame()

        if pygame.K_KP2 in events["kdown"]:
            self.hostvar["showFPS"] = not self.hostvar["showFPS"]


        self.World.runEvents(events, self.dimens[0]/2 + self.pos[0])
        self.surfaceDrawn = True

    def percents(self, val, off):
        x = ((self.dimens[0] * val[0])/100) + off[0]
        y = ((self.dimens[1] * val[1])/100) + off[1]
        pixels = [x, y]
        return pixels
    
    def updatePanel(self):
        self.surfaceDrawn = False
    
        if self.hostvar["Game Paused"] == False:
        # if pygame.mouse.get_pos()[0] > self.pos[0] and pygame.mouse.get_pos()[0] < self.pos[0] + self.dimens[0] and pygame.mouse.get_pos()[1] > self.pos[1] and pygame.mouse.get_pos()[1] < self.pos[1] + self.dimens[1] and self.hostvar["Game Paused"] == False:
            pygame.mouse.set_visible(False)
            
        else:
            pygame.mouse.set_visible(True)
            
            
        if self.hostvar["Game Paused"] and self.hostvar["DebugStart"]:
            return
        
        
        self.Panel.fill(self.World.backgroundColor)
        # self.Panel.blit(self.World.backgroundImage, [20, 0])
        self.World.Draw(self.dimens)

        for i in self.World.retDrawUnder:
            drawPos = [i[1][0] + self.offsetWorld[0], i[1][1] + self.offsetWorld[1]]
            if (drawPos[0] > 0 - i[0].get_width() and drawPos[0] < self.dimens[0]) and (drawPos[1] > 0 - i[0].get_height() and drawPos[1] < self.dimens[1]):
                self.Panel.blit(i[0], drawPos)

        for i in self.World.retDraw:
            drawPos = [i[1][0] + self.offsetWorld[0], i[1][1] + self.offsetWorld[1]]
            if (drawPos[0] > 0 - i[0].get_width() and drawPos[0] < self.dimens[0]) and (drawPos[1] > 0 - i[0].get_height() and drawPos[1] < self.dimens[1]):
                self.Panel.blit(i[0], drawPos)

        for i in self.World.retDrawOver:
            drawPos = [i[1][0] + self.offsetWorld[0], i[1][1] + self.offsetWorld[1]]
            if (drawPos[0] > 0 - i[0].get_width() and drawPos[0] < self.dimens[0]) and (drawPos[1] > 0 - i[0].get_height() and drawPos[1] < self.dimens[1]):
                self.Panel.blit(i[0], drawPos)



        # if self.hostvar["Developer Mode"]:
        #     counter = 0
        if self.hostvar["DebugStart"]:
            pygame.draw.circle (self.Panel, [255, 255, 255], pygame.mouse.get_pos(), 5, 2)
            pygame.draw.circle (self.Panel, [0, 0, 0], pygame.mouse.get_pos(), 6, 2)
            pygame.draw.circle(self.Panel, [255, 255, 255], pygame.mouse.get_pos(), 15, 2)
            pygame.draw.circle(self.Panel, [0, 0, 0], pygame.mouse.get_pos(), 16, 2)
            self.surfaceDrawn = True


        if self.World.editor != None:
            if self.World.editor.inEditorMode:
                pygame.draw.rect(self.Panel, [50, 255, 50], pygame.Rect([0, 0], self.dimens), 20)

        # self.Panel.blit(self.hostvar["ContentPackageManager"].loadImage("@EXP1:Candice_Pinup.png"), [0, 0])
            
    def get_updatePanel(self):
        return True

    def newGame(self):

        self.hostvar["flipbookM"].trigger("NewGame")

        # self.World = EngineControl.Environment(2000, 1000, self.Panel, "_EXP", [0, 0])
        self.World = EngineControl.Environment(2000, 1000, self, "_OverWorld", [100, 100])
        if not self.hostvar["useEditor"]:
            self.World.editor = None

        self.World.notif = self.hostvar["Game Notif"]
        self.World.dialog = self.hostvar["dialogM"]
        self.World.flipbook = self.hostvar["flipbookM"]
        self.World.debugLog = self.hostvar["debugLogging"]

        self.World.steamApi = self.hostvar["steamAPI"]
        self.World.audio = self.hostvar["masterAudio"]
        self.World.saveMan = self.hostvar["saveM"]
        self.World.storeMan = self.hostvar["storeManager"]
        self.World.contentPackageManager = self.hostvar["ContentPackageManager"]
        self.World.loadContentPacks()


    def saveGame(self):

        if self.World.canSave():
            # mainWorld = copy.deepcopy(self.World)
            self.World.sanitizeForPickling()

            saveFile = open(self.savePath, "w")
            pickle.dump(self.World, saveFile)
            saveFile.close()

            self.World.reloadGame()
            self.World.steamApi = self.hostvar["steamAPI"]
            self.World.audio = self.hostvar["masterAudio"]
            self.World.saveMan = self.hostvar["saveM"]
            self.World.dialog = self.hostvar["dialogM"]
            self.World.storeMan = self.hostvar["storeManager"]
            self.World.contentPackageManager = self.hostvar["ContentPackageManager"]
            self.World.loadContentPacks()

            self.World.notif.notify("Game Saved!", 180)
        else:
            self.World.notif.notify("Cannot Save Now!", 180)

    def loadGame(self):


        loadFile = open(self.savePath, "r")
        self.World = pickle.load(loadFile)
        loadFile.close()

        self.World.reloadGame()
        if not self.hostvar["useEditor"]:
            self.World.editor = None
        self.World.steamApi = self.hostvar["steamAPI"]
        self.World.dialog = self.hostvar["dialogM"]
        self.World.audio = self.hostvar["masterAudio"]
        self.World.saveMan = self.hostvar["saveM"]
        self.World.storeMan = self.hostvar["storeManager"]
        self.World.contentPackageManager = self.hostvar["ContentPackageManager"]
        self.World.loadContentPacks()
        self.World.mainPlayer.sanitizeInventory()

        self.World.panel = self.Panel
        self.World.updateInvUI = True
        self.World.notif.notify("Game Loaded!", 180)

# if __name__ == '__main__':
    # disp=GUI([800,600], [0, 0])
    # screen = pygame.display.set_mode(disp.dimens)
    # disp.updatePanel()
    # while not os.path.isfile("kill"):
        # disp.bg_tasks()
        # disp.event_loop()
        # if disp.get_updatePanel() == True:    
            # disp.updatePanel()
            
        # screen.blit(disp.Panel, disp.pos)
        # pygame.display.flip()

        # time.sleep(.05)
        
