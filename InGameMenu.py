# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 16:03:01 2015

@author: alex
"""

import pygame, AssetUI, gameSettingsMaster
from dataManagers import contentPackages
contentHandler = contentPackages.mainHandler

pygame.init()
pygame.font.init()


class GUI:
    def __init__(self, rect, pos, jsonArgs = None):
        self.jsonArgs = jsonArgs
        self.surfaceDrawn = True
        self.show = False
        self.pos = pos
        self.dimens = rect
        self.Panel = pygame.Surface(self.dimens)

        self.textSize = self.jsonArgs["text size"]
        self.textButtonSize = self.jsonArgs["text button size"]

        self.fontRend = pygame.font.Font("_IMAGES\\ComicSans.ttf", 40)
        self.fontSubRend = pygame.font.Font("_IMAGES\\ComicSans.ttf", self.textSize)
        self.labelMenu = self.fontRend.render("In-Game Menu:", True, [0, 0, 0])
        self.mode = "LevelUp"

        self.tabButtons = {
            "Map":AssetUI.LabelButton([400, 40], self.pos, "Map", self.textSize),
            "Inventory":AssetUI.LabelButton([550, 40], self.pos, "Inventory", self.textSize),
            "Equipment":AssetUI.LabelButton([800, 40], self.pos, "Equipment", self.textSize),
            "Status": AssetUI.LabelButton([1030, 40], self.pos, "Status", self.textSize),
            "LevelUp": AssetUI.LabelButton([1200, 40], self.pos, "Level Up", self.textSize)
        }




        # Inventory Screen Stuff
        self.invButtons = {
            "Use":AssetUI.LabelButton([(self.dimens[0] / 2) - 160, self.dimens[1] - 160], self.pos, "Use", self.textButtonSize),
            "Next":AssetUI.LabelButton([520, self.dimens[1] -200], self.pos, ">>", 60),
            "Prev":AssetUI.LabelButton([450, self.dimens[1] - 200], self.pos, "<<", 60),
            "Assign 1":AssetUI.LabelButton([160, self.dimens[1] - 180], self.pos, "1", 40),
            "Assign 2":AssetUI.LabelButton([200, self.dimens[1] - 180], self.pos, "2", 40),
            "Assign 3":AssetUI.LabelButton([240, self.dimens[1] - 180], self.pos, "3", 40),
            "Assign 4":AssetUI.LabelButton([280, self.dimens[1] - 180], self.pos, "4", 40),
            "Assign 5":AssetUI.LabelButton([320, self.dimens[1] - 180], self.pos, "5", 40),
            "Assign 6":AssetUI.LabelButton([160, self.dimens[1] - 120], self.pos, "Middle Click", 40),
            "Equip":AssetUI.LabelButton([(self.dimens[0] / 2) - 350, self.dimens[1] - 160], self.pos, "Equip", self.textButtonSize)
        }

        self.itemsPerPage = 6
        self.ItemBtnList = []
        self.pageNum = 0
        self.descPane = AssetUI.descriptionPane.DescriptionPane([self.dimens[0] / 2 + 50, 100], [self.dimens[0] / 2 - 70, self.dimens[1] - 250], self.pos, self.textSize)
        self.startingInvPoint = 0

        self.selectedItem = None

        self.isInvConstructed = False



        # Equipment Screen Stuff:
        self.equipmentList = AssetUI.scrollingList.ScrollingList([20, 200], [self.dimens[0] / 2 - 100, self.dimens[1] - 350], self.pos, {"Hello": "Alex"})
        self.equipLabel = self.fontSubRend.render("Currently Equipped Items:", True, [0, 0, 0])
        self.equipLabelPos = [40, 130]
        self.equipButtons = {
            "Unequip": AssetUI.LabelButton([200, self.dimens[1] - 160], self.pos, "Unequip", self.textSize)
        }

        self.ctrls = gameSettingsMaster.getSettingsDict()["Controls"]


        # Status Screen Data:
        self.statsMenuList = AssetUI.scrollingList.ScrollingList([20, 200], [self.dimens[0] / 2 - 100, self.dimens[1] - 350], self.pos, {"gen": "General Stats", "level": "Levelling" })

        self.statsStrings = {
            "gen": "",
            "level": ""
        }

        # Level Up Screen:
        self.attrLabel = self.fontSubRend.render("Attribute Points:", True, [0, 0, 0])
        self.pwrLabel = self.fontSubRend.render("Fatal Power Upgrade Points:", True, [0, 0, 0])
        self.attrLabelPos = [30, 130]
        self.pwrLabelPos = [480, 130]

        self.attrDict = {"attrSpeed": "Speed", "attrAimSpeed": "Aiming Speed", "attrJump": "Jump Power", "attrDam": "Attack Damage"}
        self.attrMenuList = AssetUI.scrollingList.ScrollingList([20, 200], [self.dimens[0] / 4 - 100, self.dimens[1] - 350], self.pos, self.attrDict)

        self.pwrDict = {"pwrBurn": "Nova Burn", "pwrBlitz": "Fatal Blitz"}
        self.pwrMenuList = AssetUI.scrollingList.ScrollingList([self.dimens[0] / 4 + 20, 200], [self.dimens[0] / 4 - 100, self.dimens[1] - 350], self.pos, self.pwrDict)

        self.levelUpButtons = {
            "Apply Attribute Point": AssetUI.LabelButton([50, self.dimens[1] - 140], self.pos, "Apply Attribute Point", self.textSize),
            "Apply Power Point": AssetUI.LabelButton([self.dimens[0] / 4 + 50, self.dimens[1] - 140], self.pos, "Apply Power Point", self.textSize)
        }

    def determineEndInvPoint(self):
        self.endInvPoint = self.startingInvPoint + 8
        if self.endInvPoint >= len(self.hostvar["Game Env"].mainPlayer.inventory):
            self.endInvPoint = len(self.hostvar["Game Env"].mainPlayer.inventory)

    def countItemsOnThisPage(self):
        if self.endInvPoint - self.startingInvPoint < self.itemsPerPage:
            self.itemsOnThisPage = self.endInvPoint - self.startingInvPoint
        else:
            self.itemsOnThisPage = self.itemsPerPage


    def constructItemUI(self):
        self.hostvar["Game Env"].updateInvUI = False
        self.ItemBtnList = []

        self.determineEndInvPoint()
        self.countItemsOnThisPage()

        screenPos = 0
        pageNum = 0
        thisPageList = []
        for i in self.hostvar["Game Env"].mainPlayer.inventory:
            if self.hostvar["Game Env"].mainPlayer.inventory[i].getValue() == 0:
                continue


            if screenPos >= self.itemsPerPage:
                pageNum += 1
                screenPos = 0
                self.ItemBtnList.append(thisPageList[:])
                thisPageList = []

            screenPos += 1
            thisPageList.append(AssetUI.ItemInventoryButton([20, ((self.textButtonSize + 40) * screenPos)], [self.dimens[0] / 2 - 180, self.textButtonSize + 20], self.pos, self.textSize, i, self.hostvar["Game Env"]))
            # thisPageList.append(AssetUI.ItemInventoryButton([self.dimens[0] / 2 + 150, (100 * screenPos)], [self.dimens[0] / 2 - 180, 75], self.pos, 30, i, self.hostvar["Game Env"]))

        if thisPageList != []:
            self.ItemBtnList.append(thisPageList[:])



    # def getItemName(self, itemRef):
    #     item = itemRef(self.hostvar["Game Env"])
    #     return item.name

    def constructEquipmentUI(self):
        equiplist = {}

        for i in self.hostvar["Game Env"].mainPlayer.equipment:
            equiplist[i] = i + ": " + self.hostvar["Game Env"].items[self.hostvar["Game Env"].mainPlayer.equipment[i]].name

        self.equipmentList.generateButtons(equiplist)

    def genStatStrings(self):
        self.statsStrings["gen"] = "Health: " + self.hostvar["Game Env"].mainPlayer.stats["health"].getOutOfStr() + "\nFatal Aura: " + self.hostvar["Game Env"].mainPlayer.stats["weapEnergy"].getOutOfStr() + "\nMagic: " + self.hostvar["Game Env"].mainPlayer.stats["magic"].getOutOfStr()
        self.statsStrings["level"] = "Current Level: " + str(self.hostvar["Game Env"].mainPlayer.level.getLevel()) + "\nXP: " + str(int(self.hostvar["Game Env"].mainPlayer.level.getXP())) + "/" + str(int(self.hostvar["Game Env"].mainPlayer.level.xpToNextLevel)) + "\nAttribute Upgrade Points: " + str(self.hostvar["Game Env"].mainPlayer.attrUpgradePoints.getValue()) + "\nFatal Power Upgrade Points: " + str(self.hostvar["Game Env"].mainPlayer.fpwrUpgradePoints.getValue())



    def get_hostvar(self, var):
        self.hostvar = var

    def send_hostvar(self):
        return self.hostvar

    def bg_tasks(self):
        if not self.isInvConstructed:
            self.isInvConstructed = True
            self.constructItemUI()
        # self.show = self.hostvar["Show Status Menu"]


        if not self.show:
            return


        # Inventory Mode
        if self.mode == "Inventory":
            if self.hostvar["Game Env"].updateInvUI:
                self.constructItemUI()

        if self.mode == "Status":
            if self.statsMenuList.selectedButton != "":
                self.genStatStrings()
                self.descPane.renderText(self.statsStrings[self.statsMenuList.selectedButton])
            else:
                self.descPane.renderText("")









    def event_loop(self, event):

        if self.show:
            if self.ctrls["Status Screen"] in event["kdown"]:
                self.show = False
                self.hostvar["Game Paused"] = False

        else:
            if self.hostvar["Game Paused"]:
               return

            if self.ctrls["Status Screen"] in event["kdown"]:
                self.show = True
                self.hostvar["Game Paused"] = True
                self.constructEquipmentUI()
                self.constructItemUI()



        # self.pageNum = 1
        if not self.show:
            return

        for i in self.tabButtons:
            if self.tabButtons[i].clickBool(event):
                self.mode = i
                if i == "Inventory":
                    self.descPane.renderText("")
                    self.constructItemUI()
                elif i == "Equipment":
                    self.constructEquipmentUI()
                    if self.equipmentList.selectedButton != "":
                        self.descPane.renderText(self.hostvar["Game Env"].items[self.hostvar["Game Env"].mainPlayer.equipment[self.equipmentList.selectedButton]].desc)
                    else:
                        self.descPane.renderText("")
                elif i == "Status":
                    pass
                    # if self.statsMenuList.selectedButton != "":
                    #     self.genStatStrings()
                    #     self.descPane.renderText(self.statsStrings[self.statsMenuList.selectedButton])
                    # else:
                    #     self.descPane.renderText("")

                    # self.descPane.text = "This creates a new Surface with the specified text rendered on it. pygame provides no way to directly draw text on an existing Surface: instead you must use Font.render() to create an image (Surface) of the text, then blit this image onto another Surface."
                    # self.descPane.renderText()

        if self.mode == "LevelUp":
            self.attrMenuList.eventLoop(event)
            self.pwrMenuList.eventLoop(event)
            self.descPane.eventLoop(event)

            if self.attrMenuList.getIfClicked():
                self.descPane.renderText("Current " + self.attrDict[self.attrMenuList.selectedButton] + " Value: " + str(self.hostvar["Game Env"].mainPlayer.stats[self.attrMenuList.selectedButton].getValue()))
                self.pwrMenuList.selectedButton = ""

            if self.pwrMenuList.getIfClicked():
                # self.descPane.renderText(self.pwrMenuList.selectedButton)
                self.descPane.renderText(
                    "Current " + self.pwrDict[self.pwrMenuList.selectedButton] + " Value: " + str(
                        self.hostvar["Game Env"].mainPlayer.stats[self.pwrMenuList.selectedButton].getValue()))
                self.attrMenuList.selectedButton = ""


            if self.levelUpButtons["Apply Attribute Point"].clickBool(event):
                if self.attrMenuList.selectedButton != "":
                    if self.hostvar["Game Env"].mainPlayer.attrUpgradePoints.tryToUse(1):
                        self.hostvar["Game Env"].mainPlayer.stats[self.attrMenuList.selectedButton].modValue(1)
                        self.descPane.renderText("Current " + self.attrDict[self.attrMenuList.selectedButton] + " Value: " + str(self.hostvar["Game Env"].mainPlayer.stats[self.attrMenuList.selectedButton].getValue()))


            if self.levelUpButtons["Apply Power Point"].clickBool(event):
                if self.pwrMenuList.selectedButton != "":
                    if self.hostvar["Game Env"].mainPlayer.fpwrUpgradePoints.tryToUse(1):
                        self.hostvar["Game Env"].mainPlayer.stats[self.pwrMenuList.selectedButton].modValue(1)
                        self.descPane.renderText("Current " + self.pwrDict[self.pwrMenuList.selectedButton] + " Value: " + str(self.hostvar["Game Env"].mainPlayer.stats[self.pwrMenuList.selectedButton].getValue()))


        if self.mode == "Status":
            self.statsMenuList.eventLoop(event)
            self.descPane.eventLoop(event)

            if self.statsMenuList.getIfClicked():

                self.descPane.renderText(self.statsStrings[self.statsMenuList.selectedButton])

        if self.mode == "Equipment":
            self.equipmentList.eventLoop(event)
            self.descPane.eventLoop(event)

            if self.equipmentList.getIfClicked():
                self.descPane.renderText(self.hostvar["Game Env"].items[self.hostvar["Game Env"].mainPlayer.equipment[self.equipmentList.selectedButton]].desc, contentHandler.loadImage(self.hostvar["Game Env"].items[self.hostvar["Game Env"].mainPlayer.equipment[self.equipmentList.selectedButton]].imagePath))

            for i in self.equipButtons:
                if self.equipButtons[i].clickBool(event):
                    if self.equipmentList.selectedButton != "":
                        if i == "Unequip":
                            self.hostvar["Game Env"].mainPlayer.unequipItem(self.equipmentList.selectedButton)
                            self.constructEquipmentUI()
                            self.constructItemUI()



        if self.mode == "Inventory":
            self.descPane.eventLoop(event)
            if len(self.ItemBtnList) != 0:
                if len(self.ItemBtnList) - 1  < self.pageNum:
                    self.pageNum = len(self.ItemBtnList) - 1
                for i in self.ItemBtnList[self.pageNum]:
                    if i.clickBool(event):
                        i.isSelected = True
                        self.selectedItem = i.item
                        self.descPane.text = i.item.desc
                        self.descPane.renderText()

                    if i.item != self.selectedItem:
                        i.isSelected = False
            for i in self.invButtons:
                if self.invButtons[i].clickBool(event):
                    if self.selectedItem != None:
                        if i == "Use" and self.selectedItem.equip == None:
                            self.hostvar["Game Env"].mainPlayer.useItem(self.selectedItem.id)
                            if self.hostvar["Game Env"].mainPlayer.inventory[self.selectedItem.id].getValue() == 0:
                                self.constructItemUI()

                            # if self.hostvar["Game Env"].mainPlayer.inventory[self.selectedItem.id].hasEnough(1):
                            #     self.hostvar["Game Env"].mainPlayer.inventory[self.selectedItem.id].modValue(-1)
                            #     self.selectedItem.onUse()

                            #     self.hostvar["Game Notif"].notify("Used a " + self.selectedItem.name, 120)
                            #
                            # else:
                            #     self.hostvar["Game Notif"].notify("Out of " + self.selectedItem.name + "s", 120)
                            # self.descPane.renderText("Player's Health: " + self.hostvar["Game Env"].mainPlayer.stats["health"].getDashStr())


                        if i == "Equip" and self.selectedItem.equip != None:
                            self.hostvar["Game Env"].mainPlayer.equipItem(self.selectedItem.id)
                            if self.hostvar["Game Env"].mainPlayer.inventory[self.selectedItem.id].getValue() == 0:
                                self.constructItemUI()

                        if i.startswith("Assign"):
                            slot =  i.split(" ")[1]
                            if self.selectedItem.equip == None:
                                self.hostvar["Game Env"].mainPlayer.hotkeyItems[slot] = self.selectedItem.id

                    if i == "Prev" and self.pageNum > 0:
                        self.pageNum -= 1
                    if i == "Next" and self.pageNum < len(self.ItemBtnList) - 1:
                        self.pageNum += 1



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



        if self.mode == "Inventory":

            if self.ItemBtnList != []:
                if self.pageNum > len(self.ItemBtnList) - 1:
                    self.pageNum = len(self.ItemBtnList) - 1
                for i in self.ItemBtnList[self.pageNum]:
                    i.Draw()
                    self.Panel.blit(i.image, [i.rect.x, i.rect.y])


            for i in self.invButtons:
                # if i == "Prev" and not self.pageNum < 0:
                #     continue
                # if i == "Next" and not self.pageNum > len(self.ItemBtnList) - 1:
                #     continue
                if self.selectedItem == None:
                    if i == "Use":
                        continue
                    if i == "Equip":
                        continue
                    if i == "Unequip":
                        continue
                else:
                    if self.selectedItem.equip != None:
                        if i == "Use":
                            continue
                    else:
                        if i == "Equip":
                            continue
                        if i == "Unequip":
                            continue
                self.invButtons[i].Draw()
                self.Panel.blit(self.invButtons[i].image,
                                [self.invButtons[i].rect.x, self.invButtons[i].rect.y])


            self.descPane.Draw()
            self.Panel.blit(self.descPane.image, [self.descPane.rect.x, self.descPane.rect.y])

        elif self.mode == "Equipment":
            self.equipmentList.Draw()
            self.Panel.blit(self.equipmentList.image, self.equipmentList.pos)
            self.Panel.blit(self.equipLabel, self.equipLabelPos)

            for i in self.equipButtons:
                if self.equipmentList.selectedButton == "" and i == "Unequip":
                    continue
                self.equipButtons[i].Draw()
                self.Panel.blit(self.equipButtons[i].image,
                                [self.equipButtons[i].rect.x, self.equipButtons[i].rect.y])
            self.descPane.Draw()
            self.Panel.blit(self.descPane.image, [self.descPane.rect.x, self.descPane.rect.y])

        elif self.mode == "Status":
            self.statsMenuList.Draw()
            self.Panel.blit(self.statsMenuList.image, self.statsMenuList.pos)
            self.descPane.Draw()
            self.Panel.blit(self.descPane.image, [self.descPane.rect.x, self.descPane.rect.y])

        elif self.mode == "LevelUp":
            self.attrLabel = self.fontSubRend.render("Attribute Upgrade Points: " + str(self.hostvar["Game Env"].mainPlayer.attrUpgradePoints.getValue()), True, [0, 0, 0])
            self.pwrLabel = self.fontSubRend.render("Fatal Power Upgrade Points: " + str(self.hostvar["Game Env"].mainPlayer.fpwrUpgradePoints.getValue()), True, [0, 0, 0])
            # self.lvlLabelPos = [40, 130]


            self.Panel.blit(self.attrLabel, self.attrLabelPos)
            self.Panel.blit(self.pwrLabel, self.pwrLabelPos)

            for i in self.levelUpButtons:
                self.levelUpButtons[i].Draw()
                self.Panel.blit(self.levelUpButtons[i].image, [self.levelUpButtons[i].rect.x, self.levelUpButtons[i].rect.y])


            self.attrMenuList.Draw()
            self.Panel.blit(self.attrMenuList.image, self.attrMenuList.pos)
            self.pwrMenuList.Draw()
            self.Panel.blit(self.pwrMenuList.image, self.pwrMenuList.pos)

            self.descPane.Draw()
            self.Panel.blit(self.descPane.image, [self.descPane.rect.x, self.descPane.rect.y])

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

