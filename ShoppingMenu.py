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
        self.surfaceDrawn = True
        self.show = False
        self.pos = pos
        self.dimens = rect
        self.Panel = pygame.Surface(self.dimens)

        self.fontRend = pygame.font.Font("_IMAGES\\ComicSans.ttf", 40)
        self.fontSubRend = pygame.font.Font("_IMAGES\\ComicSans.ttf", 30)
        self.labelMenu = self.fontRend.render("Shopping Menu:", True, [0, 0, 0])
        self.mode = ""

        self.CloseButton = AssetUI.LabelButton([self.dimens[0] - 400, 40], self.pos, "DONE!", 30)

        self.tabButtons = {
            "Buy":AssetUI.LabelButton([400, 40], self.pos, "Buy", 30)
            # "Buy":AssetUI.LabelButton([400, 40], self.pos, "Buy", 30),
            # "Sell":AssetUI.LabelButton([550, 40], self.pos, "Sell", 30),
        }

        self.descPane = AssetUI.descriptionPane.DescriptionPane([self.dimens[0] / 2 + 20, 100], [self.dimens[0] / 2 - 40, self.dimens[1] - 150], self.pos)
        self.itemList = AssetUI.scrollingList.ScrollingList([20, 200], [self.dimens[0] / 2 - 40, self.dimens[1] - 250], self.pos, {})

        self.storeInv = ["HealthItem"]

        self.purchaseButton = AssetUI.LabelButton([50, 150], self.pos, "Purchase", 32)
        self.sellButton = AssetUI.LabelButton([50, 150], self.pos, "Sell", 32)

    def get_hostvar(self, var):
        self.hostvar = var

    def send_hostvar(self):
        return self.hostvar

    def loadStoreInvList(self):

        newButtons = {}
        for i in self.storeInv:
            # self.hostvar["debugLogging"].log(i)
            if self.hostvar["Game Env"].items[i].canSell and (self.hostvar["Game Env"].items[i].value > 0):
                newButtons[i] = self.hostvar["Game Env"].items[i].name + ": $" + str(self.hostvar["Game Env"].items[i].value) + " each"
        self.itemList.generateButtons(newButtons)

    def loadPlayerInvList(self):
        newButtons = {}
        for i in self.hostvar["Game Env"].mainPlayer.inventory:
            # self.hostvar["debugLogging"].log(i)
            if self.hostvar["Game Env"].items[i].canSell and (self.hostvar["Game Env"].items[i].value > 0):
                newButtons[i] = self.hostvar["Game Env"].items[i].name + ": $" + str(self.hostvar["Game Env"].items[i].value) + " each"

        self.itemList.generateButtons(newButtons)


    def attemptPurchase(self):
        if self.itemList.selectedButton in self.hostvar["Game Env"].mainPlayer.inventory:
            if self.hostvar["Game Env"].mainPlayer.inventory[self.itemList.selectedButton].getIsFull():
                self.hostvar["Game Notif"].notify("You can't carry any more...", 120)
                return False

        if self.hostvar["Game Env"].mainPlayer.money.tryToUse(self.hostvar["Game Env"].items[self.itemList.selectedButton].value):
            self.hostvar["Game Env"].mainPlayer.addItem(self.itemList.selectedButton)
            self.hostvar["Game Notif"].notify("Purchased a " + self.hostvar["Game Env"].items[self.itemList.selectedButton].name, 120)
            return True
        else:
            self.hostvar["Game Notif"].notify("Not enough money...", 120)
            return False

    def renderItemDesc(self):
        if self.itemList.selectedButton in self.hostvar["Game Env"].mainPlayer.inventory:
            self.descPane.renderText("(You have " + self.hostvar["Game Env"].mainPlayer.inventory[self.itemList.selectedButton].getOutOfStr() + ") \n" + self.hostvar["Game Env"].items[self.itemList.selectedButton].desc, pygame.image.load(self.hostvar["Game Env"].items[self.itemList.selectedButton].imagePath))
        else:
            self.descPane.renderText("(You have 0 out of 20) \n" + self.hostvar["Game Env"].items[self.itemList.selectedButton].desc, pygame.image.load(self.hostvar["Game Env"].items[self.itemList.selectedButton].imagePath))

    def bg_tasks(self):

        if self.mode == "":
            self.mode = "Buy"
            self.loadStoreInvList()

        # print self.hostvar["storeManager"]


        if not self.show:
            newInv = self.hostvar["storeManager"].getStore()
            if newInv != None:
                self.storeInv = newInv
                self.show = True
                self.mode = "Buy"
                self.loadStoreInvList()
            return

        self.hostvar["Game Paused"] = True


    def event_loop(self, event):

        if not self.show:
            return

        if self.CloseButton.clickBool(event):
            self.hostvar["Game Paused"] = False
            self.show = False

        if self.mode == "Buy":
            if self.purchaseButton.clickBool(event):
                if self.itemList.selectedButton != "":
                    self.attemptPurchase()
                    self.renderItemDesc()

        # self.pageNum = 1


        for i in self.tabButtons:
            if self.tabButtons[i].clickBool(event):
                self.mode = i
                if i == "Sell":
                    self.loadPlayerInvList()
                elif i == "Buy":
                    self.loadStoreInvList()

        self.descPane.eventLoop(event)
        self.itemList.eventLoop(event)

        if self.itemList.getIfClicked():
            self.renderItemDesc()

        if self.mode == "Sell":
            pass




    def percents(self, val, off):
        x = ((self.dimens[0] * val[0]) / 100) + off[0]
        y = ((self.dimens[1] * val[1]) / 100) + off[1]
        pixels = [x, y]
        return pixels

    def updatePanel(self):
        self.surfaceDrawn = False
        self.Panel.fill([255, 235, 135])

        pygame.draw.rect(self.Panel, [0, 0, 0], pygame.Rect([0, 0], self.dimens), 10)
        self.Panel.blit(self.labelMenu, [30, 30])


        for i in self.tabButtons:
            if self.mode == i:
                # print i, "is BOLD"
                self.tabButtons[i].fontRend.set_bold(True)
            else:
                self.tabButtons[i].fontRend.set_bold(False)

            self.tabButtons[i].Draw()
            self.Panel.blit(self.tabButtons[i].image,
                            [self.tabButtons[i].rect.x, self.tabButtons[i].rect.y])

        self.descPane.Draw()
        self.Panel.blit(self.descPane.image, self.descPane.pos)


        self.itemList.Draw()
        self.Panel.blit(self.itemList.image, self.itemList.pos)

        self.CloseButton.Draw()
        self.Panel.blit(self.CloseButton.image, self.CloseButton.pos)

        if self.mode == "Buy":
            self.purchaseButton.Draw()
            self.Panel.blit(self.purchaseButton.image, self.purchaseButton.pos)

        elif self.mode == "Sell":
            self.sellButton.Draw()
            self.Panel.blit(self.sellButton.image, self.sellButton.pos)

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

