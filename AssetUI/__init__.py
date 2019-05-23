import pygame

import descriptionPane, scrollingList
from dataManagers import audioMan
from dataManagers import contentPackages
contentHandler = contentPackages.mainHandler

# __all__ = ["descriptionPane", "scrollingList"]

buttonSounds = audioMan.SoundController()

buttonSounds.soundDict = {
    "MouseOver": pygame.mixer.Sound("_AUDIO\\UI\\Button2.wav"),
    "MouseHit": pygame.mixer.Sound("_AUDIO\\UI\\Button1.wav")

}


pygame.font.init()


class ButtonUI(pygame.sprite.Sprite):
    def __init__(self, pos, dimens, offset, color=[0, 0, 0], highlightColor=[125, 125, 125], clickboolCanHighlight=True):
        global buttonSounds
        super(ButtonUI, self).__init__()

        self.sounds = buttonSounds
        self.image = pygame.Surface(dimens)
        self.rect = pygame.Rect(pos, dimens)
        self.screenOffset = offset
        self.highlightColor = highlightColor
        self.color = color
        self.clickboolCanHighlight = clickboolCanHighlight
        self.isHighlighted = False
        self.wasHighlighted = False
        self.mLast = [0, 0, 0]
        self.image.fill([0, 0, 0])

    def clickCheck(self, events):
        if self.rect.collidepoint(
                [pygame.mouse.get_pos()[0] - self.screenOffset[0], pygame.mouse.get_pos()[1] - self.screenOffset[1]]):
            if self.mLast[0] == 1 and events["mstate"][0] == 0:
                self.onClicked()
        self.mLast = events["mstate"]

    def clickBool(self, events):
        self.wasHighlighted = self.isHighlighted

        if self.rect.collidepoint(
                [pygame.mouse.get_pos()[0] - self.screenOffset[0], pygame.mouse.get_pos()[1] - self.screenOffset[1]]):
            self.isHighlighted = True
            # self.Draw()
            if self.mLast[0] == 1 and events["mstate"][0] == 0:
                self.mLast = events["mstate"]
                self.sounds.triggerSound("MouseHit")
                return True
        else:
            self.isHighlighted = False
            # self.Draw()
        self.mLast = events["mstate"]

        # if self.isHighlighted and not self.wasHighlighted:
        #     self.sounds.triggerSound("MouseOver")
        return False

    def onClicked(self):
        pass

    def Draw(self):
        pass


########



class CloseButton(ButtonUI):
    def __init__(self, pos, dimens, offset):
        super(CloseButton, self).__init__(pos, dimens, offset)

    def onClicked(self):
        exit()


class DirectionButton(ButtonUI):
    def __init__(self, pos, dimens, offset, vector):
        super(DirectionButton, self).__init__(pos, dimens, offset)
        self.vector = vector


class LabelButton(ButtonUI):
    def __init__(self, pos, offset, string, size, useOutline = False):
        self.pos = pos
        super(LabelButton, self).__init__(pos, [1, 1], offset)
        self.string = string
        self.id = string
        self.fontRend = pygame.font.Font("_IMAGES\\ComicSans.ttf", size)
        self.image = self.fontRend.render(self.string, True, self.color)
        self.rect = pygame.Rect(pos, self.image.get_size())
        self.useOutline = useOutline

    def makeBlack(self):
        self.image = self.fontRend.render(self.string, True, [0, 0, 0])
        self.rect = pygame.Rect(self.pos, self.image.get_size())

    def makeWhite(self):
        self.image = self.fontRend.render(self.string, True, [255, 255, 255])
        self.rect = pygame.Rect(self.pos, self.image.get_size())

    def setColor(self, color):
        self.image = self.fontRend.render(self.string, True, color)
        self.rect = pygame.Rect(self.pos, self.image.get_size())

    def Draw(self, useColor = None):
        # self.fontRend = pygame.font.Font("_IMAGES\\ComicSans.ttf", size)
        if self.clickboolCanHighlight and self.isHighlighted:
            self.image = self.fontRend.render(self.string, True, self.highlightColor)
            if self.useOutline:
                pygame.draw.rect(self.image, self.highlightColor, pygame.Rect([0, 0], self.image.get_size()), 2)
        else:
            if useColor != None:
                self.image = self.fontRend.render(self.string, True, useColor)
            else:
                self.image = self.fontRend.render(self.string, True, self.color)
            if self.useOutline:
                pygame.draw.rect(self.image, self.color, pygame.Rect([0, 0], self.image.get_size()), 2)




class ItemInventoryButton(ButtonUI):
    def __init__(self, pos, dimens, offset, size, itemRef, world, textColor=[0, 0, 0], fillColor=[255, 235, 135], selectedFillColor = [255, 255, 255]):

        super(ItemInventoryButton, self).__init__(pos, dimens, offset)
        self.pos = pos
        self.dimens = dimens
        self.rect = pygame.Rect(pos, dimens)
        self.textColor = textColor
        self.fillColor = fillColor
        self.selectedFillColor = selectedFillColor
        self.isSelected = False
        self.image = pygame.Surface(dimens)
        self.fontRend = pygame.font.Font("_IMAGES\\ComicSans.ttf", size)

        #Data Related to the item:
        self.world = world
        # self.itemRef = itemRef
        self.item = self.world.items[itemRef]
        self.counter = self.world.mainPlayer.inventory[self.item.id]

        self.itemImage = contentHandler.loadImage(self.item.imagePath)
        self.itemNamePlate = self.fontRend.render(self.item.name, True, self.textColor)
        self.itemCountPlate = self.fontRend.render(self.counter.getOutOfStr(), True, self.textColor)

    def updateCountPlate(self):
        self.itemCountPlate = self.fontRend.render(self.counter.getOutOfStr(), True, self.textColor)

    def Draw(self):
        if self.isSelected:
            self.image.fill(self.selectedFillColor)
        else:
            self.image.fill(self.fillColor)
        pygame.draw.rect(self.image, [0, 0, 0], pygame.Rect([0, 0], self.dimens), 10)
        self.updateCountPlate()

        self.image.blit(self.itemImage, [10, 10])
        self.image.blit(self.itemNamePlate, [100, 10])
        self.image.blit(self.itemCountPlate, [self.dimens[0] - self.itemCountPlate.get_width() - 20 , 10])
