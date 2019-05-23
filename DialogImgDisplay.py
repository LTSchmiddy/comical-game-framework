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
        self.show = False
        self.pos = pos
        self.dimens = rect
        self.Panel = pygame.Surface(self.dimens)
        self.imagePath = ""


    def get_hostvar(self, var):
        self.hostvar = var
 
    def send_hostvar(self):
        return self.hostvar           
            
    def bg_tasks(self):
        self.imagePath = self.hostvar["dialogM"].getImage()

        if self.imagePath == "":
            pass
        elif self.imagePath == None:
            self.show = False
        else:
            self.show = True
            self.Panel.fill([0, 0, 0])
            newImage = pygame.image.load(self.imagePath)
            self.Panel.blit(newImage, [0, 0])

    def event_loop(self, event):
        pass


    def percents(self, val, off):
        x = ((self.dimens[0] * val[0])/100) + off[0]
        y = ((self.dimens[1] * val[1])/100) + off[1]
        pixels = [x, y]
        return pixels
    
    def updatePanel(self):
        pass

            
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
        
