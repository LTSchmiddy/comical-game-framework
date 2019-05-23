import pygame, AssetUI


from dataManagers import contentPackages
contentHandler = contentPackages.mainHandler

class ScrollingList(object):
    def __init__(self, pos, dimens, offset, buttons, size = 40, textColor=[0, 0, 0], fillColor=[255, 235, 135]):
        self.pos = pos
        self.dimens = dimens
        self.screenOffset = offset
        self.rect = pygame.Rect(pos, dimens)
        self.size = size
        self.fillColor = fillColor
        self.textColor = textColor
        self.textStartingPoint = 10

        self.useBorder = True
        self.allowScrolling = True

        self.scrollSpeed = 20

        self.textOffset = 10

        self.text = ""

        self.buttonStrs = buttons
        self.buttons = {}

        self.wasHit = False

        self.selectedButton = ""

        self.generateButtons()

        self.image = pygame.Surface(self.dimens)
        # self.textArea = pygame.Surface([self.dimens[0], self.dimens[1] - self.textStartingPoint])
        # self.textArea.fill(self.fillColor)

        self.fontRend = pygame.font.Font("_IMAGES\\ComicSans.ttf", self.size)

    def generateButtons(self, buttonStrs = None):
        self.selectedButton = ""
        if buttonStrs != None:
            self.buttonStrs = buttonStrs
        self.buttons = {}
        self.textStartingPoint = 10
        nextPos = self.textStartingPoint

        for i in self.buttonStrs:
            thisOffset = [self.screenOffset[0] + self.pos[0], self.screenOffset[1] + self.pos[1] + self.textStartingPoint]
            nextButton = AssetUI.LabelButton([10, nextPos], thisOffset, self.buttonStrs[i], self.size)

            self.buttons[i] = nextButton

            nextPos += self.size + self.textOffset

    def getIfClicked(self):
        retVal = self.wasHit
        self.wasHit = False
        return retVal

    def eventLoop(self, events):
        # self.text = ""
        # for i in events["mstate"]:
        #     self.text = self.text + str(i) + ", "
        # self.renderText()


        if self.rect.collidepoint([pygame.mouse.get_pos()[0] - self.screenOffset[0], pygame.mouse.get_pos()[1] - self.screenOffset[1]]):
            if self.allowScrolling:
                self.textStartingPoint += events["mstate"][3] * self.scrollSpeed

            for i in self.buttons:
                self.buttons[i].screenOffset = [self.screenOffset[0] + self.pos[0], self.screenOffset[1] + self.pos[1] + self.textStartingPoint]
                if self.buttons[i].clickBool(events):
                    self.selectedButton = i
                    self.wasHit = True
                    # print i




    def Draw(self):
        self.image.fill(self.fillColor)
        # self.image.blit(self.textArea, [0, self.textStartingPoint])
        for i in self.buttons:
            if i == self.selectedButton:
                self.buttons[i].Draw([125, 125, 235])
            else:
                self.buttons[i].Draw()

            self.image.blit(self.buttons[i].image, [self.buttons[i].rect.x, self.buttons[i].rect.y + self.textStartingPoint])

        if self.useBorder:
            pygame.draw.rect(self.image, [0, 0, 0], pygame.Rect([0, 0], self.dimens), 10)

