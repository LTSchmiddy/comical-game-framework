# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 16:03:01 2015

@author: alex
"""

import pygame, os, AssetUI
pygame.init()
pygame.font.init()

from dataManagers import flipBookHandler, counter

class GUI:
    def __init__(self, rect, pos, jsonArgs = None):
        self.surfaceDrawn = True
        self.show = False
        self.pos = pos
        self.dimens = rect
        self.Panel = pygame.Surface(self.dimens)
        self.PanelRect = pygame.Rect([0, 0], self.Panel.get_size())

        self.color = [0, 0, 0]
        self.flipbookManager = None
        self.flipbook = None
        self.OnDeathBook = flipBookHandler.Flipbook("OnDeathLongC")

        self.controlBoxRect = pygame.Rect([0, 10], [250, 50])

        self.rendImage = None
        self.rendRect = None
        # self.color = [255, 235, 135]

        self.Buttons = [
            AssetUI.LabelButton([10, 10], self.pos, "Prev", 30),
            AssetUI.LabelButton([160, 10], self.pos, "Next", 30),
            # AssetUI.LabelButton([160, 10], self.pos, "Close", 30)
        ]

        self.useTimer = False
        self.controlCounter = counter.TickCounter(15, True, False)

    def get_hostvar(self, var):
        self.hostvar = var
        self.flipbookManager = self.hostvar["flipbookM"]
 
    def send_hostvar(self):
        self.hostvar["flipbookM"] = self.flipbookManager
        return self.hostvar



    def setRendImage(self):
        self.rendImage = self.flipbook.returnImage()
        self.rendRect = pygame.Rect([0, 0], self.rendImage.get_size())
        self.rendRect.center = self.PanelRect.center

    def bg_tasks(self):
        if not self.show:
            data = self.flipbookManager.getFlipbookID()


            if data != None:
                nextFB = data[0]

                if nextFB == self.OnDeathBook.bookName:
                    self.OnDeathBook.currentIndex = 0
                    self.flipbook = self.OnDeathBook
                else:
                    self.flipbook = flipBookHandler.Flipbook(nextFB)

                if data[1] != None:
                    self.controlCounter.ticks = data[1]
                    self.controlCounter.reset()
                    self.useTimer = True

                self.hostvar["Game Paused"] = True
                self.show = True

                self.setRendImage()

        else:



            if self.flipbook.isLast():
                self.Buttons[1].string = "Close"
                self.useTimer = False
            else:
                self.Buttons[1].string = "Next"
                if self.useTimer and self.controlCounter.check():
                    self.flipbook.nextImg()
                    self.setRendImage()










    def event_loop(self, event):
        if not self.show:
            return

        if self.useTimer:
            return


        for i in self.Buttons:
            if i.clickBool(event):
                if i.string == "Prev" and not self.flipbook.isFirst():
                    self.flipbook.prevImg()
                    self.setRendImage()

                elif i.string == "Next":
                    self.flipbook.nextImg()
                    self.setRendImage()
                elif i.string == "Close":
                    self.show = False
                    self.hostvar["Game Paused"] = False


    def percents(self, val, off):
        x = ((self.dimens[0] * val[0])/100) + off[0]
        y = ((self.dimens[1] * val[1])/100) + off[1]
        pixels = [x, y]
        return pixels
    
    def updatePanel(self):
        self.surfaceDrawn = False
        if self.show:
            self.Panel.fill(self.color)
            self.Panel.blit(self.rendImage, self.rendRect)

            if self.useTimer:
                return

            pygame.draw.rect(self.Panel, [255, 235, 135], self.controlBoxRect)
            pygame.draw.rect(self.Panel, [0, 0, 0], self.controlBoxRect, 5)


            if self.flipbook != None:


                for i in self.Buttons:
                    if i.string == "Prev" and self.flipbook.isFirst():
                        pass

                    else:
                        i.Draw()
                        self.Panel.blit(i.image, i.pos)
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
        
