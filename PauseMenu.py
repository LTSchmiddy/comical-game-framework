# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 16:03:01 2015

@author: alex
"""

import pygame, AssetUI, gameSettingsMaster, sys

pygame.init()
pygame.font.init()


class GUI:
    def __init__(self, rect, pos, jsonArgs = None):

        self.surfaceDrawn = True
        self.show = False
        self.pos = pos
        self.dimens = rect
        self.Panel = pygame.Surface(self.dimens)

        self.fontRend = pygame.font.Font("_IMAGES\\ComicSans.ttf", 40)
        self.labelMenu = self.fontRend.render("PAUSED", True, [0, 0, 0])

        self.Buttons = {
            "closegame": AssetUI.LabelButton([30, 80], self.pos, "Quit", 60)

        }
        self.Buttons["closegame"].makeBlack()
        self.ctrls = gameSettingsMaster.getSettingsDict()["Controls"]

        self.menuList = AssetUI.scrollingList.ScrollingList([20, 100], [self.dimens[0] - 40, self.dimens[1] - 100], self.pos, {
            1: "Resume",
            2: "Save Game",
            3: "Options",
            4: "Quit Game"

        })

        self.menuList.useBorder = False
        self.menuList.allowScrolling = False


    def get_hostvar(self, var):
        self.hostvar = var

    def send_hostvar(self):
        return self.hostvar

    def bg_tasks(self):
        # self.hostvar["Show Pause Menu"] = self.show
        pass

    def event_loop(self, event):



        if self.show:
            # if self.Buttons["closegame"].clickBool(event):
            #     sys.exit(0)

            self.menuList.eventLoop(event)
            if self.menuList.getIfClicked():
                if self.menuList.selectedButton == 1:
                    self.show = False
                    self.hostvar["Game Paused"] = False
                elif self.menuList.selectedButton == 2:
                    self.hostvar["saveM"].save()
                elif self.menuList.selectedButton == 3:
                    pass
                elif self.menuList.selectedButton == 4:
                    sys.exit(0)

            if self.ctrls["Pause Menu"] in event["kdown"]:
                self.show = False
                self.hostvar["Game Paused"] = False

        else:
            if self.hostvar["Game Paused"]:
               return

            if self.ctrls["Pause Menu"] in event["kdown"]:
                self.show = True
                self.hostvar["Game Paused"] = True



    def percents(self, val, off):
        x = ((self.dimens[0] * val[0]) / 100) + off[0]
        y = ((self.dimens[1] * val[1]) / 100) + off[1]
        pixels = [x, y]
        return pixels

    def updatePanel(self):
        self.surfaceDrawn = False
        self.Panel.fill([255, 235, 135])


        self.Panel.blit(self.labelMenu, [30, 30])

        self.menuList.Draw()
        self.Panel.blit(self.menuList.image, self.menuList.pos)
        pygame.draw.rect(self.Panel, [0, 0, 0], pygame.Rect([0, 0], self.dimens), 10)

        # for i in self.Buttons:
        #     self.Buttons[i].Draw()
        #     self.Panel.blit(self.Buttons[i].image,
        #                     [self.Buttons[i].rect.x, self.Buttons[i].rect.y])
        self.surfaceDrawn = True

    def get_updatePanel(self):
        return self.show


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

