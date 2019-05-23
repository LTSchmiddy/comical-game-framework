# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 16:03:01 2015

@author: alex
"""

import AssetUI
import pygame

pygame.init()
pygame.font.init()


class GUI:
    def __init__(self, rect, pos, jsonArgs = None):
        self.show = True
        self.surfaceDrawn = True
        self.pos = pos
        self.dimens = rect
        self.Panel = pygame.Surface(self.dimens)
        self.fillColor = [255, 235, 135]

        self.LogoSplash = pygame.image.load("_IMAGES/InGameLogo.png")

        self.menuList = AssetUI.scrollingList.ScrollingList([0, 260], [self.dimens[0], self.dimens[1] - 260], self.pos, {
            1: "1. New Game",
            2: "2. Load Game",
            3: "3. Options"

        })

        self.menuList.allowScrolling = False

        self.fontRend = pygame.font.Font("_IMAGES\\ComicSans.ttf", 40)
        self.fontSubRend = pygame.font.Font("_IMAGES\\ComicSans.ttf", 30)
        self.labelMenu = self.fontSubRend.render("TABLE OF CONTENTS:", True, [0, 0, 0])


    def get_hostvar(self, var):
        self.hostvar = var
 
    def send_hostvar(self):
        return self.hostvar           
            
    def bg_tasks(self):
        self.show = not self.hostvar["saveM"].isGameFileLoaded
        if not self.show:
            return

        # if self.hostvar["DebugStart"]:
        #     self.show = False
        #     self.hostvar["Game Paused"] = False


    def event_loop(self, event):
        if not self.show:
            return

        self.menuList.eventLoop(event)
        if self.menuList.getIfClicked():
            if self.menuList.selectedButton == 1:
                self.hostvar["saveM"].newGame()
                self.loadToGame()
            elif self.menuList.selectedButton == 2:
                self.hostvar["saveM"].DisplayLoadMenu()
                # self.hostvar["saveM"].load()
                # self.loadToGame()

        # pass

    def loadToGame(self):
        self.show = False
        self.hostvar["Game Paused"] = False
        self.hostvar["DebugStart"] = True

    def percents(self, val, off):
        x = ((self.dimens[0] * val[0])/100) + off[0]
        y = ((self.dimens[1] * val[1])/100) + off[1]
        pixels = [x, y]
        return pixels
    
    def updatePanel(self):
        self.surfaceDrawn = False
        self.Panel.fill(self.fillColor)
        pygame.draw.rect(self.Panel, [0, 0, 0], pygame.Rect([0, 0], self.dimens), 10)

        self.Panel.blit(self.LogoSplash, [0, 0])
        self.menuList.Draw()
        self.Panel.blit(self.menuList.image, self.menuList.pos)
        self.Panel.blit(self.labelMenu, [10, 200])


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
        
