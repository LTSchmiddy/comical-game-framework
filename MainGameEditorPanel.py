# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 16:03:01 2015

@author: alex
"""

import EngineControl
import gameSettingsMaster
import pygame

import AssetUI

pygame.init()
pygame.font.init()


class GUI:
    def __init__(self, rect, pos):
        self.postWorld = True
        self.surfaceDrawn = True
        self.show = True
        self.pos = pos
        self.dimens = rect
        self.Panel = pygame.Surface(self.dimens)
        self.fillColor = [75, 75, 75]
        self.backgroundColor = [75, 75, 75]
        
        self.offsetWorld = [0, 0]
        self.World = EngineControl.Editor.Environment(2000, 1000)
        self.fontRend = pygame.font.Font(None, 40)
        self.savePath = "C:\Users\Alex Schmid\Google Drive\Code\Python\Comical\gameSaves\save1.cgs"

        self.inputTracker = {"w": False, "s": False, "a": False, "d": False, "space": False, "shift": False}
        self.ctrls = gameSettingsMaster.getSettingsDict()["Controls"]

        self.moveSpeed = 10

        self.addButton = AssetUI.LabelButton([30, 30], [0, 0], "ADD", 30)
        self.editButton = AssetUI.LabelButton([120, 30], [0, 0], "EDIT", 30)
        self.delButton = AssetUI.LabelButton([240, 30], [0, 0], "DELETE", 30)
        self.reloadButton = AssetUI.LabelButton([350, 30], [0, 0], "RELOAD", 30)
        self.setCurPosButton = AssetUI.LabelButton([500, 30], [0, 0], "SET CURSOR POS", 30)
        self.saveButton = AssetUI.LabelButton([730, 30], [0, 0], "SAVE", 30)
        self.makeTemplateButton = AssetUI.LabelButton([900, 30], [0, 0], "MAKE TEMPLATE", 30)


    def get_hostvar(self, var):
        self.hostvar = var

 
    def send_hostvar(self):
        return self.hostvar           
            
    def bg_tasks(self):
        if self.postWorld:
            self.hostvar["Game Env"] = self.World
            self.postWorld = False

        self.surfaceDrawn = False
        if self.hostvar["Game Paused"]:
            return
        

        self.World.logicStep(self.offsetWorld)
        
        


        self.surfaceDrawn = True
            
        
        # print "whiter"

    def event_loop(self, events):
        self.surfaceDrawn = False

        if self.hostvar["Game Paused"]:
            return
        self.World.runEvents(events)
        self.surfaceDrawn = True
        if pygame.K_F5 in events["kdown"]:
            self.saveGame()

        if pygame.K_F7 in events["kdown"]:
            self.loadGame()

        # Adding Button Commands:
        # if self.addButton.clickBool(events):
        #     print "Please Select an Object to add:"
        #     for i in self.World.templates:
        #         print i
        #     nextObj = raw_input("Enter Template Name:")
        #     if nextObj in self.World.templates:
        #         nextLabel = raw_input("Enter Label for New Object:")
        #         newObj = self.World.templates[nextObj]
        #         newObj["pos"] = self.World.cursorPos
        #         self.World.envObj[nextLabel] = newObj
        #     else:
        #         print "Template Not Found"
        #
        # elif self.makeTemplateButton.clickBool(events):
        #     print "Making Template of", self.World.selectedObject
        #     tempName = raw_input("Please Name the Template:")
        #     self.World.saveAsTemplate(tempName)
        #
        # else:

        self.handleInputTracking(events)


        if self.inputTracker["w"]:
            self.offsetWorld[1] += self.moveSpeed

        if self.inputTracker["s"]:
            self.offsetWorld[1] -= self.moveSpeed

        if self.inputTracker["a"]:
            self.offsetWorld[0] += self.moveSpeed

        if self.inputTracker["d"]:
            self.offsetWorld[0] -= self.moveSpeed


    def handleInputTracking(self, events):
        if self.ctrls["Up"] in events["kdown"]:
            self.inputTracker["w"] = True
        if self.ctrls["Up"] in events["kup"]:
            self.inputTracker["w"] = False

        if self.ctrls["Down"] in events["kdown"]:
            self.inputTracker["s"] = True
        if self.ctrls["Down"] in events["kup"]:
            self.inputTracker["s"] = False

        if self.ctrls["Left"] in events["kdown"]:
            self.inputTracker["a"] = True
        if self.ctrls["Left"] in events["kup"]:
            self.inputTracker["a"] = False

        if self.ctrls["Right"] in events["kdown"]:
            self.inputTracker["d"] = True
        if self.ctrls["Right"] in events["kup"]:
            self.inputTracker["d"] = False

        if self.ctrls["Jump"] in events["kdown"]:
            self.inputTracker["space"] = True
        if self.ctrls["Jump"] in events["kup"]:
            self.inputTracker["space"] = False

        if self.ctrls["Sprint"] in events["kdown"]:
            self.inputTracker["shift"] = True
        if self.ctrls["Sprint"] in events["kup"]:
            self.inputTracker["shift"] = False

        if self.ctrls["Status Screen"] in events["kup"]:
            self.World.reloadEvl()



    def percents(self, val, off):
        x = ((self.dimens[0] * val[0])/100) + off[0]
        y = ((self.dimens[1] * val[1])/100) + off[1]
        pixels = [x, y]
        return pixels
    
    def updatePanel(self):
        self.surfaceDrawn = False


    
        # if pygame.mouse.get_pos()[0] > self.pos[0] and pygame.mouse.get_pos()[0] < self.pos[0] + self.dimens[0] and pygame.mouse.get_pos()[1] > self.pos[1] and pygame.mouse.get_pos()[1] < self.pos[1] + self.dimens[1] and self.hostvar["Game Paused"] == False:
        #     pygame.mouse.set_visible(False)
        #
        # else:
        #     pygame.mouse.set_visible(True)
            
            
        if self.hostvar["Game Paused"]:
            pass
        
        
        self.Panel.fill(self.World.backgroundColor)
        arrDraw = self.World.Draw(self.dimens)



        for i in arrDraw:
            self.Panel.blit(i[0], [i[1][0] + self.offsetWorld[0], i[1][1] + self.offsetWorld[1]])
            # self.Panel.blit(self.fontRend.render(str(counter), True, [0, 0, 0]), [i[1][0] + self.offsetWorld[0], i[1][1] + self.offsetWorld[1]])
            # counter += 1
        if self.hostvar["Developer Mode"]:
            counter = 0
            for i in arrDraw:
                # self.Panel.blit(i[0], [i[1][0] + self.offsetWorld[0], i[1][1] + self.offsetWorld[1]])
                self.Panel.blit(self.fontRend.render(str(counter), True, [125, 125, 125]), [i[1][0] + self.offsetWorld[0], i[1][1] + self.offsetWorld[1]])
                counter += 1
        mouseDraw = [self.World.cursorPos[0] + self.offsetWorld[0], self.World.cursorPos[1] + self.offsetWorld[1]]
        pygame.draw.circle (self.Panel, [255, 255, 255], mouseDraw, 5, 2)
        pygame.draw.circle (self.Panel, [0, 0, 0], mouseDraw, 6, 2)
        pygame.draw.circle(self.Panel, [255, 255, 255], mouseDraw, 15, 2)
        pygame.draw.circle(self.Panel, [0, 0, 0], mouseDraw, 16, 2)

        # pygame.draw.line(self.Panel, [0, 0, 0], [0, 45], [self.dimens[0], 45], 90)
        # self.Panel.blit(self.addButton.image, [self.addButton.rect.x, self.addButton.rect.y])
        # self.Panel.blit(self.editButton.image, [self.editButton.rect.x, self.editButton.rect.y])
        # self.Panel.blit(self.delButton.image, [self.delButton.rect.x, self.delButton.rect.y])
        # self.Panel.blit(self.reloadButton.image, [self.reloadButton.rect.x, self.reloadButton.rect.y])
        # self.Panel.blit(self.setCurPosButton.image, [self.setCurPosButton.rect.x, self.setCurPosButton.rect.y])
        # self.Panel.blit(self.saveButton.image, [self.saveButton.rect.x, self.saveButton.rect.y])
        # self.Panel.blit(self.makeTemplateButton.image, [self.makeTemplateButton.rect.x, self.makeTemplateButton.rect.y])




        self.surfaceDrawn = True
            
        

            
    def get_updatePanel(self):
        return True


    # def saveGame(self):
    #     self.World.sanitizeForPickling()
    #
    #     saveFile = open(self.savePath, "w")
    #     pickle.dump(self.World, saveFile)
    #     saveFile.close()
    #
    #     self.World.reloadGame()
    #
    # def loadGame(self):
    #     self.World
    #
    #     loadFile = open(self.savePath, "r")
    #     self.World = pickle.load(loadFile)
    #     loadFile.close()
    #
    #     self.World.reloadGame()

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
        
