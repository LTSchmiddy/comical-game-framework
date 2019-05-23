# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 16:03:01 2015

@author: alex
"""

import pygame, os, AssetUI, sys, subprocess
pygame.init()
pygame.font.init()

class GUI:
    def __init__(self, rect, pos, jsonArgs = None):
        self.show = True
        self.pos = pos
        self.dimens = rect
        self.Panel = pygame.Surface(self.dimens)

        self.gameSub = None

        self.fillColor = [255, 235, 135]

        self.menuList = AssetUI.scrollingList.ScrollingList([0, 60], [self.dimens[0], self.dimens[1] - 60], self.pos, {
            1: "Play Game",
            2: "Settings",
            3: "Exit"

        })

        self.fontRend = pygame.font.Font("_IMAGES\\ComicSans.ttf", 40)
        self.fontSubRend = pygame.font.Font("_IMAGES\\ComicSans.ttf", 30)
        self.labelMenu = self.fontSubRend.render("COMICAL - Cover Page:", True, [0, 0, 0])


    def get_hostvar(self, var):
        self.hostvar = var
 
    def send_hostvar(self):
        return self.hostvar           
            
    def bg_tasks(self):
        pass

    def event_loop(self, event):
        if self.gameSub == None:
            self.menuList.eventLoop(event)

            if self.menuList.getIfClicked():
                if self.menuList.selectedButton == 1:

                    if __name__ == "__main__":
                        self.gameSub = subprocess.Popen(["Python27\python.exe", "Disp_Host.py"])
                        # os.system("Python27\python.exe Disp_Host.py")
                        self.gameSub.wait()
                        sys.exit()
                    else:
                        self.hostvar["kill"] = True
                elif self.menuList.selectedButton == 3:
                    sys.exit()


    def percents(self, val, off):
        x = ((self.dimens[0] * val[0])/100) + off[0]
        y = ((self.dimens[1] * val[1])/100) + off[1]
        pixels = [x, y]
        return pixels
    
    def updatePanel(self):
        self.surfaceDrawn = False
        self.Panel.fill(self.fillColor)
        pygame.draw.rect(self.Panel, [0, 0, 0], pygame.Rect([0, 0], self.dimens), 10)

        self.menuList.Draw()
        self.Panel.blit(self.menuList.image, self.menuList.pos)
        self.Panel.blit(self.labelMenu, [10, 10])

        self.surfaceDrawn = True
            
    def get_updatePanel(self):
        return True
            


# UI MainLoop:

def loadLauncher():
    disp=GUI([400,600], [0, 0])
    screen = pygame.display.set_mode(disp.dimens)

    pygame.display.set_caption("Comical - v0.1")
    pygame.display.set_icon(pygame.image.load("_IMAGES/Icons/IconV2.png"))

    disp.updatePanel()
    keyheldlist = []

    hostvar = {"kill" : False}

    panels = [disp]

    clockLogic = pygame.time.Clock()

    while not hostvar["kill"]:
            # GET EVENTS
        event_list = pygame.event.get()

        kdnlist = []
        kuplist = []

        mouseDownList = []
        mouseUpList = []

        mouseaction = list(pygame.mouse.get_pressed())
        mouseaction.append(0)

        for event in event_list:
            if event.type == pygame.QUIT:

                sys.exit()
            elif event.type == pygame.KEYDOWN:
                kdnlist.append(event.key)
                keyheldlist.append(event.key)

            elif event.type == pygame.KEYUP:
                kuplist.append(event.key)
                keyheldlist.remove(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    mouseaction[3] = (1)

                elif event.button == 5:
                    mouseaction[3] = (-1)

                mouseDownList.append(event.button)

            elif event.type == pygame.MOUSEBUTTONUP:
                mouseUpList.append(event.button)

        if (pygame.K_RALT in keyheldlist or pygame.K_LALT in keyheldlist) and pygame.K_F4 in keyheldlist:
            sys.exit()


        screen.fill([0, 0, 0])
        # RUN EACH PANEL
        for i in panels:

            i.get_hostvar(hostvar)
            i.bg_tasks()

            i.event_loop(
                {"kdown": kdnlist, "kup": kuplist, "kheld": keyheldlist, "mdown": mouseDownList, "mup": mouseUpList,
                 "mstate": mouseaction})
            hostvar = i.send_hostvar()


            if i.show:
                if i.get_updatePanel():
                    i.updatePanel()

                screen.blit(i.Panel, i.pos)

        clockLogic.tick(20)
        pygame.display.flip()


if __name__ == "__main__":
    loadLauncher()