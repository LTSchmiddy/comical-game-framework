# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 16:03:01 2015

@author: alex
"""

import pygame, os
pygame.init()
pygame.font.init()


class GUI:
    def __init__(self, rect, pos, jsonArgs = None):
        self.show = True
        self.surfaceDrawn = True
        self.pos = pos
        self.dimens = rect
        self.Panel = pygame.Surface(self.dimens)

        self.imgSurf = {
            "1": None,
            "2": None,
            "3": None,
            "4": None,
            "5": None,
            "6": None
        }

        self.itemLast = {
            "1": None,
            "2": None,
            "3": None,
            "4": None,
            "5": None,
            "6": None,

        }

        self.imgPos = {
            "1": [15, 15],
            "2": [55, 15],
            "3": [95, 15],
            "4": [135, 15],
            "5": [175, 15],
            "6": [215, 15]
        }


    def get_hostvar(self, var):
        self.hostvar = var
 
    def send_hostvar(self):
        return self.hostvar           
            
    def bg_tasks(self):
        if self.hostvar["DebugStart"]:
            self.show = True
        else:
            self.show = False
        if not self.show:
            return



    def event_loop(self, event):
        pass


    def percents(self, val, off):
        x = ((self.dimens[0] * val[0])/100) + off[0]
        y = ((self.dimens[1] * val[1])/100) + off[1]
        pixels = [x, y]
        return pixels
    
    def updatePanel(self):
        self.surfaceDrawn = False
        self.Panel.fill([255, 235, 135])
        pygame.draw.rect(self.Panel, [0, 0, 0], pygame.Rect([0, 0], self.dimens), 10)

        for i in range(1, 7):
            i = str(i)
            if self.hostvar["Game Env"].mainPlayer.hotkeyItems[i] != self.itemLast[i]:
                if self.hostvar["Game Env"].mainPlayer.hotkeyItems[i] == None:
                    self.imgSurf[i] = None
                else:

                    self.imgSurf[i] = pygame.image.load(self.hostvar["Game Env"].items[self.hostvar["Game Env"].mainPlayer.hotkeyItems[i]].imagePath)

                self.itemLast[i] = self.hostvar["Game Env"].mainPlayer.hotkeyItems[i]


            if self.imgSurf[i] != None:
                self.Panel.blit(self.imgSurf[i], self.imgPos[i])

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
        
