# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 16:03:01 2015

@author: alex
"""

import pygame, os, AssetUI
pygame.init()
pygame.font.init()


class GUI:
    def __init__(self, rect, pos, jsonArgs = None):
        self.show = False
        self.surfaceDrawn = True
        self.pos = pos
        self.dimens = rect
        self.Panel = pygame.Surface(self.dimens)
        self.diaMan = None
        self.dialog = None
        self.nextPlace = None
        self.place = None

        self.textPane = AssetUI.descriptionPane.DescriptionPane([20, 100], [self.dimens[0] / 2, self.dimens[1] - 120], self.pos)
        # self.textPane.renderText("HELLO ALEX!!")

        self.fontRend = pygame.font.Font("_IMAGES\\ComicSans.ttf", 40)
        self.dialogLabel = self.fontRend.render("Dialog - ", True, [0, 0, 0])
        self.replyLabel = self.fontRend.render("You Reply:", True, [0, 0, 0])


        self.respStart = [(self.dimens[0] / 2) + 100, 100]
        self.respSize = 30
        self.respButtons = {}
        #     "r1":AssetUI.LabelButton([400, 40], self.pos, "1", 30),
        #     "r2":AssetUI.LabelButton([400, 40], self.pos, "2", 30),
        #     "r3":AssetUI.LabelButton([400, 40], self.pos, "3", 30),
        #     "r4":AssetUI.LabelButton([400, 40], self.pos, "4", 30)
        # }


    def get_hostvar(self, var):
        self.hostvar = var
        self.diaMan = self.hostvar["dialogM"]
 
    def send_hostvar(self):
        self.hostvar["dialogM"] = self.diaMan
        return self.hostvar

    def loadPlace(self, className):
        self.place = self.dialog[className](self.hostvar["Game Env"], self.dialog["host"])

        if "image" in self.place.__dict__:
            self.hostvar["dialogM"].triggerImage(self.place.image)

        if "icon" in self.place.__dict__:
            self.textPane.renderText(self.place.msg, pygame.image.load(self.place.icon))
        else:
            self.textPane.renderText(self.place.msg)



        startPos = 0
        self.respButtons = {}
        for i in self.place.resp:
            self.respButtons[i] = AssetUI.LabelButton([self.respStart[0],  self.respStart[1] + startPos], self.pos, i, self.respSize)
            startPos += self.respSize + 10

    def handleReply(self, reply):
        if callable(reply):
            reply = reply()

        if reply == "_EXIT":
            self.show = False
            self.hostvar["dialogM"].triggerImage(None)
            self.hostvar["Game Paused"] = False
        else:
            self.nextPlace = reply

    def bg_tasks(self):
        if not self.show:
            self.dialog = self.diaMan.getDialog()
            if self.dialog != None:
                self.show = True
                self.loadPlace(self.dialog["onStart"](self.hostvar["Game Env"], self.dialog["host"]))
                self.dialogLabel = self.fontRend.render(self.place.host.name + " Says:", True, [0, 0, 0])




        if self.show:
            self.hostvar["Show Status Menu"] = False
            self.hostvar["Game Paused"] = True





    def event_loop(self, event):
        if self.show:
            self.textPane.eventLoop(event)

            for i in self.respButtons:
                if self.respButtons[i].clickBool(event):
                    # self.hostvar["Game Notif"].notify(i)
                    self.handleReply(self.place.resp[i])


            if self.nextPlace != None:
                self.loadPlace(self.nextPlace)
                self.nextPlace = None

    def percents(self, val, off):
        x = ((self.dimens[0] * val[0])/100) + off[0]
        y = ((self.dimens[1] * val[1])/100) + off[1]
        pixels = [x, y]
        return pixels
    
    def updatePanel(self):
        self.surfaceDrawn = True
        self.Panel.fill([255, 235, 135])
        pygame.draw.rect(self.Panel, [0, 0, 0], pygame.Rect([0, 0], self.dimens), 10)
        self.Panel.blit(self.dialogLabel, [30, 30])
        self.Panel.blit(self.replyLabel, [(self.dimens[0]/2) + 100, 30])

        self.textPane.Draw()
        self.Panel.blit(self.textPane.image, [self.textPane.rect.x, self.textPane.rect.y])

        for i in self.respButtons:
            self.respButtons[i].Draw()
            self.Panel.blit(self.respButtons[i].image, self.respButtons[i].pos)

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
        # pygame.d