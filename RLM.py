# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 16:03:01 2015

@author: alex
"""

import pygame, AssetUI, gameSettingsMaster

pygame.init()
pygame.font.init()


class GUI:
    def __init__(self, rect, pos, jsonArgs = None):
        self.show = False
        self.pos = pos
        self.dimens = rect
        self.Panel = pygame.Surface(self.dimens)

        self.fontRend = pygame.font.Font("_IMAGES\\ComicSans.ttf", 30)
        self.labelMenu = self.fontRend.render("Rotor Loader Menu:", True, [0, 0, 0])
        self.ctrls = gameSettingsMaster.getSettingsDict()["Controls"]

        self.itemDesc = AssetUI.descriptionPane.DescriptionPane([self.dimens[0]/2, 0], [self.dimens[0]/2, self.dimens[1]], self.pos, 20)
        self.weapList = AssetUI.scrollingList.ScrollingList([0, 50], [self.dimens[0]/2, self.dimens[1]-50], self.pos, {"hello":"ALex"})


    def get_hostvar(self, var):
        self.hostvar = var
 
    def send_hostvar(self):
        return self.hostvar           
            
    def bg_tasks(self):
        pass

    def checkWeapList(self):
        newWeapDict = {None: "Nova Splitter"}

        if "Weapon" in self.hostvar["Game Env"].mainPlayer.equipment:
            newWeapDict.update({self.hostvar["Game Env"].mainPlayer.equipment["Weapon"]: "*" + self.hostvar["Game Env"].items[self.hostvar["Game Env"].mainPlayer.equipment["Weapon"]].name})
        else:
            newWeapDict.update({None: "*Nova Splitter"})



        # self.hostvar["Game Env"].items[self.hostvar["Game Env"].mainPlayer.equipment[self.equipmentList.selectedButton]].desc
        for i in self.hostvar["Game Env"].mainPlayer.inventory:
            if (self.hostvar["Game Env"].items[i].equip == "Weapon") and (self.hostvar["Game Env"].mainPlayer.inventory[i].getValue() > 0):
                if not i in newWeapDict:
                    newWeapDict.update({i:self.hostvar["Game Env"].items[i].name})


        self.weapList.generateButtons(newWeapDict)

    def event_loop(self, event):
        if self.show:
            if not self.ctrls["Rotor Loader Menu"] in event["kheld"]:
                self.show = False
                self.hostvar["Game Paused"] = False

        else:
            if self.hostvar["Game Paused"]:
               return

            if self.ctrls["Rotor Loader Menu"] in event["kheld"]:
                self.show = True
                self.hostvar["Game Paused"] = True
                self.checkWeapList()
            return

        self.weapList.eventLoop(event)
        self.itemDesc.eventLoop(event)

        if self.weapList.getIfClicked():
            if self.weapList.selectedButton == None:
                self.hostvar["Game Env"].mainPlayer.unequipItem("Weapon")
            else:
                self.hostvar["Game Env"].mainPlayer.equipItem(self.weapList.selectedButton)
                self.itemDesc.renderText(self.hostvar["Game Env"].items[self.weapList.selectedButton].desc)
            self.checkWeapList()



    def percents(self, val, off):
        x = ((self.dimens[0] * val[0])/100) + off[0]
        y = ((self.dimens[1] * val[1])/100) + off[1]
        pixels = [x, y]
        return pixels
    
    def updatePanel(self):
        self.surfaceDrawn = False
        self.Panel.fill([255, 235, 135])
        pygame.draw.rect(self.Panel, [0, 0, 0], pygame.Rect([0, 0], self.dimens), 10)

        self.weapList.Draw()

        self.itemDesc.Draw()

        self.Panel.blit(self.labelMenu, [10, 10])
        self.Panel.blit(self.weapList.image, self.weapList.rect.topleft)
        self.Panel.blit(self.itemDesc.image, self.itemDesc.rect.topleft)

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
        
