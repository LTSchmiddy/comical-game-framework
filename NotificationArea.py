# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 16:03:01 2015

@author: alex
"""

import pygame

from dataManagers import counter

pygame.init()
pygame.font.init()




class GUI:
    def __init__(self, rect, pos, jsonArgs = None):
        self.surfaceDrawn = True
        self.show = True
        self.pos = pos
        self.dimens = rect
        self.Panel = pygame.Surface(self.dimens)
        self.mainNotif = None

        self.fontRend = pygame.font.Font("_IMAGES\\ComicSans.ttf", 30)
        self.notifText = self.fontRend.render("TESTING...", True, [0, 0, 0])

        self.myCounter = counter.TickCounter(0)


    def get_hostvar(self, var):
        self.hostvar = var
 
    def send_hostvar(self):
        return self.hostvar           
            
    def bg_tasks(self):
        self.mainNotif = self.hostvar["Game Notif"]

        if self.myCounter.check():
            self.show = True
        else:
            if self.mainNotif.hasQueued():
                nextMessage = self.mainNotif.pullNext()
                self.notifText = self.fontRend.render(nextMessage.message, True, [0, 0, 0])
                self.myCounter.setTime(nextMessage.time)
                self.myCounter.reset()
            else:
                self.show = False




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
        self.Panel.blit(self.notifText, [30, 30])
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
        
