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
        self.pos = pos
        self.dimens = rect
        self.Panel = pygame.Surface(self.dimens)
        self.Panel.set_alpha(170)

        self.fontRend = pygame.font.Font("_IMAGES\\ComicSans.ttf", 30)


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
        ammoSurf = self.fontRend.render(self.hostvar["Game Env"].mainPlayer.ammo[self.hostvar["Game Env"].mainPlayer.currentAmmo].getDashStr(), True, [0, 0, 0])
        self.Panel.blit(ammoSurf, [10, self.dimens[1] - ammoSurf.get_height() - 20])

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
        
