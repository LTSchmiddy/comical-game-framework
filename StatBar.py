# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 16:03:01 2015

@author: alex
"""

import pygame, gameSettingsMaster
pygame.init()
pygame.font.init()


class GUI:
    def __init__(self, rect, pos, jsonArgs = None):
        self.surfaceDrawn = True
        self.show = False
        self.pos = pos
        self.dimens = rect
        self.Panel = pygame.Surface(self.dimens)

        self.scaleFactor = (self.dimens[1] / 200.0)

        self.fillColor = [255, 235, 135]

        self.labelRend = pygame.font.Font("_IMAGES\\ComicSans.ttf", int(30 * self.scaleFactor))
        self.labelHealth = self.labelRend.render("HEALTH:", True, [0, 0, 0])
        self.labelWeapEnergy = self.labelRend.render("FATAL AURA:", True, [0, 0, 0])
        self.labelMagic = self.labelRend.render("MAGIC:", True, [0, 0, 0])
        self.labelWeapName = self.labelRend.render("EQUIPPED:", True, [0, 0, 0])
        self.labelCoinsName = self.labelRend.render("WALLET:", True, [0, 0, 0])
        
        self.weapNameRend = pygame.font.Font(None, int(35 * self.scaleFactor))

        self.ctrls = gameSettingsMaster.getSettingsDict()["Controls"]

        self.useScalingBarWidths = gameSettingsMaster.getSettingsDict()["Game"]["UseScalingBarWidths"]
        
    def get_hostvar(self, var):
        self.hostvar = var
 
    def send_hostvar(self):
        return self.hostvar           
            
    def bg_tasks(self):
        if self.hostvar["DebugStart"]:
            self.show = True

        if self.hostvar["Game Paused"]:
            self.Panel.set_alpha(255)
        else:
            self.Panel.set_alpha(170)


    def event_loop(self, events):
        # .stats["health"].getValue()

        if not self.show:
            return

        if self.ctrls["Dev Mode"] in events["kdown"]:
            self.hostvar["Developer Mode"] = not self.hostvar["Developer Mode"]

        # if not self.hostvar["Game Paused"]:
        #     if self.ctrls["Pause Menu"] in events["kdown"]:
        #         self.hostvar["Game Paused"] = True
        #         self.hostvar["Show Pause Menu"] = True
        #     elif self.ctrls["Status Screen"] in events["kdown"]:
        #         self.hostvar["Game Paused"] = True
        #         self.hostvar["Show Status Menu"] = True
        # else:
        #     if self.ctrls["Pause Menu"] in events["kdown"] and self.hostvar["Show Pause Menu"]:
        #         self.hostvar["Game Paused"] = False
        #         self.hostvar["Show Pause Menu"] = False
        #     elif self.ctrls["Status Screen"] in events["kdown"] and self.hostvar["Show Status Menu"]:
        #         self.hostvar["Game Paused"] = False
        #         self.hostvar["Show Status Menu"] = False


    def percents(self, val, off):
        x = ((self.dimens[0] * val[0])/100) + off[0]
        y = ((self.dimens[1] * val[1])/100) + off[1]
        pixels = [x, y]
        return pixels
    
    def updatePanel(self):
        self.surfaceDrawn = False
        self.Panel.fill(self.fillColor)
        pygame.draw.rect(self.Panel, [0, 0, 0], pygame.Rect([0, 0], self.dimens), 10)



        self.Panel.blit(self.labelHealth, [20, 40])
        pygame.draw.line(self.Panel, [0, 0, 0], [145, 50], [155 + ((200) * 1 * self.scaleFactor), 50], 40)
        # pygame.draw.line(self.Panel, [0, 0, 0], [145, 50], [155 + ((200 * self.hostvar["Player Health"]/self.hostvar["Player Health Max"]) * 1 * self.scaleFactor), 50], 40)
        if self.useScalingBarWidths:
            pygame.draw.line(self.Panel, [255, 0, 0], [150, 50], [150 + ((200 * self.hostvar["Player Health"]/self.hostvar["Player Health Max"]) * 1 * self.scaleFactor), 50], int(30 * self.hostvar["Player Health"]/self.hostvar["Player Health Max"]))
        else:
            pygame.draw.line(self.Panel, [255, 0, 0], [150, 50], [150 + ((200 * self.hostvar["Player Health"] / self.hostvar["Player Health Max"]) * 1 * self.scaleFactor), 50], 30)



        self.Panel.blit(self.labelWeapEnergy, [20, 100])
        pygame.draw.line(self.Panel, [0, 0, 0], [175, 110], [185 + ((200) * 1 * self.scaleFactor), 110], 40)
        # pygame.draw.line(self.Panel, [0, 0, 0], [175, 110], [185 + ((200 * self.hostvar["Player Weapon Energy"]/self.hostvar["Player Weapon Energy Max"]) * 1 * self.scaleFactor), 110], 40)
        if self.useScalingBarWidths:
            pygame.draw.line(self.Panel, [0, 0, 225], [180, 110], [180 + ((200 * self.hostvar["Player Weapon Energy"]/self.hostvar["Player Weapon Energy Max"]) * 1 * self.scaleFactor), 110], int(30 * self.hostvar["Player Weapon Energy"]/self.hostvar["Player Weapon Energy Max"]))
        else:
            pygame.draw.line(self.Panel, [0, 0, 225], [180, 110], [180 + ((200 * self.hostvar["Player Weapon Energy"] / self.hostvar["Player Weapon Energy Max"]) * 1 * self.scaleFactor), 110], 30)


        self.Panel.blit(self.labelMagic, [325, 40])
        pygame.draw.line(self.Panel, [0, 0, 0], [425, 50], [435 + ((200) * 1 * self.scaleFactor), 50], 40)
        # pygame.draw.line(self.Panel, [0, 0, 0], [425, 50], [435 + ((200 * self.hostvar["Player Magic"] / self.hostvar["Player Magic Max"]) * 1 * self.scaleFactor), 50], 40)
        if self.useScalingBarWidths:
            pygame.draw.line(self.Panel, [0, 225, 0], [430, 50], [430 + ((200 * self.hostvar["Player Magic"] / self.hostvar["Player Magic Max"]) * 1 * self.scaleFactor), 50], int(30 * self.hostvar["Player Magic"] / self.hostvar["Player Magic Max"]))
        else:
            pygame.draw.line(self.Panel, [0, 225, 0], [430, 50], [430 + ((200 * self.hostvar["Player Magic"] / self.hostvar["Player Magic Max"]) * 1 * self.scaleFactor), 50], 30)

        self.labelCoinsName = self.labelRend.render("| $" + str(self.hostvar["Game Env"].mainPlayer.money.getValue()) , True, [0, 0, 0])
        self.Panel.blit(self.labelCoinsName, [350, 100])

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
        
