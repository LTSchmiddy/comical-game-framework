# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 16:03:01 2015

@author: alex
"""

import pygame, os, AssetUI, gameSettingsMaster


pygame.init()
pygame.font.init()


def execCon(string, world, hostvar, safeMode = True):
    retVal = None
    player = world.mainPlayer

    if safeMode:
        try:

            if string.startswith("bat "):

                print os.getcwd()
                print "bat\\" + string[4:] + ".dcc"
                strFile = open("bat\\" + string[4:] + ".dcc")
                string = strFile.read()
                print string
                strFile.close()

            if string.startswith("log "):
                string = "retVal = " + string[4:]


            exec string

            return str(retVal)
        except Exception as ex:
            template = "An exception of type {0} occurred:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            return message
            # return "Error: Try Again..."
    else:
        if string.startswith("log"):
            string = "retVal = " + string[3:]

        exec string


        return str(retVal)


class GUI:
    def __init__(self, rect, pos, jsonArgs = None):
        self.show = False
        self.surfaceDrawn = True
        self.pos = pos
        self.dimens = rect
        self.Panel = pygame.Surface(self.dimens)

        # self.Panel.set_alpha(240)

        self.fillColor = [255, 235, 135]
        self.charList = list("zxcvbnm,./asdfghjkl;'qwertyuiop[]\\1234567890-= ")
        self.charListUp = list("ZXCVBNM<>?ASDFGHJKL:\"QWERTYUIOP{}|!@#$%^&*()_+ ")

        self.fontSize = jsonArgs["textSize"]
        self.fontRend = pygame.font.Font("_IMAGES\\ComicSans.ttf", self.fontSize)
        self.debugLabel = self.fontRend.render("Debug Console:", True, [0, 0, 0])

        # self.cmdRend = pygame.font.Font("_IMAGES\\ComicSans.ttf", 200)
        self.command = None

        self.outputArea = AssetUI.descriptionPane.DescriptionPane([20, 150], [self.dimens[0] - 40, self.dimens[1] - 200], self.pos, self.fontSize)

        self.selection = -1
        self.lastCommands = []

        self.cmdStr = ""
        self.cmdStrP1 = ""
        self.cmdStrP2 = ""
        self.cursorPos = 0
        # self.useSafeMode = Tre

        self.isTransparent = False

        self.Buttons = {
            "Clear": AssetUI.LabelButton([self.dimens[0] - 240, 40], self.pos, "Clear", 25),
            "Toggle Transparent": AssetUI.LabelButton([self.dimens[0] - 240, 70], self.pos, "Toggle Transparent", 25)
            # "Get Objects": AssetUI.LabelButton([self.dimens[0] - 240, 90], self.pos, "Get Objects", 25),

        }

        self.ctrls = gameSettingsMaster.getSettingsDict()["Controls"]


    def get_hostvar(self, var):
        self.hostvar = var
 
    def send_hostvar(self):
        return self.hostvar           
            
    def bg_tasks(self):
        while self.hostvar["debugLogging"].hasQueued():
            msg = self.hostvar["debugLogging"].pullNext()
            objStr = str(type(msg.object))
            self.writeLog(objStr + " -> " + msg.message)

    def event_loop(self, event):
        # Handle Show/Hide:
        if self.show:
            if self.ctrls["Show Console"] in event["kdown"]:
                self.show = False
                self.hostvar["Game Paused"] = False

        else:
            if self.hostvar["Game Paused"]:
               return

            if self.ctrls["Show Console"] in event["kdown"]:
                self.show = True
                self.hostvar["Game Paused"] = True



        if not self.show:
            return

        for i in self.Buttons:
            if self.Buttons[i].clickBool(event):
                if i == "Clear":
                    self.selection = -1
                    self.lastCommands = []
                    # self.history = ""
                    self.outputArea.renderText("")

                if i == "Toggle Transparent":
                    self.isTransparent = not self.isTransparent



        # Handle keyboard Input:
        for i in event["kdown"]:

            if i == pygame.K_BACKSPACE:
                self.cmdStrP1 = self.cmdStrP1[:-1]

            elif i == pygame.K_DELETE:
                self.cmdStrP2 = self.cmdStrP2[1:]

            elif i == pygame.K_HOME:
                self.cmdStrP2 = self.cmdStrP1 + self.cmdStrP2
                self.cmdStrP1 = ""

            elif i == pygame.K_END:
                self.cmdStrP1 = self.cmdStrP1 + self.cmdStrP2
                self.cmdStrP2 = ""

            elif i == pygame.K_RETURN:
                if pygame.K_LSHIFT in event["kheld"] or pygame.K_RSHIFT in event["kheld"]:
                    self.cmdStr = self.cmdStrP1 + self.cmdStrP2
                    self.runCMD(False)
                else:
                    self.cmdStr = self.cmdStrP1 + self.cmdStrP2
                    self.runCMD()

            elif i == pygame.K_UP:
                if self.selection < len(self.lastCommands) - 1:
                    self.selection += 1
                    self.cmdStrP1 = self.lastCommands[self.selection]
                    self.cmdStrP2 = ""

            elif i == pygame.K_DOWN:
                if self.selection > 0:
                    self.selection -= 1
                    self.cmdStrP1 = self.lastCommands[self.selection]
                    self.cmdStrP2 = ""

            elif i == pygame.K_LEFT and self.cmdStrP1 != "":
                swapList1 = list(self.cmdStrP1)
                swapList2 = list(self.cmdStrP2)
                swapList2.insert(0, swapList1.pop())

                self.cmdStrP1 = "".join(swapList1)
                self.cmdStrP2 = "".join(swapList2)

            elif i == pygame.K_RIGHT and self.cmdStrP2 != "":
                swapList1 = list(self.cmdStrP1)
                swapList2 = list(self.cmdStrP2)
                swapList1.append(swapList2.pop(0))

                self.cmdStrP1 = "".join(swapList1)
                self.cmdStrP2 = "".join(swapList2)


            elif unichr(i) in self.charList:
                if pygame.K_LSHIFT in event["kheld"] or pygame.K_RSHIFT in event["kheld"]:
                    self.cmdStrP1 = self.cmdStrP1 + self.charListUp[self.charList.index(unichr(i))]
                else:
                    self.cmdStrP1 = self.cmdStrP1 + unichr(i)


    def runCMD(self, useSafe = True):
        result = execCon(self.cmdStr, self.hostvar["Game Env"], self.hostvar, useSafe)


        if result != None:
            self.writeLog("-- " + self.cmdStr + ":   " + result + "\n")

        else:
            self.writeLog("-- " + self.cmdStr + "\n")


        self.lastCommands.insert(0, self.cmdStr)
        self.selection = -1
        self.cmdStr = ""
        self.cmdStrP1 = ""
        self.cmdStrP2 = ""

    def writeLog(self, text):
        self.outputArea.text = text + "\n" + self.outputArea.text
        self.outputArea.renderText()

    def percents(self, val, off):
        x = ((self.dimens[0] * val[0])/100) + off[0]
        y = ((self.dimens[1] * val[1])/100) + off[1]
        pixels = [x, y]
        return pixels
    
    def updatePanel(self):
        self.surfaceDrawn = False


        if not self.show:
            return

        if self.isTransparent:
            self.Panel.set_alpha(170)
        else:
            self.Panel.set_alpha(255)

        self.Panel.fill(self.fillColor)
        pygame.draw.rect(self.Panel, [0, 0, 0], pygame.Rect([0, 0], self.dimens), 10)

        self.command = self.fontRend.render("-- " + self.cmdStrP1 + "|" + self.cmdStrP2, True, [125, 125, 125])

        self.Panel.blit(self.debugLabel, [20, 20])
        self.outputArea.Draw()
        self.Panel.blit(self.outputArea.image, self.outputArea.pos)
        self.Panel.blit(self.command, [20, 80])

        for i in self.Buttons:
            self.Buttons[i].Draw()
            self.Panel.blit(self.Buttons[i].image, self.Buttons[i].pos)

        self.surfaceDrawn = True


    def get_updatePanel(self):
        return True
            

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
        
